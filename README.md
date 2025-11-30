"# Google Docs & Gemini Character Creator

Complete Python toolkit to programmatically create character documents using:
- **Google Docs** as templates and storage
- **Gemini AI** to fill in character details
- **D&D 5e 2024** support for enhanced gameplay (optional)
- **CSV** for tracking character creation history

## Features

- Load a Google Docs template with placeholders (`{{NAME}}`, `{{SEX}}`, `{{GENDER}}`, `{{AGE_RANGE}}`, `{{OCCUPATION}}`)
- Send the template + character inputs to Gemini AI for creative filling
- Create a new Google Docs file with the filled content
- Upload to your Google Drive
- **[NEW] D&D 5e 2024 Enhancement:** Optionally add D&D mechanics including:
  - Species traits and abilities
  - Class features and proficiencies
  - Ability scores (STR, DEX, CON, INT, WIS, CHA)
  - Hit points calculation
  - Equipment recommendations
  - Skill proficiencies
- Track all creations in a local CSV with metadata and doc links

## Setup

### Prerequisites

1. **Google Cloud Project** with Drive API and Docs API enabled
2. **Service Account** JSON file with Drive/Docs permissions
3. **Vertex AI API** enabled (for Gemini access)

### Installation

1. Clone or download this repository
2. Install Python 3.10+

3. **Create and activate virtual environment:**

   **Windows (PowerShell):**
   ```powershell
   .\scripts\setup_venv.ps1
   ```

   **Windows (Command Prompt):**
   ```cmd
   scripts\setup_venv.bat
   ```

   **Linux/macOS:**
   ```bash
   chmod +x scripts/setup_venv.sh
   ./scripts/setup_venv.sh
   ```

   This will create a `venv/` directory, activate it, and install all dependencies.

4. Copy `.env.example` to `.env` and fill in your values:
   ```bash
   cp .env.example .env
   ```

5. Edit `.env`:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\service_account.json
   GOOGLE_PROJECT=your-gcp-project-id
   GOOGLE_LOCATION=us-central1
   GEMINI_MODEL=gemini-1.5-flash
   CHARACTERS_CSV=characters.csv
   TEMPLATE_DOC_ID=your-google-docs-template-id
   ```

## Usage

### Quick Start

**First time setup:**
```powershell
# PowerShell
.\scripts\setup_venv.ps1

# OR Command Prompt
scripts\setup_venv.bat

# OR Linux/macOS
./scripts/setup_venv.sh
```

**Run a character creation:**
```bash
python main.py \
  --name "Astra Moon" \
  --sex female \
  --gender "she/her" \
  --age_range adult \
  --occupation "Starship Pilot"
```

**Run a character with structured JSON output:**
```bash
python main.py \
  --name "Astra Moon" \
  --sex female \
  --gender "she/her" \
  --age_range adult \
  --occupation "Starship Pilot" \
  --json_output
```
This will parse your template structure and request Gemini to return JSON with each template section as a key.

**Run a character with D&D 5e 2024 enhancements:**
```bash
python main.py \
  --name "Bram Ironforge" \
  --sex male \
  --gender "he/him" \
  --age_range adult \
  --occupation "Warrior" \
  --species Dwarf \
  --class Fighter \
  --level 5
```

**Run a character with D&D 5e 2024 enhancements AND subclass:**
```bash
python main.py \
  --name "Eldra Shadowblade" \
  --sex female \
  --gender "she/her" \
  --age_range adult \
  --occupation "Assassin" \
  --species Half-Elf \
  --class Rogue \
  --subclass "Arcane Trickster" \
  --level 7
```

**Deactivate virtual environment when done:**
```powershell
# PowerShell
.\venv\Scripts\Deactivate.ps1

# OR Command Prompt
venv\Scripts\deactivate.bat

