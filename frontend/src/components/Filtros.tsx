import type { Categoria } from "../types"
import { CATEGORIAS } from "../types"

interface FiltrosProps {
  active: Categoria | null
  onChange: (cat: Categoria | null) => void
}

export default function Filtros({ active, onChange }: FiltrosProps) {
  return (
    <div className="filtros">
      <button
        className={`filtro-btn ${active === null ? "active" : ""}`}
        onClick={() => onChange(null)}
      >
        Todas
      </button>
      {CATEGORIAS.map((c) => (
        <button
          key={c.value}
          className={`filtro-btn ${active === c.value ? "active" : ""}`}
          onClick={() => onChange(c.value)}
        >
          {c.label}
        </button>
      ))}
    </div>
  )
}
