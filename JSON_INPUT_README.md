# JSON/JSONL Input Support - Complete Implementation

## 🎯 What's New

The character creation system now supports **JSON and JSONL file inputs** for batch character generation, while maintaining full backward compatibility with existing CLI arguments.

**In one command:**
- ✅ Create 1 character from JSON
- ✅ Create 100+ characters from JSONL
- ✅ Use template fields to guide character generation
- ✅ Set custom Google Doc titles and output formats
- ✅ Leverage all 121 character template fields

---

## 📁 Files Created

### Core Implementation

| File | Purpose | Lines |
|------|---------|-------|
| `src/character_input.py` | Input validation & parsing module | 422 |
| Updated `main.py` | JSON/JSONL support in CLI | +80 |
| `character_template_structure.json` | Updated with metadata | +4 |

### Documentation

| File | Purpose | Lines |
|------|---------|-------|
| `USAGE_GUIDE.md` | Quick start & practical examples | 350+ |
| `CHARACTER_INPUT_FORMAT.md` | Complete field reference | 250+ |
| `CHARACTER_DATA_MODEL.md` | TypeScript-like schema | 400+ |
| `UPDATE_SUMMARY.md` | Implementation details | 200+ |

### Examples & Tests

| File | Purpose |
|------|---------|
| `example_character.json` | Single detailed character |
| `example_characters.jsonl` | Three character batch |
| `test_character_input.py` | Validation test script |

---

## ⚡ Quick Start

### 1. Create One Character from JSON

```bash
python main.py --json example_character.json
```

**`example_character.json`:**
```json
{
  "metadata": {
    "new_doc_title": "Elara - The Ranger",
    "json_output": true
  },
  "Demographics": {
    "name": "Elara Moonwhisper",
    "age": "26",
    "sex/gender": "female|she/her",
    "ethnicity": "Half-Elf",
    "occupation": "Ranger"
  }
}
```

### 2. Create Multiple Characters from JSONL

```bash
python main.py --jsonl example_characters.jsonl
```

### 3. Use Traditional CLI (Still Works!)

```bash
python main.py --name "Elara" --sex female --gender she/her \
  --age_range "young adult" --ethnicity "Half-Elf" --occupation "Ranger"
```

### 4. Combine JSON + D&D Enhancement

```bash
python main.py --json example_character.json \
  --species Elf --class Ranger --level 5 --subclass "Gloom Stalker"
```

---

## 📋 Mandatory Fields

Every character **must** have these 5 fields:

1. **`name`** - Character's name
2. **`ethnicity`** - Character's ethnicity
3. **`sex/gender`** - Character's sex/gender identity
4. **`age`** - Character's age or age range
5. **`occupation`** - Character's occupation

---

## 🎨 Optional Fields (120+)

Provide any fields from the template to guide Gemini:

**8 Sections:**
- Demographics (9 additional fields)
- Physical Appearance (19 fields)
- History (11 fields)
- Psychological Traits (28 fields)
- Communication (11 fields)
- Strengths/Weaknesses (11 fields)
- Relationships (21 fields)
- Character Growth (10 fields)

**See `CHARACTER_INPUT_FORMAT.md` for all 121 fields with examples.**

---

## 🔧 Metadata Options

Control character output with metadata:

```json
{
  "metadata": {
    "new_doc_title": "Custom Google Doc Title",
    "json_output": true
  }
}
```

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `new_doc_title` | string | null | Custom Google Doc name |
| `json_output` | boolean | false | Request structured JSON |

---

## 📊 Input Format Examples

### Single Character (JSON)

```json
{
  "metadata": {"json_output": true},
  "Demographics": {
    "name": "Kael Shadowstep",
    "age": "38",
    "sex/gender": "male|he/him",
    "ethnicity": "Human",
    "occupation": "Mage"
  },
  "Psychological Traits": {
    "personality traits": "Mysterious, ambitious"
  }
}
```

### Multiple Characters (JSONL)

```
{"Demographics": {"name": "Kael", "age": "38", "sex/gender": "male|he/him", "ethnicity": "Human", "occupation": "Mage"}}
{"Demographics": {"name": "Lyra", "age": "24", "sex/gender": "female|she/her", "ethnicity": "Half-Orc", "occupation": "Bard"}}
{"Demographics": {"name": "Thora", "age": "45", "sex/gender": "female|she/her", "ethnicity": "Dwarf", "occupation": "Warrior"}}
```

