"""
Shortlist Agent
Picks the top-N candidates from the ranked list.
"""

def run_shortlist(ranked: list[dict], top_n: int = 5) -> list[dict]:
    return ranked[:top_n]
