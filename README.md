# OfertasPy

Dashboard estático que centraliza ofertas y descuentos de Paraguay — supermercados, bancos, tiendas, restaurantes y más. **103 ofertas** de 14 fuentes + PDFs.

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
│  │ Ueno Bank  │  │ Supermerc  │  │Gastronom │ │
│  │  40% OFF   │  │  Hasta 25% │  │ 2x1 chipa│ │
│  │ Ver 3 tien │  │ Ver 8 tien │  │ Ver 1 tien│ │
│  └────────────┘  └────────────┘  └──────────┘ │
│  ┌────────────┐  ┌────────────┐  ┌──────────┐ │
│  │   Eko      │  │ Automóvil  │  │  Salud   │ │
│  │  20% OFF   │  │  Hasta 25% │  │ Hasta 60%│ │
│  │ Farmatotal │  │ Ver 10 tie │  │Ver 33 tie│ │
│  │ (Martes)   │  │            │  │           │ │
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
| Backend | Python (requests + beautifulsoup4 + pymupdf) |
| Deploy | Render (static site) |
| CI | GitHub Actions (scrapers cada 6h) |

## Características

- **Filtro por categoría** — supermercado, ropa, tecnología, etc.
- **Filtro por día** — seleccioná un día y mostrá solo las ofertas que aplican ese día
- **Ver tiendas adheridas** — drawer lateral con lista completa de locales por categoría
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

Las ofertas se generan con scrapers Python. Para actualizar:

```bash
# 1. Correr scrapers (14 bancos + PDFs)
python backend/run.py

# 2. Copiar resultado al frontend
cp backend/data/ofertas.json frontend/src/data/ofertas.json

# 3. Rebuild
cd frontend && npm run build
```

O automáticamente cada 6 horas via GitHub Actions (`.github/workflows/scrape.yml`).

### Fuentes incluidas

| Fuente | Tipo | Ofertas |
|---|---|---|
| Banco Atlas | HTML parse | 22 |
| Banco Familiar | HTML parse (filtrado) | 24 |
| PDFs (Basa) | PDF section parse | 22 |
| Eko | Hardcoded | 7 |
| BBVA Paraguay | Hardcoded | 6 |
| Banco Continental | Hardcoded | 4 |
| Superseis | Hardcoded | 3 |
| Cooperativa Universitaria | Hardcoded | 2 |
| GNB Paraguay | Hardcoded | 2 |
| Banco Sudameris | Hardcoded | 2 |
| Banco Visión | Hardcoded | 2 |
| Banco Regional | Hardcoded | 2 |
| Itaú Paraguay | Hardcoded | 2 |
| Banco Basa | Hardcoded | 2 |
| Ueno Bank | Hardcoded | 1 |

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
│   │   │   ├── Header.tsx         # Título animado + partículas
│   │   │   ├── Dashboard.tsx      # Grid + filtros + contador
│   │   │   ├── OfertaCard.tsx     # Card individual + botón tiendas
│   │   │   ├── DrawerTiendas.tsx  # Drawer lateral con lista de tiendas
│   │   │   ├── Filtros.tsx        # Filtro por categoría
│   │   │   ├── SelectorDia.tsx    # Filtro por día de semana
│   │   │   └── Footer.tsx         # Créditos + contacto
│   │   ├── data/ofertas.json
│   │   ├── types.ts               # Oferta interface con tiendas[]
│   │   └── App.css                # Estilos + drawer
│   └── package.json
├── backend/
│   ├── scrapers/
│   │   ├── base.py                # Oferta dataclass con tiendas[]
│   │   ├── pdf_scraper.py         # Basa PDF section parser
│   │   ├── urls.py                # URLs centralizadas
│   │   └── (14 scrapers por fuente)
│   ├── data/
│   │   ├── ofertas.json
│   │   └── pdfs/                  # PDFs por fuente
│   ├── run.py
│   └── requirements.txt
├── .github/workflows/scrape.yml
└── .gitignore
```

## Licencia

MIT
