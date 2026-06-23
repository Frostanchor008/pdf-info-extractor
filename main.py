from __future__ import annotations

import argparse
from pathlib import Path

from src.pdf_extractor.exporters import export_records
from src.pdf_extractor.extract import collect_pdf_paths, process_pdf_files


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Batch extract fields from PDF files.")
    parser.add_argument("input", help="A PDF file or a folder containing PDF files.")
    parser.add_argument(
        "--output",
        default="output/result.xlsx",
        help="Output file path. Supported: .xlsx, .csv",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    pdf_paths = collect_pdf_paths(input_path)
    if not pdf_paths:
        raise SystemExit(f"No PDF files found: {input_path}")

    records = process_pdf_files(pdf_paths)
    export_records(records, output_path)

    ok_count = sum(1 for record in records if record.status == "ok")
    fail_count = len(records) - ok_count
    print(f"Processed {len(records)} file(s): {ok_count} ok, {fail_count} failed")
    print(f"Saved to: {output_path.resolve()}")


if __name__ == "__main__":
    main()
