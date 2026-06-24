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

PROJECT_META = {
    "AI SaaS公司": {"sector": "企业软件", "stage": "B轮"},
    "新能源电池公司": {"sector": "新能源", "stage": "C轮"},
    "医疗器械公司": {"sector": "医疗器械", "stage": "B+轮"},
    "消费品牌公司": {"sector": "新消费", "stage": "A轮"},
    "智能制造公司": {"sector": "高端制造", "stage": "Pre-IPO"},
    "企业服务平台": {"sector": "企业服务", "stage": "B轮"},
    "半导体材料公司": {"sector": "半导体", "stage": "C轮"},
    "跨境电商公司": {"sector": "跨境零售", "stage": "A+轮"},
}

JUDGEMENT_OPTIONS = {
    "利好": ["订单突破", "客户导入", "融资", "收入增长", "产能释放"],
    "风险": ["客户停产", "业绩下滑", "诉讼", "供应链", "回款压力"],
    "业务发现": ["业务机会", "战略合作", "新市场", "产品延展"],
    "中性": ["公司正常运营", "常规事项", "例行沟通"],
}

JUDGEMENT_STYLES = {
    "利好": {"bg": "#E6F7ED", "fg": "#087443", "dot": "#18A058"},
    "业务发现": {"bg": "#E7F8F2", "fg": "#08745C", "dot": "#20B486"},
    "风险": {"bg": "#FFE8EC", "fg": "#B4234A", "dot": "#EF476F"},
    "中性": {"bg": "#EEF2F6", "fg": "#475467", "dot": "#667085"},
}

JUDGEMENT_PRIORITY = ["风险", "利好", "业务发现", "中性"]


def judgement(category: str, item: str) -> dict:
    return {"category": category, "item": item}


