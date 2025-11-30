## Architecture: JSON-Structured Character Generation

This document explains how the template parsing and JSON output system works programmatically.

## System Overview

```
Google Docs Template
        ↓
    [Parsed]
        ↓
Template Structure (Dict)
        ↓
[Schema Generated]
        ↓
Gemini Prompt + Schema
        ↓
    [Generated]
        ↓
JSON Response from Gemini
        ↓
[Validated & Processed]
        ↓
├── Google Doc (Text)
├── JSONL Record (Archive)
├── Individual JSON (Structured)
└── CSV Record (Metadata)
```

## Module Breakdown

### `template_parser.py` - New Core Module

**Responsibilities:**
- Parse template text into hierarchical structure
- Generate JSON schema instructions for Gemini
- Validate Gemini's JSON output
- Convert between JSON and text formats
- Save individual character JSON files

**Key Functions:**

1. **`parse_template_structure(template_text: str) -> Dict[str, Any]`**
   - Input: Plain text template from Google Docs
   - Process: Regex parsing for sections (###) and fields (**)
   - Output: Nested dict like `{"Section": {"Field": None, ...}, ...}`
   - Logging: DEBUG for each found section/field

   Example:
   ```python
   template = """
   ### Abilities
   **Strength:** [blank]
   """
   result = parse_template_structure(template)
   # Returns: {"Abilities": {"Strength": None}}
   ```

2. **`extract_template_schema(template_text: str) -> str`**
   - Input: Same template text
   - Process: Calls parse_template_structure() then formats as JSON schema
   - Output: Formatted string describing JSON structure
   - Purpose: Instruction for Gemini on output format

   Example output:
   ```
   Output the character as a JSON object with this structure:
   {
     "Abilities": {
       "Strength": "[value]",
       "Dexterity": "[value]"
     }
   }
   ```

3. **`build_json_character_prompt(template_text: str, character_inputs: dict) -> str`**
   - Combines template parsing with character inputs
   - Creates complete Gemini prompt with:
     - Character inputs (name, sex, gender, age, occupation)
     - Template content
     - JSON schema instructions
     - Validation requirements
   - Replaces legacy `build_character_prompt()` when `--json_output` used

4. **`validate_json_output(response_text: str) -> Tuple[bool, Optional[Dict], str]`**
   - Input: Raw text response from Gemini
   - Process: Regex search for JSON, parsing, error handling
   - Output: (is_valid, json_dict, error_message)
   - Handles: Malformed JSON, partial responses, nested errors

5. **`flatten_json_for_text(json_data: Dict[str, Any]) -> str`**
   - Converts structured JSON back to readable text
   - Used for Google Docs insertion
   - Format: Section headers + field: value pairs

6. **`save_character_json(file_path: str, character_data: Dict, character_name: str, pretty: bool = True) -> None`**
   - Saves JSON to individual file
   - Creates timestamped filename
   - Pretty-prints by default for readability

### Integration Points

**In `main.py`:**

```python
# New imports
from src.template_parser import (
    build_json_character_prompt,
    validate_json_output,
    flatten_json_for_text,
    save_character_json
)

# New CLI flag
parser.add_argument('--json_output', action='store_true', help='Save character data as structured JSON')

# Processing logic
if args.json_output:
    prompt = build_json_character_prompt(template_text, character_inputs)
else:
    prompt = build_character_prompt(template_text, character_inputs)  # Legacy

# Validation
if args.json_output:
    is_valid, character_json, error_msg = validate_json_output(gemini_response)
    if not is_valid:
        # Fallback to text
        filled_content = gemini_response
    else:
        filled_content = flatten_json_for_text(character_json)

# Storage
if args.json_output and character_json:
    save_character_json(json_file_path, character_json, args.name)
```

## Data Flow Example

### Input
```bash
python main.py \
  --name "Bram" \
  --sex male \
  --gender "he/him" \
  --age_range adult \
  --occupation "Warrior" \
  --json_output
```

### Template Fetched from Google Docs
```
### Basic Info
**Name:** {{NAME}}
**Sex:** {{SEX}}

### Abilities
**Strength:** [blank]
**Dexterity:** [blank]
```

### Step 1: Parse Structure
```python
structure = {
    "Basic Info": {"Name": None, "Sex": None},
    "Abilities": {"Strength": None, "Dexterity": None}
}
```

### Step 2: Generate Schema
```
Output JSON with structure:
{
  "Basic Info": {
    "Name": "[value]",
    "Sex": "[value]"
  },
  "Abilities": {
    "Strength": "[value]",
    "Dexterity": "[value]"
  }
}
```

### Step 3: Gemini Request
```
Prompt includes:
- Character inputs (Bram, male, he/him, adult, Warrior)
- Full template text
- Schema instructions
- Validation requirements
```

### Step 4: Gemini Response
```json
{
  "Basic Info": {
    "Name": "Bram",
    "Sex": "male"
  },
  "Abilities": {
    "Strength": "16",
    "Dexterity": "12"
  }
}
```

### Step 5: Validation & Processing
```python
is_valid, character_json, _ = validate_json_output(response)
# is_valid = True
# character_json = {the parsed dict}

filled_content = flatten_json_for_text(character_json)
# "Basic Info\n===========\nName: Bram\nSex: male\n..."
```

### Step 6: Multi-Format Storage

**Google Doc:** Flattened text inserted
**JSONL:** Full metadata + AI output (already stored by append_character_json)
**Individual JSON:** `characters/bram_20251129_123456.json` created
**CSV:** Metadata row added (already tracked by append_character_record)

## Error Handling

### JSON Parsing Fails
```
User runs with --json_output
↓
Gemini returns malformed JSON
↓
validate_json_output() returns (False, None, error_msg)
↓
Log warning, use gemini_response as fallback text
↓
Continue with text-based workflow
↓
User notified: "⚠️  JSON validation failed, using text output instead"
```

### Missing Sections in Response
- Schema is "strict" but not validated server-side
- Partial responses still validate as JSON
- Missing sections stored as None values in individual JSON
- Logged as DEBUG-level info for debugging

## Configuration

### Environment Variables
```
CHARACTERS_JSON_DIR=characters  # Where individual JSONs are saved
CHARACTERS_CSV=characters.csv   # CSV metadata
CHARACTERS_JSONL=characters.jsonl  # Full records
```

### Gemini Settings (in main.py)
```python
temperature=0.7      # Slight randomness for creativity
max_output_tokens=2048  # Enough for JSON + content
```

## Performance Characteristics

- **Template Parsing:** ~50ms for typical template (regex-based, very fast)
- **Schema Generation:** <1ms (simple string formatting)
- **JSON Validation:** ~5-10ms (JSON parsing overhead)
- **Text Flattening:** <5ms (simple iteration)
- **File I/O:** Depends on system (typically 10-50ms)

Total overhead vs. text mode: **~100ms** (negligible)

## Testing Strategy

To test the template parser:

```python
from src.template_parser import parse_template_structure, extract_template_schema

# Test parsing
template = """
### Section
**Field:** value
"""
result = parse_template_structure(template)
assert result == {"Section": {"Field": None}}

# Test schema generation
schema = extract_template_schema(template)
assert "Section" in schema
assert "Field" in schema
```

## Future Enhancements

1. **Bidirectional Schema**: Serialize JSON back to template format
2. **Schema Validation**: Stricter validation against predefined schema
3. **Template Versioning**: Track template structure changes over time
4. **Array Fields**: Support lists in JSON structure
5. **Conditional Sections**: Only include sections when certain fields exist
6. **Type Hints**: Mark fields as string/number/date in schema
7. **Export Formats**: Convert JSON to XML, YAML, CSV for different systems
