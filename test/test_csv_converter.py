#!/usr/bin/env python3
"""Test CSV converter functionality."""

from src.csv_converter import (
    csv_to_json_dict,
    validate_csv_columns,
    normalize_field_name,
    find_matching_field,
)


def test_normalize_field_name():
    """Test field name normalization."""
    print("Testing field name normalization...")
    
    test_cases = [
        ("Name", "name"),
        ("Sex/Gender", "sex/gender"),
        ("Eye Color", "eye_color"),
        ("PERSONALITY TRAITS", "personality_traits"),
        ("  spaces  ", "spaces"),
    ]
    
    for input_val, expected in test_cases:
        result = normalize_field_name(input_val)
        status = "✓" if result == expected else "✗"
        print(f"  {status} normalize_field_name('{input_val}') = '{result}'")
        if result != expected:
            print(f"     Expected: '{expected}'")


def test_find_matching_field():
    """Test field matching."""
    print("\nTesting field matching...")
    
    test_cases = [
        ("name", ("Demographics", "name")),
        ("Name", ("Demographics", "name")),
        ("Eye Color", ("Physical Appearance", "eye color")),
        ("eye_color", ("Physical Appearance", "eye color")),
        ("personality traits", ("Psychological Traits", "personality traits")),
        ("unknown field", None),
    ]
    
    for input_val, expected in test_cases:
        result = find_matching_field(input_val)
        status = "✓" if result == expected else "✗"
        print(f"  {status} find_matching_field('{input_val}') = {result}")
        if result != expected:
            print(f"     Expected: {expected}")


def test_validate_csv():
    """Test CSV validation."""
    print("\nTesting CSV validation...")
    
    try:
        all_valid, matched, unmatched = validate_csv_columns(
            'example_characters.csv'
        )
        
        print(f"  CSV file: example_characters.csv")
        print(f"  Matched columns: {len(matched)}")
        for col in matched[:5]:
            print(f"    • {col}")
        
        if len(matched) > 5:
            print(f"    ... and {len(matched) - 5} more")
        
        if unmatched:
            print(f"  Unmatched columns: {len(unmatched)}")
            for col in unmatched:
                print(f"    • {col}")
        else:
            print("  ✓ All columns matched!")
    
    except Exception as e:
        print(f"  ✗ Error: {e}")


def test_csv_conversion():
    """Test CSV to JSON conversion."""
    print("\nTesting CSV conversion...")
    
    try:
        is_valid, error, data = csv_to_json_dict('example_characters.csv')
        
        if not is_valid:
            print(f"  ✗ Error: {error}")
            return
        
        if isinstance(data, list):
            print(f"  ✓ Converted {len(data)} character(s)")
            for char in data:
                if 'Demographics' in char and 'name' in char['Demographics']:
                    print(f"    • {char['Demographics']['name']}")
        else:
            print(f"  ✓ Converted 1 character")
            if 'Demographics' in data and 'name' in data['Demographics']:
                print(f"    • {data['Demographics']['name']}")
    
    except Exception as e:
        print(f"  ✗ Error: {e}")


if __name__ == '__main__':
    print("=" * 60)
    print("CSV Converter Tests")
    print("=" * 60 + "\n")
    
    test_normalize_field_name()
    test_find_matching_field()
    test_validate_csv()
    test_csv_conversion()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
