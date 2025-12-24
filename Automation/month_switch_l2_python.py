import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LEVELS = ["Easy", "Medium", "Hard"]


def update(level):
    path = BASE_DIR / "Runtime_Question_Files" / "L2" / "Python" / level

    active = path / f"active_l2_python_{level.lower()}.json"
    build  = path / f"build_l2_python_{level.lower()}.json"

    if not build.exists():
        return

    with open(build, "r", encoding="utf-8") as f:
        new_data = json.load(f)

    if not new_data:
        print(f"⚠ No new {level} questions")
        return

    with open(active, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)

    with open(build, "w", encoding="utf-8") as f:
        json.dump([], f)

    print(f"🔄 L2 PYTHON {level} month switch")


def run():
    for level in LEVELS:
        update(level)


if __name__ == "__main__":
    run()
