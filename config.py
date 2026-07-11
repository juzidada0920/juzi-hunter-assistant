"""全局配置模块"""

import os
import sys

import streamlit as st

# ── Claude API 配置 ──────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# JD 分析推荐用 Haiku：结构化提取任务，能力足够，成本约为 Sonnet 的 1/10
MODEL = os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001")

# ── 数据库路径 ───────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "headhunter.db")

# ── 启动校验 ─────────────────────────────────────────────────
def validate():
    """校验必要配置，未通过时给出中文提示。"""
    if not ANTHROPIC_API_KEY:
        st.error(
            "❌ 未检测到 ANTHROPIC_API_KEY 环境变量。\n\n"
            "请先设置你的 Claude API Key：\n\n"
            "```bash\n"
            "# Windows CMD:\n"
            "set ANTHROPIC_API_KEY=sk-ant-xxx\n\n"
            "# Windows PowerShell:\n"
            "$env:ANTHROPIC_API_KEY=\"sk-ant-xxx\"\n"
            "```\n\n"
            "设置后重新启动应用即可。"
        )
        st.stop()
