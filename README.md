# L30N4RD018.github.io

Página personal de Leonardo Mendoza (backend y datos, Python) y, en una subcarpeta, el sitio que
respalda la aplicación OAuth **JobsTracker** en Google Cloud.

| Archivo | URL | Para qué |
|---|---|---|
| `index.html` | `/` | Página personal (ES/EN). Conserva la etiqueta `google-site-verification` de Search Console: **no quitarla** |
| `jobstracker/index.html` | `/jobstracker/` | Página principal de la aplicación JobsTracker |
| `privacidad.html` | `/privacidad.html` | Política de Privacidad de JobsTracker |
| `condiciones.html` | `/condiciones.html` | Condiciones del Servicio de JobsTracker |
| `img/` | | Capturas de los proyectos (WebP) |
| `js/mapa.js` | | Datos del mapa de la portada: sedes del REPS público por municipio (datos.gov.co `c36g-9fc2`), coordenadas DIVIPOLA (`gdxc-w37w`) y contorno de Natural Earth |
| `herramientas/generar_mapa.py` | | Regenera `js/mapa.js` a partir de esas tres descargas |

Sin frameworks. Únicas dependencias externas: las fuentes Inter y JetBrains Mono de Google Fonts. El idioma se elige con el botón ES/EN y se recuerda en el navegador.
