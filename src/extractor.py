"""
Metadata extraction using Pillow and its EXIF support.
"""

import json
from pathlib import Path
from typing import Dict, Any

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


class MetadataExtractor:
    def extract(self, image_path: Path) -> Dict[str, Any]:
        """Extract all metadata from an image file."""
        if not PILLOW_AVAILABLE:
            raise RuntimeError("Pillow is not installed. Run: pip install Pillow")

        meta = {}
        try:
            with Image.open(image_path) as img:
                # Basic image info
                meta["filename"] = image_path.name
                meta["format"] = img.format
                meta["mode"] = img.mode
                meta["size"] = {"width": img.width, "height": img.height}
                meta["file_size_kb"] = round(image_path.stat().st_size / 1024, 2)

                # EXIF data
                exif_data = img._getexif() if hasattr(img, "_getexif") else None
                if exif_data:
                    exif = {}
                    gps_info_raw = {}
                    for tag_id, value in exif_data.items():
                        tag_name = TAGS.get(tag_id, str(tag_id))
                        if tag_name == "GPSInfo":
                            for gps_tag_id, gps_value in value.items():
                                gps_tag_name = GPSTAGS.get(gps_tag_id, str(gps_tag_id))
                                gps_info_raw[gps_tag_name] = str(gps_value)
                        else:
                            # Serialize complex types to string
                            try:
                                json.dumps(value)
                                exif[tag_name] = value
                            except (TypeError, ValueError):
                                exif[tag_name] = str(value)
                    meta["exif"] = exif
                    if gps_info_raw:
                        meta["gps"] = self._parse_gps(gps_info_raw)
                else:
                    meta["exif"] = {}
                    meta["gps"] = None
        except Exception as e:
            meta["error"] = str(e)

        return meta

    def _parse_gps(self, gps_raw: Dict) -> Dict:
        """Convert raw GPS tuples to decimal degrees."""
        try:
            def to_decimal(values, ref):
                d, m, s = [float(v) for v in values.strip("()").split(",")]
                decimal = d + m / 60 + s / 3600
                if ref in ("S", "W"):
                    decimal = -decimal
                return round(decimal, 6)

            lat = to_decimal(gps_raw.get("GPSLatitude", "0,0,0"), gps_raw.get("GPSLatitudeRef", "N"))
            lon = to_decimal(gps_raw.get("GPSLongitude", "0,0,0"), gps_raw.get("GPSLongitudeRef", "E"))
            return {"latitude": lat, "longitude": lon, "raw": gps_raw}
        except Exception:
            return {"raw": gps_raw}

    def save_json(self, data: Dict, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
