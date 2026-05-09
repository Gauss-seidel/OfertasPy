import json
from dataclasses import asdict
from pathlib import Path
from scrapers.ueno import UenoScraper

DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "ofertas.json"


def run_all() -> None:
    scrapers = [
        UenoScraper(),
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
    DATA_FILE.write_text(
        json.dumps(todas, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nTotal: {len(todas)} ofertas -> {DATA_FILE}")


if __name__ == "__main__":
    run_all()
