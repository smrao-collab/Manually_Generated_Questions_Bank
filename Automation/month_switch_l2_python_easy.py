import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RUNTIME_DIR = BASE_DIR / "Runtime_Question_Files" / "L2" / "Python" / "Easy"

ACTIVE_FILE = RUNTIME_DIR / "active_l2_python_easy.json"
BUILD_FILE = RUNTIME_DIR / "build_l2_python_easy.json"


def load_json(path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def switch_month():
    new_questions = load_json(BUILD_FILE)

    if not new_questions:
        print("⚠️ No new questions found. Active file unchanged.")
        return

    save_json(ACTIVE_FILE, new_questions)
    save_json(BUILD_FILE, [])

    print("🔄 Month switch completed")


if __name__ == "__main__":
    switch_month()
