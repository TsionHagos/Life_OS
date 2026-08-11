# Life-OS — Voice Journal & Screen Time Dashboard

A simple **AI-powered productivity dashboard** built with Streamlit that helps users understand their daily screen-time habits through data visualization and a voice journal.

The application combines **screen-time tracking, voice transcription, and AI coaching** to provide personalized and actionable productivity advice.

## Features

* **Screen Time Dashboard**

  * View daily screen-time by category.
  * Track total screen time.
  * Set a personal daily screen-time goal.
  * Visualize usage with a bar chart.

* **Voice Journal**

  * Record a daily reflection directly in the browser.
  * Convert the voice recording into text using OpenAI Whisper.
  * View the generated transcript inside the dashboard.

* **AI Productivity Coach**

  * Analyzes both screen-time data and the user's reflection.
  * Identifies possible reasons for excessive phone usage.
  * Provides specific productivity recommendations.
  * Suggests offline replacement activities.
  * Gives encouraging, actionable feedback.

## Technologies Used

* **Python**
* **Streamlit** — Web application framework
* **Pandas** — Data processing
* **OpenAI Whisper** — Voice transcription
* **Google Gemini API** — AI productivity coaching
* **streamlit-mic-recorder** — Browser-based audio recording
* **python-dotenv** — Environment variable management

## How It Works

The application follows this workflow:

```text
User
 │
 ▼
Screen-Time Dashboard
 │
 ├── Daily Usage Data
 │
 └── Daily Screen-Time Goal
 │
 ▼
Voice Journal
 │
 └── Record Reflection
          │
          ▼
       Whisper
          │
          ▼
      Transcript
          │
          ▼
   Gemini AI Coach
          │
          ▼
 Personalized Productivity Advice
```

## Project Structure

```text
Life_OS/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

> **Important:** Never upload your `.env` file or API keys to GitHub.

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Assignment_7_New
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` yet, install the main packages with:

```bash
pip install streamlit pandas openai-whisper google-genai streamlit-mic-recorder python-dotenv
```

### 5. Install FFmpeg

Whisper requires FFmpeg to process audio files.

On macOS with Homebrew:

```bash
brew install ffmpeg
```

Verify the installation:

```bash
ffmpeg -version
```

## 🔑 API Key Setup

Create a file called `.env` in the project directory:

```text
GEMINI_API_KEY=your_gemini_api_key
```

The application loads the key using `python-dotenv`.

Make sure `.env` is included in `.gitignore`:

```text
.env
.venv/
__pycache__/
```

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser.

## Example Workflow

1. Open the Life-OS dashboard.
2. Set your daily screen-time goal.
3. Review your screen-time breakdown.
4. Click **Record Reflection**.
5. Talk about your day and phone usage.
6. Stop the recording.
7. Whisper converts your recording into text.
8. Click **Get Coaching**.
9. Gemini analyzes your screen-time and reflection.
10. Review your personalized productivity recommendations.

## Security

API credentials should never be hard-coded into the application.

The project uses environment variables:

```python
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

The `.env` file should never be committed to GitHub.

## Future Improvements

Possible future improvements include:

* Import real screen-time data instead of sample data.
* Store journal entries from multiple days.
* Add weekly and monthly screen-time trends.
* Add persistent storage for journal entries.
* Add user authentication.
* Add personalized productivity goals.
* Add productivity and habit analytics.
* Deploy the application publicly.
* Improve AI recommendations using historical user behavior.

## Internship Project

This project was developed as part of the **Mirai AI Summer Internship Program 2026**.

The goal of the project is to explore how AI can be used to help users become more aware of their digital habits and encourage healthier relationships with technology.

## 👩‍💻 Author

**Tsion Hagos**

Built with Python, Streamlit, Whisper, and Google Gemini.
