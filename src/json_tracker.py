"""JSON/JSONL tracking for character creation with full AI output."""

import json
import os
import logging
from datetime import datetime
from typing import Optional, Any, Dict

logger = logging.getLogger('character_creation')


def append_character_json(
    json_path: str,
    name: str,
    sex: str,
    gender: str,
    age_range: str,
    occupation: str,
    doc_url: str,
    filled_content: str,
    species: Optional[str] = None,
    character_class: Optional[str] = None,
    level: Optional[int] = None,
    subclass: Optional[str] = None,
    dnd_enhancement: Optional[str] = None
):
    """Append a character creation record as JSONL (one JSON object per line).
    
    Args:
        json_path: Path to JSONL file
        name: Character name
        sex: male/female
        gender: he/him, she/her, they/them
        age_range: child, teen, adult, middle-age, elderly
        occupation: Character occupation
        doc_url: URL to the created Google Doc
        filled_content: Full AI-generated character content
        species: Optional D&D species
        character_class: Optional D&D class
        level: Optional D&D level
        subclass: Optional D&D subclass
        dnd_enhancement: Optional D&D enhancement content from Gemini
    """
    created_at = datetime.utcnow().isoformat()
    
    record = {
        'metadata': {
            'created_at': created_at,
            'name': name,
            'inputs': {
                'sex': sex,
                'gender': gender,
                'age_range': age_range,
                'occupation': occupation,
            },
            'doc_url': doc_url,
        },
        'ai_output': {
            'base_character': filled_content,
            'dnd_enhancement': dnd_enhancement,
        }
    }
    
    # Add D&D info if provided
    if species or character_class or level or subclass:
        record['metadata']['dnd'] = {
            'species': species,
            'class': character_class,
            'subclass': subclass,
            'level': level,
        }
    
    try:
        with open(json_path, 'a', encoding='utf-8') as fh:
            json.dump(record, fh, ensure_ascii=False)
            fh.write('\n')
        logger.info(f"Character record appended to JSON: {name} (species={species}, class={character_class}, level={level})")
    except Exception as e:
        logger.error(f"Failed to append character to JSON: {e}")
        raise


def export_characters_to_json(jsonl_path: str, output_json_path: str) -> None:
    """Convert JSONL file to pretty-printed JSON array.
    
    Args:
        jsonl_path: Path to source JSONL file
        output_json_path: Path to output JSON file
    """
    if not os.path.exists(jsonl_path):
        logger.warning(f"JSONL file not found: {jsonl_path}")
        return
    
    try:
        records = []
        with open(jsonl_path, 'r', encoding='utf-8') as fh:
            for line in fh:
                if line.strip():
                    records.append(json.loads(line))
        
        with open(output_json_path, 'w', encoding='utf-8') as fh:
            json.dump(records, fh, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(records)} characters to JSON: {output_json_path}")
    except Exception as e:
        logger.error(f"Failed to export JSONL to JSON: {e}")
        raise


def get_character_by_name(jsonl_path: str, name: str) -> Optional[Dict[str, Any]]:
    """Retrieve a character record by name from JSONL.
    
    Args:
        jsonl_path: Path to JSONL file
        name: Character name to search for
        
    Returns:
        Character record dict or None if not found
    """
    if not os.path.exists(jsonl_path):
        logger.warning(f"JSONL file not found: {jsonl_path}")
        return None
    
    try:
        with open(jsonl_path, 'r', encoding='utf-8') as fh:
            for line in fh:
                if line.strip():
                    record = json.loads(line)
                    if record.get('metadata', {}).get('name') == name:
                        return record
        
        logger.debug(f"Character not found: {name}")
        return None
    except Exception as e:
        logger.error(f"Failed to retrieve character from JSONL: {e}")
        raise


def list_characters(jsonl_path: str, limit: Optional[int] = None) -> list:
    """List all characters in JSONL file with basic info.
    
    Args:
        jsonl_path: Path to JSONL file
        limit: Optional limit on number of records to return
        
    Returns:
        List of character metadata dicts
    """
    if not os.path.exists(jsonl_path):
        logger.warning(f"JSONL file not found: {jsonl_path}")
        return []
    
    try:
        characters = []
        count = 0
        with open(jsonl_path, 'r', encoding='utf-8') as fh:
            for line in fh:
                if line.strip():
                    record = json.loads(line)
                    metadata = record.get('metadata', {})
                    characters.append({
                        'name': metadata.get('name'),
                        'created_at': metadata.get('created_at'),
                        'dnd': metadata.get('dnd'),
                        'doc_url': metadata.get('doc_url'),
                    })
                    count += 1
                    if limit and count >= limit:
                        break
        
        logger.debug(f"Listed {len(characters)} characters from JSONL")
        return characters
    except Exception as e:
        logger.error(f"Failed to list characters from JSONL: {e}")
        raise
