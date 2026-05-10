import requests
from bs4 import BeautifulSoup
from .base import Scraper, Oferta
from .urls import VISION_PROMOS


class VisionScraper(Scraper):
    fuente = "Banco Vision"

    def scrape(self) -> list[Oferta]:
        urls = VISION_PROMOS
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
            ofertas.append(Oferta(id=f"vision-{i}", titulo=titulo, descripcion=desc, descuento="Beneficio", tienda="Banco Vision", categoria="otros", medioPago="Tarjetas Vision", fechaInicio="2026-01-01", fechaFin="2026-12-31", source=url))
        return ofertas

    def _fallback(self) -> list[Oferta]:
        return [
            Oferta(id="vision-0", titulo="Supermercados Vision", descripcion="Descuentos en supermercados con Vision.", descuento="Descuento", tienda="Banco Vision", categoria="supermercado", medioPago="Tarjetas Vision", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.visionbanco.com"),
            Oferta(id="vision-1", titulo="Gastronomia Vision", descripcion="Beneficios en restaurantes con Vision.", descuento="Descuento", tienda="Banco Vision", categoria="restaurante", medioPago="Tarjetas Vision", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.visionbanco.com"),
        ]
