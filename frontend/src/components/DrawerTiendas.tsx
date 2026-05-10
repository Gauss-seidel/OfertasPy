import { useEffect, useRef } from "react"
import { animate, stagger } from "animejs"

interface DrawerTiendasProps {
  open: boolean
  titulo: string
  tiendas: string[]
  onClose: () => void
}

export default function DrawerTiendas({ open, titulo, tiendas, onClose }: DrawerTiendasProps) {
  const drawerRef = useRef<HTMLDivElement>(null)
  const overlayRef = useRef<HTMLDivElement>(null)
  const listRef = useRef<HTMLUListElement>(null)

  useEffect(() => {
    if (!open) return
    const overlay = overlayRef.current
    const drawer = drawerRef.current
    const list = listRef.current
    if (!overlay || !drawer) return

    animate(overlay, {
      opacity: [0, 1],
      duration: 300,
      easing: "easeOutQuad",
    })

    animate(drawer, {
      translateX: ["100%", "0%"],
      duration: 400,
      easing: "easeOutCubic",
    })

    if (list) {
      animate(list.querySelectorAll("li"), {
        translateX: [24, 0],
        opacity: [0, 1],
        delay: stagger(40),
        easing: "easeOutQuad",
        duration: 300,
      })
    }
  }, [open])

  function handleClose() {
    const overlay = overlayRef.current
    const drawer = drawerRef.current
    if (!overlay || !drawer) {
      onClose()
      return
    }
    animate(overlay, {
      opacity: [1, 0],
      duration: 200,
      easing: "easeOutQuad",
    })
    animate(drawer, {
      translateX: ["0%", "100%"],
      duration: 250,
      easing: "easeInCubic",
      complete: () => onClose(),
    })
  }

  if (!open) return null

  return (
    <div className="drawer-overlay" ref={overlayRef} onClick={handleClose}>
      <div className="drawer" ref={drawerRef} onClick={(e) => e.stopPropagation()}>
        <div className="drawer-header">
          <h3 className="drawer-title">{titulo}</h3>
          <button className="drawer-close" onClick={handleClose}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>
        <p className="drawer-count">{tiendas.length} tienda{tiendas.length !== 1 ? "s" : ""} adherida{tiendas.length !== 1 ? "s" : ""}</p>
        <ul className="drawer-list" ref={listRef}>
          {tiendas.map((t, i) => (
            <li key={i}>{t}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}
