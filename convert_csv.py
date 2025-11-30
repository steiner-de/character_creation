#!/usr/bin/env python3
"""CLI tool to convert CSV to JSON/JSONL for character creation."""

import argparse
import sys
from pathlib import Path

from src.logger import setup_logging, get_logger
from src.csv_converter import (
    csv_to_json,
    csv_to_json_file,
    csv_to_jsonl_file,
    validate_csv_columns,
)


def main():
    """Main entry point for CSV converter CLI."""
    setup_logging()
    logger = get_logger()
    
    parser = argparse.ArgumentParser(
        description='Convert CSV files to JSON/JSONL format for character creation'
    )
    
    parser.add_argument(
        'csv_file',
        type=str,
        help='Path to CSV file to convert'
    )
    
    output_group = parser.add_mutually_exclusive_group(required=True)
    output_group.add_argument(
        '--json',
        type=str,
        help='Output to JSON file'
    )
    output_group.add_argument(
        '--jsonl',
        type=str,
        help='Output to JSONL file'
    )
    output_group.add_argument(
        '--validate',
        action='store_true',
        help='Validate CSV columns without converting'
    )
    output_group.add_argument(
        '--preview',
        action='store_true',
        help='Preview conversion without saving'
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("CSV to JSON/JSONL Converter")
    logger.info("=" * 60)
    
    csv_path = Path(args.csv_file)
    
    if not csv_path.exists():
        print(f"[ERROR] CSV file not found: {args.csv_file}")
        logger.error(f"CSV file not found: {args.csv_file}")
        sys.exit(1)
    
    print(f"[CSV] File: {args.csv_file}\n")
    
    # Validation mode
    if args.validate:
        print("[VALIDATION] Checking CSV columns...\n")
        all_valid, matched, unmatched = validate_csv_columns(args.csv_file)
        
        print(f"[OK] Matched columns: {len(matched)}")
        for col in matched:
            print(f"   - {col}")
        
        if unmatched:
            print(f"\n[WARNING] Unmatched columns: {len(unmatched)}")
            for col in unmatched:
                print(f"   - {col} (will be skipped)")
        
        if all_valid:
            print("\n[OK] All columns match template!")
        else:
            print("\n[WARNING] Some columns don't match template (will be skipped)")
        
        sys.exit(0)
    
    # Preview mode
    if args.preview:
        print("[PREVIEW] Converting...\n")
        is_valid, error, data = csv_to_json(args.csv_file)
        
        if not is_valid:
            print(f"[ERROR] {error}")
            logger.error(error)
            sys.exit(1)
        
        import json
        
        if isinstance(data, dict):
            print("[INFO] Single Character Preview:\n")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"[INFO] Multiple Characters Preview ({len(data)} characters):\n")
            for idx, char in enumerate(data[:3], 1):
                print(f"--- Character {idx} ---")
                print(json.dumps(char, indent=2, ensure_ascii=False))
                if idx < len(data):
                    print()
            
            if len(data) > 3:
                print(f"\n... and {len(data) - 3} more character(s)")
        
        sys.exit(0)
    
    # JSON conversion
    if args.json:
        print(f"[CONVERT] Converting to JSON: {args.json}\n")
        is_valid, error = csv_to_json_file(args.csv_file, args.json)
        
        if not is_valid:
            print(f"[ERROR] {error}")
            logger.error(error)
            sys.exit(1)
        
        print(f"[OK] Successfully converted and saved to: {args.json}")
        logger.info(f"Conversion complete: {args.csv_file} -> {args.json}")
        sys.exit(0)
    
    # JSONL conversion
    if args.jsonl:
        print(f"[CONVERT] Converting to JSONL: {args.jsonl}\n")
        is_valid, error = csv_to_jsonl_file(args.csv_file, args.jsonl)
        
        if not is_valid:
            print(f"[ERROR] {error}")
            logger.error(error)
            sys.exit(1)
        
        print(f"[OK] Successfully converted and saved to: {args.jsonl}")
        logger.info(f"Conversion complete: {args.csv_file} -> {args.jsonl}")
        sys.exit(0)


if __name__ == '__main__':
    main()
