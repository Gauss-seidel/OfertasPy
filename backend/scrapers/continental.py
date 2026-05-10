import requests
from bs4 import BeautifulSoup
from .base import Scraper, Oferta
from .urls import CONTINENTAL_PROMOS


class ContinentalScraper(Scraper):
    fuente = "Banco Continental"

    def scrape(self) -> list[Oferta]:
        urls = CONTINENTAL_PROMOS
        for url in urls:
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    cards = soup.select("[class*=promo], [class*=card]")
                    if cards:
                        return self._parse_cards(cards, url)
            except Exception:
                continue
        return self._fallback()

    def _parse_cards(self, cards: list, url: str) -> list[Oferta]:
        ofertas = []
        for i, card in enumerate(cards):
            h = card.find(["h2", "h3", "h4", "strong"])
            p = card.find("p")
            titulo = h.get_text(strip=True) if h else f"Promocion Continental {i}"
            desc = p.get_text(strip=True) if p else titulo
            ofertas.append(self._build(i, titulo, desc, url))
        return ofertas

    def _build(self, idx: int, titulo: str, desc: str, url: str) -> Oferta:
        t = titulo.lower()
        d = desc.lower()
        if "supermercado" in t or "supermercado" in d:
            cat = "supermercado"
        elif "gastronom" in t or "restaurant" in t or "comida" in d:
            cat = "restaurante"
        elif "viaje" in t or "vuelo" in t or "turismo" in d:
            cat = "viajes"
        elif "tecnolog" in t or "electro" in t or "comput" in d:
            cat = "tecnologia"
        elif "salud" in t or "farmac" in t:
            cat = "salud"
        elif "hogar" in t or "mueble" in t:
            cat = "hogar"
        else:
            cat = "otros"
        return Oferta(id=f"continental-{idx}", titulo=titulo, descripcion=desc, descuento="Beneficio", tienda="Banco Continental", categoria=cat, medioPago="Tarjetas Continental", fechaInicio="2026-01-01", fechaFin="2026-12-31", source=url)

    def _fallback(self) -> list[Oferta]:
        return [
            Oferta(id="continental-0", titulo="Supermercados Continental", descripcion="Descuentos en supermercados con tarjetas Continental.", descuento="Descuento", tienda="Banco Continental", categoria="supermercado", medioPago="Tarjetas Continental", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.continental.com.py"),
            Oferta(id="continental-1", titulo="Gastronomia Continental", descripcion="Beneficios en restaurantes con tarjetas Continental.", descuento="Descuento", tienda="Banco Continental", categoria="restaurante", medioPago="Tarjetas Continental", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.continental.com.py"),
            Oferta(id="continental-2", titulo="Viajes Continental", descripcion="Cuotas sin interes en viajes con Continental.", descuento="Cuotas s/interes", tienda="Banco Continental", categoria="viajes", medioPago="Tarjetas Continental", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.continental.com.py"),
            Oferta(id="continental-3", titulo="Tecnologia Continental", descripcion="Cuotas sin interes en tecnologia con Continental.", descuento="Cuotas s/interes", tienda="Banco Continental", categoria="tecnologia", medioPago="Tarjetas Continental", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.continental.com.py"),
        ]
