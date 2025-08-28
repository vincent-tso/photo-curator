# app.py
from __future__ import annotations
from pathlib import Path
from datetime import datetime
import json
import typer

from photocurator.ingest import scan_folder  # local module

app = typer.Typer(help="PhotoCurator CLI")

@app.command()
def scan(
    input: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True, readable=True,
                                 help="Folder of photos/videos"),
    out: Path = typer.Option(Path("artifacts/scan.json"), "--out", "-o", help="Output JSON path"),
):
    """Scan a folder and write artifacts/scan.json."""
    out.parent.mkdir(parents=True, exist_ok=True)
    scan = scan_folder(input)

    payload = {
        "version": 1,
        "scanned_at": datetime.now().isoformat(timespec="seconds"),
        "root": str(input.resolve()),
        "counts": {
            "total": len(scan["items"]),
            "images": sum(1 for i in scan["items"] if i["mime"].startswith("image/")),
            "videos": sum(1 for i in scan["items"] if i["mime"].startswith("video/")),
        },
        "items": scan["items"],
    }

    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    typer.secho(f"Wrote {out} with {payload['counts']['total']} items", fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()
