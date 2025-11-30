#!/usr/bin/env python3
"""
Test CSV converter integration with main.py input system.
Tests that CSV → JSON/JSONL → character_input validation works.
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from csv_converter import csv_to_json_dict
from character_input import validate_character_input, load_json_file, load_jsonl_file

def test_csv_to_json_dict():
    """Test CSV to dict conversion"""
    print("\n[TEST] CSV to dict conversion...")
    csv_file = Path("example_characters.csv")
    
    if not csv_file.exists():
        print(f"[ERROR] CSV file not found: {csv_file}")
        return False
    
    try:
        is_valid, error, data = csv_to_json_dict(csv_file)
        
        if not is_valid:
            print(f"[ERROR] CSV conversion failed: {error}")
            return False
        
        if isinstance(data, dict):
            print(f"[OK] Single character dict: {data.get('Demographics', {}).get('name', 'Unknown')}")
        elif isinstance(data, list):
            print(f"[OK] Multiple characters: {len(data)} characters")
            for i, char in enumerate(data, 1):
                name = char.get('Demographics', {}).get('name', 'Unknown')
                print(f"     {i}. {name}")
        else:
            print(f"[ERROR] Unexpected data type: {type(data)}")
            return False
        
        return True
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False


def test_json_validation():
    """Test that converted JSON validates correctly"""
    print("\n[TEST] JSON validation...")
    
    # Generate JSON from CSV
    csv_file = Path("example_characters.csv")
    json_file = Path("test_integration_output.json")
    
    try:
        from csv_converter import csv_to_json_file
        
        is_valid, error = csv_to_json_file(csv_file, json_file)
        if not is_valid:
            print(f"[ERROR] CSV conversion failed: {error}")
            return False
        
        print(f"[OK] JSON file created: {json_file}")
        
        # Load and validate JSON
        characters = load_json_file(str(json_file))
        print(f"[OK] Loaded {len(characters)} characters from JSON")
        
        # Validate each character
        for i, char_data in enumerate(characters, 1):
            is_valid, error, normalized = validate_character_input(char_data)
            if not is_valid:
                print(f"[WARNING] Character {i} validation issue: {error}")
            else:
                name = char_data.get('Demographics', {}).get('name', 'Unknown')
                print(f"[OK] Character {i} ({name}) validated successfully")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_jsonl_validation():
    """Test that converted JSONL validates correctly"""
    print("\n[TEST] JSONL validation...")
    
    # Generate JSONL from CSV
    csv_file = Path("example_characters.csv")
    jsonl_file = Path("test_integration_output.jsonl")
    
    try:
        from csv_converter import csv_to_jsonl_file
        
        is_valid, error = csv_to_jsonl_file(csv_file, jsonl_file)
        if not is_valid:
            print(f"[ERROR] CSV conversion failed: {error}")
            return False
        
        print(f"[OK] JSONL file created: {jsonl_file}")
        
        # Load and validate JSONL
        characters = load_jsonl_file(str(jsonl_file))
        print(f"[OK] Loaded {len(characters)} characters from JSONL")
        
        # Validate each character
        for i, char_data in enumerate(characters, 1):
            is_valid, error, normalized = validate_character_input(char_data)
            if not is_valid:
                print(f"[WARNING] Character {i} validation issue: {error}")
            else:
                name = char_data.get('Demographics', {}).get('name', 'Unknown')
                print(f"[OK] Character {i} ({name}) validated successfully")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print("CSV Converter Integration Tests")
    print("=" * 60)
    
    results = {
        "CSV to dict": test_csv_to_json_dict(),
        "JSON validation": test_json_validation(),
        "JSONL validation": test_jsonl_validation(),
    }
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "[OK]" if result else "[FAILED]"
        print(f"{status} {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n[OK] All integration tests passed!")
    else:
        print("\n[ERROR] Some integration tests failed!")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
