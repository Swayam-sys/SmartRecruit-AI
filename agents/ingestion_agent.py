"""
Ingestion Agent
Reads .pdf and .txt resumes from a folder, cleans text, returns list of dicts.
"""

import os, re

def _extract_txt(path: str) -> str:
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read()

def _extract_pdf(path: str) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            return "\n".join(p.extract_text() or "" for p in pdf.pages)
    except ImportError:
        raise ImportError("Install pdfplumber:  pip install pdfplumber")

def _clean(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)          # collapse whitespace
    text = re.sub(r'[^\x00-\x7F]+', ' ', text) # strip non-ASCII
    return text.strip()

def run_ingestion(folder: str) -> list[dict]:
    """Returns [{'name': filename, 'text': cleaned_text}, ...]"""
    resumes = []
    supported = (".pdf", ".txt")
    for fname in sorted(os.listdir(folder)):
        if not fname.lower().endswith(supported):
            continue
        path = os.path.join(folder, fname)
        raw  = _extract_pdf(path) if fname.lower().endswith(".pdf") else _extract_txt(path)
        resumes.append({
            "name": os.path.splitext(fname)[0],
            "text": _clean(raw)
        })
    if not resumes:
        raise ValueError(f"No .pdf or .txt resumes found in '{folder}'")
    return resumes
