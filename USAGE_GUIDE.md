# Character Input System - Complete Guide

## Quick Start

The character creation system now supports **three input methods**:

### 1. JSON File (Single or Multiple Characters)

```bash
# Single character from JSON
python main.py --json character.json

# Array of characters from JSON
python main.py --json characters.json
```

### 2. JSONL File (Multiple Characters - One Per Line)

```bash
# Multiple characters from JSONL
python main.py --jsonl characters.jsonl
```

### 3. CLI Arguments (Traditional)

```bash
python main.py --name "Elara" --sex female --gender she/her \
  --age_range "young adult" --ethnicity "Half-Elf" --occupation "Ranger"
```

## Understanding the New Input Structure

### Mandatory Fields (Required)

Every character **must** have these 5 fields:

1. **`name`** - The character's name
2. **`ethnicity`** - The character's ethnicity/heritage
3. **`sex/gender`** - Character's sex and/or gender identity
4. **`age`** - Age or age range
5. **`occupation`** - What the character does for work

### Optional Fields (All From Template)

You can optionally provide any field from the **character template structure**, including:

- **Demographics** (10 fields) - Names, titles, status, education
- **Physical Appearance** (19 fields) - Eyes, hair, height, build, style
- **History** (11 fields) - Birth, family, affiliations, secrets
- **Psychological Traits** (28 fields) - Personality, hobbies, fears, goals
- **Communication** (11 fields) - Languages, accent, speech style
- **Strengths/Weaknesses** (11 fields) - Abilities, disabilities, conditions
- **Relationships** (21 fields) - Friends, enemies, family, social
- **Character Growth** (10 fields) - Archetype, values, conflicts, goals

### Metadata (Optional)

Control output behavior with metadata:

- **`new_doc_title`** - Custom Google Doc name
- **`json_output`** - Request structured JSON output (true/false)

## Practical Examples

### Example 1: Minimal JSON Input

**File: `minimal_character.json`**
```json
{
  "Demographics": {
    "name": "Kael",
    "age": "35",
    "sex/gender": "male|he/him",
    "ethnicity": "Human",
    "occupation": "Wizard"
  }
}
```

**Usage:**
```bash
python main.py --json minimal_character.json
```

Gemini will creatively fill in all other details while maintaining consistency.

---

### Example 2: Detailed JSON Input

**File: `detailed_character.json`**
```json
{
  "metadata": {
    "new_doc_title": "Elara - The Ranger",
    "json_output": true
  },
  "Demographics": {
    "name": "Elara Moonwhisper",
    "titles": "Ranger of the Northern Woods",
    "age": "26",
    "sex/gender": "female|she/her",
    "ethnicity": "Half-Elf",
    "occupation": "Ranger",
    "socioeconomic status": "Middle class",
    "education": "Self-taught"
  },
  "Physical Appearance": {
    "eye color": "Emerald green",
    "hair color": "Silver-blonde",
    "height": "5'8\"",
    "build": "Athletic and lean",
    "tattoos": "Runes along left arm"
  },
  "Psychological Traits": {
    "personality traits": "Reserved, observant, compassionate",
    "loves": "Nature, solitude",
    "fears": "Losing the forest"
  }
}
```

**Usage:**
```bash
python main.py --json detailed_character.json
```

---

### Example 3: Multiple Characters in JSONL

**File: `party.jsonl`**
```
{"metadata": {"new_doc_title": "Kael the Mage"}, "Demographics": {"name": "Kael Shadowstep", "age": "38", "sex/gender": "male|he/him", "ethnicity": "Human", "occupation": "Mage"}, "Psychological Traits": {"personality traits": "Mysterious, ambitious"}}
{"metadata": {"new_doc_title": "Lyra the Bard"}, "Demographics": {"name": "Lyra Songborne", "age": "24", "sex/gender": "female|she/her", "ethnicity": "Half-Orc", "occupation": "Bard"}, "Communication": {"languages known": "Common, Orcish, Elvish"}}
{"metadata": {"new_doc_title": "Thora the Warrior"}, "Demographics": {"name": "Thora Ironborn", "age": "45", "sex/gender": "female|she/her", "ethnicity": "Dwarf", "occupation": "Warrior"}, "History": {"affiliations": "Dwarven Clans"}}
```

**Usage:**
```bash
python main.py --jsonl party.jsonl
```

Creates 3 characters in sequence: Kael, Lyra, and Thora.

---

### Example 4: JSON with D&D Enhancement

**File: `dnd_character.json`**
```json
{
  "metadata": {
    "new_doc_title": "Elara - Ranger (Level 5)",
    "json_output": true
  },
  "Demographics": {
    "name": "Elara Moonwhisper",
    "age": "26",
    "sex/gender": "female|she/her",
    "ethnicity": "Half-Elf",
    "occupation": "Adventurer"
  }
}
```

