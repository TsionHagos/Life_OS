# 🧠 life-os

```
$ whoami
> a person who spends too much time on TikTok

$ life-os --analyze --brutal-but-fair

[SCANNING] screentime.csv .................. OK
[LOADING]  14 days of data ................. OK
[COACH]    Coach Atlas standing by .........  READY

> WARNING: 3h 12m detected on Social Media today.
> Suggestion: that's a workout + a home-cooked meal, reclaimed.
```

## > what is this

**Life-OS** is a Streamlit dashboard that turns a boring CSV of app usage
into a full command-center: KPIs, trend charts, and an AI coach (Gemini)
that reads your day and tells you the truth about it — then tells you
what to do instead.

## > stack

```
streamlit      → UI / dashboard
pandas         → data wrangling
google-genai   → Gemini API (the "coach")
python-dotenv  → local secrets
```

## > run it locally

```bash
$ git clone https://github.com/<your-username>/life-os.git
$ cd life-os
$ pip install -r requirements.txt
$ cp .env.example .env      # then paste your real Gemini API key inside
$ streamlit run app.py
```

## > features

```
[x] 14-day synthetic screen time dataset (screentime.csv)
[x] Sidebar: day selector + daily goal slider
[x] KPI row: total time / most used app / delta vs. goal
[x] Bar chart trend over 14 days + per-category breakdown
[x] Gemini-powered coaching report (category-aware, not generic)
[x] Severity-based st.warning / st.success rendering
[x] Shareable accountability link via st.query_params
```

## > data schema (`screentime.csv`)

| Date       | App_Name | Category      | Minutes_Used |
|------------|----------|---------------|--------------|
| 2026-07-21 | TikTok   | Social Media  | 67           |

## > deployment

Deployed on **Streamlit Community Cloud**.
Live app: `<paste your live URL here>`

## > secrets

`.env` is gitignored. On Streamlit Community Cloud, set `GEMINI_API_KEY`
under **App settings → Secrets** instead of committing a `.env` file.

```
$ echo "never commit .env" >> life-lessons.log
```
