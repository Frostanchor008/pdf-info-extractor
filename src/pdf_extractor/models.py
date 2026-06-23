from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class ExtractionRecord:
    source_file: str
    page_count: int = 0
    engine: str = ""
    invoice_no: str = ""
    date: str = ""
    customer: str = ""
    amount: str = ""
    tax_id: str = ""
    phone: str = ""
    email: str = ""
    text_preview: str = ""
    status: str = "ok"
    error: str = ""

    def to_dict(self) -> dict[str, str | int]:
        return asdict(self)
