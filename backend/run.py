import json
from dataclasses import asdict
from pathlib import Path
from scrapers.ueno import UenoScraper
from scrapers.eko import EkoScraper
from scrapers.atlas import AtlasScraper
from scrapers.bbva import BBVAScraper
from scrapers.itau import ItauScraper
from scrapers.continental import ContinentalScraper
from scrapers.familiar import FamiliarScraper
from scrapers.basa import BasaScraper
from scrapers.gnb import GNBScraper
from scrapers.sudameris import SudamerisScraper
from scrapers.vision import VisionScraper
from scrapers.regional import RegionalScraper
from scrapers.cooperativa import CooperativaScraper
from scrapers.superseis import SuperseisScraper
from scrapers.pdf_scraper import PdfScraper
DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "ofertas.json"


def run_all() -> None:
    scrapers = [
        UenoScraper(),
        EkoScraper(),
        AtlasScraper(),
        BBVAScraper(),
        ItauScraper(),
        ContinentalScraper(),
        FamiliarScraper(),
        BasaScraper(),
        GNBScraper(),
        SudamerisScraper(),
        VisionScraper(),
        RegionalScraper(),
        CooperativaScraper(),
        SuperseisScraper(),
        PdfScraper(),
    ]

    todas: list[dict] = []
    for s in scrapers:
        try:
            resultados = s.scrape()
            todas.extend(asdict(r) for r in resultados)
            print(f"  OK {s.fuente}: {len(resultados)} ofertas")
        except Exception as e:
            print(f"  ERR {s.fuente}: {e}")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    limpias = [{k: v for k, v in d.items() if v is not None and v != []} for d in todas]
    DATA_FILE.write_text(
        json.dumps(limpias, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nTotal: {len(todas)} ofertas -> {DATA_FILE}")


if __name__ == "__main__":
    run_all()
