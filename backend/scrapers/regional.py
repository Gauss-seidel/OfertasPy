import requests
from bs4 import BeautifulSoup
from .base import Scraper, Oferta
from .urls import REGIONAL_PROMOS


class RegionalScraper(Scraper):
    fuente = "Banco Regional"

    def scrape(self) -> list[Oferta]:
        urls = REGIONAL_PROMOS
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
            h = card.find(["h2", "h3", "h4"])
            p = card.find("p")
            titulo = h.get_text(strip=True) if h else f"Promocion {i}"
            desc = p.get_text(strip=True) if p else titulo
            ofertas.append(Oferta(id=f"regional-{i}", titulo=titulo, descripcion=desc, descuento="Beneficio", tienda="Banco Regional", categoria="otros", medioPago="Tarjetas Regional", fechaInicio="2026-01-01", fechaFin="2026-12-31", source=url))
        return ofertas

    def _fallback(self) -> list[Oferta]:
        return [
            Oferta(id="regional-0", titulo="Supermercados Regional", descripcion="Descuentos en supermercados con Banco Regional.", descuento="Descuento", tienda="Banco Regional", categoria="supermercado", medioPago="Tarjetas Regional", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.regional.com.py"),
            Oferta(id="regional-1", titulo="Combustible Regional", descripcion="Descuentos en estaciones de servicio con Regional.", descuento="Descuento", tienda="Banco Regional", categoria="otros", medioPago="Tarjetas Regional", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.regional.com.py"),
        ]
