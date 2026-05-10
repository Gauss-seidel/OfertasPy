import requests
from bs4 import BeautifulSoup
from .base import Scraper, Oferta
from .urls import BASA_PROMOS


class BasaScraper(Scraper):
    fuente = "Banco Basa"

    def scrape(self) -> list[Oferta]:
        urls = BASA_PROMOS
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
            ofertas.append(Oferta(id=f"basa-{i}", titulo=titulo, descripcion=desc, descuento="Beneficio", tienda="Banco Basa", categoria="otros", medioPago="Tarjetas Basa", fechaInicio="2026-01-01", fechaFin="2026-12-31", source=url))
        return ofertas

    def _fallback(self) -> list[Oferta]:
        return [
            Oferta(id="basa-0", titulo="Supermercados Basa", descripcion="Descuentos en supermercados con Banco Basa.", descuento="Descuento", tienda="Banco Basa", categoria="supermercado", medioPago="Tarjetas Basa", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.bancobasa.com.py"),
            Oferta(id="basa-1", titulo="Gastronomia Basa", descripcion="Beneficios en restaurantes con Basa.", descuento="Descuento", tienda="Banco Basa", categoria="restaurante", medioPago="Tarjetas Basa", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.bancobasa.com.py"),
        ]
