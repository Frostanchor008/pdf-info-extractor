from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas


SAMPLES = [
    {
        "filename": "sample_invoice_001.pdf",
        "lines": [
            "服务费用确认单",
            "编号: INV-2026-001",
            "日期: 2026-06-01",
            "客户名称: 上海星河教育科技有限公司",
            "纳税人识别号: 91310000MA1K000001",
            "联系电话: 13800138000",
            "邮箱: finance@example.com",
            "合计金额: 1280.50",
        ],
    },
    {
        "filename": "sample_invoice_002.pdf",
        "lines": [
            "项目验收回执",
            "订单编号: ORD-2026-0098",
            "订单日期: 2026-06-12",
            "客户: 杭州青木贸易有限公司",
            "统一社会信用代码: 91330100MA2B000002",
            "手机: 13900139000",
            "Email: ops@example.cn",
            "总金额: RMB 860.00",
        ],
    },
]


def main() -> None:
    output_dir = Path(__file__).resolve().parents[1] / "data" / "samples"
    output_dir.mkdir(parents=True, exist_ok=True)
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))

    for sample in SAMPLES:
        file_path = output_dir / sample["filename"]
        pdf = canvas.Canvas(str(file_path), pagesize=A4)
        pdf.setFont("STSong-Light", 16)
        y = 790
        for line in sample["lines"]:
            pdf.drawString(72, y, line)
            y -= 34
        pdf.save()
        print(f"Created {file_path}")


if __name__ == "__main__":
    main()
