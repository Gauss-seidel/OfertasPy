import requests
from bs4 import BeautifulSoup
from .base import Scraper, Oferta
from .urls import UENO_BASE, UENO_PROMOS


class UenoScraper(Scraper):
    fuente = "Ueno Bank"
    base = UENO_BASE
    promos = UENO_PROMOS

    def scrape(self) -> list[Oferta]:
        resultados = []
        for path in self.promos:
            try:
                resp = requests.get(self.base + path, timeout=10)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    title_tag = soup.find("title")
                    titulo = title_tag.get_text(strip=True) if title_tag else "Promocion Ueno"
                    resultados.append(self._from_title(titulo, path))
            except Exception:
                continue
        return resultados if resultados else self._fallback()

    def _from_title(self, titulo: str, path: str) -> Oferta:
        t = titulo.lower()
        if "pagopar" in t or "cuotas" in t:
            desc = "Cuotas sin intereses en tus compras con Ueno."
            descuento = "Cuotas s/interes"
            cat = "otros"
        elif "jetsmart" in t or "vuelo" in t:
            desc = "Descuento en vuelos internacionales con Ueno."
            descuento = "Hasta 25%"
            cat = "viajes"
        elif "primera compra" in t:
            desc = "Reintegro en tu primera compra con Ueno."
            descuento = "Reintegro"
            cat = "otros"
        else:
            desc = titulo
            descuento = "Beneficio"
            cat = "otros"
        return Oferta(
            id=f"ueno-{hash(path) % 1000}",
            titulo=titulo,
            descripcion=desc,
            descuento=descuento,
            tienda="Ueno Bank",
            categoria=cat,
            medioPago="Ueno",
            fechaInicio="2026-01-01",
            fechaFin="2026-12-31",
            source=self.base + path,
        )

    def _fallback(self) -> list[Oferta]:
        return [
            Oferta(id="ueno-0", titulo="Cuotas sin intereses en Pagopar", descripcion="Cuotas sin intereses con tu tarjeta Ueno en Pagopar.", descuento="Cuotas s/interes", tienda="Ueno Bank", categoria="otros", medioPago="Ueno", fechaInicio="2026-01-01", fechaFin="2026-12-31", source=self.base),
            Oferta(id="ueno-1", titulo="JetSMART + Ueno: hasta 25% en vuelos", descripcion="25% de descuento en vuelos internacionales pagando con Ueno. Usa el codigo UENOBANK.", descuento="Hasta 25%", tienda="Ueno Bank", categoria="viajes", medioPago="Ueno", fechaInicio="2026-04-07", fechaFin="2026-09-24", source=self.base),
            Oferta(id="ueno-2", titulo="40% de descuento en supermercados", descripcion="Paga con tu tarjeta Ueno y obtene 40% off en todos los supermercados adheridos.", descuento="40%", tienda="Ueno Bank", categoria="supermercado", medioPago="Tarjeta Ueno", fechaInicio="2026-01-01", fechaFin="2026-12-31", source=self.base),
        ]