# OR Linux/macOS
deactivate
```

### Arguments

- `--name`: Character name (required)
- `--sex`: `male` or `female` (required)
- `--gender`: `he/him`, `she/her`, or `they/them` (required)
- `--age_range`: `child`, `teen`, `adult`, `middle-age`, or `elderly` (required)
- `--occupation`: Character occupation (required)
- `--template_doc_id`: Google Docs template file ID (required)
- `--new_doc_title`: Optional custom title for created document (default: `Character - {name} - {date}`)

**D&D 5e 2024 Enhancement Arguments (optional):**
- `--species`: D&D species - `Human`, `Elf`, `Dwarf`, `Halfling`, `Dragonborn`, `Gnome`, `Half-Elf`, `Half-Orc`, `Tiefling`, `Orc`, `Goblin`, `Kenku`, `Tabaxi`, `Aasimar`, `Genasi`
- `--class`: D&D class - `Barbarian`, `Bard`, `Cleric`, `Druid`, `Fighter`, `Monk`, `Paladin`, `Ranger`, `Rogue`, `Sorcerer`, `Warlock`, `Wizard`, `Artificer`, `Blood Hunter`
- `--subclass`: D&D subclass (optional, must match the chosen class). Examples:
  - **Fighter subclasses:** Champion, Battle Master, Eldritch Knight, Samurai, Rune Knight, Echo Knight
  - **Rogue subclasses:** Thief, Assassin, Arcane Trickster, Inquisitive, Swashbuckler, Phantom
  - **Wizard subclasses:** Abjuration, Conjuration, Divination, Enchantment, Evocation, Necromancy
  - And many more for each class!
- `--level`: Character level (1-20)

**Note:** All three base D&D parameters (`--species`, `--class`, `--level`) must be provided together to enable D&D enhancements. Subclass is optional but must be valid for the chosen class.

### Output

1. **New Google Doc** - Created in your Google Drive with Gemini-generated content
2. **CSV Record** - Appended to `characters.csv` with:
   - Input parameters (name, sex, gender, age_range, occupation)
   - Document URL
   - Creation timestamp
3. **JSONL Record** - Appended to `characters.jsonl` with:
   - Full metadata (inputs, D&D info, document URL, timestamp)
   - **Full AI output**: base character profile from Gemini
   - **D&D enhancement** (if applicable): Extended character profile with D&D mechanics

Example CSV output:
```
name,sex,gender,age_range,occupation,species,class,subclass,level,doc_url,created_at
Astra Moon,female,she/her,adult,Starship Pilot,,,,,https://docs.google.com/document/d/ABC123/edit,2025-11-29T12:34:56.789012
Bram Ironforge,male,he/him,adult,Warrior,Dwarf,Fighter,,5,https://docs.google.com/document/d/DEF456/edit,2025-11-29T12:35:10.123456
Eldra Shadowblade,female,she/her,adult,Assassin,Half-Elf,Rogue,Arcane Trickster,7,https://docs.google.com/document/d/GHI789/edit,2025-11-29T12:36:20.456789
```

Example JSONL output (`characters.jsonl`):
```json
{
  "metadata": {
    "created_at": "2025-11-29T12:34:56.789012",
    "name": "Bram Ironforge",
    "inputs": {
      "sex": "male",
      "gender": "he/him",
      "age_range": "adult",
      "occupation": "Warrior"
    },
    "dnd": {
      "species": "Dwarf",
      "class": "Fighter",
      "subclass": null,
      "level": 5
    },
    "doc_url": "https://docs.google.com/document/d/DEF456/edit"
  },
  "ai_output": {
    "base_character": "**Name:** Bram Ironforge\n**Species:** Dwarf\n**Age:** Adult...",
    "dnd_enhancement": "**D&D Profile**\n**Hit Points:** 54\n**Ability Scores:**...\n**Skills:** Athletics +4, Perception +2..."
  }
}
```

#### Why JSON/JSONL?

- **Structured data**: Easy to parse, filter, and query in code or tools
- **Full AI output preservation**: All generated content is stored locally, not just metadata
- **Archiving**: Keep a complete history of all character creations with full details
- **Integration**: Import into databases, dashboards, or character sheet builders
- **JSONL format**: One JSON object per line allows efficient streaming and line-by-line processing

### Template Structure & JSON Output

The system automatically parses your Google Docs template to understand its structure and can generate Gemini responses as **structured JSON** with each section as a key.

**How it works:**

1. **Template parsing**: The system reads your template and identifies sections (marked with `###` headings) and fields (marked with `**Field Name:**` patterns)

2. **JSON schema generation**: A JSON structure is automatically created matching your template hierarchy

3. **Gemini instruction**: Gemini is instructed to output JSON matching the exact structure

4. **Structured storage**: Character data is saved both as text (Google Docs) and as individual JSON files (when using `--json_output`)

**Example template structure:**
```
### Basic Info
**Name:** {{NAME}}
**Age:** {{AGE}}

### Abilities
**Strength:** [blank]
**Dexterity:** [blank]
**Constitution:** [blank]
```

**Resulting JSON structure:**
```json
{
  "Basic Info": {
    "Name": "Astra Moon",
    "Age": "Adult"
  },
  "Abilities": {
    "Strength": "15",
    "Dexterity": "17",
    "Constitution": "14"
  }
}
```

Each character's full JSON structure is saved to the `characters/` directory when using `--json_output`.

## File Structure

