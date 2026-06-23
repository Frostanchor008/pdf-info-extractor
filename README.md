# PDF 信息批量提取与 Excel 导出工具

这是一个面向办公自动化接单场景的小型 Python 工具。它可以批量读取 PDF 文件，提取常见业务字段，并导出为 Excel 或 CSV，适合用于发票、订单、合同回执、报名表、对账单等格式相对固定的 PDF 整理工作。

项目提供两种使用方式：

- Streamlit 网页界面：适合给客户演示和非技术用户使用。
- 命令行批处理：适合一次性处理文件夹中的大量 PDF。

## 适用场景

- 客户有几十份或几百份 PDF，需要整理成 Excel。
- PDF 中包含编号、日期、客户名称、金额、电话、邮箱等固定字段。
- 客户希望本地运行，不上传到第三方平台。
- 需求周期短，适合 1-3 天交付的小单。
- 作为 Python / Streamlit / Excel 自动化作品集案例展示。

## 不适合的情况

- 扫描版 PDF、图片型 PDF：当前基础版不做 OCR，需要升级 OCR 版本。
- 字段位置和名称完全不固定：需要先拿样本做规则适配。
- 需要登录系统、绕过验证码、自动投标、自动私信的平台自动化需求。
- 涉及大量敏感隐私数据且客户没有明确授权的场景。

## 功能清单

- 批量上传或批量读取 PDF 文件
- 自动提取 PDF 文本
- 自动识别常见字段
- 提取状态和错误信息提示
- 表格预览
- 导出 CSV
- 导出 Excel
- 提供测试 PDF 和示例导出结果

## 默认提取字段

| 字段 | 说明 |
|---|---|
| source_file | 来源 PDF 文件名 |
| status | 处理状态 |
| page_count | PDF 页数 |
| engine | 使用的文本提取引擎 |
| invoice_no | 编号、订单号、合同号、发票号 |
| date | 日期 |
| customer | 客户名称、公司名称、甲方 |
| amount | 金额、总金额、价税合计 |
| tax_id | 税号、统一社会信用代码 |
| phone | 联系电话、手机号 |
| email | 邮箱 |
| text_preview | 文本预览 |
| error | 错误信息 |

## 可定制字段说明

如果客户提供的 PDF 字段名称不同，可以在 `src/pdf_extractor/extract.py` 中调整正则规则。例如：

- 将“客户名称”改成“供应商名称”
- 增加“项目名称”
- 增加“地址”
- 增加“银行账号”
- 增加“开票人 / 审核人”

接单时建议先向客户要 3-5 份样本 PDF，确认字段名称、页面格式和导出列名后再报价。

## 功能截图位置

## 页面展示

### 首页

![首页](docs/images/homepage.png)

### 提取结果

![提取结果](docs/images/uploaded_result_table.png)

### 导出结果

![导出结果](docs/images/export_area.png)

## 安装依赖

```bash
cd pdf_info_extractor
python -m pip install -r requirements.txt
```

## 生成测试 PDF

```bash
python scripts/make_sample_pdfs.py
```

生成的测试文件在：

```text
data/samples/
```

## 命令行运行

导出 Excel：

```bash
python main.py data/samples --output output/result.xlsx
```

导出 CSV：

```bash
python main.py data/samples --output output/result.csv
```

## Streamlit 网页运行

```bash
streamlit run app.py
```

启动后打开终端提示的本地地址，通常是：

```text
http://localhost:8501
```

## 示例输出

仓库中提供了示例导出文件：

```text
sample_outputs/result.xlsx
sample_outputs/result.csv
```

可以用于 GitHub 展示、客户演示或作品集截图。

## 测试

```bash
python -m pytest -q
```

## 常见问题

### 为什么有些 PDF 提取不到内容？

可能是扫描版 PDF 或图片型 PDF。基础版只能处理有文本层的 PDF，扫描件需要 OCR 升级版。

### 为什么字段为空？

通常是字段名称和默认规则不一致。例如客户 PDF 写的是“供应商”，但工具默认找“客户名称 / 客户 / 甲方”。需要根据样本调整规则。

### 可以处理多少个 PDF？

几十到几百个普通 PDF 通常没有问题。文件很大或页数很多时，建议分批处理。

### 客户文件会上传到互联网吗？

不会。当前版本是本地运行工具，不接入外部 API，不上传客户文件。

### 能不能做成更漂亮的客户版本？

可以。可以增加客户 Logo、固定导出模板、字段配置表、处理进度、打包成 exe 等。

## 报价参考

| 版本 | 适用需求 | 参考报价 |
|---|---|---|
| 基础版 | 固定字段 PDF 转 Excel，字段少，样本规整 | 300-500 元 |
| 定制版 | 增加字段、适配客户样本、优化导出模板 | 500-1000 元 |
| OCR 升级版 | 扫描件识别、图片 PDF 识别 | 800 元起 |
| 批量交付版 | 加界面美化、错误报告、客户操作文档 | 800-1500 元 |

报价前建议确认：PDF 是否为扫描件、字段数量、样本数量、是否需要固定 Excel 模板、是否需要远程部署或打包。

## 合规说明

本项目只处理用户主动提供的本地 PDF 文件，不包含自动登录、自动投标、自动私信、验证码绕过或违反平台规则的自动化行为。
