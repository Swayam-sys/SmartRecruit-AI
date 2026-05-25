"""
SmartRecruit AI — Elegant UI (No Sidebar)
Run with:  streamlit run smartrecruit_new.py
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
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #080810 !important;
    color: #e8e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="collapsedControl"], .stDeployButton { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

.block-container { max-width: 1100px !important; padding: 2rem 2rem !important; }

.hero { text-align: center; padding: 3.5rem 0 2.5rem; position: relative; }
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 300px;
    background: radial-gradient(ellipse at center, #6366f130 0%, transparent 70%);
    pointer-events: none;
}
.hero-tag {
    display: inline-block;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #6366f1;
    background: #6366f115;
    border: 1px solid #6366f130;
    border-radius: 100px;
    padding: 6px 18px;
    margin-bottom: 1.4rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(2.4rem, 5vw, 3.8rem) !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em;
    line-height: 1.1;
    color: #f0f0ff !important;
    margin-bottom: 1rem;
}
.hero h1 span { color: #6366f1; }
.hero p { font-size: 1.05rem; color: #888899; max-width: 520px; margin: 0 auto; line-height: 1.6; }

.divider { height: 1px; background: linear-gradient(90deg, transparent, #6366f130, transparent); margin: 2rem 0; }

.panel-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.stTextInput input, .stTextArea textarea {
    background: #13131f !important;
    border: 1px solid #2a2a42 !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 10px 14px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px #6366f115 !important;
}
.stTextInput label, .stTextArea label, .stFileUploader label, .stSlider label {
    color: #888899 !important;
    font-size: 0.82rem !important;
    font-family: 'DM Sans', sans-serif !important;
    margin-bottom: 6px !important;
}
.stFileUploader > div {
    background: #13131f !important;
    border: 1px dashed #2a2a42 !important;
    border-radius: 10px !important;
}
.stFileUploader > div:hover { border-color: #6366f1 !important; }

.stButton > button {
    width: 100% !important;
    background: #6366f1 !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #4f46e5 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px #6366f140 !important;
}

.welcome-card {
    background: #0e0e1a;
    border: 1px solid #1e1e32;
    border-radius: 16px;
    padding: 2rem 2.4rem;
    margin-bottom: 1.5rem;
    display: flex;
    gap: 1.5rem;
    align-items: flex-start;
}
.welcome-icon { font-size: 2rem; flex-shrink: 0; margin-top: 2px; }
.welcome-card h3 { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; color: #f0f0ff; margin-bottom: 0.6rem; }
.welcome-card p { color: #888899; font-size: 0.9rem; line-height: 1.7; }
.step-pill {
    display: inline-block;
    background: #6366f115;
    color: #6366f1;
    border-radius: 100px;
    padding: 2px 10px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 0 2px;
}

.progress-wrap { background: #0e0e1a; border: 1px solid #1e1e32; border-radius: 16px; padding: 1.8rem 2rem; margin: 1rem 0; }
.progress-title { font-family: 'Syne', sans-serif; font-size: 0.85rem; font-weight: 700; color: #6366f1; letter-spacing: 0.08em; margin-bottom: 1.2rem; }
.step-item { display: flex; align-items: center; gap: 12px; padding: 9px 0; font-size: 0.9rem; color: #55556a; border-bottom: 1px solid #13131f; }
.step-item:last-child { border-bottom: none; }
.step-item.done  { color: #34d399; }
.step-item.doing { color: #a5b4fc; }
.step-dot { width: 8px; height: 8px; border-radius: 50%; background: #2a2a42; flex-shrink: 0; }
.step-item.done  .step-dot { background: #34d399; }
.step-item.doing .step-dot { background: #6366f1; box-shadow: 0 0 8px #6366f180; animation: pulse 1.2s infinite; }
@keyframes pulse { 0%,100% { opacity:1; transform:scale(1); } 50% { opacity:0.5; transform:scale(1.4); } }

.success-banner {
    background: linear-gradient(135deg, #0e1e14, #0a1a10);
    border: 1px solid #34d39930;
    border-left: 4px solid #34d399;
    border-radius: 12px;
    padding: 1.2rem 1.6rem;
    margin: 1rem 0;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 0.95rem;
    color: #a7f3d0;
}

.cand-card { background: #0e0e1a; border: 1px solid #1e1e32; border-radius: 16px; padding: 1.8rem 2rem; margin: 1rem 0; }
.cand-card:hover { border-color: #6366f140; }
.cand-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.2rem; flex-wrap: wrap; gap: 10px; }
.cand-name { font-family: 'Syne', sans-serif; font-size: 1.15rem; font-weight: 700; color: #f0f0ff; }
.badges { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.badge-rank { background: #6366f115; color: #a5b4fc; border: 1px solid #6366f130; border-radius: 100px; padding: 4px 14px; font-size: 0.78rem; font-weight: 600; font-family: 'Syne', sans-serif; }
.badge-score { background: #34d39915; color: #34d399; border: 1px solid #34d39930; border-radius: 100px; padding: 4px 14px; font-size: 0.78rem; font-weight: 600; font-family: 'Syne', sans-serif; }
.score-bar-wrap { background: #13131f; border-radius: 100px; height: 4px; margin-bottom: 1.4rem; overflow: hidden; }
.score-bar-fill { height: 100%; border-radius: 100px; background: linear-gradient(90deg, #6366f1, #34d399); }
.q-section-title { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: #55556a; margin-bottom: 1rem; font-family: 'Syne', sans-serif; }
.q-item { display: flex; gap: 12px; padding: 10px 0; border-bottom: 1px solid #13131f; align-items: flex-start; }
.q-item:last-child { border-bottom: none; }
.q-num { font-family: 'Syne', sans-serif; font-size: 0.75rem; font-weight: 700; color: #55556a; min-width: 24px; padding-top: 2px; }
.q-text { font-size: 0.9rem; color: #c8c8d8; line-height: 1.5; flex: 1; }
.q-badge { font-size: 0.68rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; border-radius: 6px; padding: 2px 8px; flex-shrink: 0; margin-top: 2px; }
.q-technical   { background:#6366f115; color:#a5b4fc; }
.q-behavioural { background:#f59e0b15; color:#fbbf24; }
.q-situational { background:#10b98115; color:#34d399; }
.q-general     { background:#ffffff10; color:#888899; }

.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid #2a2a42 !important;
    color: #888899 !important;
    font-size: 0.85rem !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    margin-top: 1rem !important;
}
.stDownloadButton > button:hover { border-color: #6366f1 !important; color: #a5b4fc !important; background: #6366f110 !important; }
.stAlert { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state
for key, val in [("ran", False), ("results", None)]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── HERO
st.markdown("""
<div class="hero">
    <div class="hero-tag">Agentic AI ·</div>
    <h1>Smart<span>Recruit</span> AI</h1>
    <p>Multi-agent candidate screening & personalised interview generation powered by Groq LLaMA3</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── INPUTS
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="panel-title">🔑 &nbsp;API KEY</div>', unsafe_allow_html=True)
    groq_key = st.text_input("Groq API Key", type="password",
                              value=os.environ.get("GROQ_API_KEY",""),
                              placeholder="gsk_...",
                              label_visibility="collapsed")
    st.markdown('<div class="panel-title" style="margin-top:1.2rem">📋 &nbsp;JOB DESCRIPTION</div>', unsafe_allow_html=True)
    jd_text = st.text_area("Job Description", height=220,
                            placeholder="Paste the full job description here...",
                            label_visibility="collapsed")

