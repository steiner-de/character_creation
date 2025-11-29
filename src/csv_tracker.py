"""CSV tracking for character creation history."""

import csv
import os
from datetime import datetime
from typing import Optional


def append_character_record(
    csv_path: str,
    name: str,
    sex: str,
    gender: str,
    age_range: str,
    occupation: str,
    doc_url: str,
    species: Optional[str] = None,
    character_class: Optional[str] = None,
    level: Optional[int] = None
):
    """Append a character creation record to the CSV file.
    
    Args:
        csv_path: Path to CSV file
        name: Character name
        sex: male/female
        gender: he/him, she/her, they/them
        age_range: child, teen, adult, middle-age, elderly
        occupation: Character occupation
        doc_url: URL to the created Google Doc
        species: Optional D&D species
        character_class: Optional D&D class
        level: Optional D&D level
    """
    header = [
        'name', 'sex', 'gender', 'age_range', 'occupation',
        'species', 'class', 'level', 'doc_url', 'created_at'
    ]
    exists = os.path.exists(csv_path)
    
    row = {
        'name': name,
        'sex': sex,
        'gender': gender,
        'age_range': age_range,
        'occupation': occupation,
        'species': species or '',
        'class': character_class or '',
        'level': level or '',
        'doc_url': doc_url,
        'created_at': datetime.utcnow().isoformat()
    }
    
    with open(csv_path, 'a', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=header)
        if not exists:
            writer.writeheader()
        writer.writerow(row)
