"""
Interview Agent (GROQ VERSION)
Uses Groq's LLaMA3 (free) to generate 7 personalised interview questions.
Requires GROQ_API_KEY in your .env file.
"""

import os, json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an expert technical recruiter.
Given a job description and a candidate's resume, generate exactly 7 personalised
interview questions. Return ONLY a JSON array of objects, each with:
  - "type"     : one of ["technical", "behavioural", "situational"]
  - "question" : the interview question string
No extra text, no markdown fences."""

def _generate_questions(jd: str, resume_text: str, name: str) -> list[dict]:
    user_msg = f"""
JOB DESCRIPTION:
{jd[:2000]}

CANDIDATE: {name}
RESUME (excerpt):
{resume_text[:3000]}

Generate 7 tailored interview questions.
"""
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_msg}
        ],
        temperature=0.7,
        max_tokens=800
    )
    raw = resp.choices[0].message.content.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return [{"type": "general", "question": raw}]

def run_interview(jd_text: str, shortlisted: list[dict]) -> list[dict]:
    results = []
    for c in shortlisted:
        print(f"     Generating questions for: {c['name']}")
        questions = _generate_questions(jd_text, c["text"], c["name"])
        results.append({
            "rank"      : c["rank"],
            "name"      : c["name"],
            "score"     : c["score"],
            "questions" : questions
        })
    return results