def seed_activities() -> list[dict]:
    return [
        {
            "date": "2026-06-21",
            "project": "AI SaaS公司",
            "method": "电话",
            "content": "管理层反馈二季度企业客户续费率提升，新签客户主要来自华东制造业。",
            "judgements": [judgement("利好", "收入增长"), judgement("利好", "客户导入")],
            "judgement_note": "续费和新签客户均有改善，可继续跟踪大客户转化质量。",
        },
        {
            "date": "2026-06-08",
            "project": "AI SaaS公司",
            "method": "走访",
            "content": "销售团队完成行业方案拆分，预计下月启动渠道伙伴联合拜访。",
            "judgements": [judgement("业务发现", "业务机会"), judgement("中性", "常规事项")],
            "judgement_note": "渠道联合拜访可能带来新增行业线索。",
        },
        {
            "date": "2026-06-18",
            "project": "新能源电池公司",
            "method": "走访",
            "content": "二期产线设备已到厂，调试进度符合计划，预计三季度释放新增产能。",
            "judgements": [judgement("利好", "产能释放")],
            "judgement_note": "产能节点符合预期，需关注后续订单消化。",
        },
        {
            "date": "2026-05-30",
            "project": "新能源电池公司",
            "method": "电话",
            "content": "核心客户追加订单意向明确，但上游材料价格波动仍需持续跟踪。",
            "judgements": [judgement("利好", "订单突破"), judgement("风险", "供应链")],
            "judgement_note": "订单侧积极，但成本端波动可能影响毛利。",
        },
        {
            "date": "2026-06-16",
            "project": "医疗器械公司",
            "method": "邮件",
            "content": "创新器械注册审批进入补充资料阶段，公司预计两周内完成回复。",
            "judgements": [judgement("风险", "业绩下滑")],
            "judgement_note": "审批进度存在不确定性，可能影响商业化节奏。",
        },
        {
            "date": "2026-05-25",
            "project": "医疗器械公司",
            "method": "电话",
            "content": "经销商反馈重点医院试用效果良好，术后随访数据正在汇总。",
            "judgements": [judgement("利好", "客户导入"), judgement("业务发现", "新市场")],
            "judgement_note": "医院试用反馈积极，可跟踪重点科室转化。",
        },
        {
            "date": "2026-06-15",
            "project": "消费品牌公司",
            "method": "走访",
            "content": "线下渠道动销改善，华南区域新门店复购表现优于预期。",
            "judgements": [judgement("利好", "收入增长")],
            "judgement_note": "渠道复购改善，有利于验证线下模型。",
        },
        {
            "date": "2026-06-01",
            "project": "消费品牌公司",
            "method": "电话",
            "content": "达人投放转化下降，团队已暂停低ROI渠道并重排预算。",
            "judgements": [judgement("风险", "业绩下滑")],
            "judgement_note": "投放效率下降，需要观察调整后的获客成本。",
        },
        {
            "date": "2026-06-12",
            "project": "智能制造公司",
            "method": "电话",
            "content": "关键零部件供应周期延长，可能影响部分订单交付节奏。",
            "judgements": [judgement("风险", "供应链")],
            "judgement_note": "交付风险上升，需跟踪替代供应商进展。",
        },
        {
            "date": "2026-05-22",
            "project": "智能制造公司",
            "method": "走访",
            "content": "新自动化产线良率爬坡顺利，单位人工成本环比下降。",
            "judgements": [judgement("利好", "产能释放"), judgement("业务发现", "产品延展")],
            "judgement_note": "效率改善明显，后续可关注规模化复制。",
        },
        {
            "date": "2026-06-10",
            "project": "企业服务平台",
            "method": "邮件",
            "content": "公司完成新一轮组织调整，大客户成功团队改为行业线管理。",
            "judgements": [judgement("中性", "公司正常运营")],
            "judgement_note": "属于常规管理动作，后续观察客户续费效果。",
        },
        {
            "date": "2026-05-28",
            "project": "企业服务平台",
            "method": "电话",
            "content": "回款节奏较上月改善，存量应收账款已有明确催收计划。",
            "judgements": [judgement("利好", "融资"), judgement("业务发现", "业务机会")],
            "judgement_note": "现金回收改善，有助于缓解短期资金压力。",
        },
        {
            "date": "2026-06-06",
            "project": "半导体材料公司",
            "method": "走访",
            "content": "客户验证批次通过率提升，下一阶段将进入小批量供货谈判。",
            "judgements": [judgement("利好", "客户导入"), judgement("业务发现", "战略合作")],
            "judgement_note": "客户验证接近商业化节点，是后续重点跟踪事项。",
        },
        {
            "date": "2026-05-20",
            "project": "半导体材料公司",
            "method": "邮件",
            "content": "研发费用投入继续增加，管理层确认全年预算不做上调。",
            "judgements": [judgement("中性", "常规事项")],
            "judgement_note": "投入节奏仍在预算内，暂未形成明显风险。",
        },
        {
            "date": "2026-06-03",
            "project": "跨境电商公司",
            "method": "电话",
            "content": "欧洲仓库存周转天数下降，旺季备货计划已提前启动。",
            "judgements": [judgement("利好", "收入增长")],
            "judgement_note": "库存效率改善，可继续观察旺季销售兑现。",
        },
        {
            "date": "2026-05-18",
            "project": "跨境电商公司",
            "method": "邮件",
            "content": "平台广告费率上升，管理层正在评估利润率压力。",
            "judgements": [judgement("风险", "业绩下滑")],
            "judgement_note": "获客成本上升可能压缩利润率。",
        },
    ]


def init_state() -> None:
    if "activities" not in st.session_state:
        st.session_state.activities = seed_activities()


def get_frame() -> pd.DataFrame:
    df = pd.DataFrame(st.session_state.activities)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date", ascending=False).reset_index(drop=True)


def primary_judgement(judgements: list[dict]) -> str:
    categories = {item["category"] for item in judgements}
    for category in JUDGEMENT_PRIORITY:
        if category in categories:
            return category
    return "中性"


def judgement_badges(judgements: list[dict]) -> str:
    badges = []
    for item in judgements:
        category = item["category"]
        style = JUDGEMENT_STYLES[category]
        badges.append(
            f"<span class='judgement-badge' style='background:{style['bg']}; color:{style['fg']}'>"
            f"<i style='background:{style['dot']}'></i>"
            f"{escape(category)} · {escape(item['item'])}</span>"
        )
    return "".join(badges)


