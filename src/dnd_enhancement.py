"""D&D 5e 2024 specific character generation and enhancements."""

import logging
from typing import Optional, List, Dict, TYPE_CHECKING

from src.gemini_client import generate_from_prompt

if TYPE_CHECKING:
    from src.gemini_client import GeminiClient

logger = logging.getLogger('character_creation')


class DNDEnhancer:
    """D&D 5e 2024 character enhancement system.
    
    Manages D&D mechanics, character enhancements, and lore integration
    for character profiles using Gemini AI generation.
    """

    # D&D 5e 2024 Subclasses by Class
    SUBCLASSES: Dict[str, List[str]] = {
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
            'Brute', 'Cavalier', 'Samurai', 'Arcane Archer', 'Rune Knight',
            'Echo Knight'
        ],
        'Monk': [
            'Way of the Open Hand', 'Way of Shadow', 'Way of the Long Death',
            'Way of the Four Elements', 'Way of the Kensei', 'Way of Mercy',
            'Way of Tranquility', 'Way of the Ascendant Dragon',
            'Way of Twilight'
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
            'Mastermind', 'Swashbuckler', 'Scout', 'Phantom', 'Soulknife',
            'Aberrant Mind'
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
            'Illusion', 'Necromancy', 'Transmutation', 'War Magic',
            'Chronurgy Magic'
        ],
        'Artificer': [
            'Alchemist', 'Armorer', 'Artillerist', 'Battle Smith',
            'Infusion Master'
        ],
        'Blood Hunter': [
            'Order of the Lycan', 'Order of the Profane Soul', 'Order of the Mutant',
            'Order of the Ghostslayer', 'Order of the Ritual'
        ]
    }

    # Valid D&D 5e 2024 species
    SPECIES: List[str] = [
        'Human', 'Elf', 'Dwarf', 'Halfling', 'Dragonborn',
        'Gnome', 'Half-Elf', 'Half-Orc', 'Tiefling', 'Orc',
        'Goblin', 'Kenku', 'Tabaxi', 'Aasimar', 'Genasi',
        'Firbolg', 'Kobold', 'Lizardfolk', 'Triton', 'Bugbear',
        'Bearfolk', 'Centaur', 'Changeling', 'Goliath', 'Hobgoblin',
        'Loxodon', 'Minotaur', 'Satyr', 'Vedalken', 'Warforged'
    ]

    # Valid D&D 5e 2024 classes
    CLASSES: List[str] = [
        'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter',
        'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer',
        'Warlock', 'Wizard', 'Artificer', 'Blood Hunter'
    ]

    def __init__(
        self,
        project: str,
        location: str,
        model_name: str,
        gemini_client: Optional['GeminiClient'] = None
    ) -> None:
        """Initialize the D&D enhancer.
        
        Args:
            project: GCP project ID
            location: GCP region
            model_name: Gemini model name (e.g., 'gemini-2.5-flash')
            gemini_client: Optional GeminiClient instance for text generation.
                          If not provided, will create internal calls.
        """
        self.project: str = project
        self.location: str = location
        self.model_name: str = model_name
        self.gemini_client: Optional['GeminiClient'] = gemini_client
        logger.debug(
            f"DNDEnhancer initialized with model: {model_name} "
            f"(project: {project}, location: {location})"
        )

    def is_valid_species(self, species: str) -> bool:
        """Check if a species is valid in D&D 5e 2024.
        
        Args:
            species: Species name to validate
            
        Returns:
            True if species is valid, False otherwise
        """
        is_valid = species in self.SPECIES
        if not is_valid:
            logger.warning(f"Invalid D&D species: {species}")
        return is_valid

    def is_valid_class(self, character_class: str) -> bool:
        """Check if a class is valid in D&D 5e 2024.
        
        Args:
            character_class: Class name to validate
            
        Returns:
            True if class is valid, False otherwise
        """
        is_valid = character_class in self.CLASSES
        if not is_valid:
            logger.warning(f"Invalid D&D class: {character_class}")
        return is_valid

    def is_valid_subclass(
        self, character_class: str,
        subclass: str
    ) -> bool:
        """Check if a subclass is valid for a given class.
        
        Args:
            character_class: Parent class name
            subclass: Subclass name to validate
            
        Returns:
            True if subclass is valid for class, False otherwise
        """
        if not self.is_valid_class(character_class):
            return False

        if character_class not in self.SUBCLASSES:
            logger.warning(
                f"Class '{character_class}' has no subclass list defined"
            )
            return False

        is_valid = subclass in self.SUBCLASSES[character_class]
        if not is_valid:
            logger.warning(
                f"Invalid D&D subclass '{subclass}' for class '{character_class}'"
            )
        return is_valid

    def get_subclasses_for_class(
        self, character_class: str
    ) -> Optional[List[str]]:
        """Get all available subclasses for a given class.
        
        Args:
            character_class: Class name
            
        Returns:
            List of subclasses or None if class not found
        """
        if not self.is_valid_class(character_class):
            return None

        return self.SUBCLASSES.get(character_class)

    def build_enhancement_prompt(
        self,
        base_character: str,
        species: str,
        character_class: str,
        level: int,
        subclass: Optional[str] = None
    ) -> str:
        """Build a prompt for Gemini to enhance a character with D&D 5e 2024.

        Args:
            base_character: The already-generated base character profile
            species: D&D species (e.g., Human, Elf, Dwarf)
            character_class: D&D class (e.g., Fighter, Wizard, Rogue)
            level: Character level (1-20)
            subclass: Optional D&D subclass (e.g., Champion, Berserker)

        Returns:
            Prompt string for Gemini enhancement
        """
        subclass_line = f"- Subclass: {subclass}\n" if subclass else ""

        subclass_requirements = (
            "1. Add 'D&D Profile' section with:\n"
            "   - Class Features (appropriate for level)\n"
            f"   - Subclass Features: Detail specific abilities from the "
            f"{subclass or 'chosen'} subclass\n"
            "   - Species Traits (inherent racial abilities)\n"
            "   - Ability Scores breakdown (STR, DEX, CON, INT, WIS, CHA)\n"
            "   - Hit Points (with CON modifier calculation)\n"
            "   - Skills & Proficiencies (tied to class and subclass)\n"
            "   - Equipment (starting or level-appropriate)\n"
            "   - Suggested Background hooks tied to character background\n"
            "2. Include specific subclass mechanics and roleplay implications\n"
            "3. Explain how subclass features enhance the character concept\n"
            "4. Maintain consistency with existing character personality and "
            "background\n"
            "5. Make mechanical choices align with the character concept\n"
            "6. Include roleplay notes for how species/class/subclass traits "
            "manifest in their personality\n"
        ) if subclass else (
            "1. Add 'D&D Profile' section with:\n"
            "   - Class Features (appropriate for level)\n"
            "   - Species Traits (inherent racial abilities)\n"
            "   - Ability Scores breakdown (STR, DEX, CON, INT, WIS, CHA)\n"
            "   - Hit Points (with CON modifier calculation)\n"
            "   - Skills & Proficiencies (tied to class)\n"
            "   - Equipment (starting or level-appropriate)\n"
            "   - Suggested Background hooks tied to character background\n"
            "2. Maintain consistency with existing character personality and "
            "background\n"
            "3. Make mechanical choices align with the character concept\n"
            "4. Include roleplay notes for how species/class traits manifest in "
            "their personality\n"
        )

        prompt = (
            "You are a Dungeons & Dragons 5e 2024 character specialist. "
            "Your task is to enhance an existing character profile with "
            "D&D-specific details.\n\n"
            
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
            "Provide the full enhanced character profile with the new D&D "
            "section integrated naturally. "
            "Output ONLY the complete character profile with D&D enhancements, "
            "nothing else."
        )
        return prompt

    def enhance_character(
        self,
        base_character: str,
        species: str,
        character_class: str,
        level: int,
        subclass: Optional[str] = None
    ) -> str:
        """Generate D&D 5e 2024 enhancements for a character.

        Args:
            base_character: The base character profile to enhance
            species: D&D species
            character_class: D&D class
            level: Character level (1-20)
            subclass: Optional D&D subclass

        Returns:
            Enhanced character profile with D&D mechanics

        Raises:
            ValueError: If species or class is invalid
        """
        if not self.is_valid_species(species):
            raise ValueError(f"Invalid D&D species: {species}")

        if not self.is_valid_class(character_class):
            raise ValueError(f"Invalid D&D class: {character_class}")

        if subclass and not self.is_valid_subclass(character_class, subclass):
            raise ValueError(
                f"Invalid D&D subclass '{subclass}' for class '{character_class}'"
            )

        logger.info(
            f"Generating D&D enhancement for {species} {character_class} "
            f"(Level {level})"
        )
        if subclass:
            logger.debug(f"Subclass: {subclass}")

        prompt = self.build_enhancement_prompt(
            base_character, species, character_class, level, subclass
        )

        logger.debug("Calling Gemini to generate D&D enhancements")
        if self.gemini_client:
            enhanced = self.gemini_client.generate(
                prompt=prompt,
                temperature=0.8,
                max_output_tokens=3500
            )
        else:
            enhanced = generate_from_prompt(
                project=self.project,
                location=self.location,
                model_name=self.model_name,
                prompt=prompt,
                temperature=0.8,
                max_output_tokens=3500
            )

        logger.info(f"D&D enhancement completed ({len(enhanced)} characters)")
        return enhanced


