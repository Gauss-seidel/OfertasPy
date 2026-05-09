import { DIAS } from "../types"

interface SelectorDiaProps {
  value: number | null
  onChange: (dia: number | null) => void
}

export default function SelectorDia({ value, onChange }: SelectorDiaProps) {
  return (
    <div className="selector-dia">
      <span className="selector-dia-label">Día:</span>
      <button
        className={`filtro-btn ${value === null ? "active" : ""}`}
        onClick={() => onChange(null)}
      >
        Todos
      </button>
      {DIAS.map((d) => (
        <button
          key={d.value}
          className={`filtro-btn ${value === d.value ? "active" : ""}`}
          onClick={() => onChange(d.value)}
          title={d.label}
        >
          {d.short}
        </button>
      ))}
    </div>
  )
}
