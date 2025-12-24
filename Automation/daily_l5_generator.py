import json
import os
import time
from datetime import datetime
from google.genai import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(api_key=os.getenv("GEMINI_API_KEY"))

BASE = r"D:\Downloads\Manually_Generated_Questions_Bank\Runtime_Question_Files\L5"
EASY_FILE   = os.path.join(BASE, "Easy",   "build_l5_easy.json")
MEDIUM_FILE = os.path.join(BASE, "Medium", "build_l5_medium.json")
HARD_FILE   = os.path.join(BASE, "Hard",   "build_l5_hard.json")

DAILY_COUNT = 3

TOPICS = {
    "easy": [
        "Email etiquette", "Basic meetings", "Simple feedback",
        "Daily teamwork role", "New tool learning", "Time management"
    ],
    "medium": [
        "Presenting updates", "Conflict resolution", "Remote collaboration",
        "Mentoring juniors", "Scope change handling", "Pressure prioritization"
    ],
    "hard": [
        "Stakeholder communication", "Persuasion", "Leading initiatives",
        "Escalation handling", "Crisis management", "Strategic planning"
    ]
}

PROMPT = """
You are generating strict, scenario-based MCQs for workplace soft skills.

Generate EXACTLY {easy} EASY questions, {medium} MEDIUM questions, and {hard} HARD questions.

STRICT RULES:
- MCQ format only
- Each question MUST be scenario based
- No explanation
- JSON only

FORMAT:
[
  {{
    "question": "text",
    "options": ["A","B","C","D"],
    "correct_answer": "A",
    "topic": "Email etiquette",
    "difficulty": "easy"
  }},
  ...
]
"""

def load_json(path):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write("[]")
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def extract_json(text):
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("No JSON content found in model output.")
    return json.loads(text[start:end+1])

def pick_topic(level):
    today = datetime.utcnow().day
    return TOPICS[level][today % len(TOPICS[level])]

def dedupe(existing, new):
    existing_questions = {q["question"] for q in existing}
    result = []
    for q in new:
        if q["question"] not in existing_questions:
            result.append(q)
    return result

def run():

    easy_topic   = pick_topic("easy")
    medium_topic = pick_topic("medium")
    hard_topic   = pick_topic("hard")

    prompt = PROMPT.format(
        easy=DAILY_COUNT,
        medium=DAILY_COUNT,
        hard=DAILY_COUNT
    )

    response=None
    for attempt in range(5):
        try:
            response=client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=prompt
            )
            break
        except:
            time.sleep(10)

    if response is None or not hasattr(response,"text"):
        print("❌ API failed — no result")
        return

    raw=response.text.strip()

    try:
        parsed = extract_json(raw)
    except:
        print("❌ JSON extract failed")
        return

    final_easy=[q for q in parsed if q.get("difficulty")=="easy"]
    final_medium=[q for q in parsed if q.get("difficulty")=="medium"]
    final_hard=[q for q in parsed if q.get("difficulty")=="hard"]

    if not final_easy or not final_medium or not final_hard:
        print("❌ Missing difficulty block")
        return

    exE=load_json(EASY_FILE)
    exM=load_json(MEDIUM_FILE)
    exH=load_json(HARD_FILE)

    newE=dedupe(exE,final_easy)
    newM=dedupe(exM,final_medium)
    newH=dedupe(exH,final_hard)

    exE.extend(newE); save_json(EASY_FILE,exE)
    exM.extend(newM); save_json(MEDIUM_FILE,exM)
    exH.extend(newH); save_json(HARD_FILE,exH)

    print("\n=====================================")
    print("   DAILY L5 SUCCESS")
    print(f"   Easy   → +{len(newE)} | Topic: {easy_topic}")
    print(f"   Medium → +{len(newM)} | Topic: {medium_topic}")
    print(f"   Hard   → +{len(newH)} | Topic: {hard_topic}")
    print("=====================================\n")


if __name__ == "__main__":
    run()
