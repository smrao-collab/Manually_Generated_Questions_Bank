import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LEVELS = ["Easy","Medium","Hard"]

def update(level):
    path = BASE_DIR / "Runtime_Question_Files" / "L1" / level
    active = path / f"active_l1_{level.lower()}.json"
    build  = path / f"build_l1_{level.lower()}.json"

    if not build.exists():
        return

    with open(build) as f:
        new = json.load(f)

    if not new:
        return

    with open(active,"w") as f:
        json.dump(new,f,indent=2)

    with open(build,"w") as f:
        json.dump([],f)

    print(f"🔄 L1 {level} switch done")

def run():
    for level in LEVELS:
        update(level)

if __name__=="__main__":
    run()
