# GitHub 上传步骤

## 1. 检查项目文件

确认项目中包含：

- `README.md`
- `requirements.txt`
- `app.py`
- `main.py`
- `src/`
- `tests/`
- `docs/`
- `data/samples/`
- `sample_outputs/`

## 2. 初始化 Git 仓库

在项目目录运行：

```bash
git init
git add .
git commit -m "Initial PDF info extractor project"
```

## 3. 在 GitHub 创建仓库

进入 GitHub，创建一个新仓库，例如：

```text
pdf-info-extractor
```

建议仓库描述：

```text
Batch extract fields from PDF files and export to Excel/CSV with Python and Streamlit.
```

## 4. 关联远程仓库

将下面地址替换为你自己的 GitHub 仓库地址：

```bash
git remote add origin https://github.com/你的用户名/pdf-info-extractor.git
git branch -M main
git push -u origin main
```

## 5. 上传后检查

上传后检查：

- README 是否能正常显示中文
- 示例截图是否能显示
- `sample_outputs/result.xlsx` 和 `sample_outputs/result.csv` 是否存在
- `requirements.txt` 是否完整
- 不要上传客户真实文件或敏感数据

## 6. 作品集展示建议

可以在仓库首页补充：

- 页面截图
- 示例输入 PDF
- 示例输出 Excel
- 适用场景
- 报价参考
- 后续可升级方向
