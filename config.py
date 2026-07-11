"""全局配置模块"""

import os
import sys

from dotenv import load_dotenv

# 加载 .env 文件（优先于系统环境变量）
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

import streamlit as st

# ── DeepSeek API 配置 ───────────────────────────────────────
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# deepseek-chat = DeepSeek-V3（性价比最高，中文能力强）
MODEL = os.getenv("LLM_MODEL", "deepseek-chat")

# ── 数据库路径 ───────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "headhunter.db")

# ── 启动校验 ─────────────────────────────────────────────────
def validate():
    """校验必要配置，未通过时给出中文提示。"""
    if not DEEPSEEK_API_KEY:
        st.error(
            "❌ 未检测到 DEEPSEEK_API_KEY 环境变量。\n\n"
            "请先在 `.env` 文件中设置你的 DeepSeek API Key：\n\n"
            "```\nDEEPSEEK_API_KEY=sk-xxx\n```\n\n"
            "获取地址：https://platform.deepseek.com/api_keys"
        )
        st.stop()
