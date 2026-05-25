"""
SmartRecruit AI — Chatbot UI
Run with:  streamlit run smartrecruit.py
"""

import os, json, tempfile, time
import streamlit as st
from dotenv import load_dotenv

from agents.ingestion_agent  import run_ingestion
from agents.scoring_agent    import run_scoring
from agents.ranking_agent    import run_ranking
from agents.shortlist_agent  import run_shortlist
from agents.interview_agent  import run_interview

load_dotenv()

st.set_page_config(
    page_title="SmartRecruit AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0f0f1a; }
    .stApp { background-color: #0f0f1a; color: #e0e0e0; }
    .title-box {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #00d4ff33;
        border-radius: 16px;
        padding: 28px 36px;
        margin-bottom: 24px;
        text-align: center;
    }
    .title-box h1 { color: #00d4ff; font-size: 2.4rem; margin: 0; }
    .title-box p  { color: #888; font-size: 1rem; margin: 6px 0 0; }
    .bubble-bot {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #00d4ff33;
        border-radius: 16px 16px 16px 4px;
        padding: 16px 20px;
        margin: 10px 0;
        color: #e0e0e0;
    }
    .bubble-user {
        background: linear-gradient(135deg, #0d3b66, #1a5276);
        border: 1px solid #00d4ff55;
        border-radius: 16px 16px 4px 16px;
        padding: 16px 20px;
        margin: 10px 0;
        color: #ffffff;
        text-align: right;
    }
    .candidate-card {
        background: #12122a;
        border: 1px solid #00d4ff22;
        border-left: 4px solid #00d4ff;
        border-radius: 12px;
        padding: 18px 22px;
        margin: 12px 0;
    }
    .rank-badge {
        display: inline-block;
        background: #00d4ff22;
        color: #00d4ff;
        border-radius: 20px;
        padding: 3px 14px;
        font-size: 0.85rem;
        font-weight: bold;
        margin-right: 10px;
    }
    .score-badge {
        display: inline-block;
        background: #00ff8822;
        color: #00ff88;
        border-radius: 20px;
        padding: 3px 14px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .q-type-technical   { color: #00d4ff; font-weight: bold; }
    .q-type-behavioural { color: #ff9f43; font-weight: bold; }
    .q-type-situational { color: #a29bfe; font-weight: bold; }
    .q-type-general     { color: #aaa;    font-weight: bold; }
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #0a0a18 !important;
        border-right: 1px solid #00d4ff22;
    }
    [data-testid="stSidebar"] * { color: #ccc !important; }
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff, #0077ff);
        color: #000;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 10px 28px;
        font-size: 1rem;
        width: 100%;
    }
    .stButton > button:hover { opacity: 0.85; }
    .step-row {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 0;
        color: #ccc;
        font-size: 0.95rem;
    }
    .step-done  { color: #00ff88; }
    .step-doing { color: #00d4ff; }
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "results" not in st.session_state:
    st.session_state.results = None
if "ran" not in st.session_state:
    st.session_state.ran = False

st.markdown("""
<div class="title-box">
    <h1>🤖 SmartRecruit AI</h1>
    <p>Multi-Agent Candidate Screening & Interview Generation · </p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")
    groq_key = st.text_input(
        "🔑 Groq API Key",
        type="password",
        value=os.environ.get("GROQ_API_KEY", ""),
        placeholder="gsk_..."
    )
    st.markdown("---")
    st.markdown("### 📋 Job Description")
    jd_text = st.text_area(
        "Paste the Job Description",
        height=200,
        placeholder="e.g. We are looking for a Python Backend Developer..."
    )
    st.markdown("### 📁 Upload Resumes")
    uploaded_files = st.file_uploader(
        "Upload .pdf or .txt resumes",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )
    top_n = st.slider("🏆 Number of candidates to shortlist", 1, 10, 5)
    st.markdown("---")
    run_btn = st.button("🚀 Run SmartRecruit AI")

if not st.session_state.ran:
    st.markdown("""
    <div class="bubble-bot">
        👋 <b>Welcome to SmartRecruit AI!</b><br><br>
        To get started:<br>
        1️⃣ &nbsp;Paste your <b>Job Description</b> in the sidebar<br>
        2️⃣ &nbsp;Upload <b>candidate resumes</b> (.pdf or .txt)<br>
        3️⃣ &nbsp;Click <b>🚀 Run SmartRecruit AI</b><br><br>
        I'll screen, rank, and generate personalised interview questions for the top candidates!
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bubble-bot">{msg["content"]}</div>', unsafe_allow_html=True)

if run_btn:
    if not groq_key:
        st.error("❌ Please enter your Groq API key in the sidebar.")
        st.stop()
    if not jd_text.strip():
        st.error("❌ Please paste a Job Description in the sidebar.")
        st.stop()
    if not uploaded_files:
        st.error("❌ Please upload at least one resume.")
        st.stop()

    os.environ["GROQ_API_KEY"] = groq_key

    st.markdown(f"""
    <div class="bubble-user">
        📋 JD provided &nbsp;|&nbsp; 📁 {len(uploaded_files)} resume(s) uploaded &nbsp;|&nbsp; 🏆 Top {top_n} requested
    </div>
    """, unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "user",
        "content": f"📋 JD provided | 📁 {len(uploaded_files)} resume(s) uploaded | 🏆 Top {top_n} requested"
    })

    progress_placeholder = st.empty()

    def show_progress(steps):
        html = '<div class="bubble-bot"><b>⚙️ Running Pipeline...</b><br><br>'
        for label, status in steps:
            if status == "done":
                html += f'<div class="step-row step-done">✅ &nbsp;{label}</div>'
            elif status == "doing":
                html += f'<div class="step-row step-doing">⏳ &nbsp;{label}</div>'
            else:
                html += f'<div class="step-row">⬜ &nbsp;{label}</div>'
        html += "</div>"
        progress_placeholder.markdown(html, unsafe_allow_html=True)

    step_labels = [
        "Ingestion Agent — extracting resumes",
        "Scoring Agent  — matching with JD",
        "Ranking Agent  — sorting candidates",
        "Shortlist Agent — picking top candidates",
        "Interview Agent — generating questions",
    ]

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            show_progress([(s, "doing" if i==0 else "wait") for i,s in enumerate(step_labels)])
            for f in uploaded_files:
                path = os.path.join(tmpdir, f.name)
                with open(path, "wb") as out:
                    out.write(f.read())
            resumes = run_ingestion(tmpdir)
            time.sleep(0.3)

            show_progress([(s, "done" if i<1 else ("doing" if i==1 else "wait")) for i,s in enumerate(step_labels)])
            scored = run_scoring(jd_text, resumes)
            time.sleep(0.3)

            show_progress([(s, "done" if i<2 else ("doing" if i==2 else "wait")) for i,s in enumerate(step_labels)])
            ranked = run_ranking(scored)
            time.sleep(0.2)

            show_progress([(s, "done" if i<3 else ("doing" if i==3 else "wait")) for i,s in enumerate(step_labels)])
            shortlisted = run_shortlist(ranked, top_n)
            time.sleep(0.2)

            show_progress([(s, "done" if i<4 else ("doing" if i==4 else "wait")) for i,s in enumerate(step_labels)])
            final = run_interview(jd_text, shortlisted)
            show_progress([(s, "done") for s in step_labels])
            time.sleep(0.5)

        os.makedirs("output", exist_ok=True)
        with open("output/results.json", "w") as f:
            json.dump(final, f, indent=2)

        st.session_state.results = final
        st.session_state.ran = True
        progress_placeholder.empty()

        st.markdown(f"""
        <div class="bubble-bot">
            ✅ <b>Pipeline complete!</b> Screened <b>{len(resumes)}</b> resumes.
            Shortlisted top <b>{len(final)}</b> candidates below. 👇
        </div>
        """, unsafe_allow_html=True)

        for c in final:
            q_html = ""
            for i, q in enumerate(c["questions"], 1):
                qtype = q.get("type", "general").lower()
                css   = f"q-type-{qtype}"
                q_html += f'<p><span class="{css}">[{qtype.upper()}]</span> <b>Q{i}.</b> {q["question"]}</p>'

            st.markdown(f"""
            <div class="candidate-card">
                <span class="rank-badge">Rank #{c['rank']}</span>
                <span style="font-size:1.1rem; font-weight:bold; color:#fff;">{c['name'].replace('_',' ').title()}</span>
                <span class="score-badge" style="float:right;">Match: {c['score']}%</span>
                <hr style="border-color:#ffffff11; margin:12px 0;">
                <b style="color:#aaa;">🎯 Interview Questions</b><br><br>
                {q_html}
            </div>
            """, unsafe_allow_html=True)

        st.download_button(
            label="⬇️ Download Full Results (JSON)",
            data=json.dumps(final, indent=2),
            file_name="smartrecruit_results.json",
            mime="application/json"
        )

    except Exception as e:
        progress_placeholder.empty()
        st.error(f"❌ Error: {str(e)}")