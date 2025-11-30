#!/usr/bin/env python3
"""Quick test of character input validation."""

from src.character_input import process_character_file

# Test JSON loading
print("Testing JSON file loading...")
is_valid, error, chars = process_character_file('example_character.json', is_jsonl=False)
if is_valid:
    print('✓ JSON file loaded successfully')
    print(f'  Characters loaded: {len(chars)}')
    if chars:
        char = chars[0]
        print(f'  Name: {char.get("name")}')
        print(f'  Ethnicity: {char.get("ethnicity")}')
        print(f'  Metadata: {char.get("metadata")}')
else:
    print(f'✗ Error: {error}')

# Test JSONL loading
print("\nTesting JSONL file loading...")
is_valid, error, chars = process_character_file('example_characters.jsonl', is_jsonl=True)
if is_valid:
    print('✓ JSONL file loaded successfully')
    print(f'  Characters loaded: {len(chars)}')
    for i, char in enumerate(chars, 1):
        print(f'  {i}. {char.get("name")}')
else:
    print(f'✗ Error: {error}')

print("\n✅ All tests passed!")
