import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MASTER_FILE = (
    BASE_DIR
    / "L2 Round"
    / "Python"
    / "L2_easy_master.json"
)

RUNTIME_DIR = (
    BASE_DIR
    / "Runtime_Question_Files"
    / "L2"
    / "Python"
    / "Easy"
)

DEFAULT_FILE = RUNTIME_DIR / "default_l2_python_easy.json"
ACTIVE_FILE = RUNTIME_DIR / "active_l2_python_easy.json"
BUILD_FILE = RUNTIME_DIR / "build_l2_python_easy.json"
STATE_FILE = RUNTIME_DIR / "topic_state.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def bootstrap():
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    master_data = load_json(MASTER_FILE)

    if not DEFAULT_FILE.exists():
        save_json(DEFAULT_FILE, master_data)

    if not ACTIVE_FILE.exists():
        save_json(ACTIVE_FILE, master_data)

    if not BUILD_FILE.exists():
        save_json(BUILD_FILE, [])

    if not STATE_FILE.exists():
        save_json(STATE_FILE, {
            "topic_index": 0,
            "day_count": 0,
            "last_date": ""
        })

    print("✅ Bootstrap completed")


if __name__ == "__main__":
    bootstrap()
