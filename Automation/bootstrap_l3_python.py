import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FOLDERS = ["Easy", "Medium", "Hard"]

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def bootstrap():

    for level in FOLDERS:

        master_path = BASE_DIR / "L3 Round" / "Python" / f"L3_{level.lower()}_master.json"
        runtime_dir = BASE_DIR / "Runtime_Question_Files" / "L3" / "Python" / level

        default_path = runtime_dir / f"default_l3_python_{level.lower()}.json"
        active_path  = runtime_dir / f"active_l3_python_{level.lower()}.json"
        build_path   = runtime_dir / f"build_l3_python_{level.lower()}.json"
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
            save_json(state_path, {
                "topic_index": 0,
                "day_count": 0,
                "last_date": ""
            })

    print("✅ L3 Python bootstrap completed")

if __name__ == "__main__":
    bootstrap()
