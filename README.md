# SmartRecruit AI 🤖
**Multi-Agent System for Candidate Screening & Interview Generation**
Team 5 — Agentic AI Project

---

## Project Structure

```
smartrecruit_ai/
│
├── main.py                   ← Entry point (run this)
│
├── agents/
│   ├── ingestion_agent.py    ← Reads & cleans resumes (.pdf / .txt)
│   ├── scoring_agent.py      ← Embeds JD + resumes, computes cosine similarity
│   ├── ranking_agent.py      ← Sorts candidates by score
│   ├── shortlist_agent.py    ← Picks top 5
│   └── interview_agent.py    ← Generates 7 personalised questions via GPT-4o
│
├── utils/
│   └── display.py            ← Pretty terminal output
│
├── data/
│   ├── job_description.txt   ← Paste your JD here
│   └── resumes/              ← Drop .pdf or .txt resumes here
│
├── output/
│   └── results.json          ← Auto-generated after run
│
├── requirements.txt
└── .env.example
```

---

## Setup

### 1. Clone / download the project
```bash
cd smartrecruit_ai
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your OpenAI API key
```bash
cp .env.example .env
# Open .env and paste your key:  OPENAI_API_KEY=sk-...
```
Or just export it directly:
```bash
export OPENAI_API_KEY="sk-..."   # Mac/Linux
set OPENAI_API_KEY=sk-...        # Windows
```

### 5. Add your data
- Paste/edit your job description in `data/job_description.txt`
- Add candidate resumes (`.pdf` or `.txt`) into `data/resumes/`
  *(5 sample resumes are already included for testing)*

---

## Run

```bash
python main.py
```

### Expected Output
```
🚀  SmartRecruit AI — Starting Pipeline
──────────────────────────────────────────────────
📄  [1/5] Ingestion Agent — extracting resumes...
     ✔  5 resume(s) loaded.

🧠  [2/5] Scoring Agent — matching with Job Description...
     Embedding job description...
     Embedding resume 1/5: arun_sharma
     ...

📊  [3/5] Ranking Agent — sorting candidates...
🏆  [4/5] Shortlist Agent — selecting top 5...
💬  [5/5] Interview Agent — generating questions...

════════════════════════════════════════════════════════════
  🏅  SmartRecruit AI — Shortlisted Candidates
════════════════════════════════════════════════════════════

  Rank #1  |  karthik_rajan  |  Match Score: 87.43%
  ────────────────────────────────────────────────────────
  Q1 [TECHNICAL]      Can you walk us through a RAG pipeline you built?
  ...

✅  Done! Full results saved to output/results.json
```

---

## Output Format (`output/results.json`)

```json
[
  {
    "rank": 1,
    "name": "karthik_rajan",
    "score": 87.43,
    "questions": [
      { "type": "technical",    "question": "Describe your experience with FAISS..." },
      { "type": "behavioural",  "question": "Tell me about a time you debugged..." },
      ...
    ]
  }
]
```

---

## Customisation

| What to change | Where |
|---|---|
| Number of shortlisted candidates | `TOP_N` in `main.py` |
| Embedding model | `scoring_agent.py` → model string |
| Interview LLM | `interview_agent.py` → model string |
| Number of questions per candidate | Prompt in `interview_agent.py` |

---

## Technologies Used
- **Python 3.10+**
- **OpenAI API** — `text-embedding-3-small` for embeddings, `gpt-4o` for question generation
- **pdfplumber** — PDF text extraction
- **NumPy** — cosine similarity computation
- **Pandas** — (available for extended analytics)
