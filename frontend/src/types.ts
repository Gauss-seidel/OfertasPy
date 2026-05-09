export interface Oferta {
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
  diasSemana?: number[]
}

export type Categoria =
  | "supermercado"
  | "ropa"
  | "tecnologia"
  | "restaurante"
  | "viajes"
  | "salud"
  | "hogar"
  | "entretenimiento"
  | "otros"

export const CATEGORIAS: { value: Categoria; label: string }[] = [
  { value: "supermercado", label: "Supermercado" },
  { value: "ropa", label: "Ropa y Accesorios" },
  { value: "tecnologia", label: "Tecnología" },
  { value: "restaurante", label: "Restaurantes" },
  { value: "viajes", label: "Viajes" },
  { value: "salud", label: "Salud" },
  { value: "hogar", label: "Hogar" },
  { value: "entretenimiento", label: "Entretenimiento" },
  { value: "otros", label: "Otros" },
]

export const DIAS: { value: number; label: string; short: string }[] = [
  { value: 0, label: "Domingo", short: "Dom" },
  { value: 1, label: "Lunes", short: "Lun" },
  { value: 2, label: "Martes", short: "Mar" },
  { value: 3, label: "Miércoles", short: "Mié" },
  { value: 4, label: "Jueves", short: "Jue" },
  { value: 5, label: "Viernes", short: "Vie" },
  { value: 6, label: "Sábado", short: "Sáb" },
]
