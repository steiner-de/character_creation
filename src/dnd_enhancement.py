"""D&D 5e 2024 specific character generation and enhancements."""

from src.gemini_client import generate_from_prompt


def build_dnd_enhancement_prompt(
    base_character: str,
    species: str,
    character_class: str,
    level: int,
    project: str,
    location: str,
    model_name: str
) -> str:
    """Build a prompt for Gemini to enhance a character with D&D 5e 2024 specifics.
    
    Args:
        base_character: The already-generated base character profile
        species: D&D species (e.g., Human, Elf, Dwarf, Halfling, etc.)
        character_class: D&D class (e.g., Fighter, Wizard, Rogue, etc.)
        level: Character level (1-20)
        project: GCP project ID
        location: GCP region
        model_name: Gemini model name
        
    Returns:
        Enhanced character profile with D&D mechanics and lore
    """
    prompt = (
        "You are a Dungeons & Dragons 5e 2024 character specialist. "
        "Your task is to enhance an existing character profile with D&D-specific details.\n\n"
        
        "EXISTING CHARACTER PROFILE:\n"
        "---\n"
        f"{base_character}\n"
        "---\n\n"
        
        f"D&D 5e 2024 DETAILS:\n"
        f"- Species: {species}\n"
        f"- Class: {character_class}\n"
        f"- Level: {level}\n\n"
        
        "ENHANCEMENT REQUIREMENTS:\n"
        "1. Add 'D&D Profile' section with:\n"
        "   - Class Features (appropriate for level)\n"
        "   - Species Traits (inherent racial abilities)\n"
        "   - Ability Scores breakdown (STR, DEX, CON, INT, WIS, CHA)\n"
        "   - Hit Points (with CON modifier calculation)\n"
        "   - Skills & Proficiencies (tied to class)\n"
        "   - Equipment (starting or level-appropriate)\n"
        "   - Suggested Background hooks tied to character background\n"
        "2. Maintain consistency with the existing character personality and background\n"
        "3. Make mechanical choices align with the character concept\n"
        "4. Include roleplay notes for how species/class traits manifest in their personality\n\n"
        
        "OUTPUT:\n"
        "Provide the full enhanced character profile with the new D&D section integrated naturally. "
        "Output ONLY the complete character profile with D&D enhancements, nothing else."
    )
    return prompt


def generate_dnd_enhancement(
    base_character: str,
    species: str,
    character_class: str,
    level: int,
    project: str,
    location: str,
    model_name: str
) -> str:
    """Generate D&D 5e 2024 enhancements for a character.
    
    Args:
        base_character: The base character profile to enhance
        species: D&D species
        character_class: D&D class
        level: Character level
        project: GCP project ID
        location: GCP region
        model_name: Gemini model name
        
    Returns:
        Enhanced character profile with D&D mechanics
    """
    prompt = build_dnd_enhancement_prompt(
        base_character, species, character_class, level, project, location, model_name
    )
    
    enhanced = generate_from_prompt(
        project=project,
        location=location,
        model_name=model_name,
        prompt=prompt,
        temperature=0.8,
        max_output_tokens=3000
    )
    
    return enhanced


# Valid D&D 5e 2024 options
DND_SPECIES = [
    'Human', 'Elf', 'Dwarf', 'Halfling', 'Dragonborn',
    'Gnome', 'Half-Elf', 'Half-Orc', 'Tiefling', 'Orc',
    'Goblin', 'Kenku', 'Tabaxi', 'Aasimar', 'Genasi'
]

DND_CLASSES = [
    'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter',
    'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer',
    'Warlock', 'Wizard', 'Artificer', 'Blood Hunter'
]
