import requests
from bs4 import BeautifulSoup
from .base import Scraper, Oferta
from .urls import FAMILIAR_PROMOS


PROMO_KEYWORDS = {"descuento", "reintegro", "beneficio", "promocion", "cuotas", "gratis", "off", "%", "2x1", "3x2"}


class FamiliarScraper(Scraper):
    fuente = "Banco Familiar"

    def scrape(self) -> list[Oferta]:
        urls = FAMILIAR_PROMOS
        for url in urls:
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    cards = soup.select("[class*=promo], [class*=card], [class*=beneficio]")
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
            ofertas.append(Oferta(id=f"familiar-{i}", titulo=titulo, descripcion=desc, descuento="Beneficio", tienda="Banco Familiar", categoria="otros", medioPago="Tarjetas Familiar", fechaInicio="2026-01-01", fechaFin="2026-12-31", source=url))
        return ofertas if ofertas else self._fallback()

    def _fallback(self) -> list[Oferta]:
        return [
            Oferta(id="familiar-0", titulo="Supermercados Familiar", descripcion="Descuentos en supermercados pagando con Familiar.", descuento="Descuento", tienda="Banco Familiar", categoria="supermercado", medioPago="Tarjetas Familiar", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.familiar.com.py"),
            Oferta(id="familiar-1", titulo="Farmacias Familiar", descripcion="Descuentos en farmacias con tarjetas Familiar.", descuento="Descuento", tienda="Banco Familiar", categoria="salud", medioPago="Tarjetas Familiar", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.familiar.com.py"),
            Oferta(id="familiar-2", titulo="Gastronomia Familiar", descripcion="Beneficios en restaurantes con Familiar.", descuento="Descuento", tienda="Banco Familiar", categoria="restaurante", medioPago="Tarjetas Familiar", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.familiar.com.py"),
        ]
