# Update Summary: JSON/JSONL Input Support

## Overview

The character creation system has been updated to support **JSON and JSONL file inputs** in addition to traditional CLI arguments. Characters can now be created from structured data files with full template field support and metadata options.

## Changes Made

### 1. **Updated Character Template Structure**

**File:** `character_template_structure.json`

Added metadata section at the top level:

```json
{
  "metadata": {
    "new_doc_title": null,
    "json_output": false
  },
  "High-Level Overview": [],
  "Demographics": [...],
  ...
}
```

**Purpose:** Schema reference for all valid character input fields.

---

### 2. **New Character Input Module**

**File:** `src/character_input.py` (422 lines)

**Functions:**

- **`load_json_file(file_path)`** - Load and parse JSON file
- **`load_jsonl_file(file_path)`** - Load and parse JSONL file (one JSON per line)
- **`validate_character_input(character_data)`** - Validate mandatory fields and structure
- **`process_character_file(file_path, is_jsonl)`** - Load and validate file, return validated characters
- **`extract_character_args(character_data)`** - Convert validated data to CLI-compatible arguments

**Features:**

- ✅ Case-insensitive field matching
- ✅ Space/underscore normalization (`sex_gender` → `sex/gender`)
- ✅ Nested section handling (Demographics, Physical Appearance, etc.)
- ✅ Metadata extraction (`new_doc_title`, `json_output`)
- ✅ Comprehensive validation with meaningful error messages
- ✅ Support for both single objects and arrays in JSON
- ✅ Full JSONL line-by-line parsing

**Mandatory Fields Validated:**
- `name` (Character name)
- `ethnicity` (Character ethnicity)
- `sex/gender` (Character sex/gender)
- `age` (Character age)
- `occupation` (Character occupation)

---

### 3. **Updated Main CLI**

**File:** `main.py` (refactored from 316 to 396 lines)

**Key Changes:**

- Added mutually exclusive input group:
  - `--json` - Path to JSON file
  - `--jsonl` - Path to JSONL file
  - `--name` - CLI mode (original behavior)

- **New flow:**
  1. Parse arguments to determine input source
  2. Load and validate character data from file or CLI
  3. Process each character sequentially
  4. For each character:
     - Build prompt with all provided fields
     - Call Gemini API
     - Create Google Doc
     - Save to CSV/JSONL/JSON tracking files

- **Batch processing:** Automatically handles multiple characters from JSONL files
- **CLI parameter override:** D&D parameters from CLI override/supplement file data
- **Metadata support:** Respects `new_doc_title` and `json_output` from input

**New Imports:**
```python
from src.character_input import (
    process_character_file,
    extract_character_args,
)
```

---

### 4. **Documentation Files**

#### **`CHARACTER_INPUT_FORMAT.md`** (250+ lines)

Complete reference guide including:
- All template sections and fields
- Field descriptions and examples
- JSON structure specifications
- Usage examples (JSON, JSONL, CLI)
- Field name matching rules
- Validation rules
- Output behavior

#### **`USAGE_GUIDE.md`** (350+ lines)

Practical usage guide including:
- Quick start examples
- 5+ real-world example characters
- Batch processing guide
- D&D enhancement examples
- Feature explanations
- Error troubleshooting
- Performance notes

---

### 5. **Example Files**

#### **`example_character.json`**
Single detailed character example with:
- Metadata settings
- Demographics
- Physical Appearance
- History
- Psychological Traits
- Communication
- Relationships
- Character Growth

#### **`example_characters.jsonl`**
Three characters (Kael, Lyra, Thora) demonstrating:
- JSONL format (one character per line)
- Minimal field sets
- Different ethnicities and occupations
- Optional metadata

---

### 6. **Test File**

**File:** `test_character_input.py`

Simple validation script that:
- Tests JSON file loading
- Tests JSONL file loading
- Displays loaded characters
- Verifies metadata extraction

---

## Usage Examples

### Single Character from JSON

```bash
python main.py --json character.json
```

### Multiple Characters from JSONL

```bash
python main.py --jsonl party.jsonl
```

### Traditional CLI Mode

```bash
python main.py --name "Elara" --sex female --gender she/her \
  --age_range "young adult" --ethnicity "Half-Elf" --occupation "Ranger"
```

### JSON + D&D Enhancement

```bash
python main.py --json character.json \
  --species Elf --class Ranger --level 5 --subclass "Gloom Stalker"
```

---

