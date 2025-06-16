import os
import psycopg2
from psycopg2 import sql

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            question TEXT NOT NULL,
            service_type TEXT,
            service_price INTEGER,
            timestamp BIGINT
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def save_question(user_id, question, service_type, service_price, timestamp):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO questions (user_id, question, service_type, service_price, timestamp)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    ''', (user_id, question, service_type, service_price, timestamp))
    question_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return question_id

def get_question_by_id(question_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions WHERE id = %s', (question_id,))
    row = cursor.fetchone()
    cursor.close()
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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions')
    rows = cursor.fetchall()
    cursor.close()
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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(timestamp) FROM questions WHERE user_id = %s', (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row[0] if row and row[0] else None

def delete_question(question_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM questions WHERE id = %s', (question_id,))
    conn.commit()
    cursor.close()
    conn.close()

# ملاحظة: من الأفضل استخدام connection pooling أو ORM مثل SQLAlchemy في المستقبل