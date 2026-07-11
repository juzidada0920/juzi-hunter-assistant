"""猎头智能辅助系统 —— Streamlit 入口"""

import os
import sys

# 将项目根目录加入 PATH，确保模块可 import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

import config

# ── 页面全局配置 ─────────────────────────────────────────────
st.set_page_config(
    page_title="猎头智能辅助系统",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 启动校验 ─────────────────────────────────────────────────
config.validate()

# ── 侧边栏导航 ───────────────────────────────────────────────
st.sidebar.title("🎯 猎头智能辅助系统")
st.sidebar.caption("v0.1 · 大瀚专用")

page = st.sidebar.radio(
    "功能导航",
    options=["📋 JD分析", "📄 简历筛选", "👤 候选人管理", "📊 数据看板"],
    index=0,
)

st.sidebar.divider()
st.sidebar.caption(f"AI 引擎：DeepSeek ({config.MODEL})")

# ── 页面路由 ─────────────────────────────────────────────────
if page == "📋 JD分析":
    from ui.page_jd_analysis import show
    show()
elif page == "📄 简历筛选":
    st.info("🚧 简历筛选功能开发中，敬请期待...")
elif page == "👤 候选人管理":
    st.info("🚧 候选人管理功能开发中，敬请期待...")
elif page == "📊 数据看板":
    st.info("🚧 数据看板功能开发中，敬请期待...")
