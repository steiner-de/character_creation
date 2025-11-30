"""Character input validation and parsing from JSON/JSONL sources."""

import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from src.logger import get_logger

logger = get_logger()

# Mandatory fields that must be present in input
MANDATORY_FIELDS = {
    'name': 'Character name',
    'ethnicity': 'Character ethnicity',
    'sex/gender': 'Character sex/gender',
    'age': 'Character age',
    'occupation': 'Character occupation',
}

# All template section field names (normalized to lowercase)
TEMPLATE_SECTIONS = {
    'High-Level Overview': [],
    'Demographics': [
        'name',
        'titles',
        'age',
        'sex/gender',
        'pronouns',
        'ethnicity',
        'occupation',
        'socioeconomic status',
        'education',
        'other notes',
    ],
    'Physical Appearance': [
        'eye color',
        'skin color',
        'hair color',
        'height',
        'weight',
        'body type',
        'fitness level',
        'tattoos',
        'scars/birthmarks',
        'other distinguishing features',
        'disabilities',
        'fashion style',
        'accessories',
        'cleanliness/grooming',
        'posture/gait',
        'tics',
        'coordination (or lack thereof)',
        'weaknesses',
        'other notes',
    ],
    'History': [
        'birth date',
        'place of birth',
        'key family members',
        'notable family events/milestones',
        'notable personal events/milestones',
        'criminal record',
        'affiliations',
        'allies',
        'enemies',
        'skeletons in the closet',
        'other historical notes',
    ],
    'Psychological Traits': [
        'personality type',
        'personality traits',
        'temperament',
        'introvert/extrovert',
        'mannerisms',
        'educational background',
        'intelligence',
        'self-esteem',
        'hobbies',
        'skills/talents',
        'loves',
        'morals/virtues',
        'phobias/fears',
        'angered by',
        'pet peeves',
        'obsessed with',
        'routines',
        'bad habits',
        'desires',
        'flaws',
        'quirks',
        'favorite sayings',
        'disabilities',
        'secrets',
        'regrets',
        'accomplishments',
        'memories',
        'other notes',
    ],
    'Communication': [
        'languages known',
        'preferred communication methods',
        'accent',
        'style and pacing of speech',
        'pitch',
        'laughter',
        'smile',
        'use of gestures',
        'facial expressions',
        'verbal expressions',
        'other notes',
    ],
    'Strengths, Weaknesses, and Abilities': [
        'physical strengths',
        'physical weaknesses',
        'intellectual strengths',
        'intellectual weaknesses',
        'interpersonal strengths',
        'interpersonal weaknesses',
        'physical abilities',
        'magical abilities',
        'physical illnesses/conditions',
        'mental illnesses/conditions',
        'other notes',
    ],
    'Relationships': [
        'partner(s)significant other(s)',
        'lover(s)',
        'parents/guardians',
        'children',
        'grandparents',
        'grandchildren',
        'family',
        'pets',
        'best friends',
        'friends',
        'rivals',
        'enemies',
        'colleagues',
        'mentors/teachers',
        'idols/role models',
        'followers',
        'strangers',
        'non-living things',
        'clubs/memberships',
        'social media presence',
        'public perception of them',
        'other notes',
    ],
    'Character Growth': [
        'character archetype',
        'character arc',
        'core values',
        'internal conflicts',
        'external conflicts',
        'goals',
        'motivations',
        'epiphanies',
        'significant events/plot points',
        'other notes',
    ],
}


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load a JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON object
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_jsonl_file(file_path: str) -> list[Dict[str, Any]]:
    """Load a JSONL file (JSON Lines format - one JSON object per line).
    
    Args:
        file_path: Path to JSONL file
        
    Returns:
        List of parsed JSON objects
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If any line is not valid JSON
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    records = []
    with open(path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error on line {line_num}: {e}")
                raise
    
    return records


def validate_character_input(
    character_data: Dict[str, Any]
) -> Tuple[bool, Optional[str], Dict[str, Any]]:
    """Validate character input data against template.
    
    Args:
        character_data: Character data to validate
        
    Returns:
        Tuple of (is_valid, error_message, normalized_data)
    """
    normalized = {}
    
    # First, flatten nested structure to look for mandatory fields
    flat_data = {}
    
    # Add top-level keys
    for key, value in character_data.items():
        if key not in ['metadata', 'High-Level Overview', 'Demographics', 
                       'Physical Appearance', 'History', 'Psychological Traits',
                       'Communication', 'Strengths, Weaknesses, and Abilities',
                       'Relationships', 'Character Growth']:
            flat_data[key] = value
    
    # Add nested section keys (flatten hierarchy)
    for section, fields in TEMPLATE_SECTIONS.items():
        if section in character_data and isinstance(character_data[section], dict):
            for key, value in character_data[section].items():
                flat_data[key.lower().replace('_', ' ')] = value
    
    # Check mandatory fields (case-insensitive key matching)
    for mandatory_key, description in MANDATORY_FIELDS.items():
        found = False
        for key in flat_data.keys():
            if key.lower().replace('_', ' ') == mandatory_key.lower():
                normalized[mandatory_key] = flat_data[key]
                found = True
                break
        
        if not found:
            return False, f"Missing mandatory field: {description}", {}
    
    # Process all optional fields from template
    for section, fields in TEMPLATE_SECTIONS.items():
        section_data = {}
        
        if section in character_data and isinstance(character_data[section], dict):
            for key, value in character_data[section].items():
                template_field = key.lower().replace('_', ' ')
                # Skip mandatory fields already processed
                if not any(m.lower() == template_field for m in MANDATORY_FIELDS.keys()):
                    section_data[template_field] = value
        
        if section_data:
            normalized[section] = section_data
    
    # Extract and validate metadata
    metadata = {}
    if 'metadata' in character_data:
        meta = character_data['metadata']
        if isinstance(meta, dict):
            if 'new_doc_title' in meta:
                metadata['new_doc_title'] = meta['new_doc_title']
            if 'json_output' in meta:
                metadata['json_output'] = bool(meta['json_output'])
    
    if metadata:
        normalized['metadata'] = metadata
    
    return True, None, normalized


def process_character_file(
    file_path: str,
    is_jsonl: bool = False
) -> Tuple[bool, Optional[str], list[Dict[str, Any]]]:
    """Load and validate character data from JSON or JSONL file.
    
    Args:
        file_path: Path to JSON or JSONL file
        is_jsonl: Whether file is JSONL format (True) or JSON (False)
        
    Returns:
        Tuple of (is_valid, error_message, list_of_valid_characters)
    """
    try:
        if is_jsonl:
            records = load_jsonl_file(file_path)
        else:
            data = load_json_file(file_path)
            # Handle both single object and array of objects
            records = data if isinstance(data, list) else [data]
        
        if not records:
            return False, "No character records found in file", []
        
        valid_characters = []
        for idx, record in enumerate(records):
            is_valid, error, normalized = validate_character_input(record)
            if not is_valid:
                logger.error(f"Record {idx + 1} validation failed: {error}")
                return False, f"Record {idx + 1} validation failed: {error}", []
            valid_characters.append(normalized)
        
        return True, None, valid_characters
        
    except FileNotFoundError as e:
        return False, str(e), []
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON format: {e}", []
    except Exception as e:
        return False, f"Error processing file: {e}", []


def extract_character_args(
    character_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Extract character arguments from validated character data.
    
    Args:
        character_data: Validated character data
        
    Returns:
        Dictionary with keys suitable for argparse-style processing
    """
    args = {}
    
    # Extract mandatory fields with proper key names
    if 'name' in character_data:
        args['name'] = character_data['name']
    
    if 'sex/gender' in character_data:
        sex_gender = character_data['sex/gender']
        if isinstance(sex_gender, str):
            # Try to parse "male", "female", or "male|he/him" format
            parts = sex_gender.lower().split('|')
            args['sex'] = parts[0].strip()
            if len(parts) > 1:
                args['gender'] = parts[1].strip()
        elif isinstance(sex_gender, dict):
            args['sex'] = sex_gender.get('sex', '').lower()
            args['gender'] = sex_gender.get('gender', '').lower()
    
    if 'age' in character_data:
        args['age_range'] = character_data['age']
    
    if 'occupation' in character_data:
        args['occupation'] = character_data['occupation']
    
    if 'ethnicity' in character_data:
        args['ethnicity'] = character_data['ethnicity']
    
    # Extract optional fields from sections
    for section, fields in TEMPLATE_SECTIONS.items():
        if section in character_data and isinstance(character_data[section], dict):
            for field_name, field_value in character_data[section].items():
                args[field_name.lower().replace(' ', '_')] = field_value
    
    # Extract metadata
    if 'metadata' in character_data:
        meta = character_data['metadata']
        if isinstance(meta, dict):
            if 'new_doc_title' in meta and meta['new_doc_title']:
                args['new_doc_title'] = meta['new_doc_title']
            if 'json_output' in meta:
                args['json_output'] = meta['json_output']
    
    return args
