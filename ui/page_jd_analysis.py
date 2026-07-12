"""JD 分析页面 —— 输入 JD → AI 生成搜索栏位配置"""

import streamlit as st

from ai.jd_analyzer import analyze_jd
from db.connection import init_db
from db.jd_dao import delete, get_by_id, list_all, save
from utils.file_handler import extract_text_from_upload


# ── 渲染函数 ──────────────────────────────────────────────────


def _render_hard_filters(hard_filters: dict):
    """渲染硬性筛选条件 — 一票否决项，页面最顶部"""
    st.subheader("🚫 硬性筛选条件")

    summary = hard_filters.get("summary", "")
    if summary:
        st.markdown(f"> 🔴 **{summary}**")

    items = hard_filters.get("items", [])
    if items:
        cols = st.columns(len(items))
        for i, item in enumerate(items):
            condition = item.get("condition", "")
            requirement = item.get("requirement", "")
            note = item.get("note", "")

            with cols[i]:
                st.markdown(
                    f"<div style='text-align:center;padding:8px 0'>"
                    f"<span style='font-size:0.75em;color:#888'>{condition}</span><br>"
                    f"<span style='font-size:1.1em;font-weight:700;color:#d32f2f'>{requirement}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                if note:
                    st.caption(note)
        st.divider()


def _render_search_fields_table(search_fields: list):
    """渲染搜索栏位配置表"""
    st.subheader("🔧 搜索栏位配置建议")

    cols = st.columns([1.3, 0.7, 3.5, 2.5])
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

        cols = st.columns([1.3, 0.7, 3.5, 2.5])
        cols[0].markdown(f"**{field}**")

        if enabled:
            cols[1].markdown("✅ 设置")
            cols[2].markdown(
                f"<span style='color:#00c853;font-weight:bold;font-size:0.9em'>{value}</span>",
                unsafe_allow_html=True,
            )
        else:
            cols[1].markdown("⬜ 不设置")
            cols[2].markdown("<span style='color:#888'>—</span>", unsafe_allow_html=True)

        cols[3].markdown(
            f"<span style='color:#888;font-size:0.8em'>{reason}</span>",
            unsafe_allow_html=True,
        )
        st.divider()


def _render_keywords(keyword_combinations: list):
    """渲染关键词组合策略 — badge 标签样式"""
    st.subheader("🔑 关键词组合策略")
    badges = []
    for combo in keyword_combinations:
        badge = (
            f"<span style='"
            f"background:#1565c0;color:white;"
            f"padding:4px 14px;border-radius:14px;margin:3px;"
            f"display:inline-block;font-size:0.85em;line-height:1.5'"
            f">{combo}</span>"
        )
        badges.append(badge)
    st.markdown(" ".join(badges), unsafe_allow_html=True)


def _render_talent_profile(profile: dict):
    """渲染人才画像 — 使用原生 Streamlit 组件，自动适配主题"""
    st.subheader("🎯 人才画像")

    col1, col2, col3 = st.columns(3)
    col1.caption("学历要求")
    col1.markdown(f"**{profile.get('education', '—')}**")
    col2.caption("经验年限")
    col2.markdown(f"**{profile.get('experience_years', '—')}**")
    col3.caption("薪资预估")
    col3.markdown(f"**{profile.get('salary_estimate', '—')}**")

    salary_info = profile.get("salary_info", {})
    if salary_info and any(salary_info.values()):
        with st.expander("💰 薪资结构详情"):
            if salary_info.get("range"):
                st.markdown(f"**范围：** {salary_info['range']}")
            if salary_info.get("structure"):
                st.markdown(f"**结构：** {salary_info['structure']}")
            if salary_info.get("bonus"):
                st.markdown(f"**奖金/股权：** {salary_info['bonus']}")

    industry = profile.get("industry_background", "")
    if industry:
        st.caption(f"行业背景：{industry}")

    must_skills = profile.get("must_have_skills", [])
    nice_skills = profile.get("nice_to_have_skills", [])

    if must_skills:
        st.caption("必备技能：")
        badges = " ".join(
            f"<span style='background:#1565c0;color:white;padding:2px 10px;"
            f"border-radius:12px;margin:2px;display:inline-block;font-size:0.8em'>{s}</span>"
            for s in must_skills
        )
        st.markdown(badges, unsafe_allow_html=True)

    if nice_skills:
        st.caption("加分技能：")
        badges = " ".join(
            f"<span style='background:#2e7d32;color:white;padding:2px 10px;"
            f"border-radius:12px;margin:2px;display:inline-block;font-size:0.8em'>{s}</span>"
            for s in nice_skills
        )
        st.markdown(badges, unsafe_allow_html=True)


def _render_talent_source(source: dict):
    """渲染人才来源策略"""
    if not source:
        return

    st.subheader("🏢 人才来源 — 从哪挖人")

    strategy = source.get("strategy", "")
    if strategy:
        st.info(f"💡 **策略：** {strategy}")

    companies = source.get("target_companies", [])
    if companies:
        type_colors = {
            "直接竞品": "red",
            "上游供应商": "blue",
            "下游客户": "green",
            "同赛道": "orange",
            "JD指定": "violet",
        }

        for c in companies:
            name = c.get("name", "—")
            ctype = c.get("type", "")
            reason = c.get("reason", "")

            tag_color = type_colors.get(ctype, "gray")

            with st.container(border=True):
                st.markdown(f"**{name}**  `:{tag_color}[{ctype}]`")
                if reason:
                    st.caption(f"— {reason}")


def _render_full_result(result: dict):
    """渲染完整分析结果（复用所有渲染函数）"""
    st.markdown(f"### 📌 {result.get('position_title', '未知岗位')}")
    st.caption(result.get("position_summary", ""))

    st.divider()

    hard_filters = result.get("hard_filters", {})
    if hard_filters:
        _render_hard_filters(hard_filters)

    search_fields = result.get("search_fields", [])
    if search_fields:
        _render_search_fields_table(search_fields)

    keywords = result.get("keyword_combinations", [])
    if keywords:
        _render_keywords(keywords)

    profile = result.get("talent_profile", {})
    if profile:
        _render_talent_profile(profile)

    talent_source = result.get("talent_source", {})
    if talent_source:
        _render_talent_source(talent_source)


# ── 页面入口 ──────────────────────────────────────────────────


def show():
    """JD 分析页面入口"""
    init_db()

    # 初始化 session_state
    if "viewing_history_id" not in st.session_state:
        st.session_state.viewing_history_id = None
    if "current_result" not in st.session_state:
        st.session_state.current_result = None

    st.title("📋 JD 分析 — 生成搜索策略")
    st.caption("输入岗位 JD，AI 自动生成招聘平台的搜索栏位配置建议")

    # ── 两栏布局 ──────────────────────────────────────
    left, right = st.columns([1, 3])

    # ── 左栏：历史记录 ────────────────────────────────
    with left:
        st.subheader("📂 历史记录")

        if st.button("➕ 新建分析", use_container_width=True):
            st.session_state.viewing_history_id = None
            st.session_state.current_result = None
            st.rerun()

        st.divider()

        records = list_all()
        if not records:
            st.caption("暂无历史记录")

        for r in records:
            c1, c2 = st.columns([3.5, 1])
            with c1:
                label = f"**{r['title']}**\n{r['created_at'][:10]}"
                if st.button(
                    label,
                    key=f"hist_{r['id']}",
                    use_container_width=True,
                    help=f"查看 {r['title']} 的分析结果",
                ):
                    st.session_state.viewing_history_id = r["id"]
                    st.session_state.current_result = None
                    st.rerun()
            with c2:
                if st.button("🗑️", key=f"del_{r['id']}", help="删除此记录"):
                    delete(r["id"])
                    if st.session_state.viewing_history_id == r["id"]:
                        st.session_state.viewing_history_id = None
                        st.session_state.current_result = None
                    st.rerun()

    # ── 右栏：内容区 ──────────────────────────────────
    with right:
        viewing_id = st.session_state.viewing_history_id

        # 状态 A：查看历史记录
        if viewing_id is not None:
            record = get_by_id(viewing_id)
            if record:
                st.success(
                    f"📂 历史记录 · {record['title']} · {record['created_at'][:10]}"
                )
                _render_full_result(record["result"])
            else:
                st.error("记录不存在或已被删除")
                st.session_state.viewing_history_id = None
                st.rerun()
            return  # 查看历史时不显示输入区

        # 状态 B：显示上次分析结果（如果有）
        if st.session_state.current_result is not None:
            st.success("✅ 已保存到历史记录")
            _render_full_result(st.session_state.current_result)
            st.divider()
            # 继续显示输入区（让用户可以直接分析下一个 JD）

        # ── 输入区（始终显示，除非在查看历史） ─────────
        tab1, tab2 = st.tabs(["📝 粘贴 JD 文本", "📎 上传 JD 文件"])

        with tab1:
            jd_text = st.text_area(
                "将 JD 原文粘贴到下方",
                placeholder=(
                    "例如：\n\n岗位名称：Java 开发工程师\n工作地点：上海\n"
                    "岗位职责：\n1. 负责公司核心业务系统的设计与开发\n2. ...\n\n"
                    "任职要求：\n1. 本科及以上学历，计算机相关专业\n"
                    "2. 3年以上 Java 开发经验\n3. 精通 Spring Cloud 微服务架构\n4. ..."
                ),
                height=250,
            )

        with tab2:
            uploaded_file = st.file_uploader(
                "支持 PDF / Word / TXT 格式",
                type=["pdf", "docx", "doc", "txt"],
            )
            if uploaded_file:
                try:
                    jd_text = extract_text_from_upload(uploaded_file)
                    st.success(f"✅ 已提取文件内容（{len(jd_text)} 字符）")
                    with st.expander("预览提取的文本"):
                        st.text(jd_text[:2000] + ("..." if len(jd_text) > 2000 else ""))
                except Exception as e:
                    st.error(f"❌ 文件读取失败：{e}")

        # ── 分析按钮 ────────────────────────────────────
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
                    # 自动保存
                    title = result.get("position_title", "未知岗位")
                    save(title, jd_text.strip(), result)

                    # 存入 session_state 展示结果
                    st.session_state.current_result = result
                    st.session_state.viewing_history_id = None
                    st.rerun()
