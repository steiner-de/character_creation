"""CSV tracking for character creation history."""

import csv
import os
import logging
from datetime import datetime
from typing import Optional, Dict, List

logger = logging.getLogger('character_creation')


class CharacterCSVTracker:
    """CSV tracker for character creation records.
    
    Manages reading and writing character creation history to CSV files
    with support for D&D mechanics (species, class, level, subclass).
    """

    # CSV file headers
    HEADERS: List[str] = [
        'name', 'sex', 'gender', 'age_range', 'occupation',
        'species', 'class', 'subclass', 'level', 'doc_url', 'created_at'
    ]

    def __init__(self, csv_path: str) -> None:
        """Initialize the CSV tracker.
        
        Args:
            csv_path: Path to the CSV file for tracking characters
        """
        self.csv_path: str = csv_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Create CSV file with headers if it doesn't exist."""
        if not os.path.exists(self.csv_path):
            with open(
                self.csv_path, 'w',
                newline='', encoding='utf-8'
            ) as fh:
                writer = csv.DictWriter(fh, fieldnames=self.HEADERS)
                writer.writeheader()
                logger.debug(f"CSV file created: {self.csv_path}")

    def append_record(
        self,
        name: str,
        sex: str,
        gender: str,
        age_range: str,
        occupation: str,
        doc_url: str,
        species: Optional[str] = None,
        character_class: Optional[str] = None,
        level: Optional[int] = None,
        subclass: Optional[str] = None
    ) -> None:
        """Append a character creation record to the CSV file.

        Args:
            name: Character name
            sex: male/female
            gender: he/him, she/her, they/them
            age_range: child, teen, adult, middle-age, elderly
            occupation: Character occupation
            doc_url: URL to the created Google Doc
            species: Optional D&D species
            character_class: Optional D&D class
            level: Optional D&D level
            subclass: Optional D&D subclass
        """
        row: Dict[str, str | int] = {
            'name': name,
            'sex': sex,
            'gender': gender,
            'age_range': age_range,
            'occupation': occupation,
            'species': species or '',
            'class': character_class or '',
            'subclass': subclass or '',
            'level': level or '',
            'doc_url': doc_url,
            'created_at': datetime.utcnow().isoformat()
        }

        with open(
            self.csv_path, 'a',
            newline='', encoding='utf-8'
        ) as fh:
            writer = csv.DictWriter(fh, fieldnames=self.HEADERS)
            writer.writerow(row)
            class_desc = (
                f"{species} {character_class}" if character_class
                else "generic"
            )
            logger.info(
                f"Character record added to CSV: {name} ({class_desc})"
            )

    def get_all_records(self) -> List[Dict[str, str]]:
        """Retrieve all character records from CSV.

        Returns:
            List of character records as dictionaries
        """
        if not os.path.exists(self.csv_path):
            return []

        records: List[Dict[str, str]] = []
        with open(
            self.csv_path, 'r',
            newline='', encoding='utf-8'
        ) as fh:
            reader = csv.DictReader(fh)
            records = list(reader) if reader else []

        logger.debug(f"Retrieved {len(records)} records from CSV")
        return records

    def get_character_by_name(self, name: str) -> Optional[Dict[str, str]]:
        """Find a character by name.

        Args:
            name: Character name to search for

        Returns:
            Character record dict or None if not found
        """
        records = self.get_all_records()
        for record in records:
            if record.get('name', '').lower() == name.lower():
                logger.debug(f"Found character: {name}")
                return record

        logger.warning(f"Character not found: {name}")
        return None

    def get_records_by_species(
        self, species: str
    ) -> List[Dict[str, str]]:
        """Find all characters of a specific species.

        Args:
            species: Species name to filter by

        Returns:
            List of character records matching the species
        """
        records = self.get_all_records()
        matching = [
            r for r in records
            if r.get('species', '').lower() == species.lower()
        ]
        logger.debug(f"Found {len(matching)} characters of species: {species}")
        return matching

    def get_records_by_class(
        self, character_class: str
    ) -> List[Dict[str, str]]:
        """Find all characters of a specific class.

        Args:
            character_class: Class name to filter by

        Returns:
            List of character records matching the class
        """
        records = self.get_all_records()
        matching = [
            r for r in records
            if r.get('class', '').lower() == character_class.lower()
        ]
        logger.debug(
            f"Found {len(matching)} characters of class: {character_class}"
        )
        return matching

    def get_record_count(self) -> int:
        """Get total number of character records.

        Returns:
            Number of characters tracked
        """
        records = self.get_all_records()
        return len(records)

    def clear_all_records(self) -> None:
        """Clear all records and reset CSV file with headers.

        Warning: This action is irreversible!
        """
        with open(
            self.csv_path, 'w',
            newline='', encoding='utf-8'
        ) as fh:
            writer = csv.DictWriter(fh, fieldnames=self.HEADERS)
            writer.writeheader()
        logger.warning(f"All records cleared from CSV: {self.csv_path}")


# Backward compatibility: Keep module-level function
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
    level: Optional[int] = None,
    subclass: Optional[str] = None
) -> None:
    """Append a character creation record to the CSV file.
    
    Deprecated: Use CharacterCSVTracker class instead.
    
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
        subclass: Optional D&D subclass
    """
    tracker = CharacterCSVTracker(csv_path)
    tracker.append_record(
        name=name,
        sex=sex,
        gender=gender,
        age_range=age_range,
        occupation=occupation,
        doc_url=doc_url,
        species=species,
        character_class=character_class,
        level=level,
        subclass=subclass
    )
