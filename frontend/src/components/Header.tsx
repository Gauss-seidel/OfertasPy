import { useEffect, useRef } from "react"
import { animate, stagger, splitText } from "animejs"

const PARTICLE_COLORS = [
  "rgba(245, 158, 11, 0.35)",
  "rgba(255, 255, 255, 0.15)",
  "rgba(20, 184, 166, 0.25)",
  "rgba(251, 191, 36, 0.2)",
]

export default function Header() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return

    const title = el.querySelector("h1")
    if (!title) return

    const { chars } = splitText(title, { chars: true })
    chars.forEach((c) => c.classList.add("header-title-char"))

    const subtitle = el.querySelector("p")

    animate(chars, {
      translateY: [-10, 0],
      opacity: [0, 1],
      delay: stagger(40),
      duration: 300,
      easing: "easeOutQuad",
    })

    chars[0].classList.add("char-coin")
    animate(chars[0], {
      rotateY: [180, 360],
      scale: [1.4, 1],
      duration: 700,
      easing: "easeOutQuad",
      delay: 40,
    })

    if (subtitle) {
      animate(subtitle, {
        translateY: [12, 0],
        opacity: [0, 1],
        duration: 400,
        easing: "easeOutQuad",
        delay: 300,
      })
    }

    const bgEl = el.querySelector(".header-bg")
    if (!bgEl) return

    const particles: HTMLDivElement[] = []
    for (let i = 0; i < 10; i++) {
      const p = document.createElement("div")
      p.className = "header-particle"
      const size = 3 + Math.random() * 5
      p.style.width = `${size}px`
      p.style.height = `${size}px`
      p.style.left = `${5 + Math.random() * 90}%`
      p.style.top = `${20 + Math.random() * 60}%`
      p.style.background = PARTICLE_COLORS[i % PARTICLE_COLORS.length]
      bgEl.appendChild(p)
      particles.push(p)
    }

    particles.forEach((p) => {
      const duration = 10000 + Math.random() * 8000
      const distY = -(40 + Math.random() * 60)
      const distX = -20 + Math.random() * 40
      animate(p, {
        translateY: [0, distY],
        translateX: [0, distX],
        opacity: [0, 0.25, 0],
        scale: [0.5, 1.2, 0.5],
        duration,
        loop: true,
        delay: 500 + Math.random() * 6000,
        easing: "easeInOutSine",
      })
    })
  }, [])

  return (
    <header className="header" ref={ref}>
      <div className="header-bg" aria-hidden="true" />
      <div className="header-content">
        <h1>OfertasPy</h1>
        <p>
          Todas las mejores ofertas y descuentos de Paraguay en un solo lugar
        </p>
      </div>
    </header>
  )
}
