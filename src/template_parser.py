"""Parse Google Docs templates into structured JSON schemas and build JSON outputs."""

import re
import json
import logging
from typing import Dict, Any, List, Tuple, Optional

logger = logging.getLogger('character_creation')


def parse_template_structure(template_text: str) -> Dict[str, Any]:
    """Parse a template into a hierarchical JSON structure.
    
    Assumes template uses heading hierarchies:
    - Lines starting with ### or **Section Name:** are top-level keys
    - Lines starting with #### or bullet points with field names are sub-keys
    
    Args:
        template_text: Plain text template content
        
    Returns:
        Dict representing the template structure with empty values
        
    Example:
        Template:
        ### Basic Info
        **Name:** {{NAME}}
        **Age:** {{AGE}}
        
        ### Abilities
        - Strength: [blank]
        - Dexterity: [blank]
        
        Returns:
        {
            "Basic Info": {
                "Name": None,
                "Age": None
            },
            "Abilities": {
                "Strength": None,
                "Dexterity": None
            }
        }
    """
    structure = {}
    current_section = None
    lines = template_text.split('\n')
    
    logger.debug(f"Parsing template structure from {len(lines)} lines")
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        if not line_stripped:
            continue
        
        # Match main sections (###)
        if line_stripped.startswith('###'):
            # Remove markdown
            section_name = line_stripped.replace('#', '').strip().rstrip(':')
            current_section = section_name
            structure[current_section] = {}
            logger.debug(f"Found section: {current_section}")
            
        elif current_section is not None:
            # Try to match **Field:** pattern (where colon is inside the bold)
            if line_stripped.startswith('**') and '**' in line_stripped[2:]:
                # Find the closing **
                end_bold = line_stripped.find('**', 2)
                if end_bold > 2:
                    field_text = line_stripped[2:end_bold]
                    # Remove trailing colon if present
                    field_name = field_text.rstrip(':').strip()
                    if field_name:
                        structure[current_section][field_name] = None
                        logger.debug(f"  Found field: {field_name}")
                    
            # Try to match bullet point fields
            elif line_stripped.startswith('- ') or line_stripped.startswith('* '):
                field_text = line_stripped.lstrip('- *').strip()
                # Extract field name before colon if exists
                if ':' in field_text:
                    field_name = field_text.split(':')[0].strip()
                else:
                    field_name = field_text
                
                if field_name and not field_name.lower().startswith('['):
                    structure[current_section][field_name] = None
                    logger.debug(f"  Found field: {field_name}")
    
    logger.info(f"Parsed template into {len(structure)} sections")
    return structure


def extract_template_schema(template_text: str) -> str:
    """Extract template structure and convert to JSON schema instructions for Gemini.
    
    Args:
        template_text: Plain text template content
        
    Returns:
        String description of expected JSON output structure
    """
    structure = parse_template_structure(template_text)
    
    schema_description = "Output the character as a JSON object with this structure:\n{\n"
    
    for section, fields in structure.items():
        schema_description += f'  "{section}": {{\n'
        for field in fields.keys():
            schema_description += f'    "{field}": "[value]",\n'
        schema_description = schema_description.rstrip(',\n') + '\n  },\n'
    
    schema_description = schema_description.rstrip(',\n') + '\n}'
    
    return schema_description


def build_json_character_prompt(template_text: str, character_inputs: dict) -> str:
    """Build a prompt for Gemini to fill template and output structured JSON.
    
    Args:
        template_text: The Google Docs template text
        character_inputs: Dict with name, sex, gender, age_range, occupation
        
    Returns:
        A formatted prompt for Gemini to output JSON
    """
    schema = extract_template_schema(template_text)
    
    prompt = (
        "You are a creative character development assistant. Fill in the following character template "
        "by replacing all placeholder fields with realistic and interesting details based on the provided inputs. "
        "Maintain creative consistency and make the character vivid and memorable.\n\n"
        
        "CHARACTER INPUTS:\n"
        f"- Name: {character_inputs['name']}\n"
        f"- Sex: {character_inputs['sex']}\n"
        f"- Gender Identity: {character_inputs['gender']}\n"
        f"- Age Range: {character_inputs['age_range']}\n"
        f"- Occupation: {character_inputs['occupation']}\n\n"
        
        "TEMPLATE TO FILL:\n"
        "---START TEMPLATE---\n"
        f"{template_text}\n"
        "---END TEMPLATE---\n\n"
        
        f"REQUIRED JSON OUTPUT STRUCTURE:\n{schema}\n\n"
        
        "Instructions:\n"
        "1. Fill in all placeholder fields ({{NAME}}, {{SEX}}, {{GENDER}}, {{AGE_RANGE}}, {{OCCUPATION}}) with provided values\n"
        "2. Fill in all empty sections with creative and consistent character details\n"
        "3. Make the character's background, personality, and traits coherent\n"
        "4. Output ONLY valid JSON matching the structure above, nothing else\n"
        "5. Ensure all strings are properly escaped and the JSON is valid\n"
    )
    
    return prompt


def validate_json_output(response_text: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """Validate and extract JSON from Gemini response.
    
    Args:
        response_text: Raw text response from Gemini
        
    Returns:
        Tuple of (is_valid, json_dict, error_message)
    """
    try:
        # Try to extract JSON from response (in case there's extra text)
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if not json_match:
            return False, None, "No JSON found in response"
        
        json_str = json_match.group(0)
        data = json.loads(json_str)
        logger.info(f"Valid JSON extracted with {len(data)} top-level keys")
        return True, data, ""
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in response: {e}")
        return False, None, f"JSON decode error: {e}"
    except Exception as e:
        logger.error(f"Error validating JSON: {e}")
        return False, None, f"Validation error: {e}"


def flatten_json_for_text(json_data: Dict[str, Any]) -> str:
    """Convert structured JSON back to readable text format for Google Docs.
    
    Args:
        json_data: Structured character data
        
    Returns:
        Formatted text representation
    """
    text_output = ""
    
    for section, fields in json_data.items():
        if isinstance(fields, dict):
            text_output += f"\n{section}\n" + "=" * len(section) + "\n"
            for field_name, field_value in fields.items():
                text_output += f"\n{field_name}: {field_value}"
        else:
            text_output += f"\n{section}: {fields}"
    
    return text_output


def merge_json_into_structure(base_structure: Dict[str, Any], 
                              filled_data: Dict[str, Any]) -> Dict[str, Any]:
    """Merge Gemini-filled data into base template structure, handling nested data.
    
    Args:
        base_structure: Original template structure
        filled_data: Data from Gemini
        
    Returns:
        Merged structure with all data
    """
    merged = base_structure.copy()
    
    for section, fields in filled_data.items():
        if section in merged:
            if isinstance(fields, dict):
                merged[section].update(fields)
            else:
                merged[section] = fields
        else:
            merged[section] = fields
    
    return merged


def save_character_json(file_path: str, character_data: Dict[str, Any], 
                       character_name: str, pretty: bool = True) -> None:
    """Save character data to individual JSON file.
    
    Args:
        file_path: Path to save JSON file
        character_data: Structured character data
        character_name: Character name (for logging)
        pretty: Whether to pretty-print JSON
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as fh:
            if pretty:
                json.dump(character_data, fh, indent=2, ensure_ascii=False)
            else:
                json.dump(character_data, fh, ensure_ascii=False)
        
        logger.info(f"Character JSON saved: {file_path} ({character_name})")
    except Exception as e:
        logger.error(f"Failed to save character JSON: {e}")
        raise
