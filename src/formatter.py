"""
Pretty-prints metadata dictionaries to the terminal.
"""

from typing import Dict, Any


def format_metadata(meta: Dict[str, Any], gps_only: bool = False):
    if "error" in meta:
        print(f"  ⚠ Error: {meta['error']}")
        return

    if not gps_only:
        print(f"  Format      : {meta.get('format', 'N/A')}")
        print(f"  Mode        : {meta.get('mode', 'N/A')}")
        size = meta.get("size", {})
        print(f"  Dimensions  : {size.get('width')} x {size.get('height')} px")
        print(f"  File Size   : {meta.get('file_size_kb', 0)} KB")

        exif = meta.get("exif", {})
        if exif:
            print(f"\n  EXIF Data:")
            important = ["Make", "Model", "DateTime", "ExposureTime", "FNumber",
                         "ISOSpeedRatings", "FocalLength", "Flash", "Software"]
            for key in important:
                if key in exif:
                    print(f"    {key:<20}: {exif[key]}")

    gps = meta.get("gps")
    if gps:
        print(f"\n  GPS Coordinates:")
        print(f"    Latitude   : {gps.get('latitude', 'N/A')}")
        print(f"    Longitude  : {gps.get('longitude', 'N/A')}")
        if gps.get("latitude") and gps.get("longitude"):
            lat, lon = gps["latitude"], gps["longitude"]
            print(f"    Maps Link  : https://maps.google.com/?q={lat},{lon}")
    elif gps_only:
        print("  No GPS data found in this image.")
