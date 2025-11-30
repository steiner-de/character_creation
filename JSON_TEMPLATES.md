## JSON-Structured Template Output Guide

This guide explains how to use the template parsing and structured JSON output features.

## Understanding Template Structure

The system automatically parses your Google Docs template to extract its structure. Templates should use **markdown-style headings** for organization:

### Template Format

**Main sections** (top-level JSON keys):
```
### Section Name
```

**Fields** (nested JSON keys):
- Using bold syntax: `**Field Name:** [content]`
- Using bullet points: `- Field Name: [content]`

### Example Template

```
### Basic Information
**Name:** {{NAME}}
**Sex:** {{SEX}}
**Gender:** {{GENDER}}
**Age Range:** {{AGE_RANGE}}
**Occupation:** {{OCCUPATION}}

### Physical Description
**Height:** [to be filled]
**Build:** [to be filled]
**Distinguishing Features:** [to be filled]

### Personality
**Temperament:** [to be filled]
**Fears:** [to be filled]
**Motivations:** [to be filled]

### Background
**Childhood:** [to be filled]
**Family:** [to be filled]
**Defining Moment:** [to be filled]
```

## Generated JSON Structure

Running with `--json_output` flag will produce this structure:

```json
{
  "Basic Information": {
    "Name": "Astra Moon",
    "Sex": "female",
    "Gender": "she/her",
    "Age Range": "adult",
    "Occupation": "Starship Pilot"
  },
  "Physical Description": {
    "Height": "5'6\"",
    "Build": "Athletic",
    "Distinguishing Features": "Cybernetic left arm with constellation tattoos"
  },
  "Personality": {
    "Temperament": "Confident and quick-witted",
    "Fears": "Loss of autonomy, being grounded",
    "Motivations": "Explore unknown space, find purpose among the stars"
  },
  "Background": {
    "Childhood": "Grew up in a space station...",
    "Family": "Parents were both pilots...",
    "Defining Moment": "First solo flight at age 16..."
  }
}
```

## Using JSON Output Mode

### Basic Usage

```bash
python main.py \
  --name "Character Name" \
  --sex male \
  --gender "he/him" \
  --age_range adult \
  --occupation "Profession" \
  --json_output
```

### Features

1. **Structured Storage**: Individual JSON files saved to `characters/` directory
2. **Filename Format**: `character_name_YYYYMMDD_HHMMSS.json`
3. **Text Fallback**: If JSON parsing fails, text output is used
4. **Dual Tracking**: Data saved to both JSONL and individual JSON files

### Output Files

When using `--json_output`, you get:

1. **Google Doc** (as always) - for collaborative editing
2. **JSONL record** in `characters.jsonl` - for archival
3. **Individual JSON** in `characters/character_name_YYYYMMDD_HHMMSS.json` - for programmatic access

## Programmatic Access to JSON Data

### Reading Character JSON

```python
import json

# Load a single character
with open('characters/astra_moon_20251129_123456.json', 'r') as f:
    character = json.load(f)

# Access nested fields
print(character['Basic Information']['Name'])
print(character['Personality']['Motivations'])
```

### Querying JSONL Records

```python
import json

# Read all character records from JSONL
with open('characters.jsonl', 'r') as f:
    for line in f:
        record = json.loads(line)
        name = record['metadata']['name']
        character_data = record['ai_output']['base_character']
        print(f"{name}: {character_data[:100]}...")
```

### Building Tools on Top

Since all character data is JSON, you can:

- Import into databases (MongoDB, PostgreSQL with JSON columns)
- Build dashboards to visualize character traits
- Export to D&D Beyond or Roll20
- Create character sheet PDFs from the JSON
- Train ML models on character personalities
- Build a searchable character archive

## Advanced: Custom Template Sections

You can extend the template with custom sections. The parser supports:

### Nested Sections (Multiple Fields)

```
### Combat Profile
**Attack Bonus:** +5
**Armor Class:** 16
**Hit Points:** 45
**Special Abilities:** Multiple attacks, Bonus action
```

Results in:
```json
{
  "Combat Profile": {
    "Attack Bonus": "+5",
    "Armor Class": "16",
    "Hit Points": "45",
    "Special Abilities": "Multiple attacks, Bonus action"
  }
}
```

### List Items with Colons

```
### Skills
- Acrobatics: +3
- Animal Handling: +2
- Arcana: +4
```

Results in:
```json
{
  "Skills": {
    "Acrobatics": "+3",
    "Animal Handling": "+2",
    "Arcana": "+4"
  }
}
```

## Troubleshooting

### JSON Validation Failed

If Gemini doesn't return valid JSON:
- The system automatically falls back to text mode
- Check logs in `logs/` directory for details
- Ensure template structure is clear and well-organized
- Try simplifying the template

### Missing Fields in Output

If some fields are empty:
- Verify your template has clear markers (`**Field:**` or `- Field:`)
- Check that Gemini has enough context to fill fields
- Ensure field names don't conflict with special characters

### Large JSON Files

If character JSON is very large:
- Consider splitting template into multiple sections
- Reduce template complexity
- Check for duplicate fields

## Tips for Best Results

1. **Clear structure**: Use consistent formatting for sections and fields
2. **Meaningful names**: Use descriptive field names that guide Gemini
3. **Templates as hints**: Add `[descriptive hint]` to show expected format
4. **Consistent placeholders**: Use `{{PLACEHOLDER_NAME}}` for user inputs
5. **Test parsing**: First run without `--json_output` to see text output

## Environment Variables for JSON

Add to your `.env` file:

```
# Output location for individual character JSON files
CHARACTERS_JSON_DIR=characters

# This controls where Gemini sends data for JSON output
# When --json_output flag is used, Gemini receives schema from parsed template
```

## Future Enhancements

Possible additions to template parsing:

- [ ] Array fields (lists of items)
- [ ] Conditional fields (only if D&D enabled)
- [ ] Default values in schema
- [ ] Validation schemas
- [ ] Export templates to OpenAPI spec
