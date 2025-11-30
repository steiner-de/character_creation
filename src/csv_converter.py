"""Convert CSV files to JSON/JSONL format for character creation."""

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from src.logger import get_logger

logger = get_logger()

# Template structure for reference
TEMPLATE_SECTIONS = {
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

# Metadata field names
METADATA_FIELDS = ['new_doc_title', 'json_output']

# All valid field names (lowercase for matching)
ALL_VALID_FIELDS = set(METADATA_FIELDS)
for section_fields in TEMPLATE_SECTIONS.values():
    ALL_VALID_FIELDS.update(f.lower().replace(' ', '_') for f in section_fields)


def normalize_field_name(field: str) -> str:
    """Normalize a field name for matching.
    
    Args:
        field: Field name to normalize
        
    Returns:
        Normalized field name (lowercase, spaces to underscores)
    """
    return field.lower().strip().replace(' ', '_')


def find_matching_field(csv_column: str) -> Optional[Tuple[str, str]]:
    """Find the template field that matches a CSV column name.
    
    Args:
        csv_column: Column name from CSV
        
    Returns:
        Tuple of (section_name, field_name) or None if no match
    """
    normalized = normalize_field_name(csv_column)
    
    # Check metadata fields
    for meta_field in METADATA_FIELDS:
        if normalize_field_name(meta_field) == normalized:
            return ('metadata', meta_field)
    
    # Check template sections
    for section, fields in TEMPLATE_SECTIONS.items():
        for field in fields:
            if normalize_field_name(field) == normalized:
                return (section, field)
    
    return None


def convert_value(value: str, field_name: str) -> Union[str, bool, None]:
    """Convert a CSV cell value to appropriate Python type.
    
    Args:
        value: CSV cell value
        field_name: Name of field (for context-based conversion)
        
    Returns:
        Converted value (str, bool, or None)
    """
    if not value or value.strip() == '':
        return None
    
    value = value.strip()
    
    # Boolean conversion for specific fields
    if field_name.lower() == 'json_output':
        if value.lower() in ('true', '1', 'yes', 'y'):
            return True
        elif value.lower() in ('false', '0', 'no', 'n'):
            return False
    
    return value


def csv_row_to_character(row: Dict[str, str]) -> Tuple[bool, Optional[str], Dict[str, Any]]:
    """Convert a CSV row to a character object.
    
    Args:
        row: Dictionary representing a CSV row
        
    Returns:
        Tuple of (is_valid, error_message, character_data)
    """
    character = {}
    unmatched_fields = []
    
    for csv_column, value in row.items():
        if not value or value.strip() == '':
            continue
        
        match = find_matching_field(csv_column)
        
        if not match:
            unmatched_fields.append(csv_column)
            logger.warning(f"No template field found for CSV column: {csv_column}")
            continue
        
        section, field = match
        converted_value = convert_value(value, field)
        
        if converted_value is None:
            continue
        
        if section == 'metadata':
            if 'metadata' not in character:
                character['metadata'] = {}
            character['metadata'][field] = converted_value
        else:
            if section not in character:
                character[section] = {}
            character[section][field] = converted_value
    
    if unmatched_fields:
        logger.warning(
            f"Skipped {len(unmatched_fields)} unmatched CSV columns: "
            f"{', '.join(unmatched_fields[:5])}"
            f"{'...' if len(unmatched_fields) > 5 else ''}"
        )
    
    return True, None, character


def csv_to_json(
    csv_path: str,
    json_output_path: Optional[str] = None,
    jsonl_output_path: Optional[str] = None,
) -> Tuple[bool, Optional[str], Union[Dict, List[Dict], None]]:
    """Convert CSV file to JSON or JSONL format.
    
    Args:
        csv_path: Path to CSV file
        json_output_path: Path to save JSON output (single file)
        jsonl_output_path: Path to save JSONL output (one character per line)
        
    Returns:
        Tuple of (is_valid, error_message, data)
        - If single row: Returns dict of character data
        - If multiple rows: Returns list of character dicts
    """
    csv_file = Path(csv_path)
    
    if not csv_file.exists():
        error = f"CSV file not found: {csv_path}"
        logger.error(error)
        return False, error, None
    
    if not csv_file.suffix.lower() == '.csv':
        error = f"File is not a CSV: {csv_path}"
        logger.error(error)
        return False, error, None
    
    logger.info(f"Reading CSV file: {csv_path}")
    
    try:
        characters = []
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            if not reader.fieldnames:
                error = "CSV file is empty or has no header row"
                logger.error(error)
                return False, error, None
            
            logger.debug(f"CSV columns: {reader.fieldnames}")
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is 1)
                is_valid, error, character = csv_row_to_character(row)
                
                if not is_valid:
                    error_msg = f"Row {row_num} validation failed: {error}"
                    logger.error(error_msg)
                    return False, error_msg, None
                
                if character:  # Only add if we got valid data
                    characters.append(character)
                else:
                    logger.warning(f"Row {row_num} produced no character data")
        
        if not characters:
            error = "No valid character data found in CSV"
            logger.error(error)
            return False, error, None
        
        logger.info(f"Converted {len(characters)} character(s) from CSV")
        
        # Save output files if paths provided
        if json_output_path and len(characters) == 1:
            output_file = Path(json_output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(characters[0], f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved JSON to: {json_output_path}")
            return True, None, characters[0]
        
        elif json_output_path and len(characters) > 1:
            output_file = Path(json_output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(characters, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved JSON array to: {json_output_path}")
            return True, None, characters
        
        if jsonl_output_path:
            output_file = Path(jsonl_output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                for character in characters:
                    json_line = json.dumps(character, ensure_ascii=False)
                    f.write(json_line + '\n')
            
            logger.info(f"Saved JSONL to: {jsonl_output_path}")
            return True, None, characters
        
        # Return data without saving
        if len(characters) == 1:
            return True, None, characters[0]
        else:
            return True, None, characters
    
    except csv.Error as e:
        error = f"CSV parsing error: {e}"
        logger.error(error)
        return False, error, None
    except json.JSONDecodeError as e:
        error = f"JSON encoding error: {e}"
        logger.error(error)
        return False, error, None
    except Exception as e:
        error = f"Unexpected error: {e}"
        logger.error(error)
        return False, error, None


def csv_to_json_file(
    csv_path: str,
    json_output_path: str,
) -> Tuple[bool, Optional[str]]:
    """Convert CSV to JSON file.
    
    Args:
        csv_path: Path to CSV file
        json_output_path: Path to save JSON file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    is_valid, error, _ = csv_to_json(
        csv_path,
        json_output_path=json_output_path
    )
    return is_valid, error


def csv_to_jsonl_file(
    csv_path: str,
    jsonl_output_path: str,
) -> Tuple[bool, Optional[str]]:
    """Convert CSV to JSONL file.
    
    Args:
        csv_path: Path to CSV file
        jsonl_output_path: Path to save JSONL file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    is_valid, error, _ = csv_to_json(
        csv_path,
        jsonl_output_path=jsonl_output_path
    )
    return is_valid, error


def csv_to_json_dict(csv_path: str) -> Tuple[bool, Optional[str], Union[Dict, List[Dict], None]]:
    """Convert CSV to Python dict (single character) or list of dicts (multiple).
    
    Args:
        csv_path: Path to CSV file
        
    Returns:
        Tuple of (is_valid, error_message, data)
    """
    return csv_to_json(csv_path)


def validate_csv_columns(csv_path: str) -> Tuple[bool, List[str], List[str]]:
    """Validate CSV columns against template fields.
    
    Args:
        csv_path: Path to CSV file
        
    Returns:
        Tuple of (all_valid, matched_columns, unmatched_columns)
    """
    csv_file = Path(csv_path)
    
    if not csv_file.exists():
        logger.error(f"CSV file not found: {csv_path}")
        return False, [], []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            columns = reader.fieldnames or []
        
        matched = []
        unmatched = []
        
        for column in columns:
            if find_matching_field(column):
                matched.append(column)
            else:
                unmatched.append(column)
        
        all_valid = len(unmatched) == 0
        
        logger.info(
            f"CSV validation: {len(matched)} matched, {len(unmatched)} unmatched"
        )
        
        return all_valid, matched, unmatched
    
    except Exception as e:
        logger.error(f"Error validating CSV columns: {e}")
        return False, [], []
