# Character Data & Input Format

## Schema Overview

```typescript
interface Character {
  metadata?: { new_doc_title?: string; json_output?: boolean };
  Demographics?: { [key: string]: any };
  "Physical Appearance"?: { [key: string]: any };
  History?: { [key: string]: any };
  "Psychological Traits"?: { [key: string]: any };
  Communication?: { [key: string]: any };
  "Strengths, Weaknesses, and Abilities"?: { [key: string]: any };
  Relationships?: { [key: string]: any };
  "Character Growth"?: { [key: string]: any };
}
```

## Mandatory Fields (5 Required)

| Field | Type | Examples |
|-------|------|----------|
| **name** | string | "Elara Moonwhisper", "Kael Shadowstep" |
| **ethnicity** | string | "Human", "Half-Elf", "Dwarf", "Half-Orc" |
| **sex/gender** | string | "female\|she/her", "male\|he/him" |
| **age** | string/number | "26", "young adult", "middle-aged" |
| **occupation** | string | "Ranger", "Mage", "Warrior", "Bard" |

## Metadata (Optional)

```json
{
  "metadata": {
    "new_doc_title": "Custom Google Doc title",
    "json_output": true
  }
}
```

| Field | Type | Purpose |
|-------|------|---------|
| new_doc_title | string | Custom name for generated Google Doc |
| json_output | boolean | Request structured JSON output (default: false) |

## Available Sections & Fields

### Demographics (10 fields)
name, titles, age, sex/gender, pronouns, ethnicity, occupation, socioeconomic status, education, other notes

### Physical Appearance (19 fields)
eye color, skin color, hair color, height, weight, body type, fitness level, tattoos, scars/birthmarks, distinguishing features, disabilities, fashion style, accessories, cleanliness/grooming, posture/gait, tics, coordination, weaknesses, other notes

### History (11 fields)
birth date, place of birth, family members, family events, personal events, criminal record, affiliations, allies, enemies, skeletons in the closet, other notes

### Psychological Traits (28 fields)
personality type, personality traits, temperament, introvert/extrovert, mannerisms, educational background, intelligence, self-esteem, hobbies, skills/talents, loves, morals/virtues, phobias/fears, angered by, pet peeves, obsessed with, routines, bad habits, desires, flaws, quirks, favorite sayings, disabilities, secrets, regrets, accomplishments, memories, other notes

### Communication (11 fields)
languages known, preferred communication methods, accent, style and pacing of speech, pitch, laughter, smile, use of gestures, facial expressions, verbal expressions, other notes

### Strengths, Weaknesses, and Abilities (11 fields)
physical strengths, physical weaknesses, intellectual strengths, intellectual weaknesses, interpersonal strengths, interpersonal weaknesses, physical abilities, magical abilities, physical illnesses/conditions, mental illnesses/conditions, other notes

### Relationships (21 fields)
partner(s), lover(s), parents/guardians, children, grandparents, grandchildren, family, pets, best friends, friends, rivals, enemies, colleagues, mentors/teachers, idols/role models, followers, strangers, non-living things, clubs/memberships, social media presence, public perception

### Character Growth (10 fields)
character archetype, character arc, core values, internal conflicts, external conflicts, goals, motivations, epiphanies, significant events/plot points, other notes

**Total: 121 fields across 8 sections**

## Input Formats

### JSON File (Single Character)
```bash
python main.py --json character.json
```

```json
{
  "metadata": { "new_doc_title": "My Character" },
  "Demographics": {
    "name": "Elara Moonwhisper",
    "age": "26",
    "sex/gender": "female|she/her",
    "ethnicity": "Half-Elf",
    "occupation": "Ranger"
  },
  "Physical Appearance": {
    "eye_color": "Emerald green",
    "hair_color": "Silver-blonde"
  }
}
```

### JSON Array (Multiple Characters)
```bash
python main.py --json characters.json
```

```json
[
  { "Demographics": { "name": "Elara", ... } },
  { "Demographics": { "name": "Kael", ... } }
]
```

### JSONL (Multiple Characters - One Per Line)
```bash
python main.py --jsonl characters.jsonl
```

```
{"Demographics": {"name": "Elara", ...}}
{"Demographics": {"name": "Kael", ...}}
{"Demographics": {"name": "Lyra", ...}}
```

### CSV Format (Use with CSV Converter)
```bash
python convert_csv.py characters.csv --json output.json
python main.py --json output.json
```

```csv
name,age,sex/gender,ethnicity,occupation,eye_color,hair_color
Elara,26,female|she/her,Half-Elf,Ranger,Emerald green,Silver-blonde
```

### CLI Arguments (Traditional)
```bash
python main.py --name "Elara" --age 26 --sex female --gender she/her \
  --ethnicity Half-Elf --occupation Ranger
```

## Field Name Normalization

All field names automatically normalized:
- **Case-insensitive:** `name` = `Name` = `NAME`
- **Space/underscore:** `eye color` = `eye_color`
- **Special chars:** `sex/gender` = `sex_gender`

## Complete Example

```json
{
  "metadata": {
    "new_doc_title": "Elara Moonwhisper - Complete Profile",
    "json_output": true
  },
  "Demographics": {
    "name": "Elara Moonwhisper",
    "titles": "Ranger of the Northern Woods",
    "age": "26",
    "sex/gender": "female|she/her",
    "ethnicity": "Half-Elf",
    "occupation": "Ranger",
    "education": "Self-taught by forest druids"
  },
  "Physical Appearance": {
    "eye_color": "Emerald green",
    "hair_color": "Silver-blonde",
    "height": "5'8\"",
    "body_type": "Athletic and lean",
    "tattoos": "Runes along left arm"
  },
  "Psychological Traits": {
    "personality_traits": "Reserved, observant, compassionate",
    "hobbies": "Tracking, carving, meditation",
    "skills_talents": "Archery, herbalism, animal communication",
    "loves": "Nature, solitude, helping the vulnerable"
  },
  "Relationships": {
    "best_friends": "Theron the Blacksmith",
    "mentors_teachers": "Sage of the Old Forest"
  },
  "Character Growth": {
    "character_archetype": "The Ranger",
    "goals": "Protect the forest from destruction"
  }
}
```

## Validation Rules

✅ **Mandatory fields** must be present (5 required)
✅ **Optional fields** - any from 121 available
✅ **Field names** auto-normalized
✅ **Values** - any string, number, or boolean
✅ **Metadata** - optional (defaults to null/false)
✅ **Sections** - can be nested or top-level

## Output Per Character

1. **Google Doc** - Full formatted profile
2. **CSV record** - Reference in characters.csv
3. **JSONL record** - AI output in characters.jsonl
4. **JSON file** - If json_output=true

## With D&D Enhancement

```bash
python main.py --json character.json \
  --species Elf --class Ranger --level 5 --subclass "Monster Slayer"
```

CLI D&D parameters override JSON values.

## Tips

- Provide only fields you need; others auto-filled by Gemini
- Use `json_output: true` for structured output
- Combine JSON input with CLI parameters for hybrid usage
- Any field from the 121 available can be used
- Gemini maintains consistency across all fields
