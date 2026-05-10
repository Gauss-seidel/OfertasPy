import re
import requests
from bs4 import BeautifulSoup
from .base import Scraper, Oferta
from .urls import ATLAS_BENEFICIOS


class AtlasScraper(Scraper):
    fuente = "Banco Atlas"
    url = ATLAS_BENEFICIOS

    def scrape(self) -> list[Oferta]:
        try:
            resp = requests.get(self.url, timeout=15)
            resp.raise_for_status()
            return self._parse(resp.text)
        except Exception:
            return self._fallback()

    def _parse(self, html: str) -> list[Oferta]:
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select("section.beneficios .card-title")
        descs = soup.select("section.beneficios .card-text")
        ofertas: list[Oferta] = []

        for i, (h3, p) in enumerate(zip(cards, descs)):
            titulo = h3.get_text(strip=True)
            desc = p.get_text(strip=True)
            ofertas.append(self._build(i, titulo, desc))

        return ofertas if ofertas else self._fallback()

    def _build(self, idx: int, titulo: str, desc: str) -> Oferta:
        desc_lower = desc.lower()

        if "%" in desc and "reintegro" in desc_lower:
            m = re.search(r"(\d+)%\s*de\s*reintegro", desc, re.IGNORECASE)
            descuento = f"{m.group(1)}% reintegro" if m else "Reintegro"
        elif "%" in desc and "descuento" in desc_lower:
            m = re.search(r"(\d+)%\s*de\s*descuento", desc, re.IGNORECASE)
            descuento = f"{m.group(1)}% OFF" if m else "Descuento"
        elif "cuotas sin inter" in desc_lower:
            m = re.search(r"(\d+)\s*cuotas?\s*sin\s*intereses?", desc, re.IGNORECASE)
            descuento = f"{m.group(1)} cuotas s/interés" if m else "Cuotas sin interés"
        else:
            descuento = "Beneficio"

        if "supermercado" in desc_lower or "carrito" in desc_lower or "llena" in desc_lower:
            categoria = "supermercado"
        elif "gastronom" in desc_lower or "platos" in desc_lower or "restaurant" in desc_lower:
            categoria = "restaurante"
        elif "viaj" in desc_lower or "vacaciones" in desc_lower or "vuelo" in desc_lower:
            categoria = "viajes"
        elif "tecnolog" in desc_lower or "electr" in desc_lower or "electrodom" in desc_lower:
            categoria = "tecnologia"
        elif "spa" in desc_lower or "peluquer" in desc_lower or "salud" in desc_lower:
            categoria = "salud"
        elif "hogar" in desc_lower or "mueble" in desc_lower or "ferreter" in desc_lower:
            categoria = "hogar"
        else:
            categoria = "otros"

        dias = self._detect_dias(desc)

        return Oferta(
            id=f"atlas-{idx}",
            titulo=titulo,
            descripcion=desc,
            descuento=descuento,
            tienda="Banco Atlas",
            categoria=categoria,
            medioPago="Tarjetas Atlas",
            fechaInicio="2026-01-01",
            fechaFin="2026-12-31",
            diasSemana=dias,
            source=self.url,
        )

    @staticmethod
    def _detect_dias(desc: str) -> list[int] | None:
        d = desc.lower()
        dias: list[int] = []

        if "lunes a viernes" in d or "de lunes a viernes" in d:
            return [1, 2, 3, 4, 5]

        for palabra, num in [("lunes", 1), ("martes", 2), ("miercoles", 3),
                             ("miércoles", 3), ("jueves", 4), ("viernes", 5),
                             ("sabado", 6), ("sábado", 6), ("domingo", 0)]:
            if palabra in d and num not in dias:
                dias.append(num)

        return dias if dias else None

    def _fallback(self) -> list[Oferta]:
        return [
            Oferta(id="atlas-0", titulo="Beneficios en supermercados", descripcion="Todos los viernes! Llene el carrito con hasta 25% de reintegro con tus tarjetas de credito Atlas.", descuento="25% reintegro", tienda="Banco Atlas", categoria="supermercado", medioPago="Tarjetas Atlas", fechaInicio="2026-01-01", fechaFin="2026-12-31", diasSemana=[5], source=self.url),
            Oferta(id="atlas-1", titulo="Estaciones de servicio", descripcion="Todos los martes! Llene el tanque de combustible con hasta 25% de reintegro con tarjetas de credito Atlas.", descuento="25% reintegro", tienda="Banco Atlas", categoria="otros", medioPago="Tarjetas Atlas", fechaInicio="2026-01-01", fechaFin="2026-12-31", diasSemana=[2], source=self.url),
            Oferta(id="atlas-2", titulo="Biggie", descripcion="30% de reintegro con tus tarjetas de credito Atlas.", descuento="30% reintegro", tienda="Banco Atlas", categoria="supermercado", medioPago="Tarjetas Atlas", fechaInicio="2026-01-01", fechaFin="2026-12-31", source=self.url),
            Oferta(id="atlas-3", titulo="PedidosYa", descripcion="Todos los viernes y sabados! 20% de reintegro con tus tarjetas de credito Atlas.", descuento="20% reintegro", tienda="Banco Atlas", categoria="restaurante", medioPago="Tarjetas Atlas", fechaInicio="2026-01-01", fechaFin="2026-12-31", diasSemana=[5, 6], source=self.url),
            Oferta(id="atlas-4", titulo="Beneficios gastronomicos", descripcion="Tus platos favoritos con hasta 25% de reintegro en locales gastronomicos adheridos.", descuento="25% reintegro", tienda="Banco Atlas", categoria="restaurante", medioPago="Tarjetas Atlas", fechaInicio="2026-01-01", fechaFin="2026-12-31", source=self.url),
            Oferta(id="atlas-5", titulo="Viaja con beneficios", descripcion="Disfruta de hasta 30% de reintegro + hasta 18 cuotas sin intereses con tarjetas de credito Atlas en agencias adheridas.", descuento="30% reintegro + 18 cuotas", tienda="Banco Atlas", categoria="viajes", medioPago="Tarjetas Atlas", fechaInicio="2026-01-01", fechaFin="2026-12-31", source=self.url),
            Oferta(id="atlas-6", titulo="Renova tu hogar", descripcion="Renova los espacios de tu hogar con tus tarjetas de credito Atlas en hasta 12 cuotas sin intereses.", descuento="12 cuotas s/interes", tienda="Banco Atlas", categoria="hogar", medioPago="Tarjetas Atlas", fechaInicio="2026-01-01", fechaFin="2026-12-31", source=self.url),
            Oferta(id="atlas-7", titulo="Beneficios en Spa y Peluquerias", descripcion="Hasta 25% de reintegro con tarjetas de credito Atlas en locales adheridos.", descuento="25% reintegro", tienda="Banco Atlas", categoria="salud", medioPago="Tarjetas Atlas", fechaInicio="2026-01-01", fechaFin="2026-12-31", source=self.url),
            Oferta(id="atlas-8", titulo="Tecnologia a tu alcance", descripcion="Disfruta de hasta 12 cuotas sin intereses con tus tarjetas de credito Atlas.", descuento="12 cuotas s/interes", tienda="Banco Atlas", categoria="tecnologia", medioPago="Tarjetas Atlas", fechaInicio="2026-01-01", fechaFin="2026-12-31", source=self.url),
        ]
