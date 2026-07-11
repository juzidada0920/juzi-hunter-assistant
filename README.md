# 猎头智能辅助系统（Juzi Hunter Assistant）

面向猎头顾问的桌面端智能辅助工具，将 AI 能力嵌入简历筛选和候选人管理两个核心环节。

## 技术栈

- **界面**：Streamlit（纯 Python）
- **数据库**：SQLite
- **AI 引擎**：Claude API
- **文件处理**：PyMuPDF / python-docx

## 项目结构

```
juzi-hunter-assistant/
├── app.py                  # Streamlit 入口
├── config.py               # 全局配置
├── ai/                     # AI 分析层
├── db/                     # 数据库层
├── ui/                     # Streamlit 页面
├── utils/                  # 工具层
├── samples/                # 示例数据
└── tests/                  # 测试
```

## 快速开始

```bash
pip install -r requirements.txt
streamlit run app.py
```
