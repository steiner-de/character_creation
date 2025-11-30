#!/usr/bin/env python3
"""Main CLI for character creation via Google Docs + Gemini AI."""

import argparse
import os
import json
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from src.logger import setup_logging, get_logger
from src.gdocs import create_services, get_template_text, create_doc, insert_text, get_doc_url
from src.gemini_client import GeminiClient
from src.csv_tracker import CharacterCSVTracker
from src.json_tracker import append_character_json
from src.template_parser import (
    build_json_character_prompt,
    validate_json_output,
    flatten_json_for_text,
    save_character_json
)
from src.dnd_enhancement import (
    DNDEnhancer,
    generate_dnd_enhancement,
    DND_SPECIES,
    DND_CLASSES,
    DND_SUBCLASSES
)
from src.character_input import (
    process_character_file,
    extract_character_args,
)


def main():
    """Main entry point for the character creation CLI."""
    # Initialize logging
    setup_logging()
    logger = get_logger()
    
    logger.info("=" * 60)
    logger.info("Character Creation System - Starting")
    logger.info("=" * 60)
    
    load_dotenv()
    logger.debug("Environment variables loaded from .env")
    
    parser = argparse.ArgumentParser(
        description='Create a character document using a Google Docs template and Gemini AI'
    )
    
    # Input source (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--json',
        type=str,
        help='Path to JSON file with character data'
    )
    input_group.add_argument(
        '--jsonl',
        type=str,
        help='Path to JSONL file with character data (one JSON object per line)'
    )
    input_group.add_argument(
        '--name',
        help='Character name (requires other CLI arguments)'
    )
    
    # Base character parameters (required if using --name)
    parser.add_argument('--sex', choices=['male', 'female'], help='Character sex')
    parser.add_argument(
        '--gender',
        choices=['he/him', 'she/her', 'they/them'],
        help='Gender identity'
    )
    parser.add_argument(
        '--age_range',
        choices=['child', 'teen', 'adult', 'middle-age', 'elderly'],
        help='Age range'
    )
    parser.add_argument('--ethnicity', help='Character ethnicity')
    parser.add_argument('--occupation', required=False, help='Character occupation')
    parser.add_argument(
        '--new_doc_title',
        default=None,
        help='Optional title for created document'
    )
    parser.add_argument(
        '--json_output',
        action='store_true',
        help='Save character data as structured JSON'
    )
    
    # D&D 5e 2024 enhancement (optional)
    parser.add_argument(
        '--species',
        choices=DND_SPECIES,
        default=None,
        help='D&D 5e 2024 species (enables D&D enhancement)'
    )
    parser.add_argument(
        '--class',
        dest='character_class',
        choices=DND_CLASSES,
        default=None,
        help='D&D 5e 2024 class'
    )
    parser.add_argument(
        '--subclass',
        default=None,
        help='D&D 5e 2024 subclass (must match chosen class)'
    )
    parser.add_argument(
        '--level',
        type=int,
        default=None,
        help='D&D 5e 2024 level (1-20)'
    )
    
    args = parser.parse_args()
    
    # Load and prepare character arguments
    character_args_list = []
    
    if args.json or args.jsonl:
        # Load from JSON/JSONL file
        file_path = args.json or args.jsonl
        is_jsonl = bool(args.jsonl)
        
        logger.info(f"Loading character data from {file_path}")
        is_valid, error_msg, characters = process_character_file(
            file_path,
            is_jsonl=is_jsonl
        )
        
        if not is_valid:
            logger.error(f"Character file validation failed: {error_msg}")
            print(f"❌ Error: {error_msg}")
            raise SystemExit(1)
        
        logger.info(f"Loaded {len(characters)} character(s)")
        
        for char_data in characters:
            char_args = extract_character_args(char_data)
            # Apply any CLI overrides
            if args.species:
                char_args['species'] = args.species
            if args.character_class:
                char_args['character_class'] = args.character_class
            if args.subclass:
                char_args['subclass'] = args.subclass
            if args.level:
                char_args['level'] = args.level
            character_args_list.append(char_args)
    else:
        # CLI mode - validate required arguments
        if not (args.name and args.sex and args.gender and args.age_range
                and args.ethnicity and args.occupation):
            logger.error(
                "CLI mode requires: --name, --sex, --gender, --age_range, "
                "--ethnicity, --occupation"
            )
            print(
                "❌ Error: CLI mode requires: --name, --sex, --gender, "
                "--age_range, --ethnicity, --occupation"
            )
            raise SystemExit(1)
        
        character_args_list = [{
            'name': args.name,
            'sex': args.sex,
            'gender': args.gender,
            'age_range': args.age_range,
            'ethnicity': args.ethnicity,
            'occupation': args.occupation,
            'species': args.species,
            'character_class': args.character_class,
            'level': args.level,
            'subclass': args.subclass,
            'new_doc_title': args.new_doc_title,
            'json_output': args.json_output,
        }]
    
    # Load environment variables
    service_account_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    project = os.getenv('GOOGLE_PROJECT')
    location = os.getenv('GOOGLE_LOCATION', 'us-central1')
    model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
    csv_path = os.getenv('CHARACTERS_CSV', 'characters.csv')
    jsonl_path = os.getenv('CHARACTERS_JSONL', 'characters.jsonl')
    json_dir = os.getenv('CHARACTERS_JSON_DIR', 'characters')
    template_doc_id = os.getenv('TEMPLATE_DOC_ID')
    
    logger.debug(
        f"Configuration: project={project}, location={location}, "
        f"model={model_name}, csv={csv_path}, jsonl={jsonl_path}, "
        f"json_dir={json_dir}, template={template_doc_id}"
    )
    
    # Initialize clients
    gemini_client = GeminiClient(project, location, model_name)
    logger.debug("Gemini client initialized")
    
    # Initialize D&D enhancer with shared gemini_client
    dnd_enhancer = DNDEnhancer(
        project, location, model_name,
        gemini_client=gemini_client
    )
    logger.debug("D&D Enhancer initialized")
    
    # Validate configuration
    if not service_account_file or not os.path.exists(service_account_file):
        logger.error(f"Service account file not found: {service_account_file}")
        raise SystemExit(
            'ERROR: Set GOOGLE_APPLICATION_CREDENTIALS to a valid '
            'service account JSON path'
        )
    if not project:
        logger.error("GOOGLE_PROJECT environment variable not set")
        raise SystemExit('ERROR: Set GOOGLE_PROJECT environment variable')
    if not template_doc_id:
        logger.error("TEMPLATE_DOC_ID environment variable not set")
        raise SystemExit('ERROR: Set TEMPLATE_DOC_ID environment variable')
    
    logger.info("Configuration validated successfully")
    
    # Initialize Google services once
    print("🔗 Connecting to Google APIs...")
    logger.info("Connecting to Google APIs...")
    drive_service, docs_service = create_services(service_account_file)
    
    # Fetch template once
    print("📋 Loading template...")
    logger.info(f"Loading template from document: {template_doc_id}")
    template_text = get_template_text(drive_service, template_doc_id)
    
    # Process each character
    for char_idx, char_args in enumerate(character_args_list, 1):
        print(f"\n{'='*60}")
        print(f"📝 Character {char_idx}/{len(character_args_list)}: {char_args['name']}")
        print(f"{'='*60}\n")
        
        logger.info(
            f"Processing character {char_idx}: name={char_args.get('name')}, "
            f"ethnicity={char_args.get('ethnicity')}, "
            f"sex/gender={char_args.get('sex')}/{char_args.get('gender')}, "
            f"age={char_args.get('age_range')}, "
            f"occupation={char_args.get('occupation')}"
        )
        
        # Prepare character inputs
        character_inputs = {
            'name': char_args.get('name'),
            'sex': char_args.get('sex'),
            'gender': char_args.get('gender'),
            'age_range': char_args.get('age_range'),
            'ethnicity': char_args.get('ethnicity'),
            'occupation': char_args.get('occupation'),
        }
        
        # Add optional template fields if present
        optional_fields = {}
        for section in [
            'Demographics', 'Physical Appearance', 'History',
            'Psychological Traits', 'Communication',
            'Strengths, Weaknesses, and Abilities', 'Relationships',
            'Character Growth'
        ]:
            for key, value in char_args.items():
                if key not in [
                    'name', 'sex', 'gender', 'age_range', 'ethnicity',
                    'occupation', 'species', 'character_class', 'level',
                    'subclass', 'new_doc_title', 'json_output'
                ]:
                    optional_fields[key] = value
        
        if optional_fields:
            character_inputs['optional_fields'] = optional_fields
            logger.debug(f"Added {len(optional_fields)} optional fields")
        
        # Build prompt and call Gemini
        print("🤖 Generating character with Gemini AI...")
        logger.info("Building character generation prompt")
        
        json_output_mode = char_args.get('json_output', False)
        
        if json_output_mode:
            print("   → Using structured JSON output")
            logger.info("JSON output mode: requesting JSON from Gemini")
            prompt = build_json_character_prompt(template_text, character_inputs)
        else:
            # Use legacy text-based approach
            optional_text = ""
            if optional_fields:
                optional_text = (
                    "\nOPTIONAL TEMPLATE FIELDS:\n"
                    + "\n".join(
                        f"- {k}: {v}" for k, v in optional_fields.items()
                    ) + "\n"
                )
            
            prompt = (
                "You are a creative character development assistant. "
                "Fill in the following character template "
                "by replacing all placeholder fields with realistic and interesting "
                "details based on the provided inputs. "
                "Maintain creative consistency and make the character vivid and memorable.\n\n"
                
                "CHARACTER INPUTS:\n"
                f"- Name: {character_inputs['name']}\n"
                f"- Sex: {character_inputs['sex']}\n"
                f"- Gender Identity: {character_inputs['gender']}\n"
                f"- Ethnicity: {character_inputs['ethnicity']}\n"
                f"- Age Range: {character_inputs['age_range']}\n"
                f"- Occupation: {character_inputs['occupation']}\n"
                f"{optional_text}"
                
                "TEMPLATE TO FILL:\n"
                "---START TEMPLATE---\n"
                f"{template_text}\n"
                "---END TEMPLATE---\n\n"
                
                "Instructions:\n"
                "1. Replace all {{NAME}}, {{SEX}}, {{GENDER}}, {{AGE_RANGE}}, "
                "{{OCCUPATION}} with the provided values\n"
                "2. Fill in any other blank sections with creative and consistent "
                "character details\n"
                "3. Make the character's background, personality, and traits coherent\n"
                "4. Output ONLY the completed character profile, nothing else\n"
            )
        
        logger.info("Calling Gemini to generate base character profile")
        gemini_response = gemini_client.generate(
            prompt=prompt,
            temperature=0.7,
            max_output_tokens=2048
        )
        
        # Process response based on output mode
        character_json = None
        if json_output_mode:
            print("✓ Validating JSON structure...")
            is_valid, character_json, error_msg = validate_json_output(
                gemini_response
            )
            if not is_valid:
                logger.warning(
                    f"JSON validation failed: {error_msg}. Falling back to text mode."
                )
                print("⚠️  JSON validation failed, using text output instead")
                filled_content = gemini_response
            else:
                logger.info("JSON validation successful")
                filled_content = flatten_json_for_text(character_json)
        else:
            filled_content = gemini_response
        
        # Create new Google Doc
        print("📄 Creating Google Doc...")
        doc_title = (
            char_args.get('new_doc_title') or
            f"Character - {char_args['name']} - {datetime.utcnow().date()}"
        )
        logger.info(f"Creating new Google Doc: {doc_title}")
        doc_id = create_doc(docs_service, doc_title)
        
        # Insert generated content
        print("✍️  Inserting generated content...")
        logger.info("Inserting generated content into document")
        insert_text(docs_service, doc_id, filled_content)
        
        # Check if D&D enhancement is requested
        enhanced_content = None
        species = char_args.get('species')
        character_class = char_args.get('character_class')
        level = char_args.get('level')
        subclass = char_args.get('subclass')
        
        if species and character_class and level:
            print("🐉 Generating D&D 5e 2024 enhancements...")
            logger.info("D&D enhancement requested")
            
            if level < 1 or level > 20:
                print("⚠️  Warning: Level should be between 1-20")
                logger.warning(f"Invalid level: {level}")
            
            # Validate subclass if provided
            if subclass:
                valid_subclasses = DND_SUBCLASSES.get(character_class, [])
                if subclass not in valid_subclasses:
                    print(
                        f"⚠️  Warning: '{subclass}' is not a valid subclass "
                        f"for {character_class}"
                    )
                    logger.warning(
                        f"Invalid subclass: {subclass} for {character_class}"
                    )
                    print(f"Valid options: {', '.join(valid_subclasses)}")
                    subclass = None
                else:
                    print(f"   Subclass: {subclass}")
                    logger.debug(f"Subclass validated: {subclass}")
            
            enhanced_content = dnd_enhancer.enhance_character(
                base_character=filled_content,
                species=species,
                character_class=character_class,
                level=level,
                subclass=subclass
            )
            
            # Clear the doc and insert enhanced content
            print("📝 Updating document with D&D enhancements...")
            logger.info("Replacing document content with D&D enhanced version")
            requests = [
                {
                    'deleteContentRange': {
                        'range': {'startIndex': 1, 'endIndex': 99999}
                    }
                },
                {
                    'insertText': {
                        'location': {'index': 1},
                        'text': enhanced_content
                    }
                }
            ]
            docs_service.documents().batchUpdate(
                documentId=doc_id, body={'requests': requests}
            ).execute()
            final_content = enhanced_content
        else:
            final_content = filled_content
        
        # Get the document URL
        doc_url = get_doc_url(doc_id)
        logger.debug(f"Document created: {doc_url}")
        
        # Save to CSV
        print("💾 Saving to character tracking CSV...")
        logger.info(f"Saving character record to CSV: {csv_path}")
        csv_tracker = CharacterCSVTracker(csv_path)
        csv_tracker.append_record(
            name=char_args['name'],
            sex=char_args.get('sex'),
            gender=char_args.get('gender'),
            age_range=char_args.get('age_range'),
            occupation=char_args.get('occupation'),
            doc_url=doc_url,
            species=species,
            character_class=character_class,
            level=level,
            subclass=subclass
        )
        
        # Save to JSONL with full AI output
        print("📄 Saving to character tracking JSONL...")
        logger.info(f"Saving character record to JSONL: {jsonl_path}")
        append_character_json(
            json_path=jsonl_path,
            name=char_args['name'],
            sex=char_args.get('sex'),
            gender=char_args.get('gender'),
            age_range=char_args.get('age_range'),
            occupation=char_args.get('occupation'),
            doc_url=doc_url,
            filled_content=filled_content,
            species=species,
            character_class=character_class,
            level=level,
            subclass=subclass,
            dnd_enhancement=enhanced_content
        )
        
        # Save individual character JSON if requested
        if json_output_mode and character_json:
            os.makedirs(json_dir, exist_ok=True)
            json_filename = (
                f"{char_args['name'].lower().replace(' ', '_')}_"
                f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
            )
            json_file_path = os.path.join(json_dir, json_filename)
            print("💾 Saving structured character JSON...")
            logger.info(f"Saving structured character JSON: {json_file_path}")
            save_character_json(json_file_path, character_json, char_args['name'])
            print(f"   → {json_filename}")
        
        # Success output
        print("\n✅ Character created successfully!\n")
        print(f"📎 Document URL: {doc_url}")
        logger.info("Character Creation Completed Successfully")
        
        if species:
            subclass_info = f" ({subclass})" if subclass else ""
            print(
                f"🐉 D&D Profile: {species} {character_class} "
                f"(Level {level}){subclass_info}"
            )
            logger.info(
                f"D&D Profile: {species} {character_class} "
                f"(Level {level}){subclass_info}"
            )
        
        print(f"📊 Tracked in: {csv_path} & {jsonl_path}")
        if json_output_mode:
            print(f"💾 JSON saved to: {json_dir}/")
    
    # Final summary
    print("\n" + "=" * 60)
    print(f"✅ COMPLETE: {len(character_args_list)} character(s) created successfully!")
    print("=" * 60)
    print("\nYour character(s) are ready to view and edit in Google Docs!")
    logger.info("=" * 60)
    logger.info("All characters created successfully")


if __name__ == '__main__':
    main()
