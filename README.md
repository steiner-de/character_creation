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
   .\setup_venv.ps1
   ```

   **Windows (Command Prompt):**
   ```cmd
   setup_venv.bat
   ```

   **Linux/macOS:**
   ```bash
   chmod +x setup_venv.sh
   ./setup_venv.sh
   ```

   This will create a `venv/` directory, activate it, and install all dependencies.

4. Copy `.env.example` to `.env` and fill in your values:
   ```bash
   cp .env.example .env
   ```

5. Edit `.env`:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/service_account.json
   GOOGLE_PROJECT=your-gcp-project-id
   GOOGLE_LOCATION=us-central1
   GEMINI_MODEL=text-bison@001
   CHARACTERS_CSV=characters.csv
   ```

## Usage

### Quick Start

**First time setup:**
```powershell
# PowerShell
.\setup_venv.ps1

# OR Command Prompt
setup_venv.bat

# OR Linux/macOS
./setup_venv.sh
```

**Run a character creation:**
```bash
python main.py \
  --name "Astra Moon" \
  --sex female \
  --gender "she/her" \
  --age_range adult \
  --occupation "Starship Pilot" \
  --template_doc_id "YOUR_TEMPLATE_DOC_ID"
```

**Run a character with D&D 5e 2024 enhancements:**
```bash
python main.py \
  --name "Bram Ironforge" \
  --sex male \
  --gender "he/him" \
  --age_range adult \
  --occupation "Warrior" \
  --template_doc_id "YOUR_TEMPLATE_DOC_ID" \
  --species Dwarf \
  --class Fighter \
  --level 5
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

See `DEACTIVATE_VENV.md` for more deactivation options.

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
- `--level`: Character level (1-20)

**Note:** All three D&D parameters (`--species`, `--class`, `--level`) must be provided together to enable D&D enhancements.

### Output

1. **New Google Doc** - Created in your Google Drive with Gemini-generated content
2. **CSV Record** - Appended to `characters.csv` with:
   - Input parameters (name, sex, gender, age_range, occupation)
   - Document URL
   - Creation timestamp

Example CSV output:
```
name,sex,gender,age_range,occupation,species,class,level,doc_url,created_at
Astra Moon,female,she/her,adult,Starship Pilot,,,https://docs.google.com/document/d/ABC123/edit,2025-11-28T12:34:56.789012
Bram Ironforge,male,he/him,adult,Warrior,Dwarf,Fighter,5,https://docs.google.com/document/d/DEF456/edit,2025-11-28T12:35:10.123456
```

## File Structure

```
character_creation/
├── main.py                # Main CLI entry point
├── setup_venv.ps1        # Virtual environment setup (PowerShell)
├── setup_venv.bat        # Virtual environment setup (Command Prompt)
├── setup_venv.sh         # Virtual environment setup (Linux/macOS)
├── DEACTIVATE_VENV.md    # How to deactivate virtual environment
├── src/
│   ├── __init__.py
│   ├── gdocs.py          # Google Docs API helpers
│   ├── gemini_client.py  # Gemini/Vertex AI wrapper
│   ├── csv_tracker.py    # CSV tracking
│   └── dnd_enhancement.py # D&D 5e 2024 specific enhancements
├── venv/                 # Virtual environment (created by setup scripts)
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Environment variables (create from .env.example)
├── .gitignore            # Git ignore rules
├── characters.csv        # Output tracking (created on first run)
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

5. **Check results**:
   - New doc link printed to console
   - `characters.csv` updated with metadata
   - If D&D parameters provided, character sheet includes mechanics and abilities

## Troubleshooting

- **Authentication error**: Ensure `GOOGLE_APPLICATION_CREDENTIALS` points to a valid service account JSON
- **API not enabled**: Check that Drive, Docs, and Vertex AI APIs are enabled in your GCP project
- **Quota exceeded**: Your service account may have hit API rate limits; wait a few minutes before retrying

## License

[Your License Here]" 
