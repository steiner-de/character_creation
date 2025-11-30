# Quick Start: JSON-Structured Character Generation

## What's New

Your character creation system now supports **automatic template parsing** and **structured JSON output**. Each section and field in your Google Docs template is automatically converted to a JSON structure.

## Quick Examples

### Generate with JSON output
```bash
python main.py \
  --name "Astra Moon" \
  --sex female \
  --gender "she/her" \
  --age_range adult \
  --occupation "Starship Pilot" \
  --json_output
```

### With D&D enhancements AND JSON
```bash
python main.py \
  --name "Bram Ironforge" \
  --sex male \
  --gender "he/him" \
  --age_range adult \
  --occupation "Warrior" \
  --species Dwarf \
  --class Fighter \
  --level 5 \
  --json_output
```

## What Gets Created

When you use `--json_output`:

1. **Google Doc** - Traditional formatted document for viewing/sharing
2. **characters.csv** - Quick lookup spreadsheet with metadata
3. **characters.jsonl** - Full archive of all characters (one per line)
4. **characters/{name}_{timestamp}.json** - Individual structured JSON file

## Output Example

**Your template:**
```
### Basic Info
**Name:** {{NAME}}
**Sex:** {{SEX}}

### Abilities
**Strength:** [blank]
**Intelligence:** [blank]
```

**Generated JSON:**
```json
{
  "Basic Info": {
    "Name": "Astra Moon",
    "Sex": "female"
  },
  "Abilities": {
    "Strength": "14",
    "Intelligence": "16"
  }
}
```

## Template Format

Use these markdown-style patterns in your Google Doc template:

```
### Section Name        <- Creates top-level key
**Field Name:** {{PLACEHOLDER}}  <- Creates nested key
- Bullet Field: value   <- Also works
```

## Key Features

✅ **Automatic parsing** - No configuration needed, reads template structure automatically  
✅ **Validation** - JSON validated before storage, falls back to text if needed  
✅ **Dual format** - Get both text (Google Docs) and JSON (programmatic)  
✅ **Archival** - Full AI responses stored locally in JSONL  
✅ **Flexible** - Works with any template structure you have  

## Advanced Usage

### Access character JSON programmatically
```python
import json

# Read the individual JSON file
with open('characters/astra_moon_20251129_123456.json', 'r') as f:
    character = json.load(f)

# Access nested data
strength = character['Abilities']['Strength']
name = character['Basic Info']['Name']
```

### Query JSONL records
```python
# Read all characters from JSONL archive
with open('characters.jsonl', 'r') as f:
    for line in f:
        record = json.loads(line)
        print(record['metadata']['name'])
```

## Files to Know

| File | Purpose |
|------|---------|
| `src/template_parser.py` | Parses templates & handles JSON |
| `main.py` | CLI entry point with `--json_output` flag |
| `characters/` | Directory for individual character JSON files |
| `characters.jsonl` | All characters archived in JSON Lines format |
| `JSON_TEMPLATES.md` | Detailed template documentation |
| `ARCHITECTURE.md` | Technical system overview |

## Troubleshooting

**JSON validation failed** → Template structure unclear, check Google Doc format  
**Empty sections** → Verify template uses `###` for sections and `**Field:**` for fields  
**Character JSON not saved** → Ensure `characters/` directory exists (auto-created on first run)  

## Next Steps

1. Check your template structure in Google Docs
2. Run a test with `--json_output` flag
3. Look in `characters/` for the generated JSON file
4. Use the JSON for integrations with other tools

For full documentation, see `JSON_TEMPLATES.md` and `ARCHITECTURE.md`
