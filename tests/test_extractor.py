from __future__ import annotations

from pathlib import Path

from src.pdf_extractor.exporters import export_records
from src.pdf_extractor.extract import extract_fields_from_text, process_pdf_files
from src.pdf_extractor.models import ExtractionRecord


def test_extract_fields_from_text() -> None:
    text = """
    服务费用确认单
    编号: INV-2026-001
    日期: 2026-06-01
    客户名称: 上海星河教育科技有限公司
    纳税人识别号: 91310000MA1K000001
    联系电话: 13800138000
    邮箱: finance@example.com
    合计金额: 1280.50
    """

    fields = extract_fields_from_text(text)

    assert fields["invoice_no"] == "INV-2026-001"
    assert fields["date"] == "2026-06-01"
    assert fields["customer"] == "上海星河教育科技有限公司"
    assert fields["tax_id"] == "91310000MA1K000001"
    assert fields["phone"] == "13800138000"
    assert fields["email"] == "finance@example.com"
    assert fields["amount"] == "1280.50"


def test_export_records_to_csv(tmp_path: Path) -> None:
    output_path = tmp_path / "result.csv"
    records = [
        ExtractionRecord(
            source_file="a.pdf",
            invoice_no="INV-1",
            date="2026-06-01",
            customer="测试客户",
            amount="100.00",
        )
    ]

    export_records(records, output_path)

    content = output_path.read_text(encoding="utf-8-sig")
    assert "INV-1" in content
    assert "测试客户" in content


def test_process_missing_pdf_returns_failed_record(tmp_path: Path) -> None:
    missing_pdf = tmp_path / "missing.pdf"

    records = process_pdf_files([missing_pdf])

    assert records[0].source_file == "missing.pdf"
    assert records[0].status == "failed"
