"""
Ranking Agent
Sorts scored candidates in descending order of match score.
"""

def run_ranking(scored: list[dict]) -> list[dict]:
    ranked = sorted(scored, key=lambda x: x["score"], reverse=True)
    for i, c in enumerate(ranked, 1):
        c["rank"] = i
    return ranked
