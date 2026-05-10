# AGENTS.md — OfertasPy

Dashboard estático de ofertas y descuentos en Paraguay. Frontend Vite + React + TS con animejs v4. Backend Python para scraping. Deploy en Render. **103 ofertas** de 14 fuentes + PDFs.

## Estructura

```
OfertasPy/
├── frontend/          # Vite + React + TypeScript
│   ├── src/
│   │   ├── components/  # Header, Dashboard, OfertaCard, DrawerTiendas, Filtros, SelectorDia, Footer
│   │   ├── data/
│   │   │   └── ofertas.json   # Datos que consume la app (103 ofertas)
│   │   ├── types.ts       # Oferta con tiendas?: string[]
│   │   ├── App.tsx
│   │   └── App.css        # Incluye estilos del drawer tiendas
│   └── index.html
├── backend/           # Python scrapers
│   ├── scrapers/       # Uno por fuente + urls.py + pdf_scraper.py
│   ├── data/
│   │   ├── ofertas.json
│   │   └── pdfs/       # Subcarpetas por fuente (basa/, continental/, ueno/)
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
python backend/run.py  # Ejecuta scrapers → backend/data/ofertas.json (103 ofertas)
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
| `OfertaCard` | IntersectionObserver → stagger entrance al hacer scroll + botón "Ver tiendas" |
| `DrawerTiendas` | Overlay fadeIn + drawer slide desde derecha + stagger en lista |
| `Dashboard` | grid remount con fadeIn al filtrar, contador count-up |
| `Footer` | toggle expandible con stagger en enlaces |

## Tipos

```ts
interface Oferta {
  id: string
  titulo: string
  descripcion: string
  descuento: string
  tienda: string
  categoria: Categoria
  medioPago?: string
  fechaInicio?: string
  fechaFin?: string
  source: string
  logo?: string
  diasSemana?: number[]      // 0=Dom…6=Sáb
  tiendas?: string[]         // Lista de locales adheridos (PDF Basa)
}
```

## Notas

- `diasSemana: number[]` (0=Dom…6=Sáb) en el JSON: si no se incluye la oferta aplica todos los días.
- Al filtrar por día solo aparecen ofertas que tengan ese día explicitamente en `diasSemana`.
- `tiendas: string[]` contiene la lista de locales adheridos para ofertas de categoría (ej: todos los supermercados con 25% los jueves). Se muestra en un drawer lateral.
- `prefers-reduced-motion` desactiva animaciones globalmente via CSS.
- Favicon: moneda SVG con `%` en `public/favicon.svg`.
- Las URLs de scraping se centralizan en `backend/scrapers/urls.py`. Editar solo ahí cuando un banco cambie su web.
- Los PDFs de ofertas van en `backend/data/pdfs/<fuente>/`. `PdfScraper` los parsea automáticamente (requiere pymupdf).
- PDF Basa se parsea por secciones (22 ofertas con tiendas). PDFs Continental y Ueno tienen baja calidad de texto → se filtran automáticamente.
- `run.py` filtra valores `None` y arrays vacíos (`[]`) del JSON output.
- Atlas (22), Familiar (24) y PDF Basa (22) generan la mayoría de las ofertas. El resto son datos hardcoded de fallback.
