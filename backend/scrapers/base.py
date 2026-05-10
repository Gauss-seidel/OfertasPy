from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Oferta:
    id: str = ""
    titulo: str = ""
    descripcion: str = ""
    descuento: str = ""
    tienda: str = ""
    categoria: str = ""
    medioPago: str | None = None
    fechaInicio: str | None = None
    fechaFin: str | None = None
    source: str = ""
    logo: str | None = None
    diasSemana: list[int] | None = None
    tiendas: list[str] | None = None


class Scraper(ABC):
    fuente: str = ""

    @abstractmethod
    def scrape(self) -> list[Oferta]:
        ...
