"""Copy the newspaper front page to the output path."""
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "entry.png")

if not os.path.isfile(SRC):
    raise FileNotFoundError(f"source image not found: {SRC}")

out = os.environ.get("ENTRY_OUTPUT", "/output/entry.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
shutil.copyfile(SRC, out)
print(out)
