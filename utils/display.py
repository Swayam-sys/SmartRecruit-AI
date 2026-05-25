"""
Display utility — pretty-prints final results to terminal.
"""

def print_results(results: list[dict]):
    print("\n" + "═"*60)
    print("  🏅  SmartRecruit AI — Shortlisted Candidates")
    print("═"*60)
    for c in results:
        print(f"\n  Rank #{c['rank']}  |  {c['name']}  |  Match Score: {c['score']}%")
        print("  " + "─"*56)
        for i, q in enumerate(c["questions"], 1):
            tag = f"[{q.get('type','general').upper()}]"
            print(f"  Q{i} {tag:<16} {q['question']}")
    print("\n" + "═"*60)
