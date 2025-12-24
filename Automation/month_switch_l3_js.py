import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LEVELS = ["Easy", "Medium", "Hard"]


def update(level):
    path = BASE_DIR / "Runtime_Question_Files" / "L3" / "Javascript" / level

    active = path / f"active_l3_js_{level.lower()}.json"
    build = path / f"build_l3_js_{level.lower()}.json"

    if not build.exists():
        return

    with open(build, "r") as f:
        new_data = json.load(f)

    if not new_data:
        print(f"⚠ No new {level} questions")
        return

    with open(active, "w") as f:
        json.dump(new_data, f, indent=2)

    with open(build, "w") as f:
        json.dump([], f)

    print(f"🔄 L3 JS {level} month switch")


def run():
    for level in LEVELS:
        update(level)


if __name__ == "__main__":
    run()
