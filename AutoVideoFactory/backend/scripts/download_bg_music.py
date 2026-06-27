import io, os, sys, zipfile
from pathlib import Path
import httpx

MOOD_CATEGORY_MAP = {
    "energetic": ["electronic", "synth", "trap"],
    "educational": ["ambient", "lofi", "piano", "nature"],
    "dramatic": ["cinematic", "world"],
    "humorous": ["jazz", "electronic"],
    "serious": ["cinematic", "piano"],
    "generic": ["ambient", "electronic", "jazz", "lofi", "nature", "piano", "world"],
}

BASE_DIR = Path(__file__).resolve().parent.parent / "output" / "music"
ZIP_URL = "https://github.com/btahir/open-lofi/releases/latest/download/openlofi.zip"


def main():
    print("Downloading open-lofi CC0 music tracks...")
    resp = httpx.get(ZIP_URL, follow_redirects=True, timeout=120)
    resp.raise_for_status()
    print(f"Downloaded {len(resp.content) / 1024 / 1024:.1f} MB")

    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        for name in zf.namelist():
            p = Path(name)
            if p.suffix.lower() not in (".mp3", ".wav", ".flac", ".ogg", ".m4a"):
                continue
            parts = p.parts
            category = parts[1] if len(parts) > 2 else "generic"
            category = category.lower()

            placed = False
            for mood, cats in MOOD_CATEGORY_MAP.items():
                if category in cats:
                    dest = BASE_DIR / mood / p.name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    with zf.open(name) as src, open(dest, "wb") as dst:
                        dst.write(src.read())
                    placed = True
                    break
            if not placed:
                dest = BASE_DIR / "generic" / p.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(name) as src, open(dest, "wb") as dst:
                    dst.write(src.read())

    counts = {}
    for d in BASE_DIR.iterdir():
        if d.is_dir():
            n = len(list(d.iterdir()))
            counts[d.name] = n
    print(f"Done. Tracks per mood: {counts}")


if __name__ == "__main__":
    main()
