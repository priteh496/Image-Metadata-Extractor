# Image Metadata Extractor

## Description
Extracts EXIF metadata, GPS coordinates, and file information from image files. Supports JPEG, PNG, TIFF, and more.

## Features
- Extract camera make/model, date, exposure, ISO
- Parse GPS coordinates and generate Google Maps link
- Batch process entire directories
- Export results to JSON
- GPS-only mode

## Tech Stack
- Python 3.10+
- Pillow (PIL)

## Installation
```bash
pip install -r requirements.txt
```

## How to Run
```bash
python main.py photo.jpg
python main.py photo.jpg --gps
python main.py ./photos --batch -o metadata.json
```

## Example Output
```
📷 photo.jpg
  Format      : JPEG
  Dimensions  : 4032 x 3024 px
  File Size   : 3847.5 KB
  EXIF Data:
    Make               : Apple
    Model              : iPhone 14 Pro
    DateTime           : 2023:07:15 14:22:10
  GPS Coordinates:
    Latitude   : 48.858844
    Longitude  : 2.294351
    Maps Link  : https://maps.google.com/?q=48.858844,2.294351
```
