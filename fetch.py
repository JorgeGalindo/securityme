"""Fetch and parse RSS feeds for security monitoring."""

import json
import pathlib
import time
import xml.etree.ElementTree as ET

import httpx
from bs4 import BeautifulSoup

from sources import (
    FEEDS_EUROPE, FEEDS_SPAIN,
    EUROPE_KEYWORDS, SPAIN_KEYWORDS,
)

DATA_DIR = pathlib.Path(__file__).parent / "data"

NS = {
    "dc": "http://purl.org/dc/elements/1.1/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "atom": "http://www.w3.org/2005/Atom",
    "media": "http://search.yahoo.com/mrss/",
}


def _fetch_feed(url: str) -> str:
    """Fetch raw XML from a feed URL."""
    try:
        resp = httpx.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (SecurityMe Monitor)"},
            timeout=20,
            follow_redirects=True,
        )
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"  Failed to fetch {url}: {e}")
        return ""


def _parse_rss(xml_text: str, source_name: str) -> list[dict]:
    """Parse RSS 2.0 feed."""
    items = []
    try:
        root = ET.fromstring(xml_text)
        for item in root.findall(".//item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            author = (
                item.findtext("dc:creator", namespaces=NS)
                or item.findtext("author")
                or ""
            ).strip()
            desc = item.findtext("description") or ""
            summary = BeautifulSoup(desc, "html.parser").get_text(strip=True)[:400]
            pub_date = (item.findtext("pubDate") or "").strip()

            if title:
                items.append({
                    "title": title,
                    "link": link,
                    "author": author,
                    "summary": summary,
                    "date": pub_date,
                    "source": source_name,
                })
    except ET.ParseError as e:
        print(f"  XML parse error for {source_name}: {e}")
    return items


def _parse_atom(xml_text: str, source_name: str) -> list[dict]:
    """Parse Atom feed."""
    items = []
    try:
        root = ET.fromstring(xml_text)
        ns = {"a": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("a:entry", ns):
            title = (entry.findtext("a:title", namespaces=ns) or "").strip()
            link_el = entry.find("a:link[@rel='alternate']", ns)
            if link_el is None:
                link_el = entry.find("a:link", ns)
            link = link_el.get("href", "") if link_el is not None else ""
            author = (
                entry.findtext("a:author/a:name", namespaces=ns) or ""
            ).strip()
            summary_el = entry.findtext("a:summary", namespaces=ns) or ""
            summary = BeautifulSoup(summary_el, "html.parser").get_text(strip=True)[:400]
            pub_date = (
                entry.findtext("a:published", namespaces=ns)
                or entry.findtext("a:updated", namespaces=ns)
                or ""
            ).strip()

            if title:
                items.append({
                    "title": title,
                    "link": link,
                    "author": author,
                    "summary": summary,
                    "date": pub_date,
                    "source": source_name,
                })
    except ET.ParseError as e:
        print(f"  Atom parse error for {source_name}: {e}")
    return items


def _matches_keywords(article: dict, keywords: list[str]) -> bool:
    """Check if an article matches any security keywords."""
    text = f"{article['title']} {article['summary']}".lower()
    return any(kw.lower() in text for kw in keywords)


def _load_seen(filepath: pathlib.Path) -> set:
    if filepath.exists():
        return set(json.loads(filepath.read_text()))
    return set()


def _save_seen(filepath: pathlib.Path, seen: set):
    DATA_DIR.mkdir(exist_ok=True)
    filepath.write_text(json.dumps(list(seen)))


def fetch_europe() -> list[dict]:
    """Fetch articles from European security think tanks and agencies."""
    seen_file = DATA_DIR / "seen_europe.json"
    seen = _load_seen(seen_file)
    articles = []

    for source, url in FEEDS_EUROPE.items():
        print(f"  Fetching {source}...")
        xml = _fetch_feed(url)
        if not xml:
            continue

        # Try RSS first, then Atom
        items = _parse_rss(xml, source)
        if not items:
            items = _parse_atom(xml, source)

        for item in items[:30]:  # Max 30 per source
            if item["link"] in seen:
                continue

            # For specialized security sources (GI-TOC, OCCRP, InSight Crime,
            # Europol, EMCDDA), include everything — they're already on-topic
            specialized = source in {
                "GI-TOC", "OCCRP", "InSight Crime", "Europol",
                "EMCDDA/EUDA", "EUISS", "IDPC", "TNI",
            }

            if specialized or _matches_keywords(item, EUROPE_KEYWORDS):
                articles.append(item)
                seen.add(item["link"])

        time.sleep(0.5)

    _save_seen(seen_file, seen)
    return articles


def fetch_spain() -> list[dict]:
    """Fetch articles from Spanish media and think tanks about security."""
    seen_file = DATA_DIR / "seen_spain.json"
    seen = _load_seen(seen_file)
    articles = []

    for source, url in FEEDS_SPAIN.items():
        print(f"  Fetching {source}...")
        xml = _fetch_feed(url)
        if not xml:
            continue

        # Think tanks: include everything
        is_thinktank = source in {"Real Instituto Elcano", "CIDOB", "IEEE"}

        if "elconfidencial" in url:
            items = _parse_atom(xml, source)
        else:
            items = _parse_rss(xml, source)

        for item in items[:25]:
            if item["link"] in seen:
                continue
            if is_thinktank or _matches_keywords(item, SPAIN_KEYWORDS):
                articles.append(item)
                seen.add(item["link"])

        time.sleep(0.5)

    _save_seen(seen_file, seen)
    return articles


if __name__ == "__main__":
    print("Fetching European security sources...")
    eu = fetch_europe()
    print(f"  {len(eu)} articles")
    for a in eu[:5]:
        print(f"    [{a['source']}] {a['title']}")

    print("\nFetching Spanish security sources...")
    es = fetch_spain()
    print(f"  {len(es)} articles")
    for a in es[:5]:
        print(f"    [{a['source']}] {a['title']}")
