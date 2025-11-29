"""D&D 5e 2024 specific character generation and enhancements."""

import logging
from src.gemini_client import generate_from_prompt

logger = logging.getLogger('character_creation')

# D&D 5e 2024 Subclasses by Class
DND_SUBCLASSES = {
    'Barbarian': [
        'Berserker', 'Totem Warrior', 'Ancestral Guardian', 'Storm Herald',
        'Zealot', 'Werewolf', 'Wild Magic', 'Beast Master', 'Rune Knight'
    ],
    'Bard': [
        'Lore', 'Glamour', 'Whispers', 'Swords', 'Whispers', 'Creation',
        'Eloquence', 'Spirits', 'Aberrant Mind', 'College of Spirits'
    ],
    'Cleric': [
        'Life', 'Light', 'Tempest', 'Trickery', 'War', 'Knowledge', 'Nature',
        'Forge', 'Grave', 'Order', 'Peace', 'Twilight', 'Ambition', 'Death'
    ],
    'Druid': [
        'Land', 'Moon', 'Shepherd', 'Dreams', 'Wildfire', 'Spores',
        'Stars', 'Seas', 'Underdark', 'Mountain', 'Grassland', 'Forest'
    ],
    'Fighter': [
        'Champion', 'Battle Master', 'Eldritch Knight', 'Four Elements',
        'Brute', 'Cavalier', 'Samurai', 'Arcane Archer', 'Rune Knight', 'Echo Knight'
    ],
    'Monk': [
        'Way of the Open Hand', 'Way of Shadow', 'Way of the Long Death',
        'Way of the Four Elements', 'Way of the Kensei', 'Way of Mercy',
        'Way of Tranquility', 'Way of the Ascendant Dragon', 'Way of Twilight'
    ],
    'Paladin': [
        'Devotion', 'Ancients', 'Vengeance', 'Conquest', 'Redemption',
        'Watchers', 'Oath of the Watchers', 'Oath of Heroism', 'Oath of Glory'
    ],
    'Ranger': [
        'Hunter', 'Beast Master', 'Gloom Stalker', 'Monk', 'Rune Knight',
        'Swarmkeeper', 'Fey Wanderer', 'Twilight Cleric', 'Monster Slayer'
    ],
    'Rogue': [
        'Thief', 'Assassin', 'Arcane Trickster', 'Inquisitive',
        'Mastermind', 'Swashbuckler', 'Scout', 'Phantom', 'Soulknife', 'Aberrant Mind'
    ],
    'Sorcerer': [
        'Draconic Bloodline', 'Wild Magic', 'Divine Soul', 'Shadow Magic',
        'Storm Sorcery', 'Aberrant Mind', 'Clockwork Soul', 'Lunar Sorcery'
    ],
    'Warlock': [
        'The Fiend', 'The Great Old One', 'The Archfey', 'The Celestial',
        'The Hexblade', 'The Undead', 'The Raven Queen', 'The Genie'
    ],
    'Wizard': [
        'Abjuration', 'Conjuration', 'Divination', 'Enchantment', 'Evocation',
        'Illusion', 'Necromancy', 'Transmutation', 'War Magic', 'Chronurgy Magic'
    ],
    'Artificer': [
        'Alchemist', 'Armorer', 'Artillerist', 'Battle Smith', 'Infusion Master'
    ],
    'Blood Hunter': [
        'Order of the Lycan', 'Order of the Profane Soul', 'Order of the Mutant',
        'Order of the Ghostslayer', 'Order of the Ritual'
    ]
}


def build_dnd_enhancement_prompt(
    base_character: str,
    species: str,
    character_class: str,
    level: int,
    subclass: str|None = None,
    project: str|None = None,
    location: str|None = None,
    model_name: str|None = None
) -> str:
    """Build a prompt for Gemini to enhance a character with D&D 5e 2024 specifics.
    
    Args:
        base_character: The already-generated base character profile
        species: D&D species (e.g., Human, Elf, Dwarf, Halfling, etc.)
        character_class: D&D class (e.g., Fighter, Wizard, Rogue, etc.)
        level: Character level (1-20)
        subclass: Optional D&D subclass (e.g., Champion, Berserker, etc.)
        project: GCP project ID
        location: GCP region
        model_name: Gemini model name
        
    Returns:
        Enhanced character profile with D&D mechanics and lore
    """
    subclass_line = f"- Subclass: {subclass}\n" if subclass else ""
    
    subclass_requirements = (
        "1. Add 'D&D Profile' section with:\n"
        "   - Class Features (appropriate for level)\n"
        f"   - Subclass Features: Detail specific abilities from the {subclass or 'chosen'} subclass\n"
        "   - Species Traits (inherent racial abilities)\n"
        "   - Ability Scores breakdown (STR, DEX, CON, INT, WIS, CHA)\n"
        "   - Hit Points (with CON modifier calculation)\n"
        "   - Skills & Proficiencies (tied to class and subclass)\n"
        "   - Equipment (starting or level-appropriate)\n"
        "   - Suggested Background hooks tied to character background\n"
        "2. Include specific subclass mechanics and roleplay implications\n"
        "3. Explain how subclass features enhance the character concept\n"
        "4. Maintain consistency with the existing character personality and background\n"
        "5. Make mechanical choices align with the character concept\n"
        "6. Include roleplay notes for how species/class/subclass traits manifest in their personality\n"
    ) if subclass else (
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
        "4. Include roleplay notes for how species/class traits manifest in their personality\n"
    )
    
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
        f"- Level: {level}\n"
        f"{subclass_line}\n"
        
        "ENHANCEMENT REQUIREMENTS:\n"
        f"{subclass_requirements}\n"
        
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
    model_name: str,
    subclass: str|None = None
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
        subclass: Optional D&D subclass
        
    Returns:
        Enhanced character profile with D&D mechanics
    """
    logger.info(f"Generating D&D enhancement for {species} {character_class} (Level {level})")
    if subclass:
        logger.debug(f"Subclass: {subclass}")
    
    prompt = build_dnd_enhancement_prompt(
        base_character, species, character_class, level, subclass, project, location, model_name
    )
    
    logger.debug("Calling Gemini to generate D&D enhancements")
    enhanced = generate_from_prompt(
        project=project,
        location=location,
        model_name=model_name,
        prompt=prompt,
        temperature=0.8,
        max_output_tokens=3500
    )
    
    logger.info(f"D&D enhancement completed ({len(enhanced)} characters)")
    return enhanced


# Valid D&D 5e 2024 options
DND_SPECIES = [
    'Human', 'Elf', 'Dwarf', 'Halfling', 'Dragonborn',
    'Gnome', 'Half-Elf', 'Half-Orc', 'Tiefling', 'Orc',
    'Goblin', 'Kenku', 'Tabaxi', 'Aasimar', 'Genasi', 
    'Firbolg', 'Kobold', 'Lizardfolk', 'Triton', 'Bugbear',
    'Bearfolk', 'Centaur', 'Changeling', 'Goliath', 'Hobgoblin',
    'Loxodon', 'Minotaur', 'Satyr', 'Vedalken', 'Warforged'
]

DND_CLASSES = [
    'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter',
    'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer',
    'Warlock', 'Wizard', 'Artificer', 'Blood Hunter'
]
