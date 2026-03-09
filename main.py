"""
Image Metadata Extractor
Extracts and displays EXIF/metadata from image files.
"""

import argparse
from pathlib import Path
from src.extractor import MetadataExtractor
from src.formatter import format_metadata


def parse_args():
    parser = argparse.ArgumentParser(description="Extract image metadata/EXIF data")
    parser.add_argument("input", help="Image file or directory")
    parser.add_argument("--batch", action="store_true", help="Process all images in directory")
    parser.add_argument("-o", "--output", help="Save metadata to JSON file")
    parser.add_argument("--gps", action="store_true", help="Show GPS coordinates only")
    return parser.parse_args()


def main():
    args = parse_args()
    extractor = MetadataExtractor()
    input_path = Path(args.input)

    if args.batch:
        if not input_path.is_dir():
            print(f"Error: '{input_path}' is not a directory.")
            return
        images = list(input_path.glob("*"))
        images = [f for f in images if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".tiff", ".bmp", ".webp"}]
        all_meta = {}
        for img in images:
            meta = extractor.extract(img)
            all_meta[img.name] = meta
            print(f"\n📷 {img.name}")
            format_metadata(meta, gps_only=args.gps)
        if args.output:
            extractor.save_json(all_meta, args.output)
            print(f"\n💾 Saved to {args.output}")
    else:
        if not input_path.is_file():
            print(f"Error: '{input_path}' not found.")
            return
        meta = extractor.extract(input_path)
        print(f"\n📷 {input_path.name}")
        format_metadata(meta, gps_only=args.gps)
        if args.output:
            extractor.save_json({input_path.name: meta}, args.output)
            print(f"\n💾 Saved to {args.output}")


if __name__ == "__main__":
    main()
