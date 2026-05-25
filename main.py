"""
SmartRecruit AI — Multi-Agent System for Candidate Screening & Interview Generation
Team 5: Sushmitaa, Swayam Prabha, Swetha, Vithasini

Pipeline:
  1. Ingestion Agent   — extract & clean resume text
  2. Scoring Agent     — match resume vs JD using embeddings + cosine similarity
  3. Ranking Agent     — sort candidates by score
  4. Shortlist Agent   — pick top 5
  5. Interview Agent   — generate personalised interview questions via LLM
"""

import os, json
from agents.ingestion_agent   import run_ingestion
from agents.scoring_agent     import run_scoring
from agents.ranking_agent     import run_ranking
from agents.shortlist_agent   import run_shortlist
from agents.interview_agent   import run_interview
from utils.display            import print_results

# ── Config ──────────────────────────────────────────────────────────────────
JD_FILE       = "data/job_description.txt"
RESUME_FOLDER = "data/resumes/"
OUTPUT_FILE   = "output/results.json"
TOP_N         = 5
# ────────────────────────────────────────────────────────────────────────────

def main():
    print("\n🚀  SmartRecruit AI — Starting Pipeline\n" + "─"*50)

    # Step 1: Ingest resumes
    print("📄  [1/5] Ingestion Agent — extracting resumes...")
    resumes = run_ingestion(RESUME_FOLDER)
    print(f"     ✔  {len(resumes)} resume(s) loaded.\n")

    # Step 2: Score each resume against JD
    print("🧠  [2/5] Scoring Agent — matching with Job Description...")
    jd_text = open(JD_FILE).read()
    scored  = run_scoring(jd_text, resumes)
    print(f"     ✔  Scoring complete.\n")

    # Step 3: Rank
    print("📊  [3/5] Ranking Agent — sorting candidates...")
    ranked = run_ranking(scored)

    # Step 4: Shortlist top N
    print(f"🏆  [4/5] Shortlist Agent — selecting top {TOP_N}...")
    shortlisted = run_shortlist(ranked, TOP_N)

    # Step 5: Generate interview questions
    print("💬  [5/5] Interview Agent — generating questions...")
    final = run_interview(jd_text, shortlisted)

    # Save & display
    os.makedirs("output", exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(final, f, indent=2)

    print_results(final)
    print(f"\n✅  Done! Full results saved to {OUTPUT_FILE}\n")

if __name__ == "__main__":
    main()
