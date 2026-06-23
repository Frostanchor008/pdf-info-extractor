from __future__ import annotations

from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

import streamlit as st

from src.pdf_extractor.exporters import records_to_dataframe
from src.pdf_extractor.extract import process_pdf_files


st.set_page_config(
    page_title="PDF 批量信息提取与 Excel 导出工具",
    page_icon=":page_facing_up:",
    layout="wide",
)

st.title("PDF 批量信息提取与 Excel 导出工具")
st.caption("适用于格式较固定的 PDF 文档整理，可批量提取字段并导出 CSV / Excel。")

with st.expander("使用说明", expanded=True):
    st.markdown(
        """
        1. 上传一个或多个带有文本层的 PDF 文件。
        2. 系统会自动提取常见字段，并在下方表格中预览。
        3. 检查结果后，可下载 CSV 或 Excel 文件。
        4. 如果字段为空，通常需要根据客户样本定制提取规则。
        """
    )

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("适合处理哪些 PDF")
    st.markdown(
        """
        - 发票、订单、合同回执、报名表、对账单
        - 字段名称比较固定的 PDF
        - 可以复制文字的电子 PDF
        - 需要整理成 Excel 的批量文件
        """
    )

with right_col:
    st.subheader("当前默认字段")
    st.markdown(
        """
        - 编号 / 订单号 / 合同号 / 发票号
        - 日期
        - 客户名称 / 公司名称
        - 金额
        - 税号 / 统一社会信用代码
        - 电话、邮箱
        """
    )

st.warning("扫描版 PDF 或图片型 PDF 需要 OCR 升级版，当前基础版不做 OCR。")

uploaded_files = st.file_uploader(
    "上传 PDF 文件",
    type=["pdf"],
    accept_multiple_files=True,
)

if uploaded_files:
    with TemporaryDirectory() as temp_dir:
        pdf_paths: list[Path] = []
        for uploaded_file in uploaded_files:
            safe_name = Path(uploaded_file.name).name
            file_path = Path(temp_dir) / safe_name
            file_path.write_bytes(uploaded_file.getbuffer())
            pdf_paths.append(file_path)

        with st.spinner("正在提取 PDF 信息..."):
            records = process_pdf_files(pdf_paths)
            dataframe = records_to_dataframe(records)

    ok_count = int((dataframe["status"] == "ok").sum())
    failed_count = int((dataframe["status"] != "ok").sum())

    if failed_count:
        st.error(f"已处理 {len(dataframe)} 个文件，其中 {failed_count} 个失败。请查看 error 列。")
        with st.expander("查看失败文件"):
            st.dataframe(
                dataframe.loc[dataframe["status"] != "ok", ["source_file", "error"]],
                use_container_width=True,
            )
    else:
        st.success(f"已成功处理 {ok_count} 个文件。")

    st.subheader("提取结果预览")
    st.dataframe(dataframe, use_container_width=True)

    csv_bytes = dataframe.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    excel_buffer = BytesIO()
    dataframe.to_excel(excel_buffer, index=False)

    download_col_1, download_col_2 = st.columns(2)
    with download_col_1:
        st.download_button(
            "下载 CSV",
            data=csv_bytes,
            file_name="pdf_extract_result.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with download_col_2:
        st.download_button(
            "下载 Excel",
            data=excel_buffer.getvalue(),
            file_name="pdf_extract_result.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
else:
    st.info("请先上传 PDF 文件。建议先用 3-5 份样本测试提取效果。")
