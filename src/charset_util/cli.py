import argparse
import sys
import json
import logging
from .encoding import detect, convert
from .recovery import repair_mojibake, decode_unicode_escapes
from .inspector import inspect_text, explain_mojibake

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

    # Command: decode-escapes
    decode_parser = subparsers.add_parser("decode-escapes", help="Decode unicode escapes (e.g. \\u4f60) in text")
    decode_parser.add_argument("file", help="Path to the file containing unicode escapes")
    decode_parser.add_argument("-o", "--output", help="Path to output file (default: stdout)")

    # Command: inspect
    inspect_parser = subparsers.add_parser("inspect", help="Inspect character encodings (Educational)")
    inspect_parser.add_argument("text", help="Text to inspect (or file path)")
    inspect_parser.add_argument("--file", action="store_true", help="Treat 'text' argument as a file path")

    # Command: explain-mojibake
    explain_parser = subparsers.add_parser("explain-mojibake", help="Simulate and explain how mojibake happens")
    explain_parser.add_argument("text", help="Original text")
    explain_parser.add_argument("--source", default="utf-8", help="Source encoding (default: utf-8)")
    explain_parser.add_argument("--wrong", default="latin-1", help="Wrong decoding (default: latin-1)")

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

        elif args.command == "decode-escapes":
            with open(args.file, "rb") as f:
                content_bytes = f.read()
            content_str = convert(content_bytes)
            result = decode_unicode_escapes(content_str)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(result)
                print(f"Decoded content written to {args.output}")
            else:
                print(result)

        elif args.command == "inspect":
            text_to_inspect = args.text
            if args.file:
                with open(args.text, "r", encoding="utf-8") as f:
                    text_to_inspect = f.read()
            print(inspect_text(text_to_inspect))

        elif args.command == "explain-mojibake":
            print(explain_mojibake(args.text, args.source, args.wrong))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
