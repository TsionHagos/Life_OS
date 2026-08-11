import streamlit as st
import pandas as pd
import tempfile
import os
import whisper

from google import genai
from streamlit_mic_recorder import mic_recorder
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


# Page configuration
st.set_page_config(
    page_title="Screen Time Dashboard",
    layout="wide"
)

st.title("Today's Dashboard")


# -----------------------------
# Session State
# -----------------------------

if "whisper_model" not in st.session_state:
    st.session_state.whisper_model = whisper.load_model("base")

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "coaching_response" not in st.session_state:
    st.session_state.coaching_response = ""


# -----------------------------
# Screen Time Data
# -----------------------------

def get_today_summary():
    data = {
        "Category": [
            "Coding",
            "Social Media",
            "Education",
            "Entertainment"
        ],
        "Minutes": [
            180,
            210,
            45,
            60
        ],
    }

    df = pd.DataFrame(data)

    return df


def summarize_to_text(df):
    lines = [
        f"{row.Category}: {row.Minutes} minutes"
        for row in df.itertuples()
    ]

    return "\n".join(lines)


# -----------------------------
# Voice Transcription
# -----------------------------

def transcribe_audio(audio_bytes):

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as tmp_file:

        tmp_file.write(audio_bytes)
        tmp_path = tmp_file.name

    result = st.session_state.whisper_model.transcribe(tmp_path)

    os.remove(tmp_path)

    return result["text"].strip()


# -----------------------------
# Gemini Prompt
# -----------------------------

def build_prompt(summary_text, transcript_text):

    prompt = f"""
You are a productivity and lifestyle coach.

Here is today's screen-time summary:

{summary_text}

Here is the user's reflection:

"{transcript_text}"

Analyze both the data and the reflection together.

Explain why the user may have overused their phone.

Offer practical, specific advice.

Suggest offline replacement activities.

Avoid generic advice.

Be honest but encouraging.

Provide clear, actionable recommendations.
"""

    return prompt


# -----------------------------
# Gemini AI Coaching
# -----------------------------

def get_gemini_coaching(prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# -----------------------------
# Daily Goal
# -----------------------------

daily_goal = st.slider(
    "Set your daily screen-time goal (minutes)",
    60,
    600,
    300
)


# -----------------------------
# Dashboard
# -----------------------------

summary_df = get_today_summary()

total_minutes = summary_df["Minutes"].sum()


col1, col2 = st.columns(2)

col1.metric(
    "Total Screen Time",
    f"{total_minutes} min"
)

col2.metric(
    "Daily Goal",
    f"{daily_goal} min"
)


st.bar_chart(
    summary_df.set_index("Category")
)


# -----------------------------
# Voice Journal
# -----------------------------

st.divider()

st.header("Voice Journal")


audio = mic_recorder(
    start_prompt="Record Reflection",
    stop_prompt="Stop Recording",
    just_once=True,
    format="wav",
)


if audio:

    st.info("Recording captured. Transcribing...")

    st.session_state.transcript = transcribe_audio(
        audio["bytes"]
    )


if st.session_state.transcript:

    st.subheader("Today's Reflection")

    st.write(
        st.session_state.transcript
    )


# -----------------------------
# AI Productivity Coach
# -----------------------------

st.divider()

st.header("AI Productivity Coach")


if st.session_state.transcript:

    if st.button("Get Coaching"):

        st.info("Coach is analyzing...")

        summary_text = summarize_to_text(
            summary_df
        )

        prompt = build_prompt(
            summary_text,
            st.session_state.transcript
        )

        st.session_state.coaching_response = (
            get_gemini_coaching(prompt)
        )


    if st.session_state.coaching_response:

        if total_minutes > daily_goal:

            st.warning(
                st.session_state.coaching_response
            )

        else:

            st.info(
                st.session_state.coaching_response
            )

else:

    st.write(
        "Record a voice reflection above to unlock your coaching."
    )
