# CSV Converter - Complete Guide

## Quick Start

### Commands
```bash
# Validate CSV format
python convert_csv.py input.csv --validate

# Preview conversion
python convert_csv.py input.csv --preview

# Convert to JSON (array format)
python convert_csv.py input.csv --json output.json

# Convert to JSONL (one character per line)
python convert_csv.py input.csv --jsonl output.jsonl
```

### Use with main.py
```bash
# Single character
python main.py --json output.json

# Batch processing
python main.py --jsonl output.jsonl
```

## CSV Format

### Minimum Format (5 Required Fields)
```csv
name,age,sex/gender,ethnicity,occupation
Elara,26,female|she/her,Half-Elf,Ranger
```

### Extended Format (with optional fields)
```csv
name,age,sex/gender,ethnicity,occupation,eye_color,hair_color,personality_traits,hobbies,skills/talents
Elara,26,female|she/her,Half-Elf,Ranger,Emerald green,Silver-blonde,Reserved and observant,Tracking,Archery
```

### Field Matching Rules
- **Case-insensitive**: "Name", "name", "NAME" all work
- **Space/underscore equivalent**: "eye color" = "eye_color"
- **Special characters**: "sex/gender" automatically normalized
- **All 121 template fields supported**

### Column Names Available
**Demographics**: name, age, sex/gender, ethnicity, occupation

**Physical Appearance**: eye color, hair color, height, weight, skin tone, distinguishing features

**History**: background, family, notable events, childhood, traumas, triumphs

**Psychological Traits**: personality traits, fears, strengths, weaknesses, hobbies, interests

**Communication**: speech patterns, accent, language

**Strengths & Abilities**: abilities, talents, skills, powers, resistances, immunities

**Relationships**: allies, enemies, romantic interests, family relations

**Character Growth**: motivations, goals, potential for growth

**Metadata**: new_doc_title, json_output (true/false)

Plus 100+ additional fields from template...

## Features

✅ **Intelligent Field Matching** - Auto-recognizes field formats
✅ **Type Conversion** - String → Boolean for metadata fields
✅ **Batch Processing** - Single or multiple characters
✅ **Auto Format Selection** - JSON for 1 row, JSONL for multiple
✅ **Comprehensive Validation** - Pre-conversion checks
✅ **Full Integration** - Works with character_input validation system
✅ **Complete Logging** - Track all operations in `logs/` directory

## Testing

All tests passing:
- ✅ 15 unit tests (normalization, matching, validation, conversion)
- ✅ 4 CLI modes tested
- ✅ Integration tests: CSV → JSON/JSONL → character validation
- ✅ 5 example characters validated

**Test Results**: `python test_csv_converter.py` and `python test_csv_integration.py`

## Implementation Details

### Core Module: `src/csv_converter.py`
```python
# Main functions
csv_to_json_file(csv_path, json_output_path)         # Single/array JSON
csv_to_jsonl_file(csv_path, jsonl_output_path)       # JSONL (one per line)
csv_to_json_dict(csv_path) -> (is_valid, error, data) # Python objects
validate_csv_columns(csv_path) -> (valid, matched, unmatched)

# Utilities
normalize_field_name(field)         # Standardize field names
find_matching_field(csv_column)     # Map to template field
convert_value(value, field_name)    # Type conversion
csv_row_to_character(row)           # Convert row to character dict
```

### CLI Tool: `convert_csv.py`
- 4 operational modes: validate, preview, json, jsonl
- Error handling with clear messages
- Integrated logging
- Unicode encoding fixed for PowerShell compatibility

## Troubleshooting

**"CSV file not found"**
- Verify file path is correct and file exists

**"No columns matched template"**
- Check CSV header formatting
- Run `--validate` to see matched columns
- Verify field names match template

**"Unexpected character format"**
- Ensure CSV is properly formatted
- Check for extra quotes or special characters in data

**Emoji display issues**
- Fixed in convert_csv.py (uses [TAG] format for terminal output)

## Files

**Core**
- `src/csv_converter.py` - Conversion engine (390+ lines)
- `convert_csv.py` - CLI tool (149 lines)

**Testing**
- `test_csv_converter.py` - Unit tests (75 lines, 15 tests)
- `test_csv_integration.py` - Integration tests
- `example_characters.csv` - Test data (5 characters)

**Documentation**
- `CSV_CONVERTER.md` - This file

## Workflow

```
1. Create CSV with character data
   ↓
2. python convert_csv.py input.csv --validate
   ↓
3. python convert_csv.py input.csv --preview
   ↓
4. python convert_csv.py input.csv --json output.json
   ↓
5. python main.py --json output.json
   ↓
6. Character documents generated
```

## Backward Compatibility

✅ No changes to existing code
✅ Original main.py unchanged
✅ All existing features work
✅ CSV converter is purely additive

## Status

**PRODUCTION READY** ✅
- Core functionality: Complete
- Testing: 100% pass rate
- Integration: Fully validated
- Documentation: Complete
