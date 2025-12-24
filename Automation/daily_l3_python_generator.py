import json
import os
import time
from datetime import datetime
from google.genai import Client
from dotenv import load_dotenv

load_dotenv()

# ======================================================
# MODEL SETUP
# ======================================================
client = Client(api_key=os.getenv("GEMINI_API_KEY"))

# ======================================================
# PATH LOCATIONS
# ======================================================
BASE = r"D:\Downloads\Manually_Generated_Questions_Bank\Runtime_Question_Files\L3\Python"

EASY_FILE = os.path.join(BASE, "Easy", "build_l3_python_easy.json")
MEDIUM_FILE = os.path.join(BASE, "Medium", "build_l3_python_medium.json")
HARD_FILE = os.path.join(BASE, "Hard", "build_l3_python_hard.json")

# ======================================================
# DAILY CONFIG
# ======================================================
DAILY_COUNT = 3

# ======================================================
# TOPICS
# ======================================================
TOPICS = {
    "easy": [
        "Syntax Basics",
        "Variables",
        "Data Types",
        "Conditionals",
        "Loops",
        "Functions",
        "Lists",
        "Tuples"
    ],
    "medium": [
        "Dictionaries",
        "Sets",
        "OOP Concepts",
        "Exceptions",
        "File Handling",
        "Modules",
        "Iterators"
    ],
    "hard": [
        "Decorators",
        "Generators",
        "Context Managers",
        "Multithreading",
        "Multiprocessing",
        "Memory Management"
    ]
}

# ======================================================
# MASTER PROMPT (ESCAPED)
# ======================================================
PROMPT = """
You are generating high-quality, strictly unique Python MCQs for a hiring assessment.

Your task is to generate EXACTLY {easy} EASY questions, {medium} MEDIUM questions, and {hard} HARD questions.

======================
DIFFICULTY–TOPIC MAPPING
======================

EASY PYTHON TOPICS:
- Syntax Basics
- Variables
- Data Types
- Conditionals
- Loops
- Functions
- Lists
- Tuples

MEDIUM PYTHON TOPICS:
- Dictionaries
- Sets
- OOP Concepts
- Exceptions
- File Handling
- Modules
- Iterators

HARD PYTHON TOPICS:
- Decorators
- Generators
- Context Managers
- Multithreading
- Multiprocessing
- Memory Management

======================
STRICT RULES
======================
- NO duplicate questions
- NO reworded questions
- NO same logic repeated
- ALL questions must be unique
- Questions must match EXACT topic + difficulty

======================
QUESTION FORMAT
======================
Return output ONLY in this format:

[
  {{
    "question": "text",
    "options": ["A", "B", "C", "D"],
    "correct_answer": "A",
    "topic": "Functions",
    "difficulty": "easy"
  }}
]

======================
RESPONSE REQUIREMENTS
======================
- EXACT JSON array
- NO explanation
- NO notes
- NO markdown
- NO prose
- ONLY JSON
- EASY questions first
- MEDIUM questions next
- HARD questions last
"""

# ======================================================
# HELPER FUNCTIONS
# ======================================================
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
    return json.loads(text[start:end + 1])


def pick_topic(level):
    today = datetime.utcnow().day
    return TOPICS[level][today % len(TOPICS[level])]


def dedupe(existing, new):
    existing_questions = {q["question"] for q in existing}
    return [q for q in new if q["question"] not in existing_questions]

# ======================================================
# MAIN PROCESS
# ======================================================
def run():
    easy_topic = pick_topic("easy")
    medium_topic = pick_topic("medium")
    hard_topic = pick_topic("hard")

    prompt = PROMPT.format(
        easy=DAILY_COUNT,
        medium=DAILY_COUNT,
        hard=DAILY_COUNT
    )

    response = None

    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=prompt
            )
            break
        except Exception as e:
            msg = str(e)
            if "503" in msg or "overloaded" in msg:
                time.sleep(10)
                continue
            if "429" in msg or "quota" in msg:
                print("⚠ Quota limited today. Safe stop.")
                return
            print("❌ Unexpected error:", msg)
            return

    if not response or not hasattr(response, "text"):
        print("❌ No output received.")
        return

    parsed = extract_json(response.text.strip())

    final_easy = [q for q in parsed if q["difficulty"] == "easy"]
    final_medium = [q for q in parsed if q["difficulty"] == "medium"]
    final_hard = [q for q in parsed if q["difficulty"] == "hard"]

    if not final_easy or not final_medium or not final_hard:
        print("❌ Missing difficulty groups.")
        return

    easy_existing = load_json(EASY_FILE)
    medium_existing = load_json(MEDIUM_FILE)
    hard_existing = load_json(HARD_FILE)

    easy_new = dedupe(easy_existing, final_easy)
    medium_new = dedupe(medium_existing, final_medium)
    hard_new = dedupe(hard_existing, final_hard)

    save_json(EASY_FILE, easy_existing + easy_new)
    save_json(MEDIUM_FILE, medium_existing + medium_new)
    save_json(HARD_FILE, hard_existing + hard_new)

    print("\n=====================================")
    print(" DAILY L3 PYTHON SUCCESS")
    print(f" Easy   → +{len(easy_new)} | Topic: {easy_topic}")
    print(f" Medium → +{len(medium_new)} | Topic: {medium_topic}")
    print(f" Hard   → +{len(hard_new)} | Topic: {hard_topic}")
    print("=====================================\n")


if __name__ == "__main__":
    run()
