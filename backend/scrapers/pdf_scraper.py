import re
from pathlib import Path
from .base import Scraper, Oferta

try:
    import fitz
except ImportError:
    fitz = None


DIAS_MAP = {
    "lunes": 1, "martes": 2, "miercoles": 3, "miércoles": 3,
    "jueves": 4, "viernes": 5, "sabado": 6, "sábado": 6, "domingo": 0,
}

MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
}

TIENDA_ALIASES: dict[str, str] = {
    "bbva": "BBVA Paraguay",
    "continental": "Banco Continental",
    "familiar": "Banco Familiar",
    "basa": "Banco Basa",
    "gnb": "GNB Paraguay",
    "sudameris": "Banco Sudameris",
    "vision": "Banco Visión",
    "regional": "Banco Regional",
    "cooperativa": "Cooperativa Universitaria",
    "superseis": "Superseis",
    "atlas": "Banco Atlas",
    "itau": "Itaú Paraguay",
    "ueno": "Ueno Bank",
    "eko": "Eko",
}

CAT_ALIASES: dict[str, str] = {
    "supermercado": "supermercado", "super": "supermercado",
    "gastronomia": "restaurante", "restaurant": "restaurante", "comida": "restaurante", "gastronomía": "restaurante",
    "viaje": "viajes", "vuelo": "viajes", "turismo": "viajes",
    "tecnologia": "tecnologia", "electro": "tecnologia", "comput": "tecnologia", "tecnología": "tecnologia",
    "salud": "salud", "farmac": "salud", "spa": "salud", "peluquer": "salud", "bienestar": "salud",
    "hogar": "hogar", "mueble": "hogar", "decoracion": "hogar",
    "hotel": "viajes", "hostel": "viajes",
    "automovil": "otros", "automóvil": "otros",
    "educacion": "otros", "educación": "otros",
    "entretenimiento": "entretenimiento",
    "peaje": "otros",
    "farmacias": "salud",
    "joyer": "otros",
    "jugueter": "entretenimiento",
    "mascota": "otros",
    "tienda": "otros",
    "combustible": "otros",
    "servicio": "otros",
}

KNOWN_NON_HEADERS = {
    "compras en el exterior", "semana santa con basa (argentina, brasil & uruguay)",
    "destacados del mes", "catálogo de abril 2026", "catálogo",
}

STORE_BLACKLIST = {
    "con tarjetas de crédito basa seleccionadas", "beneficios exclusivos",
    "¿aún no tenés tu tarjeta de crédito para aprovechar estos beneficios?",
    "¡descargá acá y usala ya mismo!", "bases y condiciones en",
    "bases y condiciones en www.bancobasa.com.py/promociones-personas",
    "consultá las bases y condiciones aquí",
    "consultá las tarjetas de crédito seleccionadas",
}


def _merge_dias(new_dias: list[int] | None, target: set[int]) -> None:
    if new_dias:
        target.update(new_dias)


def _clean_text(texto: str) -> str:
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", texto)

GARBAGE_TITLES = {"tengo descuentos", "de descuento", "promocion", "beneficio", ""}


NEXT_LINE_DISCOUNT_PATTERN = re.compile(
    r"^(Hasta\s+)?\d+%\s*(de\s+)?(ahorro|descuento|off|reintegro)|"
    r"^2x1|"
    r"^cuotas\s+sin",
    re.IGNORECASE,
)

DAY_LINE_START = re.compile(
    r"^(todos los|del |lunes|martes|mi[ée]rcoles|jueves|viernes|s[aá]bado|domingo|"
    r"vi?e?r?n?e?s?\s+a\s+|d[ií]as\s+de)",
    re.IGNORECASE,
)


def _is_section_header(line: str, next_line: str) -> bool:
    if not line or not next_line:
        return False
    if not NEXT_LINE_DISCOUNT_PATTERN.match(next_line):
        return False
    ll = line.lower()
    if any(kw in ll for kw in ["todos los", "del ", "de ahorro", "de descuento",
                                "cuotas", "hasta ", "+", "%", "www.",
                                "bases y condiciones", "consultá",
                                "exclusivo con", "en productos",
                                "en medicamentos",
                                "seleccionadas", "afinidad", "tarjeta",
                                "adheridos", "2»", "4»", "al ", "y "]):
        return False
    if ll.startswith("en "):
        return False
    if DAY_LINE_START.match(ll):
        return False
    if ll in KNOWN_NON_HEADERS:
        return False
    if len(line) > 45:
        return False
    return True