```
character_creation/
├── main.py                # Main CLI entry point
├── scripts/
│   ├── setup_venv.ps1    # Virtual environment setup (PowerShell)
│   ├── setup_venv.bat    # Virtual environment setup (Command Prompt)
│   ├── setup_venv.sh     # Virtual environment setup (Linux/macOS)
│   ├── setup-linting.ps1 # Linting setup (PowerShell)
│   └── setup-linting.sh  # Linting setup (Linux/macOS)
├── test/
│   ├── test_*.py         # Unit and integration tests
│   ├── example_*.json    # Example character JSON files
│   ├── example_*.csv     # Example character CSV file
│   ├── example_*.jsonl   # Example character JSONL file
│   └── test_*.*          # Test output files
├── src/
│   ├── __init__.py
│   ├── gdocs.py          # Google Docs API helpers
│   ├── gemini_client.py  # Gemini/Vertex AI wrapper
│   ├── csv_tracker.py    # CSV tracking (metadata only)
│   ├── json_tracker.py   # JSONL tracking (full AI output)
│   ├── template_parser.py # Template structure parsing & JSON handling
│   ├── logger.py         # Logging configuration
│   └── dnd_enhancement.py # D&D 5e 2024 specific enhancements
├── venv/                 # Virtual environment (created by setup scripts)
├── logs/                 # Application logs (created on first run)
├── characters/           # Individual character JSON files (created with --json_output)
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Environment variables (create from .env.example)
├── .gitignore            # Git ignore rules
├── characters.csv        # CSV tracking (created on first run)
├── characters.jsonl      # JSONL tracking (created on first run)
└── README.md             # This file
```

## Example Workflow

1. **Prepare a template** in Google Docs with placeholders:
   ```
   CHARACTER PROFILE
   ==================
   Name: {{NAME}}
   Sex: {{SEX}}
   Gender Identity: {{GENDER}}
   Age Range: {{AGE_RANGE}}
   Occupation: {{OCCUPATION}}
   
   Background:
   [Gemini will fill this]
   
   Personality Traits:
   [Gemini will fill this]
   ```

2. **Get the template doc ID** from the URL:
   ```
   https://docs.google.com/document/d/1a2B3c4D5e6F7g8H9i0J/edit
                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                     This is the doc ID
   ```

3. **Run the CLI** for a basic character:
   ```bash
   python main.py --name "Bram" --sex male --gender "he/him" --age_range adult --occupation "Blacksmith" --template_doc_id "1a2B3c4D5e6F7g8H9i0J"
   ```

4. **OR Run with D&D 5e 2024 enhancements** for a full character sheet:
   ```bash
   python main.py --name "Bram" --sex male --gender "he/him" --age_range adult --occupation "Blacksmith" --template_doc_id "1a2B3c4D5e6F7g8H9i0J" --species Dwarf --class Fighter --level 3
   ```

5. **OR Run with D&D 5e 2024 subclass** for enhanced mechanics:
   ```bash
   python main.py --name "Eldra" --sex female --gender "she/her" --age_range adult --occupation "Spy" --template_doc_id "1a2B3c4D5e6F7g8H9i0J" --species Half-Elf --class Rogue --subclass "Arcane Trickster" --level 5
   ```

6. **Check results**:
   - New doc link printed to console
   - `characters.csv` updated with metadata
   - If D&D parameters provided, character sheet includes mechanics and abilities
   - If subclass provided, enhanced with subclass-specific features

## Code Quality & Linting

This project uses comprehensive linting and code formatting tools to maintain high code quality standards.

### Quick Start

```bash
# Setup linting tools (one-time)
# Windows
.\scripts\setup-linting.ps1

# Linux/macOS
./scripts/setup-linting.sh

# Format code before committing
black src/ main.py
isort src/ main.py

# Check code quality
ruff check src/ main.py
flake8 src/ main.py
mypy src/ main.py
bandit -r src/
```

### Tools Configured

| Tool | Purpose |
|------|---------|
| **Black** | Code formatting (100 char lines) |
| **isort** | Import organization |
| **Ruff** | Fast linting |
| **Flake8** | PEP 8 compliance |
| **Pylint** | Code analysis |
| **mypy** | Type checking |
| **Bandit** | Security scanning |
| **pre-commit** | Git automation (runs on commit) |

### Standards

- **Line Length**: 100 characters maximum
- **Python Version**: 3.10 or higher
- **Type Hints**: Required for all functions
- **Docstrings**: Required for public APIs
- **Style**: PEP 8 (Black formatting)

### Documentation

For complete linting documentation and setup, see:
- **[LINTING.md](LINTING.md)** - Comprehensive linting guide and tool reference
- **[CODE_QUALITY.md](CODE_QUALITY.md)** - Code standards and best practices

### Pre-commit Hooks

Hooks automatically run on every `git commit`:
1. Trailing whitespace
2. File ending validation
3. YAML/JSON syntax
4. Code formatting (Black)
5. Import organization (isort)
6. Linting (Flake8)
7. Fast linting (Ruff)
8. Type checking (mypy)
9. Security scanning (Bandit)

If a hook fails, fix the issues and commit again:
```bash
black src/ main.py
isort src/ main.py
ruff check --fix src/ main.py
git add .
git commit -m "Your message"
```

## Troubleshooting

- **Authentication error**: Ensure `GOOGLE_APPLICATION_CREDENTIALS` points to a valid service account JSON
- **API not enabled**: Check that Drive, Docs, and Vertex AI APIs are enabled in your GCP project
- **Quota exceeded**: Your service account may have hit API rate limits; wait a few minutes before retrying
- **Linting setup issues**: See [LINTING.md](LINTING.md) for troubleshooting

## License

[Your License Here]" 