def css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --ink: #172033;
            --muted: #667085;
            --line: #D8E1EA;
            --panel: rgba(255, 255, 255, .93);
            --teal: #087F8C;
            --green: #18A058;
            --amber: #E79B15;
            --red: #EF476F;
        }

        .stApp {
            background: linear-gradient(135deg, #F7FAFC 0%, #EEF7F5 48%, #FFF8EC 100%);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1.35rem;
            padding-bottom: 3rem;
        }

        .hero {
            border-radius: 8px;
            background: linear-gradient(120deg, #11363D 0%, #087F8C 65%, #E79B15 130%);
            color: white;
            padding: 1.25rem 1.45rem;
            margin-bottom: .9rem;
            box-shadow: 0 18px 42px rgba(16, 43, 50, .15);
        }

        .hero-label {
            display: inline-flex;
            min-height: 26px;
            align-items: center;
            border-radius: 999px;
            background: rgba(255, 255, 255, .14);
            color: rgba(255, 255, 255, .92);
            padding: 0 .75rem;
            font-weight: 700;
            font-size: .82rem;
            margin-bottom: .55rem;
        }

        .hero h1 {
            margin: 0;
            font-size: 2rem;
            line-height: 1.2;
            letter-spacing: 0;
        }

        .hero p {
            max-width: 820px;
            margin: .55rem 0 0;
            color: rgba(255, 255, 255, .84);
            line-height: 1.65;
            font-size: 1rem;
        }

        .section-title {
            display: flex;
            align-items: center;
            gap: .5rem;
            color: var(--ink);
            font-weight: 800;
            font-size: 1rem;
            margin: .9rem 0 .6rem;
        }

        .section-title:before {
            content: "";
            width: 8px;
            height: 20px;
            border-radius: 999px;
            background: linear-gradient(180deg, var(--teal), var(--amber));
        }

        .assist-note {
            border-left: 3px solid var(--teal);
            background: rgba(255, 255, 255, .66);
            color: #475467;
            padding: .65rem .8rem;
            margin: .75rem 0 .1rem;
            border-radius: 0 8px 8px 0;
            font-size: .92rem;
            line-height: 1.55;
        }

        div[data-testid="stForm"] {
            background: var(--panel);
            border: 1px solid #E4EBF2;
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 10px 26px rgba(16, 24, 40, .06);
        }

        .stButton > button {
            background: linear-gradient(90deg, var(--teal), var(--green));
            color: white;
            border: 0;
            font-weight: 800;
        }

        .stButton > button:hover {
            color: white;
            border: 0;
            filter: brightness(.98);
        }

        .info-card {
            background: var(--panel);
            border: 1px solid #E4EBF2;
            border-radius: 8px;
            padding: .9rem;
            box-shadow: 0 10px 26px rgba(16, 24, 40, .06);
        }

        .project-title {
            color: var(--ink);
            font-size: 1.04rem;
            font-weight: 800;
            margin-bottom: .65rem;
        }

        .info-row {
            display: grid;
            grid-template-columns: 72px 1fr;
            gap: .55rem;
            padding: .48rem 0;
            border-top: 1px solid #EDF2F6;
        }

        .info-label {
            color: var(--muted);
            font-size: .86rem;
        }

        .info-value {
            color: var(--ink);
            font-weight: 700;
            font-size: .9rem;
        }

        .legend {
            display: flex;
            flex-wrap: wrap;
            gap: .45rem;
            margin-top: .65rem;
        }

        .timeline-shell {
            background: rgba(255, 255, 255, .58);
            border: 1px solid rgba(228, 235, 242, .9);
            border-radius: 8px;
            padding: 1rem 1rem .15rem;
            box-shadow: 0 14px 34px rgba(16, 24, 40, .07);
        }

        .timeline-item {
            display: grid;
            grid-template-columns: 128px 1fr;
            gap: 1rem;
            min-height: 96px;
        }

        .time {
            color: #344054;
            font-size: .92rem;
            font-weight: 800;
            text-align: right;
            padding-top: .82rem;
        }

        .rail {
            position: relative;
            border-left: 2px solid var(--line);
            padding: 0 0 1rem 1rem;
        }

        .rail:before {
            content: "";
            width: 13px;
            height: 13px;
            border-radius: 50%;
            background: var(--dot);
            border: 3px solid #fff;
            box-shadow: 0 0 0 1px var(--dot), 0 0 0 6px rgba(8, 127, 140, .08);
            position: absolute;
            top: .9rem;
            left: -7.5px;
        }

        .event {
            background: #fff;
            border: 1px solid #E5ECF3;
            border-left: 5px solid var(--dot);
            border-radius: 8px;
            padding: .9rem 1rem;
            box-shadow: 0 8px 20px rgba(16, 24, 40, .05);
        }

        .event-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: .75rem;
            margin-bottom: .45rem;
        }

        .event-project {
            color: var(--ink);
            font-weight: 800;
            font-size: 1rem;
        }

        .method {
            display: inline-flex;
            align-items: center;
            min-height: 25px;
            border-radius: 999px;
            padding: 0 .65rem;
            background: #E4F7F5;
            color: var(--teal);
            font-size: .82rem;
            font-weight: 800;
            white-space: nowrap;
        }

        .event-content {
            color: #344054;
            line-height: 1.65;
            font-size: .95rem;
            margin-bottom: .55rem;
        }

        .judgement-note {
            color: #475467;
            background: #F7FAFC;
            border-radius: 8px;
            padding: .58rem .7rem;
            font-size: .88rem;
            line-height: 1.55;
            margin: .45rem 0 .6rem;
        }

        .judgement-row {
            display: flex;
            flex-wrap: wrap;
            gap: .42rem;
        }

        .judgement-badge {
            display: inline-flex;
            align-items: center;
            gap: .38rem;
            min-height: 24px;
            border-radius: 999px;
            padding: 0 .68rem;
            font-size: .8rem;
            font-weight: 800;
            white-space: nowrap;
        }

        .judgement-badge i {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            display: inline-block;
        }

        .empty {
            background: rgba(255, 255, 255, .75);
            border: 1px dashed #B8C7D4;
            border-radius: 8px;
            color: var(--muted);
            padding: 1rem;
        }

        @media (max-width: 760px) {
            .hero {
                padding: 1rem;
            }

            .hero h1 {
                font-size: 1.55rem;
            }

            .timeline-item {
                grid-template-columns: 1fr;
                gap: .3rem;
            }

            .time {
                text-align: left;
                padding-top: 0;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-label">Post-Investment Activity Timeline Prototype</div>
            <h1>投后动态跟踪模块</h1>
            <p>将投资经理的投后沟通记录结构化为时间轴，并加入投后判断字段，支持利好、风险、业务发现和中性事项的多维记录与回溯。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_project_info(df: pd.DataFrame, selected_project: str) -> None:
    project = selected_project if selected_project != "全部项目" else df.iloc[0]["project"]
    meta = PROJECT_META[project]
    count = len(df[df["project"] == project])

    st.markdown('<div class="section-title">项目基础信息</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="info-card">
            <div class="project-title">{escape(project)}</div>
            <div class="info-row">
                <div class="info-label">行业</div>
                <div class="info-value">{escape(meta["sector"])}</div>
            </div>
            <div class="info-row">
                <div class="info-label">阶段</div>
                <div class="info-value">{escape(meta["stage"])}</div>
            </div>
            <div class="info-row">
                <div class="info-label">记录数</div>
                <div class="info-value">{count} 条动态</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def collect_judgements() -> list[dict]:
    st.markdown("投后判断（可多选）")
    selected: list[dict] = []

    col1, col2 = st.columns(2)
    with col1:
        good = st.multiselect("利好", JUDGEMENT_OPTIONS["利好"])
        discovery = st.multiselect("业务发现", JUDGEMENT_OPTIONS["业务发现"])
    with col2:
        risk = st.multiselect("风险", JUDGEMENT_OPTIONS["风险"])
        neutral = st.multiselect("中性", JUDGEMENT_OPTIONS["中性"])

    for item in good:
        selected.append(judgement("利好", item))
    for item in risk:
        selected.append(judgement("风险", item))
    for item in discovery:
        selected.append(judgement("业务发现", item))
    for item in neutral:
        selected.append(judgement("中性", item))
    return selected


def render_form() -> None:
    st.markdown('<div class="section-title">新增动态记录</div>', unsafe_allow_html=True)

    with st.form("activity_form", clear_on_submit=True):
        project = st.selectbox("项目名称", PROJECTS)
        col1, col2 = st.columns(2)
        with col1:
            activity_date = st.date_input("日期", value=date.today())
        with col2:
            method = st.selectbox("沟通方式", METHODS)

        content = st.text_area(
            "动态内容",
            placeholder="例如：管理层反馈重点客户续约顺利，三季度收入确认节奏好于预期。",
            height=100,
        )

        selected_judgements = collect_judgements()
        judgement_note = st.text_area(
            "投后判断补充",
            placeholder="例如：订单侧有积极信号，但仍需观察交付和回款兑现情况。",
            height=86,
        )
        submitted = st.form_submit_button("添加动态", use_container_width=True)

    if submitted:
        if not content.strip():
            st.warning("请先填写动态内容。")
            return
        if not selected_judgements:
            st.warning("请至少选择一个投后判断。")
            return

        st.session_state.activities.append(
            {
                "date": activity_date.strftime("%Y-%m-%d"),
                "project": project,
                "method": method,
                "content": content.strip(),
                "judgements": selected_judgements,
                "judgement_note": judgement_note.strip(),
            }
        )
        st.success("已添加到时间轴。")
        st.rerun()


def render_timeline(df: pd.DataFrame, selected_project: str) -> None:
    if selected_project != "全部项目":
        df = df[df["project"] == selected_project]

    st.markdown('<div class="section-title">动态时间轴</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="assist-note">核心展示区：每条记录都是一次投后沟通事件，颜色来自投资经理勾选的投后判断。利好/业务发现为绿色，风险为红色，中性为灰色。</div>',
        unsafe_allow_html=True,
    )

    legend = "".join(
        f"{judgement_badges([judgement(category, '示例')])}"
        for category in ["利好", "业务发现", "风险", "中性"]
    )
    st.markdown(f'<div class="legend">{legend}</div>', unsafe_allow_html=True)

    if df.empty:
        st.markdown('<div class="empty">当前项目暂无动态记录。</div>', unsafe_allow_html=True)
        return

    html = ['<div class="timeline-shell">']
    for _, row in df.iterrows():
        category = primary_judgement(row["judgements"])
        dot = JUDGEMENT_STYLES[category]["dot"]
        note = row.get("judgement_note", "")
        note_html = (
            f'<div class="judgement-note">判断补充：{escape(note)}</div>' if note else ""
        )
        html.append(
            f"""
            <div class="timeline-item">
                <div class="time">{row["date"].strftime("%Y-%m-%d")}</div>
                <div class="rail" style="--dot:{dot};">
                    <div class="event" style="--dot:{dot};">
                        <div class="event-head">
                            <div class="event-project">{escape(row["project"])}</div>
                            <div class="method">{escape(row["method"])}</div>
                        </div>
                        <div class="event-content">{escape(row["content"])}</div>
                        {note_html}
                        <div class="judgement-row">{judgement_badges(row["judgements"])}</div>
                    </div>
                </div>
            </div>
            """
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(page_title="投后动态跟踪模块", page_icon="📌", layout="wide")
    init_state()
    css()
    render_header()

    df = get_frame()
    st.markdown('<div class="section-title">项目选择</div>', unsafe_allow_html=True)
    selected_project = st.selectbox("选择项目", ["全部项目"] + PROJECTS, label_visibility="collapsed")

    form_col, info_col = st.columns([1.3, .7], gap="large")
    with form_col:
        render_form()
    with info_col:
        render_project_info(df, selected_project)

    render_timeline(get_frame(), selected_project)


if __name__ == "__main__":
    main()
