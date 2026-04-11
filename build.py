"""Build static site for GitHub Pages deployment."""

import json
import pathlib
import shutil
from datetime import datetime, timezone

from jinja2 import Environment, FileSystemLoader
from sources import FEEDS_EUROPE, FEEDS_SPAIN

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

    # Build sources list with descriptions
    europe_descs = {
        "GI-TOC": "Crimen organizado transnacional",
        "OCCRP": "Periodismo de investigación — corrupción y crimen",
        "InSight Crime": "Crimen organizado en las Américas",
        "RUSI": "Seguridad y defensa (UK)",
        "Chatham House": "Política internacional (UK)",
        "Carnegie Europe": "Política europea",
        "ECFR": "Política exterior europea",
        "IISS": "Seguridad estratégica",
        "SIPRI": "Paz y conflictos armados (Suecia)",
        "Crisis Group": "Análisis de conflictos",
        "Clingendael": "Seguridad europea (Países Bajos)",
        "TNI": "Política de drogas (Países Bajos)",
        "IDPC": "Consorcio internacional de política de drogas",
        "Brookings": "Políticas públicas (EEUU)",
        "CEPS": "Política europea (Bruselas)",
        "EMCDDA/EUDA": "Agencia UE — observatorio de drogas",
        "Europol": "Agencia UE — policía",
        "EUISS": "Instituto UE — estudios de seguridad",
        "Frontex": "Agencia UE — fronteras",
        "ENISA": "Agencia UE — ciberseguridad",
        "EC Home Affairs": "Comisión Europea — asuntos de interior",
        "EC Justice": "Comisión Europea — justicia",
        "EC Security Union": "Comisión Europea — unión de seguridad",
        "SWP (EN)": "Think tank alemán — publicaciones",
        "SWP (all)": "Think tank alemán — todo el contenido",
        "DCAF": "Gobernanza del sector seguridad (Ginebra)",
        "Small Arms Survey (Medium)": "Armas pequeñas y violencia armada",
        "RAND Research Reports": "Informes de investigación RAND",
        "RAND Commentary": "Análisis y comentarios RAND",
        "Drug Policy Alliance": "Reforma de política de drogas (EEUU)",
        "Transform Drug Policy (blog)": "Reforma de política de drogas (UK)",
        "Harm Reduction International": "Reducción de daños global",
        "Release (UK)": "Política de drogas y derecho (UK)",
        "Financial Transparency Coalition": "Transparencia financiera y flujos ilícitos",
    }
    spain_descs = {
        "El País (España)": "Prensa — sección España",
        "El Confidencial": "Prensa — investigación",
        "El Mundo": "Prensa — España",
        "eldiario.es": "Prensa — política",
        "La Vanguardia (Política)": "Prensa — política",
        "La Vanguardia (Internacional)": "Prensa — internacional",
        "La Vanguardia (Sucesos)": "Prensa — sucesos",
        "ABC": "Prensa — portada",
        "Real Instituto Elcano": "Think tank — relaciones internacionales",
        "CIDOB": "Think tank — Barcelona",
        "IEEE": "Instituto de estudios estratégicos (Defensa)",
        "Fundación Alternativas": "Think tank — políticas públicas",
    }

    europe_sources = [
        (name, url, europe_descs.get(name, ""))
        for name, url in FEEDS_EUROPE.items()
    ]
    spain_sources = [
        (name, url, spain_descs.get(name, ""))
        for name, url in FEEDS_SPAIN.items()
    ]

    # Render Fuentes page
    template = env.get_template("fuentes.html")
    html = template.render(
        europe_sources=europe_sources,
        spain_sources=spain_sources,
    )
    (OUTPUT_DIR / "fuentes.html").write_text(html)

    print(f"Built static site in {OUTPUT_DIR}/")
    print(f"  Europa: {len(europe_data.get('articles', []))} articles")
    print(f"  España: {len(spain_data.get('articles', []))} articles")
    print(f"  Fuentes: {len(europe_sources)} EU + {len(spain_sources)} ES")
    print(f"  Audio: {'yes' if has_audio else 'no'}")


if __name__ == "__main__":
    build()
