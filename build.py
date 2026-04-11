"""Build static site for GitHub Pages deployment."""

import json
import pathlib
import shutil
from datetime import datetime, timezone

from jinja2 import Environment, FileSystemLoader

ROOT = pathlib.Path(__file__).parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "docs"  # GitHub Pages serves from /docs


def build():
    """Render templates with data and output static HTML."""
    # Clean and recreate output
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()

    # Copy static assets
    static_src = ROOT / "static"
    static_dst = OUTPUT_DIR / "static"
    if static_src.exists():
        shutil.copytree(static_src, static_dst)

    # Copy audio briefing if exists
    briefing_src = DATA_DIR / "briefing.mp3"
    if briefing_src.exists():
        shutil.copy2(briefing_src, OUTPUT_DIR / "briefing.mp3")

    # Load data
    europe_data = {}
    europe_file = DATA_DIR / "europe.json"
    if europe_file.exists():
        europe_data = json.loads(europe_file.read_text())

    spain_data = {}
    spain_file = DATA_DIR / "spain.json"
    if spain_file.exists():
        spain_data = json.loads(spain_file.read_text())

    # Format timestamps
    def format_date(iso_str: str) -> str:
        if not iso_str:
            return ""
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%d %b %Y, %H:%M")

    europe_generated = format_date(europe_data.get("generated_at", ""))
    spain_generated = format_date(spain_data.get("generated_at", ""))
    has_audio = briefing_src.exists()

    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(str(ROOT / "templates")))

    # Render Europe page (index)
    template = env.get_template("europa.html")
    html = template.render(
        articles=europe_data.get("articles", []),
        generated_at=europe_generated,
        has_audio=has_audio,
    )
    (OUTPUT_DIR / "index.html").write_text(html)

    # Render Spain page
    template = env.get_template("espana.html")
    html = template.render(
        articles=spain_data.get("articles", []),
        generated_at=spain_generated,
        has_audio=has_audio,
    )
    (OUTPUT_DIR / "espana.html").write_text(html)

    print(f"Built static site in {OUTPUT_DIR}/")
    print(f"  Europa: {len(europe_data.get('articles', []))} articles")
    print(f"  España: {len(spain_data.get('articles', []))} articles")
    print(f"  Audio: {'yes' if has_audio else 'no'}")


if __name__ == "__main__":
    build()