## Mandatory vs Optional Fields

### Always Required (5 fields)

- `name`
- `ethnicity`
- `sex/gender`
- `age`
- `occupation`

### Completely Optional (120+ fields)

- Demographics (9 additional fields)
- Physical Appearance (19 fields)
- History (11 fields)
- Psychological Traits (28 fields)
- Communication (11 fields)
- Strengths/Weaknesses (11 fields)
- Relationships (21 fields)
- Character Growth (10 fields)

### Metadata (Optional)

- `new_doc_title` - Custom Google Doc name
- `json_output` - Request structured JSON (true/false)

---

## Input Format Flexibility

All field names are **normalized**:

✅ These are equivalent:
- `name` / `Name` / `NAME`
- `sex_gender` / `sex/gender` / `Sex/Gender`
- `age_range` / `age`

✅ Nested sections work:
```json
{
  "Demographics": {
    "name": "Kael",
    "ethnicity": "Human",
    ...
  }
}
```

✅ Top-level fields also work:
```json
{
  "name": "Kael",
  "ethnicity": "Human",
  ...
}
```

✅ Arrays and single objects:
```json
[{...}, {...}, {...}]  // Array
{...}                  // Single object
```

---

## Processing Flow

```
Input (JSON/JSONL/CLI)
        ↓
Parse & Load
        ↓
Validate Mandatory Fields
        ↓
Extract Optional Fields
        ↓
Normalize Field Names
        ↓
For Each Character:
  - Build Gemini Prompt
  - Call Gemini API
  - Create Google Doc
  - Save Tracking Records
  - (Optionally) Save JSON
        ↓
Output Summary
```

---

## Validation & Error Handling

**Validation Checks:**
- ✅ File exists and is readable
- ✅ Valid JSON/JSONL syntax
- ✅ All 5 mandatory fields present
- ✅ Field names match template structure
- ✅ Metadata fields valid (if present)

**Error Responses:**
- File not found → Clear error message
- JSON syntax error → Reports line number
- Missing mandatory field → Lists which field
- Invalid field names → Continues with valid fields

---

## Backward Compatibility

**Fully maintained:**
- CLI mode works exactly as before
- All existing CLI arguments supported
- Legacy behavior unchanged
- All tracking files compatible

**Enhancement, not replacement:**
- JSON/JSONL as alternative input
- CLI arguments still work
- Can mix CLI + file inputs (D&D params override)

---

## File Changes Summary

| File | Change Type | Lines Changed |
|------|-------------|---------------|
| `src/character_input.py` | NEW | 422 |
| `main.py` | UPDATED | ~80 lines refactored |
| `character_template_structure.json` | UPDATED | 4 lines added (metadata) |
| `CHARACTER_INPUT_FORMAT.md` | NEW | 250+ |
| `USAGE_GUIDE.md` | NEW | 350+ |
| `example_character.json` | NEW | 50 |
| `example_characters.jsonl` | NEW | 3 |
| `test_character_input.py` | NEW | 18 |

**Total New Content:** ~1,100 lines

---

## Key Benefits

1. **Batch Processing** - Create 100+ characters in one command
2. **Data-Driven** - Characters defined in portable JSON format
3. **Template-Based** - All 121 template fields available as input
4. **Flexible** - Provide as much or as little detail as desired
5. **Documented** - Comprehensive examples and references
6. **Validated** - Clear errors when mandatory fields missing
7. **Compatible** - Works alongside existing CLI mode

---

## Testing

**Syntax validation:**
```bash
python -m py_compile src/character_input.py main.py
# ✅ No errors
```

**Functional testing:**
```bash
python test_character_input.py
# ✅ All tests passed
# ✓ JSON file loaded successfully
# ✓ JSONL file loaded successfully
```

---

## Next Steps for Users

1. ✅ Review `USAGE_GUIDE.md` for quick start
2. ✅ Try `example_character.json` for single character
3. ✅ Try `example_characters.jsonl` for batch processing
4. ✅ Reference `CHARACTER_INPUT_FORMAT.md` for complete field list
5. ✅ Create your own JSON/JSONL files for your characters

---

## Summary

The character creation system now supports professional-grade batch processing with JSON/JSONL input files, while maintaining full backward compatibility with the existing CLI interface. Mandatory fields (name, ethnicity, sex/gender, age, occupation) are validated, and optional fields from the complete 121-field template can be provided to guide AI generation. Metadata fields allow control over output format and Google Doc naming.