### Multiple Characters (JSON Array)

```json
[
  {"Demographics": {"name": "Kael", ...}},
  {"Demographics": {"name": "Lyra", ...}},
  {"Demographics": {"name": "Thora", ...}}
]
```

---

## ✨ Key Features

✅ **Batch Processing** - Create 1-100+ characters in sequence
✅ **Flexible Input** - Minimal (5 fields) to complete (121+ fields)
✅ **Template-Based** - All character template fields available
✅ **Case Insensitive** - Field names normalized automatically
✅ **Metadata Control** - Custom doc titles and output formats
✅ **D&D Integration** - CLI D&D params override/supplement JSON
✅ **Full Validation** - Clear errors for invalid input
✅ **Backward Compatible** - Original CLI mode unchanged

---

## 🔍 Validation

**Automatic checks:**
- ✅ File exists and is readable
- ✅ Valid JSON/JSONL syntax
- ✅ All 5 mandatory fields present
- ✅ Field names match template
- ✅ Metadata fields valid

**Error example:**
```
❌ Error: Record 1 validation failed: Missing mandatory field: Character name
```

---

## 📝 Field Name Flexibility

These are all equivalent:

```
name = Name = NAME
age_range = age = Age_Range = AGE RANGE
sex_gender = sex/gender = Sex/Gender
Physical_Appearance = physical appearance = PHYSICAL APPEARANCE
```

---

## 🚀 Workflow

```
Input (JSON/JSONL/CLI)
         ↓
    Parse & Load
         ↓
  Validate Input
         ↓
   Extract Args
         ↓
For Each Character:
  - Build Prompt (with template fields)
  - Call Gemini API
  - Create Google Doc
  - Save CSV Record
  - Save JSONL Record
  - (Optionally) Save JSON
         ↓
Display Summary
```

---

## 📚 Documentation Map

| Document | Purpose | Best For |
|----------|---------|----------|
| **USAGE_GUIDE.md** | Quick start & examples | Getting started |
| **CHARACTER_INPUT_FORMAT.md** | Complete field reference | Field reference |
| **CHARACTER_DATA_MODEL.md** | TypeScript schema | Developers |
| **UPDATE_SUMMARY.md** | Implementation details | Understanding changes |
| **test_character_input.py** | Validation tests | Verification |

---

## 🧪 Testing

Run the validation test:

```bash
python test_character_input.py
```

**Expected output:**
```
Testing JSON file loading...
✓ JSON file loaded successfully
  Characters loaded: 1
  Name: Elara Moonwhisper
  Ethnicity: Half-Elf
  Metadata: {'new_doc_title': 'Elara - The Forest Ranger', 'json_output': True}

Testing JSONL file loading...
✓ JSONL file loaded successfully
  Characters loaded: 3
  1. Kael Shadowstep
  2. Lyra Songborne
  3. Thora Ironborn

✅ All tests passed!
```

---

## 📦 Output Per Character

For each character created:

1. **Google Doc** - Full profile (viewable/editable online)
2. **CSV record** - Quick tracking (`characters.csv`)
3. **JSONL record** - Full AI output (`characters.jsonl`)
4. **JSON file** - Individual JSON (if `json_output=true`, in `characters/` dir)

---

## 💡 Pro Tips

### Tip 1: Provide Only What Matters
```json
{
  "Demographics": {
    "name": "Simple Name",
    "age": "25",
    "sex/gender": "female|she/her",
    "ethnicity": "Human",
    "occupation": "Warrior"
  }
}
```
Gemini will creatively fill in everything else!

### Tip 2: Guide Generation with Details
```json
{
  "Demographics": {...},
  "Psychological Traits": {
    "personality_traits": "Brooding, mysterious, honor-bound",
    "fears": "Betrayal",
    "loves": "Loyalty"
  }
}
```
Gemini uses provided details for consistency.

### Tip 3: Batch Processing
```bash
python main.py --jsonl thousand_npcs.jsonl
```
One command creates 1000 unique characters!

### Tip 4: CLI + JSON Hybrid
```bash
python main.py --json character.json --species Elf --class Ranger --level 10
```
JSON provides base, CLI adds D&D details.

