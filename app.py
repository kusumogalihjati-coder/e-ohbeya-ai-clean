import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI-Based E-Ohbeya",
    layout="wide"
)

# =========================
# OPENAI CLIENT
# =========================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# =========================
# LOAD DATA
# =========================
df = pd.read_excel("projects.xlsx")

# =========================
# AI STATUS
# =========================
def get_status(progress, risk):

    risk = str(risk).lower()

    if risk == "high" or progress < 70:
        return "Red"

    elif risk == "medium" or progress < 90:
        return "Yellow"

    else:
        return "Green"

df["AI_Status"] = df.apply(
    lambda x: get_status(x["Progress"], x["Risk"]),
    axis=1
)

# =========================
# HEADER
# =========================
st.title("🤖 AI-Based E-Ohbeya")
st.caption("Executive AI Project Monitoring System")

# =========================
# KPI SECTION
# =========================
total_project = len(df)
critical_project = len(df[df["AI_Status"] == "Red"])
overdue_project = len(df[df["Progress"] < 70])
completed_project = len(df[df["Progress"] >= 90])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Project", total_project)
col2.metric("Critical", critical_project)
col3.metric("Overdue", overdue_project)
col4.metric("Completed", completed_project)

st.divider()

# =========================
# DONUT CHART
# =========================
chart_col1, chart_col2 = st.columns([1,1])

with chart_col1:

    st.subheader("Project Health Status")

    fig = px.pie(
        df,
        names="AI_Status",
        hole=0.6,
        color="AI_Status",
        color_discrete_map={
            "Red":"red",
            "Yellow":"gold",
            "Green":"green"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# AI SUMMARY
# =========================
with chart_col2:

    st.subheader("🤖 AI Executive Insight")

    summary_prompt = f"""
    You are executive management AI.

    Analyze this project data:

    {df.to_string()}

    Create concise executive summary.
    Mention:
    - critical project
    - major issue
    - management attention

    Keep concise and professional.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"user","content":summary_prompt}
        ]
    )

    ai_summary = response.choices[0].message.content

    st.info(ai_summary)

# =========================
# TABLE
# =========================
st.subheader("Project Monitoring Table")

st.dataframe(df, use_container_width=True)

# =========================
# AI CHAT
# =========================
st.subheader("🤖 AI Project Assistant")

question = st.text_input(
    "Ask AI about project status"
)

if question:

    prompt = f"""
    You are project management AI assistant.

    Here is project data:

    {df.to_string()}

    User question:
    {question}

    Answer professionally for management.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"user","content":prompt}
        ]
    )

    answer = response.choices[0].message.content

    st.success(answer)