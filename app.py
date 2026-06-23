from datetime import date
from html import escape

import pandas as pd
import streamlit as st


PROJECTS = [
    "AI SaaS公司",
    "新能源电池公司",
    "医疗器械公司",
    "消费品牌公司",
    "智能制造公司",
    "企业服务平台",
    "半导体材料公司",
    "跨境电商公司",
]

METHODS = ["走访", "电话", "邮件"]
TAGS = ["现金流", "增长", "风险", "运营", "其他"]

TAG_STYLES = {
    "现金流": {"bg": "#DDF8EA", "color": "#097647", "dot": "#21A67A"},
    "增长": {"bg": "#DDF0FF", "color": "#175CD3", "dot": "#2E90FA"},
    "风险": {"bg": "#FFE4E8", "color": "#C01048", "dot": "#F63D68"},
    "运营": {"bg": "#FFF1D6", "color": "#B54708", "dot": "#F79009"},
    "其他": {"bg": "#EEF2F6", "color": "#475467", "dot": "#667085"},
}

PROJECT_META = {
    "AI SaaS公司": {"sector": "企业软件", "stage": "B轮", "manager": "张晨", "status": "重点跟进"},
    "新能源电池公司": {"sector": "新能源", "stage": "C轮", "manager": "李然", "status": "产能爬坡"},
    "医疗器械公司": {"sector": "医疗器械", "stage": "B+轮", "manager": "周宁", "status": "审批跟踪"},
    "消费品牌公司": {"sector": "新消费", "stage": "A轮", "manager": "王予", "status": "渠道复盘"},
    "智能制造公司": {"sector": "高端制造", "stage": "Pre-IPO", "manager": "陈砚", "status": "供应链关注"},
    "企业服务平台": {"sector": "企业服务", "stage": "B轮", "manager": "林珂", "status": "回款跟踪"},
    "半导体材料公司": {"sector": "半导体", "stage": "C轮", "manager": "赵一", "status": "客户验证"},
    "跨境电商公司": {"sector": "跨境零售", "stage": "A+轮", "manager": "沈舟", "status": "库存优化"},
}