### Tip 5: Custom Doc Naming
```json
{
  "metadata": {
    "new_doc_title": "Session 12 - The New Tavern NPC"
  },
  "Demographics": {...}
}
```

---

## 🆚 Comparison: Input Methods

| Feature | JSON | JSONL | CLI |
|---------|------|-------|-----|
| Single char | ✅ | ❌ | ✅ |
| Multiple chars | ✅ | ✅ | ❌ |
| Template fields | ✅ | ✅ | ❌ |
| Metadata | ✅ | ✅ | ❌ |
| CLI args | ❌ | ❌ | ✅ |
| Batch mode | ✅ | ✅ | ❌ |
| Backward compat | N/A | N/A | ✅ |

---

## ❓ FAQ

**Q: Can I mix CLI and JSON?**
A: Yes! `python main.py --json char.json --species Elf --level 5` works. CLI D&D params override/supplement JSON.

**Q: What if I only provide mandatory fields?**
A: Gemini creatively fills all optional fields while maintaining consistency.

**Q: Can I create 1000 characters at once?**
A: Yes! JSONL supports as many as you want. Time: ~20-30 seconds per character.

**Q: Are field names case-sensitive?**
A: No! `name`, `Name`, `NAME` all work. Same for `sex_gender`, `sex/gender`, `SEX/GENDER`.

**Q: What happens if validation fails?**
A: Program exits with clear error message. No partial processing.

**Q: Can I use both JSON and JSONL?**
A: Only one at a time. Choose `--json` or `--jsonl`, not both.

**Q: Are the old CLI arguments still supported?**
A: 100% yes! Full backward compatibility maintained.

---

## 🔗 Integration

Works seamlessly with:

✅ Google Docs (automatic doc creation)
✅ Google Drive (document storage)
✅ Gemini API (AI generation)
✅ CSV tracking (quick reference)
✅ JSONL logging (full history)
✅ D&D 5e 2024 (optional enhancement)

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| New module size | 422 lines |
| New documentation | 1000+ lines |
| Template fields available | 121 |
| Mandatory fields | 5 |
| Optional fields | 116 |
| Sections | 8 |
| Files created | 8 |
| Backward compatible | 100% |

---

## 🎓 Learning Path

1. **Start Here** → Read this file
2. **Quick Examples** → `USAGE_GUIDE.md`
3. **Field Reference** → `CHARACTER_INPUT_FORMAT.md`
4. **Technical Details** → `CHARACTER_DATA_MODEL.md`
5. **Try Examples** → Run `test_character_input.py`
6. **Create Your Own** → Edit `example_character.json`

---

## ✅ Validation Checklist

Before running with your JSON:

- [ ] All 5 mandatory fields present (name, ethnicity, sex/gender, age, occupation)
- [ ] Valid JSON syntax (test with online JSON validator)
- [ ] For JSONL: exactly one JSON object per line
- [ ] Metadata fields spelled correctly (new_doc_title, json_output)
- [ ] File path correct and file exists
- [ ] No unescaped quotes or special characters in strings

---

## 🚨 Common Issues

**"Missing mandatory field: Character name"**
→ Ensure `name` field is present in Demographics or top-level

**"Invalid JSON format"**
→ Check JSON syntax (missing braces, commas, quotes)

**"File not found: character.json"**
→ Verify file path and that file exists

**"JSONL validation failed"**
→ Ensure each line in JSONL is a complete JSON object

---

## 📞 Support Resources

- Complete examples: `example_character.json`, `example_characters.jsonl`
- Validation script: `test_character_input.py`
- Field reference: `CHARACTER_INPUT_FORMAT.md`
- Data model: `CHARACTER_DATA_MODEL.md`
- Implementation: `UPDATE_SUMMARY.md`

---

## 🎉 Summary

The character creation system now supports professional-grade batch processing with JSON/JSONL input files. Create 1-100+ unique characters with 5 mandatory fields and 116+ optional template fields for guidance. Full backward compatibility with CLI mode maintained.

**Start creating:**
```bash
python main.py --json example_character.json
```

**Create a batch:**
```bash
python main.py --jsonl example_characters.jsonl
```

**Happy character creation! 🎭**