with col2:
    st.markdown('<div class="panel-title">📁 &nbsp;CANDIDATE RESUMES</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Upload resumes (.pdf or .txt)",
                                       type=["pdf","txt"],
                                       accept_multiple_files=True,
                                       label_visibility="collapsed")
    st.markdown('<div class="panel-title" style="margin-top:1.2rem">🏆 &nbsp;SHORTLIST SIZE</div>', unsafe_allow_html=True)
    top_n = st.slider("Candidates to shortlist", 1, 10, 5, label_visibility="collapsed")

    if uploaded_files:
        st.markdown(
            f'<div style="background:#13131f;border:1px solid #1e1e32;border-radius:10px;'
            f'padding:12px 16px;margin-top:0.8rem;font-size:0.85rem;color:#888899;">'
            f'📎 &nbsp;<b style="color:#a5b4fc">{len(uploaded_files)}</b> file(s) ready'
            f'&nbsp;·&nbsp; Top <b style="color:#a5b4fc">{top_n}</b> will be shortlisted</div>',
            unsafe_allow_html=True
        )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
run_btn = st.button("🚀 &nbsp; Run SmartRecruit AI Pipeline")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── WELCOME
if not st.session_state.ran:
    st.markdown("""
    <div class="welcome-card">
        <div class="welcome-icon">🤖</div>
        <div>
            <h3>Welcome to SmartRecruit AI</h3>
            <p>
                <span class="step-pill">1</span> Enter your Groq API key above &nbsp;
                <span class="step-pill">2</span> Paste the Job Description &nbsp;
                <span class="step-pill">3</span> Upload candidate resumes &nbsp;
                <span class="step-pill">4</span> Click Run — results appear below
            </p>
            <p style="margin-top:0.6rem">
                The pipeline screens all resumes, ranks by match score using semantic embeddings,
                shortlists the top candidates, and generates 7 personalised interview questions each.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── PIPELINE
if run_btn:
    if not groq_key:
        st.error("❌ Please enter your Groq API key above."); st.stop()
    if not jd_text.strip():
        st.error("❌ Please paste a Job Description."); st.stop()
    if not uploaded_files:
        st.error("❌ Please upload at least one resume."); st.stop()

    os.environ["GROQ_API_KEY"] = groq_key

    step_labels = [
        ("📄", "Ingestion Agent",  "Extracting & cleaning resumes"),
        ("🧠", "Scoring Agent",    "Semantic similarity matching"),
        ("📊", "Ranking Agent",    "Sorting by match score"),
        ("🏆", "Shortlist Agent",  "Selecting top candidates"),
        ("💬", "Interview Agent",  "Generating interview questions"),
    ]

    progress_placeholder = st.empty()

    def show_progress(current):
        html = '<div class="progress-wrap"><div class="progress-title">⚙️ &nbsp;PIPELINE RUNNING</div>'
        for i, (icon, name, desc) in enumerate(step_labels):
            if i < current:
                cls = "done";  dot = "✓"
            elif i == current:
                cls = "doing"; dot = ""
            else:
                cls = "";      dot = ""
            html += (
                f'<div class="step-item {cls}">'
                f'<div class="step-dot"></div>'
                f'<span>{icon} &nbsp;<b>{name}</b> — {desc}</span>'
                f'<span style="margin-left:auto;font-size:0.8rem">{dot}</span>'
                f'</div>'
            )
        html += "</div>"
        progress_placeholder.markdown(html, unsafe_allow_html=True)

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            show_progress(0)
            for f in uploaded_files:
                with open(os.path.join(tmpdir, f.name), "wb") as out:
                    out.write(f.read())
            resumes = run_ingestion(tmpdir)
            time.sleep(0.3)

            show_progress(1)
            scored = run_scoring(jd_text, resumes)
            time.sleep(0.3)

            show_progress(2)
            ranked = run_ranking(scored)
            time.sleep(0.2)

            show_progress(3)
            shortlisted = run_shortlist(ranked, top_n)
            time.sleep(0.2)

            show_progress(4)
            final = run_interview(jd_text, shortlisted)
            time.sleep(0.3)

        os.makedirs("output", exist_ok=True)
        with open("output/results.json", "w") as f:
            json.dump(final, f, indent=2)

        st.session_state.results = final
        st.session_state.ran     = True
        progress_placeholder.empty()

        st.markdown(
            f'<div class="success-banner">'
            f'✅ &nbsp;Pipeline complete — screened <b>{len(resumes)}</b> resumes, '
            f'shortlisted top <b>{len(final)}</b> candidates'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ── CANDIDATE CARDS
        for c in final:
            q_html = ""
            for i, q in enumerate(c["questions"], 1):
                qtype = q.get("type", "general").lower()
                question_text = q.get("question", "")
                q_html += (
                    f'<div class="q-item">'
                    f'<span class="q-num">Q{i}</span>'
                    f'<span class="q-text">{question_text}</span>'
                    f'<span class="q-badge q-{qtype}">{qtype}</span>'
                    f'</div>'
                )

            score_pct = min(c["score"], 100)
            name_display = c["name"].replace("_", " ").title()

            card_html = (
                f'<div class="cand-card">'
                f'<div class="cand-header">'
                f'<span class="cand-name">{name_display}</span>'
                f'<div class="badges">'
                f'<span class="badge-rank">Rank #{c["rank"]}</span>'
                f'<span class="badge-score">Match {c["score"]}%</span>'
                f'</div></div>'
                f'<div class="score-bar-wrap">'
                f'<div class="score-bar-fill" style="width:{score_pct}%"></div>'
                f'</div>'
                f'<div class="q-section-title">Interview Questions</div>'
                f'{q_html}'
                f'</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)

        st.download_button(
            label="⬇️  Download Results (JSON)",
            data=json.dumps(final, indent=2),
            file_name="smartrecruit_results.json",
            mime="application/json"
        )

    except Exception as e:
        progress_placeholder.empty()
        st.error(f"❌ Error: {str(e)}")