def seed_activities() -> list[dict]:
    return [
        {
            "date": "2026-06-21",
            "project": "AI SaaS公司",
            "method": "电话",
            "content": "管理层反馈二季度企业客户续费率提升，新签客户主要来自华东制造业。",
            "tag": "增长",
        },
        {
            "date": "2026-06-08",
            "project": "AI SaaS公司",
            "method": "走访",
            "content": "销售团队完成行业方案拆分，预计下月启动渠道伙伴联合拜访。",
            "tag": "运营",
        },
        {
            "date": "2026-05-19",
            "project": "AI SaaS公司",
            "method": "邮件",
            "content": "公司提交月度经营简报，ARR保持稳定增长，现金消耗低于预算。",
            "tag": "现金流",
        },
        {
            "date": "2026-06-18",
            "project": "新能源电池公司",
            "method": "走访",
            "content": "二期产线设备已到厂，调试进度符合计划，预计三季度释放新增产能。",
            "tag": "运营",
        },
        {
            "date": "2026-05-30",
            "project": "新能源电池公司",
            "method": "电话",
            "content": "核心客户追加订单意向明确，但上游材料价格波动仍需持续跟踪。",
            "tag": "风险",
        },
        {
            "date": "2026-06-16",
            "project": "医疗器械公司",
            "method": "邮件",
            "content": "创新器械注册审批进入补充资料阶段，公司预计两周内完成回复。",
            "tag": "风险",
        },
        {
            "date": "2026-05-25",
            "project": "医疗器械公司",
            "method": "电话",
            "content": "经销商反馈重点医院试用效果良好，术后随访数据正在汇总。",
            "tag": "增长",
        },
        {
            "date": "2026-06-15",
            "project": "消费品牌公司",
            "method": "走访",
            "content": "线下渠道动销改善，华南区域新门店复购表现优于预期。",
            "tag": "增长",
        },
        {
            "date": "2026-06-01",
            "project": "消费品牌公司",
            "method": "电话",
            "content": "达人投放转化下降，团队已暂停低ROI渠道并重排预算。",
            "tag": "运营",
        },
        {
            "date": "2026-06-12",
            "project": "智能制造公司",
            "method": "电话",
            "content": "关键零部件供应周期延长，可能影响部分订单交付节奏。",
            "tag": "风险",
        },
        {
            "date": "2026-05-22",
            "project": "智能制造公司",
            "method": "走访",
            "content": "新自动化产线良率爬坡顺利，单位人工成本环比下降。",
            "tag": "运营",
        },
        {
            "date": "2026-06-10",
            "project": "企业服务平台",
            "method": "邮件",
            "content": "公司完成新一轮组织调整，大客户成功团队改为行业线管理。",
            "tag": "运营",
        },
        {
            "date": "2026-05-28",
            "project": "企业服务平台",
            "method": "电话",
            "content": "回款节奏较上月改善，存量应收账款已有明确催收计划。",
            "tag": "现金流",
        },
        {
            "date": "2026-06-06",
            "project": "半导体材料公司",
            "method": "走访",
            "content": "客户验证批次通过率提升，下一阶段将进入小批量供货谈判。",
            "tag": "增长",
        },
        {
            "date": "2026-05-20",
            "project": "半导体材料公司",
            "method": "邮件",
            "content": "研发费用投入继续增加，管理层确认全年预算不做上调。",
            "tag": "现金流",
        },
        {
            "date": "2026-06-03",
            "project": "跨境电商公司",
            "method": "电话",
            "content": "欧洲仓库存周转天数下降，旺季备货计划已提前启动。",
            "tag": "运营",
        },
        {
            "date": "2026-05-18",
            "project": "跨境电商公司",
            "method": "邮件",
            "content": "平台广告费率上升，管理层正在评估利润率压力。",
            "tag": "风险",
        },
    ]


def init_state() -> None:
    if "activities" not in st.session_state:
        st.session_state.activities = seed_activities()


def activity_frame() -> pd.DataFrame:
    df = pd.DataFrame(st.session_state.activities)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date", ascending=False).reset_index(drop=True)


def tag_badge(tag: str) -> str:
    style = TAG_STYLES[tag]
    return (
        f"<span class='tag-badge' "
        f"style='background:{style['bg']}; color:{style['color']};'>"
        f"<span style='background:{style['dot']};'></span>{tag}</span>"
    )


