"""news-image-01: write one image summing up 13 November 2026 world news to /output/entry.png. Deterministic: copies the image the repository holds. No network."""
import os
import shutil
from pathlib import Path

SRC = Path(__file__).resolve().parent / "assets" / "entry.png"
DST = Path(os.environ.get("ENTRY_OUTPUT", "/output/entry.png"))

def main() -> None:
    DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, DST)

if __name__ == "__main__":
    main()
