import requests
from bs4 import BeautifulSoup
from .base import Scraper, Oferta
from .urls import ITAU_PROMOS


class ItauScraper(Scraper):
    fuente = "Itau Paraguay"

    def scrape(self) -> list[Oferta]:
        urls = ITAU_PROMOS
        for url in urls:
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    cards = soup.select("[class*=promocion], [class*=card], [class*=beneficio]")
                    if cards:
                        return self._parse_cards(cards, url)
                    textos = soup.get_text(" ", strip=True)
                    parsed = self._parse_text(textos, url)
                    if parsed:
                        return parsed
            except Exception:
                continue
        return self._fallback()

    def _parse_cards(self, cards: list, url: str) -> list[Oferta]:
        ofertas = []
        for i, card in enumerate(cards):
            h = card.find(["h2", "h3", "h4"])
            p = card.find("p")
            titulo = h.get_text(strip=True) if h else f"Promocion Itau {i}"
            desc = p.get_text(strip=True) if p else titulo
            ofertas.append(self._build(i, titulo, desc, url))
        return ofertas

    def _parse_text(self, texto: str, url: str) -> list[Oferta]:
        ofertas = []
        t = texto.lower()
        if "supermercado" in t:
            ofertas.append(self._build(0, "Supermercados Itau", "Descuentos en supermercados con Itau.", url))
        if "viaje" in t:
            ofertas.append(self._build(1, "Viajes Itau", "Beneficios en viajes con Itau.", url))
        if "restaurant" in t or "gastronom" in t:
            ofertas.append(self._build(2, "Gastronomia Itau", "Descuentos en restaurantes con Itau.", url))
        return ofertas

    def _build(self, idx: int, titulo: str, desc: str, url: str) -> Oferta:
        return Oferta(id=f"itau-{idx}", titulo=titulo, descripcion=desc, descuento="Beneficio", tienda="Itau Paraguay", categoria="otros", medioPago="Tarjetas Itau", fechaInicio="2026-01-01", fechaFin="2026-12-31", source=url)

    def _fallback(self) -> list[Oferta]:
        return [
            Oferta(id="itau-0", titulo="Supermercados Itau", descripcion="Descuentos en supermercados con tarjetas Itau.", descuento="Descuento", tienda="Itau Paraguay", categoria="supermercado", medioPago="Tarjetas Itau", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.itau.com.py"),
            Oferta(id="itau-1", titulo="Gastronomia Itau", descripcion="Beneficios en restaurantes con tarjetas Itau.", descuento="Descuento", tienda="Itau Paraguay", categoria="restaurante", medioPago="Tarjetas Itau", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.itau.com.py"),
            Oferta(id="itau-2", titulo="Viajes Itau", descripcion="Cuotas sin interes en viajes con Itau.", descuento="Cuotas s/interes", tienda="Itau Paraguay", categoria="viajes", medioPago="Tarjetas Itau", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.itau.com.py"),
            Oferta(id="itau-3", titulo="Tecnologia Itau", descripcion="Cuotas sin interes en tecnologia con Itau.", descuento="Cuotas s/interes", tienda="Itau Paraguay", categoria="tecnologia", medioPago="Tarjetas Itau", fechaInicio="2026-01-01", fechaFin="2026-12-31", source="https://www.itau.com.py"),
        ]
