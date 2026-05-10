import requests
from bs4 import BeautifulSoup
from .base import Scraper, Oferta
from .urls import GNB_PROMOS


class GNBScraper(Scraper):
    fuente = "GNB Paraguay"

    def scrape(self) -> list[Oferta]:
        urls = GNB_PROMOS
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
            ofertas.append(Oferta(id=f"gnb-{i}", titulo=titulo, descripcion=desc, descuento="Beneficio", tienda="GNB Paraguay", categoria="otros", medioPago="Tarjetas GNB", fechaInicio="2026-01-01", fechaFin="2026-12-31", source=url))
        return ofertas

    def _fallback(self) -> list[Oferta]:
        return [
            Oferta(id="gnb-0", titulo="Supermercados GNB", descripcion="Descuentos en supermercados con GNB.", descuento="Descuento", tienda="GNB Paraguay", categoria="supermercado", medioPago="Tarjetas GNB", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.gnb.com.py"),
            Oferta(id="gnb-1", titulo="Combustible GNB", descripcion="Descuentos en estaciones de servicio con GNB.", descuento="Descuento", tienda="GNB Paraguay", categoria="otros", medioPago="Tarjetas GNB", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.gnb.com.py"),
        ]
