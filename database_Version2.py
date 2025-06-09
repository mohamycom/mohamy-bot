import json

from config import QUESTIONS_FILE

def load_questions():
    try:
        with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
            questions = json.load(f)
            return {int(k): v for k, v in questions.items()}
    except Exception:
        return {}

def save_questions(user_questions):
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(user_questions, f, ensure_ascii=False)

def get_last_question_time(user_questions, user_id):
    timestamps = [
        q.get("timestamp", 0)
        for q in user_questions.values()
        if q.get("user_id") == user_id
    ]
    return max(timestamps) if timestamps else None