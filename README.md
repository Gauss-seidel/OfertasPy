# OfertasPy

Dashboard estático que centraliza ofertas y descuentos de Paraguay — supermercados, bancos, tiendas, restaurantes y más.

```
┌──────────────────────────────────────────────┐
│               OfertasPy                       │
│   Todas las mejores ofertas de Paraguay       │
│          en un solo lugar                     │
├──────────────────────────────────────────────┤
│  Día: [Todos] [Dom] [Lun] [Mar] [Mié] [Jue] │
│  Categoría: [Todas] [Super] [Ropa] [Tecn]…   │
├──────────────────────────────────────────────┤
│  ┌────────────┐  ┌────────────┐  ┌──────────┐ │
│  │ Ueno Bank  │  │  Zara      │  │ McDonald's│ │
│  │  40% OFF   │  │  30% OFF   │  │   2x1     │ │
│  │ Superm.    │  │  Ropa      │  │ Hamburg.  │ │
│  └────────────┘  └────────────┘  └──────────┘ │
│  ┌────────────┐  ┌────────────┐  ┌──────────┐ │
│  │   Eko      │  │ Cinemark   │  │ Bancard   │ │
│  │  20% OFF   │  │   3x2      │  │  10% cash│ │
│  │ Farmatotal │  │  Cine      │  │  Online   │ │
│  │ (Martes)   │  │ (Miércoles)│  │           │ │
│  └────────────┘  └────────────┘  └──────────┘ │
├──────────────────────────────────────────────┤
│  Desarrollado por Willian Nuñez © 2026        │
│  [GitHub] [LinkedIn] [WhatsApp]               │
└──────────────────────────────────────────────┘
```

## Stack

| Capa | Tecnología |
|---|---|
| Frontend | Vite + React 19 + TypeScript |
| Animaciones | animejs v4 (splitText, stagger, timeline) |
| Backend | Python (requests + beautifulsoup4) |
| Deploy | Render (static site) |
| CI | GitHub Actions (scrapers cada 6h) |

## Características

- **Filtro por categoría** — supermercado, ropa, tecnología, etc.
- **Filtro por día** — seleccioná un día y mostrá solo las ofertas que aplican ese día
- **Animaciones suaves** — entrada escalonada al scrollear, hover en cards, header con letras animadas
- **Modo oscuro automático** — respeta `prefers-color-scheme`
- **Responsive** — mobile, tablet, desktop
- **Accesible** — `prefers-reduced-motion` desactiva animaciones

## Desarrollo local

```bash
# Frontend
cd frontend
npm install
npm run dev              # http://localhost:5173

# Build producción
npm run build            # → frontend/dist/
npm run preview          # Previsualizar build
```

## Datos

Las ofertas están en `frontend/src/data/ofertas.json` (mock). Para actualizar:

```bash
# 1. Correr scrapers
python backend/run.py

# 2. Copiar resultado al frontend
cp backend/data/ofertas.json frontend/src/data/ofertas.json

# 3. Rebuild
cd frontend && npm run build
```

O automáticamente cada 6 horas via GitHub Actions (`.github/workflows/scrape.yml`).

## Desplegar en Render

| Configuración | Valor |
|---|---|
| Root Directory | `frontend` |
| Build Command | `npm install && npm run build` |
| Publish Directory | `frontend/dist` |

Conectar repo de GitHub y Render hace deploy automático en cada push.

## Estructura del proyecto

```
OfertasPy/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.tsx       # Título animado + partículas
│   │   │   ├── Dashboard.tsx    # Grid + filtros + contador
│   │   │   ├── OfertaCard.tsx   # Card individual
│   │   │   ├── Filtros.tsx      # Filtro por categoría
│   │   │   ├── SelectorDia.tsx  # Filtro por día de semana
│   │   │   └── Footer.tsx       # Créditos + contacto
│   │   ├── data/ofertas.json
│   │   ├── types.ts
│   │   └── index.html
│   └── package.json
├── backend/
│   ├── scrapers/
│   │   ├── base.py
│   │   └── ueno.py
│   ├── data/ofertas.json
│   ├── run.py
│   └── requirements.txt
├── .github/workflows/scrape.yml
└── .gitignore
```

## Licencia

MIT
