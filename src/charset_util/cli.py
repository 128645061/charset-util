import argparse
import sys
import json
import logging
from .encoding import detect, convert
from .recovery import repair_mojibake, recover_json

def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stderr
    )

def main():
    parser = argparse.ArgumentParser(
        description="Charset Util CLI - Tools for encoding detection, conversion, and data recovery."
    )
    
    # Global arguments
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose debug logging")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: detect
    detect_parser = subparsers.add_parser("detect", help="Detect encoding of a file")
    detect_parser.add_argument("file", help="Path to the file")

    # Command: convert
    convert_parser = subparsers.add_parser("convert", help="Convert file encoding")
    convert_parser.add_argument("file", help="Path to the source file")
    convert_parser.add_argument("-t", "--target", default="utf-8", help="Target encoding (default: utf-8)")
    convert_parser.add_argument("-o", "--output", help="Path to output file (default: stdout)")

    # Command: repair
    repair_parser = subparsers.add_parser("repair", help="Repair mojibake (乱码)")
    repair_parser.add_argument("file", help="Path to the file containing mojibake")
    repair_parser.add_argument("-o", "--output", help="Path to output file (default: stdout)")

    # Command: recover-json
    recover_parser = subparsers.add_parser("recover-json", help="Recover truncated/messy JSON")
    recover_parser.add_argument("file", help="Path to the file containing messy JSON")
    recover_parser.add_argument("-o", "--output", help="Path to output file (default: stdout)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    setup_logging(args.verbose)

    try:
        if args.command == "detect":
            with open(args.file, "rb") as f:
                content = f.read()
            result = detect(content)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "convert":
            with open(args.file, "rb") as f:
                content = f.read()
            result = convert(content, target_encoding=args.target)
            if args.output:
                with open(args.output, "w", encoding=args.target) as f:
                    f.write(result)
                print(f"Converted content written to {args.output}")
            else:
                print(result)

        elif args.command == "repair":
            # Assuming file is readable as text, or we detect it first
            with open(args.file, "rb") as f:
                content_bytes = f.read()
            # First ensure we have a string
            content_str = convert(content_bytes)
            result = repair_mojibake(content_str)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(result)
                print(f"Repaired content written to {args.output}")
            else:
                print(result)

        elif args.command == "recover-json":
            with open(args.file, "rb") as f:
                content_bytes = f.read()
            # recover_json handles bytes or str
            data = recover_json(content_bytes)
            result = json.dumps(data, indent=2, ensure_ascii=False)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(result)
                print(f"Recovered JSON written to {args.output}")
            else:
                print(result)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
