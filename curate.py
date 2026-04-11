"""Claude-powered curation for security monitoring."""

import json
import pathlib
from datetime import datetime, timezone

import anthropic
from dotenv import load_dotenv

from sources import TAGS
from fetch import fetch_europe, fetch_spain

load_dotenv()

DATA_DIR = pathlib.Path(__file__).parent / "data"
EUROPE_FILE = DATA_DIR / "europe.json"
SPAIN_FILE = DATA_DIR / "spain.json"

client = anthropic.Anthropic(timeout=180.0, max_retries=3)

PROFILE = """Catalina Gil Pinzón es consultora independiente de políticas de seguridad y desarrollo,
radicada en España. Experta en política de drogas, crimen organizado transnacional, y reforma
del sector seguridad. Vinculada a Open Society Foundations (Drug Policy Program) y miembro de
la red del Global Initiative Against Transnational Organized Crime (GI-TOC). Escribe en
Washington Post y El País sobre narcotráfico, paz en Colombia, y reforma de políticas de drogas.

Áreas de expertise:
- Reforma de políticas de drogas (cannabis, cocaína, drogas sintéticas)
- Crimen organizado transnacional (rutas, redes, estructuras)
- Seguridad y desarrollo en América Latina y Europa
- Perspectiva de género en seguridad
- Peacebuilding y DDR (desarme, desmovilización, reintegración)
- Derechos humanos y reducción de daños

Lo que le interesa especialmente:
- Informes y análisis de think tanks sobre crimen organizado en Europa
- Evolución de rutas de narcotráfico (especialmente cocaína hacia Europa)
- Reformas de política de drogas basadas en evidencia
- Conexiones entre crimen organizado y corrupción institucional
- Impacto del crimen organizado en comunidades y derechos humanos
- Cooperación internacional en materia de seguridad

Lo que NO le interesa:
- Sucesos menores sin relevancia analítica
- Noticias puramente locales sin dimensión estructural
- Contenido sensacionalista sin análisis
- Deportes, cultura, crónica social"""


def curate_europe() -> dict:
    """Fetch and curate European security news and analysis."""
    print("Fetching European security sources...")
    articles = fetch_europe()
    print(f"  {len(articles)} raw articles")

    if not articles:
        return {"generated_at": datetime.now(timezone.utc).isoformat(), "articles": []}

    # Build article list for Claude
    article_list = []
    for i, a in enumerate(articles):
        article_list.append(
            f"[{i}] \"{a['title']}\" — {a['source']}\n"
            f"    {a['summary'][:250]}"
        )
    articles_text = "\n\n".join(article_list)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=6000,
        messages=[{
            "role": "user",
            "content": f"""Eres una analista de seguridad especializada en crimen organizado transnacional y política de drogas en Europa. Tu audiencia es una experta con este perfil:

{PROFILE}

De estos artículos de think tanks, agencias y medios especializados, selecciona los 15 más relevantes para un monitor de seguridad europeo.

PRIORIZA:
- Informes y análisis de think tanks sobre crimen organizado, narcotráfico, seguridad
- Nuevos datos o estadísticas sobre tráfico de drogas, rutas, incautaciones
- Cambios en políticas de drogas o seguridad a nivel europeo
- Operaciones policiales de gran alcance (Europol, coordinadas)
- Análisis de redes criminales transnacionales
- Reformas legislativas en materia penal o de drogas
- Cooperación internacional en seguridad
- Impacto del crimen organizado en instituciones y democracia
- Informes de EMCDDA/EUDA, Europol, UNODC

NO PRIORICES:
- Sucesos menores o puramente locales
- Noticias sin dimensión analítica
- Contenido repetitivo o superficial

ARTÍCULOS ({len(articles)}):
{articles_text}

TONO DE LAS FRASES DE ANÁLISIS:
- Factual, no editorial. Describe lo que ocurre y por qué importa, no lo que debería ocurrir.
- Ligeramente crítica: señala limitaciones del enfoque, ángulos que la fuente omite, o tensiones entre lo que se dice y lo que se hace.
- Ej: "La incautación récord en Amberes no altera la tendencia: el volumen total sigue creciendo pese al aumento de operaciones"
- Ej: "El informe de Europol cuantifica redes pero no aborda los incentivos estructurales que las sostienen"

Para cada seleccionado:
- index: el [N] original
- analysis_es: UNA frase factual con perspectiva crítica (no descriptiva, no editorial)
- tag: DEBE ser una de estas exactamente: {", ".join(TAGS)}
- relevance: "alta" o "media" (para priorizar visualmente)

Responde SOLO JSON array, sin markdown:
[{{"index": 0, "analysis_es": "...", "tag": "...", "relevance": "alta"}}, ...]"""
        }],
    )

    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    picks = json.loads(text)

    curated = []
    for p in picks[:15]:
        idx = p["index"]
        if 0 <= idx < len(articles):
            article = articles[idx].copy()
            article["analysis"] = p["analysis_es"]
            article["tag"] = p["tag"]
            article["relevance"] = p.get("relevance", "media")
            curated.append(article)

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "articles": curated,
    }

    DATA_DIR.mkdir(exist_ok=True)
    EUROPE_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"Europe curated: {len(curated)} articles")
    return result