**Usage with D&D Parameters:**
```bash
python main.py --json dnd_character.json \
  --species Elf --class Ranger --level 5 --subclass "Gloom Stalker"
```

Combines JSON input with D&D enhancement.

---

### Example 5: Batch Processing Multiple Characters

**File: `characters_batch.jsonl`**
```
{"Demographics": {"name": "Alice", "age": "30", "sex/gender": "female|she/her", "ethnicity": "Human", "occupation": "Cleric"}}
{"Demographics": {"name": "Bob", "age": "25", "sex/gender": "male|he/him", "ethnicity": "Dwarf", "occupation": "Rogue"}}
{"Demographics": {"name": "Carol", "age": "35", "sex/gender": "female|they/them", "ethnicity": "Elf", "occupation": "Paladin"}}
```

**Usage:**
```bash
python main.py --jsonl characters_batch.jsonl
```

Creates 3 separate Google Docs with tracked characters.

---

## Key Features

### 1. **Flexible Field Input**

Fields are **case-insensitive** and **space/underscore normalized**:
- `name` = `Name` = `NAME`
- `sex_gender` = `sex/gender`
- `age_range` = `age`

### 2. **Validation**

The system validates:
- ✅ All 5 mandatory fields are present
- ✅ Field structure matches template
- ✅ Proper JSON/JSONL formatting
- ❌ Provides clear error messages if validation fails

### 3. **Metadata Control**

- `json_output: true` → Requests structured JSON from Gemini
- `new_doc_title` → Custom Google Doc naming

### 4. **Batch Processing**

JSONL supports creating multiple characters in a single command:
```bash
python main.py --jsonl hundred_characters.jsonl
```

Each character creates:
- Individual Google Doc
- CSV tracking record
- JSONL tracking record
- Optional JSON character file (if metadata.json_output = true)

### 5. **Hybrid Mode**

Combine JSON input with CLI parameters:

```bash
# D&D parameters override/supplement JSON
python main.py --json character.json --species Elf --class Ranger --level 5

# All D&D params are optional
python main.py --jsonl party.jsonl --species Halfling
```

## Input Validation & Error Handling

### Valid JSON Examples

**Single character:**
```json
{
  "Demographics": {
    "name": "Hero",
    "age": "20",
    "sex/gender": "male|he/him",
    "ethnicity": "Human",
    "occupation": "Adventurer"
  }
}
```

**Array of characters:**
```json
[
  {"Demographics": {...}},
  {"Demographics": {...}}
]
```

**With metadata:**
```json
{
  "metadata": {"json_output": true},
  "Demographics": {...}
}
```

### Error Messages

**Missing mandatory field:**
```
❌ Error: Record 1 validation failed: Missing mandatory field: Character name
```

**Invalid JSON format:**
```
❌ Error: Invalid JSON format: Expecting value: line 1 column 1 (char 0)
```

**File not found:**
```
❌ Error: File not found: /path/to/file.json
```

## Output Files

For each character created:

1. **Google Doc** - Full character profile (viewable/editable online)
2. **characters.csv** - Quick reference tracking
3. **characters.jsonl** - Complete AI output history
4. **characters/{name}_{date}.json** - Individual JSON (if json_output=true)

## Complete Template Structure Reference

See `CHARACTER_INPUT_FORMAT.md` for the complete field reference with all available template sections and fields.

## Troubleshooting

### "Missing mandatory field" Error

**Check that you have:**
- `name` somewhere in Demographics
- `age` somewhere in Demographics
- `sex/gender` or separate `sex` and `gender` in Demographics
- `ethnicity` in Demographics
- `occupation` in Demographics

### JSON not loading

**Verify:**
- File exists at specified path
- Valid JSON syntax (use online JSON validator)
- For JSONL: exactly one JSON object per line
- No trailing commas in objects

### Metadata not being used

**Check:**
- `metadata` is a top-level key in JSON
- Fields are spelled correctly: `new_doc_title`, `json_output`
- `json_output` is a boolean (true/false, not "true"/"false" string)

## Performance Notes

- Single character: ~30-60 seconds (includes Google API calls)
- 10 characters: ~5-10 minutes
- 100+ characters: ~1-2 hours
- Time varies based on Gemini response latency

## Next Steps

1. **Create your first character:**
   ```bash
   python main.py --json example_character.json
   ```

2. **Try batch processing:**
   ```bash
   python main.py --jsonl example_characters.jsonl
   ```

3. **Add D&D details:**
   ```bash
   python main.py --json example_character.json --species Elf --class Ranger --level 5
   ```

4. **Request JSON output:**
   Edit your JSON file's metadata to set `json_output: true` for structured output.

## Questions?

Refer to:
- `CHARACTER_INPUT_FORMAT.md` - Complete field reference
- `character_template_structure.json` - Template structure
- `example_character.json` - Single character example
- `example_characters.jsonl` - Multiple character example
