from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from .models import ExtractionRecord


def collect_pdf_paths(input_path: Path) -> list[Path]:
    if input_path.is_file() and input_path.suffix.lower() == ".pdf":
        return [input_path]
    if input_path.is_dir():
        return sorted(path for path in input_path.rglob("*.pdf") if path.is_file())
    return []


def process_pdf_files(pdf_paths: Iterable[Path]) -> list[ExtractionRecord]:
    records: list[ExtractionRecord] = []
    for pdf_path in pdf_paths:
        try:
            text, page_count, engine = read_pdf_text(pdf_path)
            fields = extract_fields_from_text(text)
            records.append(
                ExtractionRecord(
                    source_file=pdf_path.name,
                    page_count=page_count,
                    engine=engine,
                    text_preview=make_preview(text),
                    **fields,
                )
            )
        except Exception as exc:
            records.append(
                ExtractionRecord(
                    source_file=pdf_path.name,
                    status="failed",
                    error=str(exc),
                )
            )
    return records


def read_pdf_text(pdf_path: Path) -> tuple[str, int, str]:
    errors: list[str] = []

    try:
        import pdfplumber

        text_parts: list[str] = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text_parts.append(page.extract_text() or "")
            return "\n".join(text_parts), len(pdf.pages), "pdfplumber"
    except Exception as exc:
        errors.append(f"pdfplumber: {exc}")

    try:
        from pypdf import PdfReader

        reader = PdfReader(str(pdf_path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text, len(reader.pages), "pypdf"
    except Exception as exc:
        errors.append(f"pypdf: {exc}")

    raise RuntimeError("PDF text extraction failed. " + " | ".join(errors))


def extract_fields_from_text(text: str) -> dict[str, str]:
    normalized = normalize_text(text)
    return {
        "invoice_no": first_match(
            normalized,
            [
                r"(?:发票号码|票据编号|订单编号|合同编号|单号|编号)\s*[:：]?\s*([A-Za-z0-9-]{4,})",
                r"\b(?:NO|No|no)\.?\s*[:：]?\s*([A-Za-z0-9-]{4,})",
            ],
        ),
        "date": first_match(
            normalized,
            [
                r"(?:开票日期|合同日期|订单日期|日期)\s*[:：]?\s*((?:20)?\d{2}[年/-]\d{1,2}[月/-]\d{1,2}日?)",
                r"\b((?:20)?\d{2}-\d{1,2}-\d{1,2})\b",
            ],
        ),
        "customer": first_match(
            normalized,
            [
                r"(?:客户名称|购买方|甲方|公司名称|客户)\s*[:：]?\s*([^\n\r]{2,40})",
            ],
        ),
        "amount": first_match(
            normalized,
            [
                r"(?:价税合计|合计金额|总金额|金额)\s*[:：]?\s*(?:人民币|RMB|¥|￥)?\s*([0-9,]+(?:\.\d{1,2})?)",
            ],
        ),
        "tax_id": first_match(
            normalized,
            [
                r"(?:纳税人识别号|统一社会信用代码|税号)\s*[:：]?\s*([A-Z0-9]{10,25})",
            ],
        ),
        "phone": first_match(
            normalized,
            [
                r"(?:联系电话|电话|手机)\s*[:：]?\s*((?:\+?86[- ]?)?1[3-9]\d{9})",
                r"\b((?:\+?86[- ]?)?1[3-9]\d{9})\b",
            ],
        ),
        "email": first_match(
            normalized,
            [
                r"\b([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})\b",
            ],
        ),
    }


def first_match(text: str, patterns: list[str]) -> str:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return clean_value(match.group(1))
    return ""


def normalize_text(text: str) -> str:
    text = text.replace("\u3000", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_value(value: str) -> str:
    value = value.strip(" \t\r\n：:，,;；")
    return re.sub(r"\s{2,}", " ", value)


def make_preview(text: str, limit: int = 120) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    return compact[:limit]
