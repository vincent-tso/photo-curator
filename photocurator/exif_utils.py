import datetime
from pathlib import Path
from PIL import Image

# EXIF tag IDs
DT_ORIGINAL = 36867   # DateTimeOriginal
DT           = 306    # DateTime
DT_DIGITIZED = 36868  # DateTimeDigitized
DATE_TAGS = (DT_ORIGINAL, DT, DT_DIGITIZED)

def _normalize_exif_datetime(value: str) -> str:
    if not value:
        return None
    s = value.strip().replace("\x00", "")
    for fmt in ("%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y:%m:%d %H:%M:%S%z"):
        try:
            dt = datetime.strptime(s, fmt)
            return dt.isoformat(timespec="seconds")
        except ValueError:
            continue
    return None

def read_exif_datetime(path: Path) -> str:
    try:
        with Image.open(path) as im:
            exif = im.getexif()

            if not exif:
                return None
            
            for tag in DATE_TAGS:
                raw = exif.get(tag)

                if isinstance(raw, bytes):
                    try:
                        raw = raw.decode(errors="ignore")
                    except Exception:
                        raw = None

                iso = _normalize_exif_datetime(raw)
                
                if iso:
                    return iso
    except Exception:
        return None
    return None
