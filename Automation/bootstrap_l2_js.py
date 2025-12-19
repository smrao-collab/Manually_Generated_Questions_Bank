import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MASTER_DIR = BASE_DIR / "L2 Round" / "Javascript"
RUNTIME_DIR = BASE_DIR / "Runtime_Question_Files" / "L2" / "Javascript"

# Master files
MASTER_EASY   = MASTER_DIR / "L2_easy_js_master.json"
MASTER_MEDIUM = MASTER_DIR / "L2_medium_js_master.json"
MASTER_HARD   = MASTER_DIR / "L2_hard_js_master.json"

# Runtime folders
EASY_DIR   = RUNTIME_DIR / "Easy"
MEDIUM_DIR = RUNTIME_DIR / "Medium"
HARD_DIR   = RUNTIME_DIR / "Hard"

# Runtime files
DEFAULT_EASY   = EASY_DIR / "default_l2_js_easy.json"
ACTIVE_EASY    = EASY_DIR / "active_l2_js_easy.json"
BUILD_EASY     = EASY_DIR / "build_l2_js_easy.json"
STATE_EASY     = EASY_DIR / "topic_state.json"

DEFAULT_MEDIUM = MEDIUM_DIR / "default_l2_js_medium.json"
ACTIVE_MEDIUM  = MEDIUM_DIR / "active_l2_js_medium.json"
BUILD_MEDIUM   = MEDIUM_DIR / "build_l2_js_medium.json"
STATE_MEDIUM   = MEDIUM_DIR / "topic_state.json"

DEFAULT_HARD   = HARD_DIR / "default_l2_js_hard.json"
ACTIVE_HARD    = HARD_DIR / "active_l2_js_hard.json"
BUILD_HARD     = HARD_DIR / "build_l2_js_hard.json"
STATE_HARD     = HARD_DIR / "topic_state.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def init_level(master, default, active, build, state, dir_path):
    dir_path.mkdir(parents=True, exist_ok=True)

    master_data = load_json(master)

    if not default.exists():
        save_json(default, master_data)

    if not active.exists():
        save_json(active, master_data)

    if not build.exists():
        save_json(build, [])

    if not state.exists():
        save_json(state, {
            "topic_index": 0,
            "day_count": 0,
            "last_date": ""
        })


def bootstrap():
    init_level(MASTER_EASY, DEFAULT_EASY, ACTIVE_EASY, BUILD_EASY, STATE_EASY, EASY_DIR)
    init_level(MASTER_MEDIUM, DEFAULT_MEDIUM, ACTIVE_MEDIUM, BUILD_MEDIUM, STATE_MEDIUM, MEDIUM_DIR)
    init_level(MASTER_HARD, DEFAULT_HARD, ACTIVE_HARD, BUILD_HARD, STATE_HARD, HARD_DIR)

    print("✅ JS L2 Bootstrap completed (Easy/Medium/Hard)")


if __name__ == "__main__":
    bootstrap()
