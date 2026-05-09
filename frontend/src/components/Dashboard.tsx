import { useState, useMemo, useRef, useEffect } from "react"
import type { Categoria, Oferta } from "../types"
import Filtros from "./Filtros"
import SelectorDia from "./SelectorDia"
import OfertaCard from "./OfertaCard"
import ofertasData from "../data/ofertas.json"

function animateCount(el: HTMLElement, from: number, to: number, duration: number) {
  const start = performance.now()
  function tick(now: number) {
    const t = Math.min((now - start) / duration, 1)
    const ease = 1 - (1 - t) * (1 - t)
    el.textContent = Math.round(from + (to - from) * ease).toString()
    if (t < 1) requestAnimationFrame(tick)
  }
  requestAnimationFrame(tick)
}

function OfertasCount({ total }: { total: number }) {
  const ref = useRef<HTMLSpanElement>(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return
    animateCount(el, 0, total, 400)
  }, [total])

  return (
    <p className="ofertas-count">
      <span ref={ref}>0</span> ofertas disponibles
    </p>
  )
}

export default function Dashboard() {
  const [activeCategoria, setActiveCategoria] = useState<Categoria | null>(null)
  const [activeDia, setActiveDia] = useState<number | null>(null)

  const ofertas = ofertasData as Oferta[]

  const filtradas = useMemo(() => {
    let r: Oferta[] = ofertas
    if (activeCategoria) {
      r = r.filter((o) => o.categoria === activeCategoria)
    }
    if (activeDia !== null) {
      r = r.filter((o) => !o.diasSemana || o.diasSemana.includes(activeDia))
    }
    return r
  }, [activeCategoria, activeDia])

  const filterKey = `${activeCategoria ?? "all"}-${activeDia ?? "all"}`

  return (
    <>
      <SelectorDia value={activeDia} onChange={setActiveDia} />
      <Filtros active={activeCategoria} onChange={setActiveCategoria} />
      {filtradas.length === 0 ? (
        <div className="empty-state" key={filterKey}>
          <h3>Sin resultados</h3>
          <p>No hay ofertas para esta combinación.</p>
        </div>
      ) : (
        <div key={filterKey} className="dashboard-grid-wrapper">
          <OfertasCount total={filtradas.length} />
          <div className="dashboard-grid">
            {filtradas.map((o, i) => (
              <OfertaCard key={o.id} oferta={o} index={i} />
            ))}
          </div>
        </div>
      )}
    </>
  )
}
