# JSON/JSONL Input System

## Quick Start

### Create One Character from JSON
```bash
python main.py --json character.json
```

### Create Multiple Characters from JSONL
```bash
python main.py --jsonl characters.jsonl
```

### Traditional CLI (Still Works!)
```bash
python main.py --name "Elara" --sex female --gender "she/her" \
  --age_range adult --ethnicity "Half-Elf" --occupation "Ranger"
```

## Mandatory Fields (All Required)

1. **`name`** - Character's name
2. **`ethnicity`** - Character's ethnicity/heritage
3. **`sex/gender`** - Character's sex/gender identity (e.g., "female|she/her")
4. **`age`** - Character's age or age range
5. **`occupation`** - Character's occupation

## Optional Fields (120+)

Provide any fields from the **8 template sections** to guide Gemini generation:

- **Demographics** (10 fields total) - Title, status, education, etc.
- **Physical Appearance** (19 fields) - Eyes, hair, height, build, style
- **History** (11 fields) - Birth, family, affiliations, secrets
- **Psychological Traits** (28 fields) - Personality, hobbies, fears, goals
- **Communication** (11 fields) - Languages, accent, speech style
- **Strengths/Weaknesses** (11 fields) - Abilities, disabilities, conditions
- **Relationships** (21 fields) - Friends, enemies, family, social
- **Character Growth** (10 fields) - Archetype, values, conflicts, goals

See `CHARACTER_DATA_MODEL.md` for all 121 fields with types and examples.

## Input Formats

### Single Character (JSON)
```json
{
  "metadata": {
    "new_doc_title": "Custom Doc Name",
    "json_output": true
  },
  "Demographics": {
    "name": "Elara",
    "age": "26",
    "sex/gender": "female|she/her",
    "ethnicity": "Half-Elf",
    "occupation": "Ranger"
  },
  "Psychological Traits": {
    "personality traits": "Reserved, observant"
  }
}
```

### Multiple Characters (JSONL - One Per Line)
```
{"Demographics": {"name": "Kael", "age": "38", "sex/gender": "male|he/him", "ethnicity": "Human", "occupation": "Mage"}}
{"Demographics": {"name": "Lyra", "age": "24", "sex/gender": "female|she/her", "ethnicity": "Half-Orc", "occupation": "Bard"}}
{"Demographics": {"name": "Thora", "age": "45", "sex/gender": "female|she/her", "ethnicity": "Dwarf", "occupation": "Warrior"}}
```

### JSON Array Format
```json
[
  {"Demographics": {"name": "Kael", ...}},
  {"Demographics": {"name": "Lyra", ...}},
  {"Demographics": {"name": "Thora", ...}}
]
```

## Metadata Options

| Option | Type | Purpose |
|--------|------|---------|
| `new_doc_title` | string | Custom Google Doc name (optional) |
| `json_output` | boolean | Request structured JSON output (default: false) |

## Field Name Flexibility

All equivalent:
- `name` = `Name` = `NAME`
- `sex_gender` = `sex/gender` = `Sex/Gender`
- `age_range` = `age` = `Age`
- `Physical_Appearance` = `physical appearance` = `PHYSICAL APPEARANCE`

## Validation

**Automatic checks:**
- ✅ File exists and is readable
- ✅ Valid JSON/JSONL syntax
- ✅ All 5 mandatory fields present
- ✅ Field names match template structure
- ✅ Metadata fields valid (if present)

**Error example:**
```
❌ Error: Record 1 validation failed: Missing mandatory field: Character name
```

## Usage Examples

### Minimal Input (5 Fields)
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
Gemini creatively fills all other details!

### Detailed Input (Guidance)
```json
{
  "Demographics": {
    "name": "Elara Moonwhisper",
    "age": "26",
    "sex/gender": "female|she/her",
    "ethnicity": "Half-Elf",
    "occupation": "Ranger"
  },
  "Physical Appearance": {
    "eye color": "Emerald green",
    "hair color": "Silver-blonde",
    "height": "5'8\""
  },
  "Psychological Traits": {
    "personality traits": "Reserved, observant, compassionate",
    "loves": "Nature, solitude",
    "fears": "Losing the forest"
  }
}
```

### Batch Processing with JSONL
```bash
python main.py --jsonl party.jsonl  # Creates 3 characters sequentially
```

### JSON + D&D Enhancement
```bash
python main.py --json character.json \
  --species Elf --class Ranger --level 5 --subclass "Gloom Stalker"
```

## Output Per Character

1. **Google Doc** - Full character profile
2. **CSV record** - Quick metadata tracking
3. **JSONL record** - Full AI output archived
4. **JSON file** - Individual structured JSON (if `json_output=true`)

Example CSV row:
```
name,sex,gender,age_range,occupation,species,class,subclass,level,doc_url,created_at
Elara,female,she/her,adult,Ranger,,,,,https://docs.google.com/...,2025-11-29T12:34:56
```

## Performance

- Single character: ~30-60 seconds
- 10 characters: ~5-10 minutes
- 100+ characters: ~1-2 hours
- Time varies based on Gemini latency

## Troubleshooting

**"Missing mandatory field" Error**
→ Ensure you have: name, age, sex/gender, ethnicity, occupation

**JSON validation failed**
→ Check JSON syntax with online validator

**JSONL not loading**
→ Verify each line is a complete JSON object (no trailing commas)

**Field not recognized**
→ Check `CHARACTER_DATA_MODEL.md` for exact field names

## Files

| File | Purpose |
|------|---------|
| `example_character.json` | Single character template |
| `example_characters.jsonl` | Batch template (3 chars) |
| `test_character_input.py` | Validation script |
| `CHARACTER_DATA_MODEL.md` | Complete field reference |

## Backward Compatibility

✅ 100% - Original CLI arguments unchanged
✅ D&D parameters work with JSON input
✅ All existing workflows unaffected

## Tips

1. **Minimal input** → Let Gemini be creative
2. **Detailed input** → Guide specific characteristics
3. **Batch mode** → `python main.py --jsonl huge_list.jsonl`
4. **Hybrid** → `python main.py --json char.json --species Elf --level 5`
5. **Custom titles** → Use `new_doc_title` in metadata

---

**Next Steps:**
1. Review `CHARACTER_DATA_MODEL.md` for all available fields
2. Try `python main.py --json example_character.json`
3. Batch test with `python main.py --jsonl example_characters.jsonl`
4. Read `USAGE_GUIDE.md` for advanced patterns
