import { useRef, useEffect, useState } from "react"
import { animate } from "animejs"
import type { Oferta } from "../types"
import { CATEGORIAS, DIAS } from "../types"
import DrawerTiendas from "./DrawerTiendas"

interface OfertaCardProps {
  oferta: Oferta
  index: number
}

function CalendarIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
      <line x1="16" y1="2" x2="16" y2="6" />
      <line x1="8" y1="2" x2="8" y2="6" />
      <line x1="3" y1="10" x2="21" y2="10" />
    </svg>
  )
}

function formatDate(s: string) {
  const d = new Date(s)
  return d.toLocaleDateString("es-PY", { day: "numeric", month: "short" })
}

function formatDias(dias: number[]): string {
  const labels = dias.map((d) => DIAS.find((d2) => d2.value === d)?.label ?? "")
  if (labels.length === 7) return "Todos los días"
  if (labels.length <= 2) return labels.join(" y ")
  return labels.join(", ")
}

function playEntrance(el: HTMLElement, index: number) {
  animate(el, {
    translateY: [24, 0],
    opacity: [0, 1],
    delay: index * 60,
    easing: "easeOutQuad",
    duration: 500,
  })
}

export default function OfertaCard({ oferta, index }: OfertaCardProps) {
  const ref = useRef<HTMLDivElement>(null)
  const [drawerOpen, setDrawerOpen] = useState(false)

  useEffect(() => {
    const el = ref.current
    if (!el) return

    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          playEntrance(el, index)
          obs.unobserve(el)
        }
      },
      { threshold: 0.05 }
    )

    obs.observe(el)
    return () => obs.disconnect()
  }, [index])

  const catLabel = CATEGORIAS.find((c) => c.value === oferta.categoria)?.label ?? oferta.categoria

  return (
    <>
    <DrawerTiendas
      open={drawerOpen}
      titulo={oferta.titulo}
      tiendas={oferta.tiendas ?? []}
      onClose={() => setDrawerOpen(false)}
    />
    <div className="oferta-card" ref={ref}>
      <div className="card-header">
        <span className="card-tienda">{oferta.tienda}</span>
        <span className="descuento-badge">{oferta.descuento}</span>
      </div>
      <h3 className="card-title">{oferta.titulo}</h3>
      <p className="card-desc">{oferta.descripcion}</p>
      <div className="card-footer">
        <span className="card-tag">{catLabel}</span>
        {oferta.medioPago && (
          <span className="card-tag pago">{oferta.medioPago}</span>
        )}
        {oferta.diasSemana && oferta.diasSemana.length > 0 && (
          <span className="card-tag dias">
            {formatDias(oferta.diasSemana)}
          </span>
        )}
        {oferta.fechaFin && (
          <span className="card-tag fecha">
            <CalendarIcon />
            Hasta {formatDate(oferta.fechaFin)}
          </span>
        )}
      </div>
      {oferta.tiendas && oferta.tiendas.length > 0 && (
        <button className="btn-tiendas" onClick={() => setDrawerOpen(true)}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="14" height="14">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
            <polyline points="9 22 9 12 15 12 15 22" />
          </svg>
          Ver {oferta.tiendas.length} tienda{oferta.tiendas.length !== 1 ? "s" : ""} adherida{oferta.tiendas.length !== 1 ? "s" : ""}
        </button>
      )}
    </div>
    </>
  )
}
