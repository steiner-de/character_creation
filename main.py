#!/usr/bin/env python3
"""Main CLI for character creation via Google Docs + Gemini AI."""

import argparse
import os
from datetime import datetime

from dotenv import load_dotenv

from src.gdocs import create_services, get_template_text, create_doc, insert_text, get_doc_url
from src.gemini_client import generate_from_prompt
from src.csv_tracker import append_character_record
from src.dnd_enhancement import (
    generate_dnd_enhancement,
    DND_SPECIES,
    DND_CLASSES
)


def build_character_prompt(template_text: str, character_inputs: dict) -> str:
    """Build a prompt for Gemini to fill in the character template.
    
    Args:
        template_text: The Google Docs template text
        character_inputs: Dict with name, sex, gender, age_range, occupation
        
    Returns:
        A formatted prompt for Gemini
    """
    prompt = (
        "You are a creative character development assistant. Fill in the following character template "
        "by replacing all placeholder fields with realistic and interesting details based on the provided inputs. "
        "Maintain creative consistency and make the character vivid and memorable.\n\n"
        
        "CHARACTER INPUTS:\n"
        f"- Name: {character_inputs['name']}\n"
        f"- Sex: {character_inputs['sex']}\n"
        f"- Gender Identity: {character_inputs['gender']}\n"
        f"- Age Range: {character_inputs['age_range']}\n"
        f"- Occupation: {character_inputs['occupation']}\n\n"
        
        "TEMPLATE TO FILL:\n"
        "---START TEMPLATE---\n"
        f"{template_text}\n"
        "---END TEMPLATE---\n\n"
        
        "Instructions:\n"
        "1. Replace all {{NAME}}, {{SEX}}, {{GENDER}}, {{AGE_RANGE}}, {{OCCUPATION}} with the provided values\n"
        "2. Fill in any other blank sections with creative and consistent character details\n"
        "3. Make the character's background, personality, and traits coherent\n"
        "4. Output ONLY the completed character profile, nothing else\n"
    )
    return prompt


def main():
    """Main entry point for the character creation CLI."""
    load_dotenv()
    
    parser = argparse.ArgumentParser(
        description='Create a character document using a Google Docs template and Gemini AI'
    )
    
    # Base character parameters (required)
    parser.add_argument('--name', required=True, help='Character name')
    parser.add_argument('--sex', choices=['male', 'female'], required=True, help='Character sex')
    parser.add_argument('--gender', choices=['he/him', 'she/her', 'they/them'], required=True, help='Gender identity')
    parser.add_argument('--age_range', choices=['child', 'teen', 'adult', 'middle-age', 'elderly'], required=True, help='Age range')
    parser.add_argument('--occupation', required=True, help='Character occupation')
    parser.add_argument('--template_doc_id', required=True, help='Google Docs template file ID')
    parser.add_argument('--new_doc_title', default=None, help='Optional title for created document')
    
    # D&D 5e 2024 enhancement (optional)
    parser.add_argument('--species', choices=DND_SPECIES, default=None, help='D&D 5e 2024 species (enables D&D enhancement)')
    parser.add_argument('--class', dest='character_class', choices=DND_CLASSES, default=None, help='D&D 5e 2024 class')
    parser.add_argument('--level', type=int, default=None, help='D&D 5e 2024 level (1-20)')
    
    args = parser.parse_args()
    
    # Load environment variables
    service_account_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    project = os.getenv('GOOGLE_PROJECT')
    location = os.getenv('GOOGLE_LOCATION', 'us-central1')
    model_name = os.getenv('GEMINI_MODEL', 'text-bison@001')
    csv_path = os.getenv('CHARACTERS_CSV', 'characters.csv')
    
    # Validate configuration
    if not service_account_file or not os.path.exists(service_account_file):
        raise SystemExit('ERROR: Set GOOGLE_APPLICATION_CREDENTIALS to a valid service account JSON path')
    if not project:
        raise SystemExit('ERROR: Set GOOGLE_PROJECT environment variable')
    
    print(f"📝 Creating character: {args.name}")
    print(f"   Sex: {args.sex}, Gender: {args.gender}, Age: {args.age_range}, Occupation: {args.occupation}\n")
    
    # Initialize Google services
    print("🔗 Connecting to Google APIs...")
    drive_service, docs_service = create_services(service_account_file)
    
    # Fetch template
    print("📋 Loading template...")
    template_text = get_template_text(drive_service, args.template_doc_id)
    
    # Prepare character inputs
    character_inputs = {
        'name': args.name,
        'sex': args.sex,
        'gender': args.gender,
        'age_range': args.age_range,
        'occupation': args.occupation,
    }
    
    # Build prompt and call Gemini
    print("🤖 Generating character with Gemini AI...")
    prompt = build_character_prompt(template_text, character_inputs)
    filled_content = generate_from_prompt(
        project=project,
        location=location,
        model_name=model_name,
        prompt=prompt,
        temperature=0.7,
        max_output_tokens=2048
    )
    
    # Create new Google Doc
    print("📄 Creating Google Doc...")
    doc_title = args.new_doc_title or f"Character - {args.name} - {datetime.utcnow().date()}"
    doc_id = create_doc(docs_service, doc_title)
    
    # Insert generated content
    print("✍️  Inserting generated content...")
    insert_text(docs_service, doc_id, filled_content)
    
    # Check if D&D enhancement is requested
    if args.species and args.character_class and args.level:
        print("🐉 Generating D&D 5e 2024 enhancements...")
        if args.level < 1 or args.level > 20:
            print("⚠️  Warning: Level should be between 1-20")
        
        enhanced_content = generate_dnd_enhancement(
            base_character=filled_content,
            species=args.species,
            character_class=args.character_class,
            level=args.level,
            project=project,
            location=location,
            model_name=model_name
        )
        
        # Clear the doc and insert enhanced content
        print("📝 Updating document with D&D enhancements...")
        # Delete all content and re-insert with enhancements
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
    
    # Save to CSV
    print("💾 Saving to character tracking CSV...")
    append_character_record(
        csv_path=csv_path,
        name=args.name,
        sex=args.sex,
        gender=args.gender,
        age_range=args.age_range,
        occupation=args.occupation,
        doc_url=doc_url,
        species=args.species,
        character_class=args.character_class,
        level=args.level
    )
    
    # Success output
    print("\n✅ Character created successfully!\n")
    print(f"📎 Document URL: {doc_url}")
    if args.species:
        print(f"🐉 D&D Profile: {args.species} {args.character_class} (Level {args.level})")
    print(f"📊 Tracked in: {csv_path}")
    print("\nYour character is ready to view and edit in Google Docs!")


if __name__ == '__main__':
    main()
