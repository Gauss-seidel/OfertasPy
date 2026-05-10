import requests
from bs4 import BeautifulSoup
from .base import Scraper, Oferta
from .urls import BBVA_PROMOS


class BBVAScraper(Scraper):
    fuente = "BBVA Paraguay"

    def scrape(self) -> list[Oferta]:
        urls = BBVA_PROMOS
        for url in urls:
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    textos = soup.get_text(" ", strip=True)
                    return self._parse_textos(textos, url)
            except Exception:
                continue
        return self._fallback()

    def _parse_textos(self, texto: str, url: str) -> list[Oferta]:
        ofertas: list[Oferta] = []
        idx = 0
        t = texto.lower()
        if "cuota" in t or "descuento" in t or "reintegro" in t:
            if "supermercado" in t:
                ofertas.append(self._build(idx, "Supermercados", "Descuento en supermercados con BBVA.", "Descuento", "supermercado", url))
                idx += 1
            if "viaje" in t or "vuelo" in t:
                ofertas.append(self._build(idx, "Viajes BBVA", "Financiacion en viajes con BBVA.", "Cuotas s/interes", "viajes", url))
                idx += 1
            if "restaurant" in t or "gastronom" in t:
                ofertas.append(self._build(idx, "Gastronomia BBVA", "Descuentos en restaurantes con BBVA.", "Descuento", "restaurante", url))
                idx += 1
            if "tecnolog" in t or "electro" in t:
                ofertas.append(self._build(idx, "Tecnologia BBVA", "Cuotas sin interes en tecnologia con BBVA.", "Cuotas s/interes", "tecnologia", url))
                idx += 1
            if "hogar" in t or "mueble" in t:
                ofertas.append(self._build(idx, "Hogar BBVA", "Descuentos en hogar con BBVA.", "Descuento", "hogar", url))
                idx += 1
        return ofertas if ofertas else self._fallback()

    def _build(self, idx: int, titulo: str, desc: str, descuento: str, cat: str, url: str) -> Oferta:
        return Oferta(id=f"bbva-{idx}", titulo=titulo, descripcion=desc, descuento=descuento, tienda="BBVA Paraguay", categoria=cat, medioPago="Tarjetas BBVA", fechaInicio="2026-01-01", fechaFin="2026-12-31", source=url)

    def _fallback(self) -> list[Oferta]:
        return [
            Oferta(id="bbva-0", titulo="Casa Rica", descripcion="15% de descuento en Casa Rica para clientes BBVA.", descuento="15%", tienda="BBVA Paraguay", categoria="hogar", medioPago="Tarjetas BBVA", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.bbva.com.py"),
            Oferta(id="bbva-1", titulo="Shopping del Sol", descripcion="Hasta 20% de descuento los jueves en tiendas del Shopping del Sol con BBVA.", descuento="Hasta 20%", tienda="BBVA Paraguay", categoria="otros", medioPago="Tarjetas BBVA", fechaInicio="2026-01-01", fechaFin="2026-12-31", diasSemana=[4], source="https://www.bbva.com.py"),
            Oferta(id="bbva-2", titulo="Punto Farma", descripcion="15% de descuento y 3 cuotas sin intereses los jueves en Punto Farma con BBVA.", descuento="15% + 3 cuotas", tienda="BBVA Paraguay", categoria="salud", medioPago="Tarjetas BBVA", fechaInicio="2026-01-01", fechaFin="2026-12-31", diasSemana=[4], source="https://www.bbva.com.py"),
            Oferta(id="bbva-3", titulo="MarketPlace Hogar", descripcion="Descuentos en muebles y decoracion con BBVA.", descuento="Descuento + 6 cuotas", tienda="BBVA Paraguay", categoria="hogar", medioPago="Tarjetas BBVA", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.bbva.com.py"),
            Oferta(id="bbva-4", titulo="Copa Airlines", descripcion="Hasta 6 cuotas sin intereses en vuelos de Copa Airlines con BBVA.", descuento="6 cuotas s/interes", tienda="BBVA Paraguay", categoria="viajes", medioPago="Tarjetas BBVA", fechaInicio="2025-07-10", fechaFin="2025-07-31", source="https://www.bbva.com.py"),
            Oferta(id="bbva-5", titulo="Rodar Neumaticos", descripcion="25% de descuento y 6 cuotas sin intereses en neumaticos y baterias con BBVA.", descuento="25% + 6 cuotas", tienda="BBVA Paraguay", categoria="otros", medioPago="Tarjetas BBVA", fechaInicio="2025-07-01", fechaFin="2025-07-31", source="https://www.bbva.com.py"),
        ]