# Backward compatibility: Keep module-level functions and constants
DND_SUBCLASSES = DNDEnhancer.SUBCLASSES
DND_SPECIES = DNDEnhancer.SPECIES
DND_CLASSES = DNDEnhancer.CLASSES


def build_dnd_enhancement_prompt(
    base_character: str,
    species: str,
    character_class: str,
    level: int,
    subclass: Optional[str] = None,
    project: Optional[str] = None,
    location: Optional[str] = None,
    model_name: Optional[str] = None
) -> str:
    """Build a prompt for Gemini to enhance a character with D&D 5e 2024.
    
    Deprecated: Use DNDEnhancer.build_enhancement_prompt() instead.
    
    Args:
        base_character: The base character profile to enhance
        species: D&D species
        character_class: D&D class
        level: Character level
        subclass: Optional D&D subclass
        project: GCP project ID (unused, for backward compatibility)
        location: GCP region (unused, for backward compatibility)
        model_name: Gemini model name (unused, for backward compatibility)
        
    Returns:
        Prompt string for Gemini
    """
    # Create a temporary enhancer just to build the prompt
    enhancer = DNDEnhancer(
        project=project or "temp",
        location=location or "us-central1",
        model_name=model_name or "gemini-2.5-flash"
    )
    return enhancer.build_enhancement_prompt(
        base_character, species, character_class, level, subclass
    )


def generate_dnd_enhancement(
    base_character: str,
    species: str,
    character_class: str,
    level: int,
    project: str,
    location: str,
    model_name: str,
    subclass: Optional[str] = None
) -> str:
    """Generate D&D 5e 2024 enhancements for a character.
    
    Deprecated: Use DNDEnhancer.enhance_character() instead.
    
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
    enhancer = DNDEnhancer(project, location, model_name)
    return enhancer.enhance_character(
        base_character, species, character_class, level, subclass
    )
