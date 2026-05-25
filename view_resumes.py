import json

with open(
    "resume_data.json",
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)

for resume in data:

    print("\n")
    print("=" * 50)

    print(
        "Name:",
        resume["name"]
    )

    print(
        "\nResume Text:\n"
    )

    print(
        resume["text"]
    )