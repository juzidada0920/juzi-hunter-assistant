"""JD 分析页面 —— 输入 JD → AI 生成搜索栏位配置"""

import streamlit as st

from ai.jd_analyzer import analyze_jd
from utils.file_handler import extract_text_from_upload


def _render_search_fields_table(search_fields: list):
    """渲染搜索栏位配置表 —— 核心输出"""
    st.subheader("🔧 搜索栏位配置建议")

    # 表头
    cols = st.columns([1.5, 0.8, 3, 2.5])
    cols[0].markdown("**搜索栏位**")
    cols[1].markdown("**状态**")
    cols[2].markdown("**建议值**")
    cols[3].markdown("**理由**")
    st.divider()

    for item in search_fields:
        field = item.get("field", "")
        enabled = item.get("enabled", False)
        value = item.get("value", "")
        reason = item.get("reason", "")

        cols = st.columns([1.5, 0.8, 3, 2.5])
        cols[0].markdown(f"**{field}**")

        if enabled:
            cols[1].markdown("✅ 设置")
            cols[2].markdown(f"<span style='color:#00c853;font-weight:bold'>{value}</span>", unsafe_allow_html=True)
        else:
            cols[1].markdown("⬜ 不设置")
            cols[2].markdown(f"<span style='color:#888'>—</span>", unsafe_allow_html=True)

        cols[3].markdown(f"<span style='color:#aaa;font-size:0.9em'>{reason}</span>", unsafe_allow_html=True)
        st.divider()


def _render_keywords(keyword_combinations: list):
    """渲染关键词组合策略"""
    st.subheader("🔑 关键词组合策略")
    for combo in keyword_combinations:
        st.markdown(f"- {combo}")


def _render_talent_profile(profile: dict):
    """渲染人才画像卡片"""
    st.subheader("🎯 人才画像")

    col1, col2, col3 = st.columns(3)
    col1.metric("学历要求", profile.get("education", "—"))
    col2.metric("经验年限", profile.get("experience_years", "—"))
    col3.metric("薪资预估", profile.get("salary_estimate", "—"))

    st.markdown(f"**行业背景：** {profile.get('industry_background', '—')}")

    must_skills = profile.get("must_have_skills", [])
    nice_skills = profile.get("nice_to_have_skills", [])

    if must_skills:
        st.markdown("**必备技能：**")
        badges = " ".join(
            f"<span style='background:#1565c0;color:white;padding:2px 10px;border-radius:12px;margin:2px;display:inline-block;font-size:0.85em'>{s}</span>"
            for s in must_skills
        )
        st.markdown(badges, unsafe_allow_html=True)

    if nice_skills:
        st.markdown("**加分技能：**")
        badges = " ".join(
            f"<span style='background:#2e7d32;color:white;padding:2px 10px;border-radius:12px;margin:2px;display:inline-block;font-size:0.85em'>{s}</span>"
            for s in nice_skills
        )
        st.markdown(badges, unsafe_allow_html=True)


def show():
    """JD 分析页面入口"""
    st.title("📋 JD 分析 — 生成搜索策略")
    st.caption("输入岗位 JD，AI 自动生成招聘平台的搜索栏位配置建议")

    # ── 输入区 ──────────────────────────────────────────
    tab1, tab2 = st.tabs(["📝 粘贴 JD 文本", "📎 上传 JD 文件"])

    with tab1:
        jd_text = st.text_area(
            "将 JD 原文粘贴到下方",
            placeholder="例如：\n\n岗位名称：Java 开发工程师\n工作地点：上海\n岗位职责：\n1. 负责公司核心业务系统的设计与开发\n2. ...\n\n任职要求：\n1. 本科及以上学历，计算机相关专业\n2. 3年以上 Java 开发经验\n3. 精通 Spring Cloud 微服务架构\n4. ...",
            height=300,
        )

    with tab2:
        uploaded_file = st.file_uploader(
            "支持 PDF / Word / TXT 格式",
            type=["pdf", "docx", "doc", "txt"],
        )
        jd_text = ""
        if uploaded_file:
            try:
                jd_text = extract_text_from_upload(uploaded_file)
                st.success(f"✅ 已提取文件内容（{len(jd_text)} 字符）")
                with st.expander("预览提取的文本"):
                    st.text(jd_text[:2000] + ("..." if len(jd_text) > 2000 else ""))
            except Exception as e:
                st.error(f"❌ 文件读取失败：{e}")

    # ── 分析按钮 ────────────────────────────────────────
    if st.button("🔍 分析搜索策略", type="primary", use_container_width=True):
        if not jd_text.strip():
            st.warning("⚠️ 请先粘贴 JD 文本或上传文件")
        elif len(jd_text.strip()) < 50:
            st.warning("⚠️ JD 文本过短（少于50字），请检查输入是否完整")
        else:
            with st.spinner("🤖 AI 正在分析 JD，提取搜索策略..."):
                result = analyze_jd(jd_text.strip())

            if "error" in result:
                st.error(f"❌ 分析失败：{result['error']}")
                if "raw_response" in result:
                    with st.expander("查看 AI 原始返回"):
                        st.code(result["raw_response"])
            else:
                st.success("✅ 分析完成！")

                # ── 结果展示 ─────────────────────────────
                st.markdown(f"### 📌 {result.get('position_title', '未知岗位')}")
                st.caption(result.get("position_summary", ""))

                st.divider()

                # 1. 搜索栏位配置表（最核心）
                search_fields = result.get("search_fields", [])
                if search_fields:
                    _render_search_fields_table(search_fields)

                # 2. 关键词组合
                keywords = result.get("keyword_combinations", [])
                if keywords:
                    _render_keywords(keywords)

                # 3. 人才画像
                profile = result.get("talent_profile", {})
                if profile:
                    _render_talent_profile(profile)
