"""
Life-OS: A Streamlit dashboard that visualizes screen time
and uses Gemini to act as a brutal-but-fair life coach.
"""

import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ── Setup ──────────────────────────────────────────────────────────
load_dotenv()  # reads GEMINI_API_KEY from a local .env file

st.set_page_config(
    page_title="Life-OS Dashboard",
    layout="wide",
)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# ── Phase 1: Data Ingestion ────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("screentime.csv")
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    return df


df = load_data()
all_dates = sorted(df["Date"].unique())

# ── Phase 2: Sidebar Controls ──────────────────────────────────────
st.sidebar.title("Command Center")
selected_date = st.sidebar.selectbox(
    "Select a day to inspect",
    options=all_dates,
    index=len(all_dates) - 1,  # default to most recent day
)

daily_goal_minutes = st.sidebar.slider(
    "Daily screen time goal (minutes)",
    min_value=30,
    max_value=480,
    value=180,
    step=15,
)
st.sidebar.caption(f"That's about **{daily_goal_minutes / 60:.1f} hours** per day.")

st.sidebar.divider()
st.sidebar.markdown("Built for the **Life-OS** assignment — Phase 4: Shareable Link")

# ── Filter to the selected day ─────────────────────────────────────
day_df = df[df["Date"] == selected_date]

total_minutes_today = int(day_df["Minutes_Used"].sum())
if not day_df.empty:
    most_used_app = (
        day_df.groupby("App_Name")["Minutes_Used"].sum().idxmax()
    )
    most_used_minutes = int(day_df.groupby("App_Name")["Minutes_Used"].sum().max())
else:
    most_used_app, most_used_minutes = "N/A", 0

delta_minutes = total_minutes_today - daily_goal_minutes

# ── Phase 4 (Innovation): Shareable Accountability Link ────────────
# Write today's total into the URL so it can be copied and shared.
st.query_params["date"] = str(selected_date)
st.query_params["total_minutes"] = str(total_minutes_today)
st.query_params["goal"] = str(daily_goal_minutes)

# ── Header ──────────────────────────────────────────────────────────
st.title("Life-OS: Digital Wellbeing Dashboard")
st.caption(f"Analyzing your day: **{selected_date.strftime('%A, %B %d, %Y')}**")

# ── Phase 2: KPI Row ────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Screen Time Today",
        value=f"{total_minutes_today} min",
        help=f"= {total_minutes_today / 60:.1f} hours",
    )

with col2:
    st.metric(
        label="Most Used App",
        value=most_used_app,
        delta=f"{most_used_minutes} min",
        delta_color="off",
    )

with col3:
    st.metric(
        label="Vs. Daily Goal",
        value=f"{daily_goal_minutes} min goal",
        delta=f"{delta_minutes:+d} min",
        delta_color="inverse",  # going OVER goal shows red, UNDER shows green
    )

st.divider()

# ── Phase 2: Visualizations ─────────────────────────────────────────
st.subheader("14-Day Trend")

trend_col, cat_col = st.columns([2, 1])

with trend_col:
    daily_totals = df.groupby("Date")["Minutes_Used"].sum()
    st.bar_chart(daily_totals)

with cat_col:
    cat_totals_today = day_df.groupby("Category")["Minutes_Used"].sum()
    st.subheader("Today by Category")
    st.bar_chart(cat_totals_today)

st.divider()


# ── Phase 3: The Data Bridge ─────────────────────────────────────────
def summarize_day(day_df: pd.DataFrame) -> str:
    """
    Aggregates a day's usage into a clean string Gemini can read.
    AI models can't parse raw DataFrames, so we roll it up by category
    and by app, then serialize it.
    """
    by_category = (
        day_df.groupby("Category")["Minutes_Used"].sum().sort_values(ascending=False)
    )
    by_app = (
        day_df.groupby("App_Name")["Minutes_Used"].sum().sort_values(ascending=False)
    )

    summary = (
        f"Total screen time: {int(day_df['Minutes_Used'].sum())} minutes\n\n"
        f"Breakdown by category (minutes):\n{by_category.to_string()}\n\n"
        f"Breakdown by app (minutes):\n{by_app.to_string()}"
    )
    return summary


# ── Phase 3: The System Prompt + AI Coaching ─────────────────────────
st.subheader("Your Life Coach's Verdict")

if st.button("Get My Coaching Report", type="primary"):
    data_summary = summarize_day(day_df)

    prompt = f"""
You are "Coach Atlas" — a brutal-but-fair holistic life coach who analyzes
a person's daily screen time and gives them real, actionable advice.

Here is today's screen time data, already aggregated by category and by app:

{data_summary}

The person's self-set daily screen time goal is {daily_goal_minutes} minutes.
They actually used {total_minutes_today} minutes today ({delta_minutes:+d} minutes vs. goal).

Your job:
1. Give a short, honest verdict on how today went (be direct, not mean).
2. Call out the SPECIFIC category or app that is the biggest problem, if any.
3. Do NOT just say "use your phone less." Instead, suggest concrete,
   real-world physical replacements for that specific time. For example,
   if there's heavy Social Media or Entertainment usage, suggest reclaiming
   that time for things like a workout, meal prepping, reading, or a walk —
   tie the suggestion to the actual minutes freed up.
4. If Education, Coding, or Productivity usage is high, acknowledge that
   as a genuine win.
5. End with ONE specific, measurable action for tomorrow.

Keep the whole response under 180 words. Use markdown formatting
(bold key phrases, use a short bullet list for the action items).
"""

    with st.spinner("Coach Atlas is reviewing your day..."):
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        advice = response.text

    # ── Phase 3: Render output, severity-based styling ───────────────
    if delta_minutes > 60:
        st.warning("**Severe overage** — Coach Atlas is not happy.")
    elif delta_minutes > 0:
        st.warning("You went over your goal today.")
    else:
        st.success("You hit your goal today. Nice work.")

    st.markdown(advice)

else:
    st.info("Click the button above to generate today's coaching report.")

st.divider()

# ── Shareable link display ──────────────────────────────────────────
with st.expander("Share your accountability link"):
    st.write(
        "Copy your browser's current URL and send it to your accountability "
        "partner — it already encodes today's date, total, and goal as "
        "query parameters they can check at a glance."
    )
    st.code(
        f"?date={selected_date}&total_minutes={total_minutes_today}&goal={daily_goal_minutes}",
        language="text",
    )