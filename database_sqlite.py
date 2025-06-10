import sqlite3

DB_FILE = "questions.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            question TEXT,
            service_type TEXT,
            service_price INTEGER,
            timestamp INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_question(user_id, question, service_type, service_price, timestamp):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO questions (user_id, question, service_type, service_price, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, question, service_type, service_price, timestamp))
    conn.commit()
    question_id = cur.lastrowid
    conn.close()
    return question_id

def get_question_by_id(question_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "user_id": row[1],
            "question": row[2],
            "service_type": row[3],
            "service_price": row[4],
            "timestamp": row[5],
        }
    return None

def get_all_questions():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions")
    rows = cur.fetchall()
    conn.close()
    questions = {}
    for row in rows:
        questions[row[0]] = {
            "id": row[0],
            "user_id": row[1],
            "question": row[2],
            "service_type": row[3],
            "service_price": row[4],
            "timestamp": row[5],
        }
    return questions

def get_last_question_time(user_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT MAX(timestamp) FROM questions WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row and row[0] else None

def delete_question(question_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM questions WHERE id = ?", (question_id,))
    conn.commit()
    conn.close()