def _find_sections(lines: list[str]) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    current_header = None
    current_body: list[str] = []

    for i, line in enumerate(lines):
        next_line = lines[i + 1] if i + 1 < len(lines) else ""
        if _is_section_header(line, next_line):
            if current_header:
                sections.append((current_header, current_body))
            current_header = line
            current_body = []
        elif current_header:
            current_body.append(line)

    if current_header:
        sections.append((current_header, current_body))

    return sections


DISCOUNT_LINE = re.compile(
    r"^(Hasta\s+)?\d+%\s*(de\s+)?(ahorro|descuento|off|reintegro)|"
    r"^\d+%\s*off|"
    r"^2x1|"
    r"^cuotas(\s+sin|\s+\d+)?\b",
    re.IGNORECASE,
)

DAY_LINE = re.compile(r"^todos los|^del |^lunes|^martes|^mi[ée]rcoles|^jueves|^viernes|^s[aá]bado|^domingo", re.IGNORECASE)

CUOTAS_LINE = re.compile(r"^(\+ )?(cuotas sin intereses|\d+ cuotas|cuotas)", re.IGNORECASE)


class PdfScraper(Scraper):
    fuente = "PDFs"

    def scrape(self) -> list[Oferta]:
        if fitz is None:
            return []
        pdf_dir = Path(__file__).parent.parent / "data" / "pdfs"
        ofertas: list[Oferta] = []
        idx = 0
        for carpeta in sorted(pdf_dir.iterdir()):
            if not carpeta.is_dir():
                continue
            tienda = TIENDA_ALIASES.get(carpeta.name, carpeta.name.title())
            for pdf_path in sorted(carpeta.glob("*.pdf")):
                texto = self._extraer_texto(pdf_path)
                if not texto.strip():
                    continue
                res = self._parsear(texto, tienda, pdf_path.name, idx)
                ofertas.extend(res)
                idx += len(res)
        return ofertas

    @staticmethod
    def _extraer_texto(path: Path) -> str:
        doc = fitz.open(path)
        paginas = []
        for page in doc:
            paginas.append(page.get_text())
        doc.close()
        return "\n".join(paginas)

    def _parsear(self, texto: str, tienda: str, filename: str, idx: int) -> list[Oferta]:
        t = texto.lower()
        if tienda == "Banco Basa":
            return self._parse_basa_style(texto, tienda, filename, idx)

        titulo = self._extract_title(texto, t)
        if titulo.lower().strip() in GARBAGE_TITLES or len(titulo.strip()) < 5:
            return []

        descuento = self._extract_descuento(t)
        dias = self._extract_dias(t)
        categoria = self._extract_categoria(t)
        fechas = self._extract_fechas(t)
        descripcion = self._extract_descripcion(texto, t)

        return [Oferta(
            id=f"pdf-{idx}",
            titulo=titulo,
            descripcion=descripcion,
            descuento=descuento,
            tienda=tienda,
            categoria=categoria,
            medioPago=None,
            fechaInicio=fechas[0],
            fechaFin=fechas[1],
            diasSemana=dias,
            source=f"PDF: {filename}",
        )]

    def _parse_basa_style(self, texto: str, tienda: str, filename: str, start_idx: int) -> list[Oferta]:
        texto_limpio = _clean_text(texto)
        lines = [l.strip() for l in texto_limpio.split("\n") if l.strip()]
        if not lines:
            return []

        sections = _find_sections(lines)
        ofertas: list[Oferta] = []

        for idx, (header, body) in enumerate(sections):
            cat = self._basa_categoria(header)
            descuento, stores, dias, fechas = self._parse_basa_section(body, header)
            if not stores or self._is_spam_section(header, stores):
                continue
            ofertas.append(Oferta(
                id=f"pdf-{start_idx + idx}",
                titulo=header,
                descripcion=f"Beneficios en {header.lower()} con tarjetas Basa seleccionadas",
                descuento=descuento,
                tienda=tienda,
                categoria=cat,
                fechaInicio=fechas[0],
                fechaFin=fechas[1],
                diasSemana=dias if dias else None,
                source=f"PDF: {filename}",
                tiendas=stores,
            ))

        return ofertas if ofertas else self._fallback_oferta(texto, tienda, filename, start_idx)

    @staticmethod
    def _is_spam_section(header: str, stores: list[str]) -> bool:
        ll = header.lower()
        if ll in ("compras en el exterior",):
            return True
        for s in stores:
            if "consultá las bases" in s.lower():
                return True
        return False

    def _fallback_oferta(self, texto: str, tienda: str, filename: str, idx: int) -> list[Oferta]:
        t = texto.lower()
        return [Oferta(
            id=f"pdf-{idx}",
            titulo=self._extract_title(texto, t),
            descripcion=self._extract_descripcion(texto, t),
            descuento=self._extract_descuento(t),
            tienda=tienda,
            categoria=self._extract_categoria(t),
            fechaInicio=None,
            fechaFin=None,
            diasSemana=self._extract_dias(t),
            source=f"PDF: {filename}",
        )]

    @staticmethod
    def _basa_categoria(header: str) -> str:
        h = header.lower()
        for kw, cat in CAT_ALIASES.items():
            if kw in h:
                return cat
        return "otros"

    @staticmethod
    def _parse_basa_section(body: list[str], header: str) -> tuple[str, list[str], list[int] | None, tuple[str | None, str | None]]:
        descuento = "Beneficio"
        stores: list[str] = []
        all_dias: set[int] = set()
        fechas: tuple[str | None, str | None] = (None, None)

        for line in body:
            ll = line.lower().strip()
            if not ll or ll in STORE_BLACKLIST:
                continue
            if len(ll) < 2:
                continue

            if DISCOUNT_LINE.match(ll):
                d = PdfScraper._extract_descuento(ll)
                if d != "Beneficio":
                    descuento = d
                continue

            if CUOTAS_LINE.match(ll):
                continue

            if ll.startswith("+") or ll.startswith("*"):
                continue

            fd = PdfScraper._extract_fechas(ll)
            if fd[0] or fd[1]:
                fechas = fd if fd[0] or fd[1] else fechas

            _merge_dias(PdfScraper._extract_dias(ll), all_dias)

            if DAY_LINE.match(ll):
                continue

            if "consultá las bases" in ll or "consultá las tarjetas" in ll:
                continue

            if re.match(r"^\d{1,2}\s+(y\s+)?\d{0,2}\s*de\s+", ll):
                continue

            if re.match(r"^\d{1,2}\s+de\s+", ll):
                continue

            stores.append(line)

        dias_list = sorted(all_dias) if all_dias else None
        return descuento, stores, dias_list, fechas

    @staticmethod
    def _extract_title(texto: str, t: str) -> str:
        lines = [l.strip() for l in texto.split("\n") if l.strip()]
        for l in lines:
            if any(w in l.lower() for w in ["promocion", "descuento", "beneficio", "oferta"]):
                return l[:120]
        return lines[0][:120] if lines else "Promocion"

    @staticmethod
    def _extract_descuento(t: str) -> str:
        m = re.search(r"(\d+)%\s*de\s*(descuento|reintegro|off)", t)
        if m:
            return f"{m.group(1)}% {m.group(2)}"
        m = re.search(r"(\d+)\s*c(uotas?|ta?s?)\s*sin\s*interes", t)
        if m:
            return f"{m.group(1)} cuotas s/interes"
        m = re.search(r"(\d+)%\s*off", t)
        if m:
            return f"{m.group(1)}% OFF"
        m = re.search(r"(\d+)%\s*de\s*ahorro", t)
        if m:
            return f"{m.group(1)}% ahorro"
        m = re.search(r"2x1|3x2", t)
        if m:
            return m.group(0)
        return "Beneficio"

    @staticmethod
    def _extract_dias(t: str) -> list[int] | None:
        dias: list[int] = []
        for nombre, num in DIAS_MAP.items():
            if nombre in t and num not in dias:
                dias.append(num)
        if "lunes a viernes" in t or "lun a vie" in t:
            dias = [1, 2, 3, 4, 5]
        return dias if dias else None

    @staticmethod
    def _extract_categoria(t: str) -> str:
        for palabra, cat in CAT_ALIASES.items():
            if palabra in t:
                return cat
        return "otros"

    @staticmethod
    def _extract_fechas(t: str) -> tuple[str | None, str | None]:
        fechas = re.findall(r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", t)
        fin = fechas[-1] if fechas else None
        inicio = fechas[0] if len(fechas) > 1 else None
        m_hasta = re.search(r"(?:hasta|valido hasta|validez hasta|vigencia)\s*(?:del?\s*.*?\s*)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", t)
        if m_hasta and not fin:
            fin = m_hasta.group(1)
        return (inicio, fin)

    @staticmethod
    def _extract_descripcion(texto: str, t: str) -> str:
        lines = [l.strip() for l in texto.split("\n") if l.strip() and len(l.strip()) > 20]
        for l in lines:
            lt = l.lower()
            if any(w in lt for w in ["descuento", "reintegro", "beneficio", "promocion"]):
                return l[:200]
        return lines[0][:200] if lines else texto[:200]
