import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MASTER_DIR = BASE_DIR / "L2 Round" / "Python"

FOLDERS = [
    ("Easy", "L2_easy_master.json"),
    ("Medium", "L2_medium_master.json"),
    ("Hard", "L2_hard_master.json")
]


def load_json(path):
    if not path.exists():
        raise FileNotFoundError(f"❌ Master file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def bootstrap():
    for level, master_file in FOLDERS:

        master_path = MASTER_DIR / master_file
        runtime_dir = BASE_DIR / "Runtime_Question_Files" / "L2" / "Python" / level

        default_path = runtime_dir / f"default_l2_python_{level.lower()}.json"
        active_path  = runtime_dir / f"active_l2_python_{level.lower()}.json"
        build_path   = runtime_dir / f"build_l2_python_{level.lower()}.json"
        state_path   = runtime_dir / "topic_state.json"

        runtime_dir.mkdir(parents=True, exist_ok=True)

        master_data = load_json(master_path)

        if not default_path.exists():
            save_json(default_path, master_data)

        if not active_path.exists():
            save_json(active_path, master_data)

        if not build_path.exists():
            save_json(build_path, [])

        if not state_path.exists():
            save_json(
                state_path,
                {
                    "topic_index": 0,
                    "day_count": 0,
                    "last_date": ""
                }
            )

    print("✅ L2 PYTHON bootstrap completed successfully")


if __name__ == "__main__":
    bootstrap()
