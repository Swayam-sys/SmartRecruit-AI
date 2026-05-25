import faiss
import numpy as np
import json


def save_vectors(embeddings, resumes):

    embeddings = np.array(
        embeddings
    ).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    faiss.write_index(
        index,
        "resume_db.faiss"
    )

    data = []

    for r in resumes:

        data.append({
            "name": r["name"],
            "text": r["text"]
        })

    with open(
        "resume_data.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("✅ Vector database saved")
    print("✅ Resume data saved")


def view_db():

    index = faiss.read_index(
        "resume_db.faiss"
    )

    print("\n===== DATABASE INFO =====")
    print(
        "Total Resumes:",
        index.ntotal
    )

    print(
        "Dimensions:",
        index.d
    )