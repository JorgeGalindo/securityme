# securityme

Monitor diario de seguridad, crimen organizado y política de drogas para **Catalina Gil Pinzón** — consultora de políticas de seguridad y desarrollo, miembro de GI-TOC y consultora de Open Society Foundations (Drug Policy Program).

Sitio estático generado diariamente por GitHub Actions y desplegado en GitHub Pages.

---

## Qué es

Dos monitores curados por Claude a partir de RSS de think tanks, agencias y medios:

- **Europa** — Informes y noticias de seguridad a nivel europeo (GI-TOC, OCCRP, Europol, EMCDDA, RUSI, Crisis Group, etc.)
- **España** — Noticias de seguridad en España (narcotráfico, crimen organizado, política penal) + think tanks nacionales (Elcano, CIDOB, IEEE)

Incluye un **briefing de audio** diario (~4 min) que sintetiza ambos monitores.

## Arquitectura

```
GitHub Actions (cron 3:00 UTC)
  → fetch.py: descarga RSS de ~25 fuentes
  → curate.py: Claude filtra y analiza (15 Europa + 10 España + audio)
  → build.py: renderiza HTML estático con Jinja2
  → deploy: push a /docs → GitHub Pages sirve el sitio
```

No hay servidor. Todo es estático.

## Fuentes

### Europa (think tanks, agencias, watchdogs)
| Fuente | Tipo |
|--------|------|
| GI-TOC | Think tank — crimen organizado transnacional |
| OCCRP | Periodismo de investigación — corrupción y crimen |
| InSight Crime | Crimen organizado en las Américas |
| RUSI | Think tank — seguridad y defensa |
| Chatham House | Think tank — política internacional |
| Carnegie Europe | Think tank — Europa |
| ECFR | Think tank — política exterior europea |
| IISS | Think tank — seguridad estratégica |
| SIPRI | Instituto — paz y conflictos |
| Crisis Group | Análisis de conflictos |
| Clingendael | Think tank — seguridad holandés/europeo |
| TNI | Think tank — política de drogas |
| IDPC | Consorcio — política de drogas |
| Brookings | Think tank — políticas públicas |
| CEPS | Think tank — política europea |
| EMCDDA/EUDA | Agencia UE — drogas |
| Europol | Agencia UE — policía |
| EUISS | Instituto UE — seguridad |

### España (medios + think tanks)
| Fuente | Tipo |
|--------|------|
| El País | Prensa — sección España |
| El Confidencial | Prensa — investigación |
| El Mundo | Prensa — España |
| eldiario.es | Prensa — política |
| Real Instituto Elcano | Think tank — relaciones internacionales |
| CIDOB | Think tank — Barcelona |
| IEEE | Instituto — estudios estratégicos |

## Stack

- Python 3.13, Jinja2
- Anthropic Claude Sonnet (curación + briefing)
- edge-tts (audio, voz es-ES-ElviraNeural)
- GitHub Actions (cron) + GitHub Pages (hosting)

## Coste estimado

- Claude API: ~$0.10-0.20/día
- edge-tts: gratis
- GitHub Pages: gratis
- **Total: ~$3-6/mes**

---

## Plan de acción

### Fase 1 — MVP (ahora)
- [x] Clon adaptado del proyecto readerme
- [x] Fuentes RSS de think tanks y agencias de seguridad europeas
- [x] Fuentes RSS de medios y think tanks españoles
- [x] Prompts adaptados a seguridad/crimen organizado/política de drogas
- [x] Perfil de Catalina integrado en los prompts
- [x] Sistema de tags de seguridad
- [x] Filtro por keywords de seguridad para fuentes generalistas
- [x] Audio briefing con voz femenina (ElviraNeural)
- [x] Build estático con Jinja2 (no Flask)
- [x] GitHub Actions workflow
- [x] Eliminados: gráficos, encuestas, mercados de predicción, feedback, Readwise, DuckDuckGo, share text, Substack

### Fase 2 — Validar fuentes
- [ ] Crear repo en GitHub, configurar `ANTHROPIC_API_KEY` en secrets
- [ ] Ejecutar `python run.py` localmente para verificar qué fuentes funcionan
- [ ] Ajustar/reemplazar RSS que fallen (algunos think tanks no tienen RSS público)
- [ ] Verificar que el filtro por keywords no es demasiado restrictivo ni demasiado laxo
- [ ] Configurar GitHub Pages (Settings > Pages > Source: branch main, folder /docs)

### Fase 3 — Ajustar curación
- [ ] Revisar con Catalina la primera salida: ¿los artículos son relevantes?
- [ ] Ajustar keywords en `sources.py` según feedback
- [ ] Ajustar prompts en `curate.py` si el análisis no tiene el tono correcto
- [ ] Considerar añadir más fuentes especializadas (UNODC, FATF/GAFI, etc.)
- [ ] Considerar sección separada para informes largos vs noticias

### Fase 4 — Mejoras opcionales
- [ ] Búsqueda web (DuckDuckGo) para complementar RSS con informes recientes
- [ ] Sección "alertas" para noticias de alta relevancia
- [ ] Newsletter por email (GitHub Actions + servicio de email)
- [ ] RSS propio del monitor (para que Catalina lo meta en su lector)
- [ ] Voz personalizada o cambio de voz
