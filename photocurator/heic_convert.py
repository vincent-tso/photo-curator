import subprocess, shutil
from pathlib import Path

SIPS = shutil.which("sips")
CACHE = Path(".heic_cache")

def heic_proxy_image(src: Path) -> Path:
    if not SIPS:
        return None
    
    CACHE.mkdir(exist_ok=True, parents=True)
    dst = CACHE / (src.name + ".jpg")

    if dst.exists():
        return dst
    
    try:
        subprocess.run(
            ["sips", "-s", "format", "jpeg", str(src), "--out", str(dst)],
            check=True, capture_output=True
        )

        return dst if dst.exists() else None
    except Exception:
        return None
