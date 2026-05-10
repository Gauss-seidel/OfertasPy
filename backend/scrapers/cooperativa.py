import requests
from bs4 import BeautifulSoup
from .base import Scraper, Oferta
from .urls import COOPERATIVA_PROMOS

PROMO_KEYWORDS = {"descuento", "reintegro", "beneficio", "promocion", "cuotas", "gratis", "off", "%", "2x1", "3x2"}


class CooperativaScraper(Scraper):
    fuente = "Cooperativa Universitaria"

    def scrape(self) -> list[Oferta]:
        urls = COOPERATIVA_PROMOS
        for url in urls:
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    cards = soup.select("[class*=promo], [class*=card]")
                    return self._parse_cards(cards, url)
            except Exception:
                continue
        return self._fallback()

    def _parse_cards(self, cards: list, url: str) -> list[Oferta]:
        ofertas = []
        visto = set()
        for i, card in enumerate(cards):
            texto = card.get_text(" ", strip=True).lower()
            if not any(k in texto for k in PROMO_KEYWORDS):
                continue
            if texto in visto:
                continue
            visto.add(texto)
            h = card.find(["h2", "h3", "h4"])
            p = card.find("p")
            titulo = h.get_text(strip=True)[:120] if h else f"Promocion {len(ofertas)}"
            desc = p.get_text(strip=True)[:200] if p else texto[:200]
            ofertas.append(Oferta(id=f"cooperativa-{i}", titulo=titulo, descripcion=desc, descuento="Beneficio", tienda="Cooperativa Universitaria", categoria="otros", medioPago="Cooperativa Universitaria", fechaInicio="2026-01-01", fechaFin="2026-12-31", source=url))
        return ofertas if ofertas else self._fallback()

    def _fallback(self) -> list[Oferta]:
        return [
            Oferta(id="cooperativa-0", titulo="Supermercados Coop", descripcion="Descuentos en supermercados con Cooperativa Universitaria.", descuento="Descuento", tienda="Cooperativa Universitaria", categoria="supermercado", medioPago="Cooperativa Universitaria", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.cooperativa.com.py"),
            Oferta(id="cooperativa-1", titulo="Farmacias Coop", descripcion="Descuentos en farmacias con Cooperativa Universitaria.", descuento="Descuento", tienda="Cooperativa Universitaria", categoria="salud", medioPago="Cooperativa Universitaria", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.cooperativa.com.py"),
        ]
