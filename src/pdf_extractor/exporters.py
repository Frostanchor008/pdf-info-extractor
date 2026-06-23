from __future__ import annotations

from pathlib import Path

import pandas as pd

from .models import ExtractionRecord


DEFAULT_COLUMNS = [
    "source_file",
    "status",
    "page_count",
    "engine",
    "invoice_no",
    "date",
    "customer",
    "amount",
    "tax_id",
    "phone",
    "email",
    "text_preview",
    "error",
]


def records_to_dataframe(records: list[ExtractionRecord]) -> pd.DataFrame:
    dataframe = pd.DataFrame([record.to_dict() for record in records])
    for column in DEFAULT_COLUMNS:
        if column not in dataframe.columns:
            dataframe[column] = ""
    return dataframe[DEFAULT_COLUMNS]


def export_records(records: list[ExtractionRecord], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe = records_to_dataframe(records)
    suffix = output_path.suffix.lower()
    if suffix == ".csv":
        dataframe.to_csv(output_path, index=False, encoding="utf-8-sig")
        return
    if suffix == ".xlsx":
        dataframe.to_excel(output_path, index=False)
        return
    raise ValueError("Only .csv and .xlsx output files are supported.")