def curate_spain() -> dict:
    """Fetch and curate Spanish security news."""
    print("Fetching Spanish security sources...")
    articles = fetch_spain()
    print(f"  {len(articles)} raw articles")

    if not articles:
        return {"generated_at": datetime.now(timezone.utc).isoformat(), "articles": []}

    article_list = []
    for i, a in enumerate(articles):
        article_list.append(
            f"[{i}] \"{a['title']}\" — {a['source']}\n"
            f"    {a['summary'][:250]}"
        )
    articles_text = "\n\n".join(article_list)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": f"""Eres una analista de seguridad especializada en crimen organizado y política de drogas en España. Tu audiencia es una experta con este perfil:

{PROFILE}

De estas noticias de medios españoles y think tanks nacionales, selecciona las 10 más relevantes para un monitor de seguridad en España.

PRIORIZA:
- Operaciones contra el narcotráfico (especialmente en el Estrecho, Campo de Gibraltar, puertos)
- Informes del Real Instituto Elcano, CIDOB o IEEE sobre seguridad
- Redes de crimen organizado operando en España
- Cambios legislativos en materia penal o de drogas
- Corrupción vinculada al crimen organizado
- Tráfico de personas y migración irregular
- Cooperación España-Marruecos, España-Latinoamérica en seguridad
- Políticas del Ministerio del Interior
- Terrorismo y radicalización

NO PRIORICES:
- Sucesos menores sin relevancia estructural
- Política general sin conexión con seguridad
- Deportes, cultura, crónica social

ARTÍCULOS ({len(articles)}):
{articles_text}

TONO DE LAS FRASES DE ANÁLISIS:
- Factual, no editorial. Describe lo que ocurre y por qué importa, no lo que debería ocurrir.
- Ligeramente crítica: señala limitaciones del enfoque, ángulos que la fuente omite, o tensiones entre lo que se dice y lo que se hace.
- Ej: "La operación en el Campo de Gibraltar se presenta como éxito pero no aborda la reposición inmediata de rutas"
- Ej: "Elcano advierte sobre narco en puertos pero no cuantifica la capacidad real de inspección"

Para cada seleccionado:
- index: el [N] original
- analysis_es: UNA frase factual con perspectiva crítica (no descriptiva, no editorial)
- tag: DEBE ser una de estas exactamente: {", ".join(TAGS)}
- relevance: "alta" o "media"

Responde SOLO JSON array, sin markdown:
[{{"index": 0, "analysis_es": "...", "tag": "...", "relevance": "alta"}}, ...]"""
        }],
    )

    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    picks = json.loads(text)

    curated = []
    for p in picks[:10]:
        idx = p["index"]
        if 0 <= idx < len(articles):
            article = articles[idx].copy()
            article["analysis"] = p["analysis_es"]
            article["tag"] = p["tag"]
            article["relevance"] = p.get("relevance", "media")
            curated.append(article)

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "articles": curated,
    }

    DATA_DIR.mkdir(exist_ok=True)
    SPAIN_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"Spain curated: {len(curated)} articles")

    return result


def generate_audio_briefing(europe_data: dict, spain_data: dict):
    """Generate a spoken security briefing from curated news."""
    import asyncio
    import edge_tts

    europe_articles = europe_data.get("articles", [])
    spain_articles = spain_data.get("articles", [])

    europe_lines = [
        f"- {a['title']} ({a['source']}): {a.get('analysis', '')}"
        for a in europe_articles
    ]
    spain_lines = [
        f"- {a['title']} ({a['source']}): {a.get('analysis', '')}"
        for a in spain_articles
    ]

    prompt = f"""Genera un briefing de audio sobre seguridad, crimen organizado y política de drogas. Será leído por un TTS, así que escribe como se habla: frases claras, ritmo natural, sin bullet points ni formato.

MONITOR EUROPA — SEGURIDAD Y CRIMEN ORGANIZADO:
{chr(10).join(europe_lines) if europe_lines else "Sin artículos hoy."}

MONITOR ESPAÑA — SEGURIDAD:
{chr(10).join(spain_lines) if spain_lines else "Sin artículos hoy."}

INSTRUCCIONES:
- Tono: factual y sobrio. NO editorial. Reporta lo que hay, no lo que debería haber. Como un parte de situación, no un artículo de opinión.
- Perspectiva ligeramente crítica: cuando una fuente presenta algo como éxito o avance, señala brevemente qué omite, qué limitaciones tiene, o qué contexto falta. No con cinismo — con rigor.
- Estructura: empieza con las señales más importantes del panorama europeo, luego España, conectando cuando tenga sentido.
- Distingue entre informes/análisis de think tanks (más peso analítico) y noticias de prensa (más peso informativo).
- Conecta las noticias entre sí cuando tenga sentido (ej: "esto se vincula con..." o "en paralelo...").
- Cierra con una valoración general factual: ¿qué tendencias se consolidan? ¿qué merece seguimiento? Sin recomendar.
- Longitud: ~800-1200 palabras (para ~4 minutos de audio).
- Idioma: español.
- NO uses encabezados, asteriscos, guiones ni ningún formato. Solo texto corrido con párrafos."""

    print("Generating audio briefing text...")
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    briefing_text = response.content[0].text.strip()

    # Save text version
    briefing_text_file = DATA_DIR / "briefing.txt"
    briefing_text_file.write_text(briefing_text)

    # Generate audio
    print("Converting to audio...")
    audio_file = DATA_DIR / "briefing.mp3"

    async def _tts():
        communicate = edge_tts.Communicate(briefing_text, "es-ES-ElviraNeural")
        await communicate.save(str(audio_file))

    asyncio.run(_tts())
    size_kb = audio_file.stat().st_size // 1024
    print(f"  Audio briefing: {size_kb}KB")


if __name__ == "__main__":
    europe = curate_europe()
    spain = curate_spain()
    generate_audio_briefing(europe, spain)
