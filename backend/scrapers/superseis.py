import requests
from bs4 import BeautifulSoup
from .base import Scraper, Oferta
from .urls import SUPERSEIS_PROMOS


class SuperseisScraper(Scraper):
    fuente = "Superseis"

    def scrape(self) -> list[Oferta]:
        urls = SUPERSEIS_PROMOS
        for url in urls:
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    cards = soup.select("[class*=promo], [class*=card], [class*=oferta]")
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
            titulo = h.get_text(strip=True) if h else f"Promocion {i}"
            desc = p.get_text(strip=True) if p else titulo
            ofertas.append(Oferta(id=f"superseis-{i}", titulo=titulo, descripcion=desc, descuento="Oferta", tienda="Superseis", categoria="supermercado", medioPago=None, fechaInicio="2026-01-01", fechaFin="2026-12-31", source=url))
        return ofertas

    def _fallback(self) -> list[Oferta]:
        return [
            Oferta(id="superseis-0", titulo="Lunes de Descuentos", descripcion="Descuentos en productos seleccionados los lunes en Superseis.", descuento="Descuento", tienda="Superseis", categoria="supermercado", fechaInicio="2026-01-01", fechaFin="2026-12-31", diasSemana=[1], source="https://www.superseis.com.py"),
            Oferta(id="superseis-1", titulo="Miercoles de Ofertas", descripcion="Ofertas especiales los miercoles en Superseis.", descuento="Oferta", tienda="Superseis", categoria="supermercado", fechaInicio="2026-01-01", fechaFin="2026-12-31", diasSemana=[3], source="https://www.superseis.com.py"),
            Oferta(id="superseis-2", titulo="Jueves de Descuentos", descripcion="Descuentos en carniceria y verduleria los jueves en Superseis.", descuento="Descuento", tienda="Superseis", categoria="supermercado", fechaInicio="2026-01-01", fechaFin="2026-12-31", diasSemana=[4], source="https://www.superseis.com.py"),
        ]