def render_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --ink: #162033;
            --muted: #667085;
            --line: #d9e4ea;
            --panel: #ffffff;
            --soft: #f6f9fb;
            --teal: #087F8C;
            --mint: #31B88F;
            --coral: #F05D5E;
            --amber: #F6A609;
            --indigo: #4661E6;
        }

        .stApp {
            background:
                radial-gradient(circle at 18% 12%, rgba(49, 184, 143, .16), transparent 28%),
                linear-gradient(135deg, #F7FBFA 0%, #F3F7FF 46%, #FFF8ED 100%);
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1.25rem;
            padding-bottom: 3rem;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .hero {
            overflow: hidden;
            position: relative;
            border-radius: 8px;
            background: linear-gradient(120deg, #12343B 0%, #087F8C 52%, #F6A609 145%);
            padding: 1.3rem 1.45rem;
            color: white;
            box-shadow: 0 18px 45px rgba(18, 52, 59, .16);
            margin-bottom: 1rem;
        }

        .hero:after {
            content: "";
            position: absolute;
            right: -42px;
            top: -78px;
            width: 260px;
            height: 260px;
            border: 1px solid rgba(255, 255, 255, .24);
            transform: rotate(28deg);
        }

        .hero-label {
            display: inline-flex;
            align-items: center;
            gap: .45rem;
            min-height: 28px;
            border-radius: 999px;
            padding: 0 .8rem;
            background: rgba(255, 255, 255, .14);
            color: rgba(255, 255, 255, .92);
            font-size: .86rem;
            font-weight: 700;
            margin-bottom: .7rem;
        }

        .hero h1 {
            position: relative;
            z-index: 1;
            margin: 0;
            font-size: 2rem;
            line-height: 1.18;
            letter-spacing: 0;
        }

        .hero p {
            position: relative;
            z-index: 1;
            max-width: 720px;
            margin: .55rem 0 0;
            color: rgba(255, 255, 255, .82);
            font-size: 1rem;
            line-height: 1.65;
        }

        .summary-row {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .8rem;
            margin: .9rem 0 1rem;
        }

        .summary-item {
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(230, 235, 241, .88);
            border-radius: 8px;
            background: rgba(255, 255, 255, .86);
            padding: 1rem 1.05rem;
            box-shadow: 0 10px 28px rgba(16, 24, 40, .06);
        }

        .summary-item:before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 5px;
            background: var(--card-color);
        }

        .summary-value {
            color: var(--ink);
            font-size: 1.65rem;
            font-weight: 800;
            line-height: 1.15;
        }

        .summary-label {
            color: var(--muted);
            font-size: .86rem;
            margin-top: .2rem;
        }

        .section-title {
            color: var(--ink);
            font-size: 1rem;
            font-weight: 800;
            margin: 1rem 0 .7rem;
            display: flex;
            align-items: center;
            gap: .45rem;
        }

        .section-title:before {
            content: "";
            width: 9px;
            height: 22px;
            border-radius: 999px;
            background: linear-gradient(180deg, var(--teal), var(--amber));
        }

        .insight-card {
            border: 1px solid rgba(230, 235, 241, .9);
            border-radius: 8px;
            background: rgba(255, 255, 255, .9);
            box-shadow: 0 10px 28px rgba(16, 24, 40, .06);
            padding: 1rem;
            margin-top: .05rem;
        }

        .insight-title {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: .8rem;
            margin-bottom: .75rem;
        }

        .insight-title strong {
            color: var(--ink);
            font-size: 1.05rem;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            min-height: 26px;
            border-radius: 999px;
            padding: 0 .75rem;
            background: #E6FBF4;
            color: #087F5B;
            font-size: .82rem;
            font-weight: 800;
            white-space: nowrap;
        }

        .meta-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .55rem;
            margin-bottom: .75rem;
        }

        .meta-box {
            border-radius: 8px;
            background: #F7FAFC;
            padding: .72rem .75rem;
            border: 1px solid #E8EEF4;
        }

        .meta-label {
            color: var(--muted);
            font-size: .78rem;
            margin-bottom: .2rem;
        }

        .meta-value {
            color: var(--ink);
            font-size: .94rem;
            font-weight: 800;
        }

        .tag-strip {
            display: flex;
            flex-wrap: wrap;
            gap: .45rem;
            margin-top: .2rem;
        }

        .timeline {
            position: relative;
            margin-top: .15rem;
        }

        .timeline-item {
            display: grid;
            grid-template-columns: 130px 1fr;
            gap: 1rem;
            position: relative;
            padding: 0 0 1rem;
        }

        .timeline-date {
            color: #35505f;
            font-weight: 800;
            font-size: .92rem;
            padding-top: .8rem;
            text-align: right;
        }

        .timeline-body {
            position: relative;
            border-left: 2px solid var(--line);
            padding-left: 1rem;
        }

        .timeline-body:before {
            content: "";
            width: 12px;
            height: 12px;
            border-radius: 999px;
            background: var(--dot-color);
            border: 3px solid #fff;
            box-shadow: 0 0 0 1px var(--dot-color), 0 0 0 6px rgba(8, 127, 140, .09);
            position: absolute;
            left: -7px;
            top: .95rem;
        }

        .timeline-card {
            border: 1px solid rgba(230, 235, 241, .95);
            border-radius: 8px;
            background: rgba(255, 255, 255, .94);
            padding: .95rem 1rem;
            box-shadow: 0 10px 28px rgba(16, 24, 40, .06);
        }

        .timeline-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: .75rem;
            margin-bottom: .45rem;
        }

        .project-name {
            color: var(--ink);
            font-weight: 700;
            font-size: 1rem;
        }

        .method {
            color: #087F8C;
            background: #E3F7F6;
            border-radius: 999px;
            padding: .18rem .58rem;
            font-weight: 800;
            font-size: .88rem;
            white-space: nowrap;
        }

        .content {
            color: #344054;
            font-size: .95rem;
            line-height: 1.65;
            margin-bottom: .55rem;
        }

        .tag-badge {
            display: inline-flex;
            align-items: center;
            gap: .38rem;
            min-height: 24px;
            border-radius: 999px;
            padding: 0 .7rem;
            font-size: .82rem;
            font-weight: 700;
        }

        .tag-badge span {
            width: 7px;
            height: 7px;
            border-radius: 999px;
            display: inline-block;
        }

        div[data-testid="stForm"] {
            background: rgba(255, 255, 255, .9);
            border: 1px solid rgba(230, 235, 241, .9);
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 10px 28px rgba(16, 24, 40, .06);
        }

        .stButton > button {
            background: linear-gradient(90deg, #087F8C, #31B88F);
            color: white;
            border: 0;
            font-weight: 800;
        }

        .stButton > button:hover {
            color: white;
            border: 0;
            filter: brightness(.98);
        }

        .empty {
            border: 1px dashed #cfd8e3;
            border-radius: 8px;
            padding: 1.2rem;
            color: var(--muted);
            background: var(--soft);
        }

        @media (max-width: 720px) {
            .hero {
                padding: 1.05rem;
            }

            .hero h1 {
                font-size: 1.55rem;
            }

            .summary-row {
                grid-template-columns: 1fr;
            }

            .timeline-item {
                grid-template-columns: 1fr;
                gap: .35rem;
            }

            .timeline-date {
                text-align: left;
                padding-top: 0;
            }

            .meta-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(df: pd.DataFrame) -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-label">Activity Timeline Page Prototype</div>
            <div>
                <h1>投后动态跟踪模块</h1>
                <p>将投后沟通记录结构化为可追踪时间轴，实现动态信息的统一管理与回溯。</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    latest_date = df["date"].max().strftime("%Y-%m-%d") if not df.empty else "-"
    st.markdown(
        f"""
        <div class="summary-row">
            <div class="summary-item" style="--card-color:#087F8C;">
                <div class="summary-value">{df["project"].nunique()}</div>
                <div class="summary-label">覆盖项目</div>
            </div>
            <div class="summary-item" style="--card-color:#F05D5E;">
                <div class="summary-value">{len(df)}</div>
                <div class="summary-label">动态记录</div>
            </div>
            <div class="summary-item" style="--card-color:#F6A609;">
                <div class="summary-value">{latest_date}</div>
                <div class="summary-label">最近更新</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_add_form() -> None:
    st.markdown('<div class="section-title">新增动态记录</div>', unsafe_allow_html=True)

    with st.form("activity_form", clear_on_submit=True):
        col1, col2, col3 = st.columns([1.2, 1, 1])
        with col1:
            project = st.selectbox("项目名称", PROJECTS)
        with col2:
            activity_date = st.date_input("日期", value=date.today())
        with col3:
            method = st.selectbox("沟通方式", METHODS)

        content = st.text_area(
            "动态内容",
            placeholder="例如：管理层反馈重点客户续约顺利，三季度收入确认节奏好于预期。",
            height=110,
        )
        tag = st.radio("标签", TAGS, horizontal=True)
        submitted = st.form_submit_button("添加动态", use_container_width=True)

    if submitted:
        cleaned_content = content.strip()
        if not cleaned_content:
            st.warning("请填写动态内容后再添加。")
            return

        st.session_state.activities.append(
            {
                "date": activity_date.strftime("%Y-%m-%d"),
                "project": project,
                "method": method,
                "content": cleaned_content,
                "tag": tag,
            }
        )
        st.success("已添加新的投后动态记录。")
        st.rerun()


def render_timeline(df: pd.DataFrame, selected_project: str) -> None:
    st.markdown('<div class="section-title">动态时间轴</div>', unsafe_allow_html=True)

    if selected_project != "全部项目":
        df = df[df["project"] == selected_project]

    if df.empty:
        st.markdown(
            '<div class="empty">当前项目暂无动态记录。</div>',
            unsafe_allow_html=True,
        )
        return

    items_html = ['<div class="timeline">']
    for _, row in df.iterrows():
        day = row["date"].strftime("%Y-%m-%d")
        dot_color = TAG_STYLES[row["tag"]]["dot"]
        items_html.append(
            f"""
            <div class="timeline-item">
                <div class="timeline-date">{escape(day)}</div>
                <div class="timeline-body" style="--dot-color:{dot_color};">
                    <div class="timeline-card">
                        <div class="timeline-head">
                            <div class="project-name">{escape(row["project"])}</div>
                            <div class="method">{escape(row["method"])}</div>
                        </div>
                        <div class="content">{escape(row["content"])}</div>
                        {tag_badge(row["tag"])}
                    </div>
                </div>
            </div>
            """
        )
    items_html.append("</div>")
    st.markdown("".join(items_html), unsafe_allow_html=True)


def render_project_snapshot(df: pd.DataFrame, selected_project: str) -> None:
    target = selected_project if selected_project != "全部项目" else df.iloc[0]["project"]
    project_df = df[df["project"] == target]
    meta = PROJECT_META[target]
    latest = project_df.iloc[0] if not project_df.empty else None

    tag_counts = project_df["tag"].value_counts().to_dict()
    tag_html = []
    for tag in TAGS:
        if tag_counts.get(tag, 0):
            tag_html.append(f"{tag_badge(tag)}")

    latest_text = escape(latest["content"]) if latest is not None else "暂无动态记录"
    latest_date = latest["date"].strftime("%Y-%m-%d") if latest is not None else "-"

    st.markdown(
        f"""
        <div class="section-title">项目跟踪画像</div>
        <div class="insight-card">
            <div class="insight-title">
                <strong>{escape(target)}</strong>
                <span class="status-pill">{escape(meta["status"])}</span>
            </div>
            <div class="meta-grid">
                <div class="meta-box">
                    <div class="meta-label">行业</div>
                    <div class="meta-value">{escape(meta["sector"])}</div>
                </div>
                <div class="meta-box">
                    <div class="meta-label">阶段</div>
                    <div class="meta-value">{escape(meta["stage"])}</div>
                </div>
                <div class="meta-box">
                    <div class="meta-label">负责人</div>
                    <div class="meta-value">{escape(meta["manager"])}</div>
                </div>
            </div>
            <div class="meta-box">
                <div class="meta-label">最近动态 · {escape(latest_date)}</div>
                <div class="meta-value">{latest_text}</div>
            </div>
            <div class="tag-strip">{''.join(tag_html) if tag_html else tag_badge("其他")}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(
        page_title="投后动态跟踪模块",
        page_icon="📌",
        layout="wide",
    )
    init_state()
    render_css()

    df = activity_frame()
    render_header(df)

    st.markdown('<div class="section-title">项目选择</div>', unsafe_allow_html=True)
    selected_project = st.selectbox("选择项目", ["全部项目"] + PROJECTS, label_visibility="collapsed")

    left, right = st.columns([1.08, .92], gap="large")
    with left:
        render_add_form()
    with right:
        render_project_snapshot(activity_frame(), selected_project)

    render_timeline(activity_frame(), selected_project)


if __name__ == "__main__":
    main()
