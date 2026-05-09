# AGENTS.md — OfertasPy

Dashboard estático de ofertas y descuentos en Paraguay. Frontend Vite + React + TS con animejs v4. Backend Python para scraping. Deploy en Render.

## Estructura

```
OfertasPy/
├── frontend/          # Vite + React + TypeScript
│   ├── src/
│   │   ├── components/  # Header, Dashboard, OfertaCard, Filtros, SelectorDia, Footer
│   │   ├── data/
│   │   │   └── ofertas.json   # Datos que consume la app
│   │   ├── types.ts
│   │   ├── App.tsx
│   │   └── App.css
│   └── index.html
├── backend/           # Python scrapers
│   ├── scrapers/       # Uno por fuente (base.py, ueno.py, ...)
│   ├── data/ofertas.json
│   ├── run.py          # Orquesta todos los scrapers
│   └── requirements.txt
├── .github/workflows/scrape.yml   # CI: corre scrapers cada 6h
└── .gitignore
```

## Comandos

```bash
# frontend
cd frontend
npm run dev            # Dev server
npm run build          # Build estático → frontend/dist/
npm run preview        # Previsualizar build
npm run lint           # ESLint

# backend
python backend/run.py  # Ejecuta scrapers → backend/data/ofertas.json
```

## Flujo de datos

```
Python scrapers → backend/data/ofertas.json → se copia a frontend/src/data/ → npm run build → dist/
```

- **Local**: correr `python backend/run.py`, copiar JSON a `frontend/src/data/`, build.
- **Auto (CI)**: GitHub Actions corre los scrapers cada 6h y commitea el JSON nuevo → Render rebuild automático.

## Deploy (Render)

| Campo | Valor |
|---|---|
| Root Directory | `frontend` |
| Build Command | `npm install && npm run build` |
| Publish Directory | `frontend/dist` |
| Auto-Deploy | Yes |

## animejs v4

No tiene default export. Usar named exports:

```ts
import { animate, stagger, splitText } from 'animejs'

// Texto dividido en caracteres
const { chars } = splitText(h1, { chars: true })

// Stagger entrance
animate('.cards', {
  translateY: [24, 0],
  opacity: [0, 1],
  delay: stagger(60),
  easing: 'easeOutQuad',
  duration: 500,
})
```

## Componentes

| Componente | Animación |
|---|---|
| `Header` | splitText en h1, letras stagger, "O" gira como moneda, gradiente animado + partículas flotantes |
| `OfertaCard` | IntersectionObserver → stagger entrance al hacer scroll |
| `Dashboard` | grid remount con fadeIn al filtrar, contador count-up |
| `Footer` | toggle expandible con stagger en enlaces |

## Notas

- `diasSemana: number[]` (0=Dom…6=Sáb) en el JSON: si no se incluye la oferta aplica todos los días.
- Las ofertas mock en `ofertas.json` son de ejemplo. Reemplazar con scrapers reales.
- `prefers-reduced-motion` desactiva animaciones globalmente via CSS.
- Favicon: moneda SVG con `%` en `public/favicon.svg`.
