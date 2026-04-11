"""RSS feed sources for European and Spanish security monitoring."""

# ── European Security: Think Tanks, Agencies & Watchdogs ──────────────────────

FEEDS_EUROPE = {
    # Think tanks & research institutes
    "GI-TOC": "https://globalinitiative.net/feed/",
    "OCCRP": "https://www.occrp.org/en/component/ocrss/?format=feed",
    "InSight Crime": "https://insightcrime.org/feed/",
    "RUSI": "https://www.rusi.org/rss.xml",
    "Chatham House": "https://www.chathamhouse.org/rss/publications",
    "Carnegie Europe": "https://carnegieeurope.eu/rss/feeds/articles",
    "ECFR": "https://ecfr.eu/feed/",
    "IISS": "https://www.iiss.org/rss/",
    "SIPRI": "https://www.sipri.org/rss.xml",
    "Crisis Group": "https://www.crisisgroup.org/rss.xml",
    "Clingendael": "https://www.clingendael.org/rss.xml",
    "TNI": "https://www.tni.org/en/rss.xml",
    "IDPC": "https://idpc.net/feed",
    "Brookings": "https://www.brookings.edu/feed/",
    "CEPS": "https://www.ceps.eu/feed/",
    # EU agencies
    "EMCDDA/EUDA": "https://www.emcdda.europa.eu/rss.xml",
    "Europol": "https://www.europol.europa.eu/rss.xml",
    "EUISS": "https://www.iss.europa.eu/rss",
}

# Security-relevant keywords to filter general feeds
EUROPE_KEYWORDS = [
    # Core topics
    "security", "seguridad", "organized crime", "crimen organizado",
    "drug trafficking", "narcotráfico", "narcotics", "cocaine", "fentanyl",
    "drug policy", "política de drogas", "illicit", "trafficking",
    "transnational crime", "money laundering", "blanqueo",
    "mafia", "cartel", "gang", "criminal network",
    # Enforcement & policy
    "europol", "interpol", "police", "policía", "law enforcement",
    "border", "frontera", "smuggling", "contrabando",
    "terrorism", "terrorismo", "radicalization", "radicalización",
    "cybercrime", "ciberdelincuencia", "fraud", "corruption", "corrupción",
    # Geopolitical security
    "arms trafficking", "weapons", "conflict", "sanctions",
    "migration", "migración", "asylum", "refugee",
    "maritime security", "port", "puerto",
    # Drug policy reform
    "harm reduction", "reducción de daños", "decriminalization",
    "regulation", "cannabis", "synthetic drugs", "drogas sintéticas",
]

# ── Spain Security: Media & Institutions ──────────────────────────────────────

FEEDS_SPAIN = {
    # National media - security/justice sections
    "El País (España)": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada",
    "El Confidencial": "https://rss.elconfidencial.com/espana/",
    "El Mundo": "https://e00-elmundo.uecdn.es/elmundo/rss/espana.xml",
    "eldiario.es": "https://www.eldiario.es/rss/politica/",
    # Think tanks
    "Real Instituto Elcano": "https://www.realinstitutoelcano.org/feed/",
    "CIDOB": "https://www.cidob.org/es/publicaciones/rss",
    "IEEE": "https://www.ieee.es/rss/",
}

# Keywords to filter Spanish media for security-relevant content
SPAIN_KEYWORDS = [
    # Crime & security
    "narcotráfico", "droga", "cocaína", "hachís", "alijo",
    "crimen organizado", "banda", "mafia", "clan",
    "blanqueo", "lavado de dinero", "corrupción",
    "detención", "detenido", "operación policial", "redada",
    "guardia civil", "policía nacional", "CNP", "CNI",
    "terrorismo", "yihadismo", "ETA",
    "trata de personas", "tráfico de personas", "inmigración irregular",
    "seguridad", "interior", "marlaska",
    # Ports & routes
    "algeciras", "campo de gibraltar", "estrecho",
    "puerto", "contenedor", "decomiso", "incautación",
    # Policy & reform
    "código penal", "ley de seguridad", "reforma penal",
    "prisión", "cárcel", "penitenciario",
    # International connections
    "marruecos", "colombia", "méxico", "latinoamérica",
    "europol", "eurojust",
]

# Tags for content classification
TAGS = [
    "narcotráfico", "crimen organizado", "política de drogas",
    "blanqueo", "corrupción", "terrorismo",
    "seguridad fronteriza", "migración", "trata de personas",
    "ciberseguridad", "seguridad marítima",
    "reforma penal", "políticas públicas",
    "cooperación internacional", "geopolítica",
    "informes y análisis", "datos y estadísticas",
    "derechos humanos", "reducción de daños",
]
