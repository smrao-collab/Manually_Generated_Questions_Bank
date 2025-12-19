import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RUNTIME_DIR = BASE_DIR / "Runtime_Question_Files" / "L2" / "Javascript"

LEVELS = {
    "easy": {
        "ACTIVE": RUNTIME_DIR / "Easy" / "active_l2_js_easy.json",
        "BUILD":  RUNTIME_DIR / "Easy" / "build_l2_js_easy.json",
    },
    "medium": {
        "ACTIVE": RUNTIME_DIR / "Medium" / "active_l2_js_medium.json",
        "BUILD":  RUNTIME_DIR / "Medium" / "build_l2_js_medium.json",
    },
    "hard": {
        "ACTIVE": RUNTIME_DIR / "Hard" / "active_l2_js_hard.json",
        "BUILD":  RUNTIME_DIR / "Hard" / "build_l2_js_hard.json",
    },
}


def load_json(path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def switch_month():

    for level, files in LEVELS.items():
        active = files["ACTIVE"]
        build = files["BUILD"]

        new_data = load_json(build)

        if not new_data:
            print(f"⚠️ No new JS {level} questions. Active unchanged.")
            continue

        save_json(active, new_data)
        save_json(build, [])

        print(f"🔄 JS month switch successful → {level}")

    print("\n🎯 JS L2 month switch completed.")


if __name__ == "__main__":
    switch_month()
