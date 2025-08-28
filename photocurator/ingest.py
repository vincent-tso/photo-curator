from PIL import Image
from pathlib import Path
# from pillow_heif import register_heif_opener
from .exif_utils import read_exif_datetime
from .heic_convert import heic_proxy_image
from datetime import datetime
import magic

# Ingest folder
# { path, size, mime, exif_datetime, phash? }
# Return scan.json
# Acceptance criteria: python app.py scan --input ~/photo_sample

# register_heif_opener()

# Enable HEIC/HEIF in Pillow
def openable_path(p: Path) -> Path:
    if p.suffix.lower() in {".heic", ".heif"}:
        return heic_proxy_image(p)  # returns JPEG proxy or None
    return p


def scan_folder(path: Path) -> dict:
    path = Path(path)
    items = []

    # Recursively search for all images/videos
    for p in path.rglob("*"):
        # Sanitise
        if not p.is_file():
            continue

        try:
            mime = magic.from_file(str(p), mime=True)
        except:
            continue

        if not (mime.startswith("image/") or mime.startswith("video/")):
            continue

        # Get image data
        size_bytes = p.stat().st_size
        exif_dt = None

        if mime.startswith("image/"):
            p_for_open = openable_path(p)

            if p_for_open is not None:
                exif_dt = read_exif_datetime(p_for_open)

        if not exif_dt:
            exif_dt = datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds")


        items.append({
            "path": str(p),
            "size": size_bytes,
            "mime": mime,
            "exif_datetime": exif_dt
        })

    return { "items": items }
