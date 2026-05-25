"""
Scoring Agent
Stores resume vectors in FAISS
Stores readable resume data in JSON
"""

import numpy as np

from sentence_transformers import (
    SentenceTransformer
)

from vector_db import save_vectors


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def _embed(text):

    vec = model.encode(
        text[:1000],
        convert_to_numpy=True
    )

    vec = vec / np.linalg.norm(vec)

    return vec


def _cosine(a, b):

    return float(
        np.dot(a, b)
    )


def run_scoring(
    jd_text,
    resumes
):

    print(
        "Embedding Job Description..."
    )

    jd_vec = _embed(
        jd_text
    )

    scored = []

    all_embeddings = []

    for idx, r in enumerate(
        resumes,
        start=1
    ):

        print(
            f"Embedding resume {idx}/{len(resumes)}"
        )

        rv = _embed(
            r["text"]
        )

        all_embeddings.append(
            rv
        )

        score = round(
            _cosine(
                jd_vec,
                rv
            ) * 100,
            2
        )

        scored.append({
            **r,
            "score": score
        })

    save_vectors(
        all_embeddings,
        resumes
    )

    return scored