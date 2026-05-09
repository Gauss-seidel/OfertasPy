from .base import Scraper, Oferta


class UenoScraper(Scraper):
    fuente = "Ueno Bank"

    def scrape(self) -> list[Oferta]:
        return [
            Oferta(
                id="1",
                titulo="40% de descuento en supermercados",
                descripcion="Pagá con tu tarjeta Ueno y obtené 40% off en todos los supermercados adheridos.",
                descuento="40%",
                tienda="Ueno Bank",
                categoria="supermercado",
                medioPago="Tarjeta Ueno",
                fechaFin="2026-12-31",
                source="https://www.ueno.com.py",
            ),
        ]
