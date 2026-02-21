import sqlite3
import os
import random
import string

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'school.db')

def get_connection():
    """Single point for getting a database connection."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    c = conn.cursor()
    
    # Tokens table - with parent_name and status
    c.execute('''CREATE TABLE IF NOT EXISTS tokens
                 (token TEXT PRIMARY KEY, student_name TEXT, grade INTEGER, status TEXT, parent_name TEXT)''')
    
    # Check if parent_name column exists (for migrations)
    c.execute("PRAGMA table_info(tokens)")
    columns = [col[1] for col in c.fetchall()]
    if 'parent_name' not in columns:
        c.execute("ALTER TABLE tokens ADD COLUMN parent_name TEXT")
    if 'academic_year' not in columns:
        c.execute("ALTER TABLE tokens ADD COLUMN academic_year TEXT")
    
    # Results table
    c.execute('''CREATE TABLE IF NOT EXISTS results
                 (token TEXT, module TEXT, score INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Check if table needs migration (adding columns if necessary in future, but for now it's okay)
    
    # Pre-populate with some test tokens if empty
    c.execute("SELECT COUNT(*) FROM tokens")
    if c.fetchone()[0] == 0:
        test_tokens = [
            ('PSK00001', 'Test Student 1', 1, 'active', 'Parent A'),
            ('PSK00002', 'Test Student 2', 2, 'active', 'Parent B'),
            ('ADMIN100', 'Admin', 0, 'admin', 'N/A')
        ]
        c.executemany("INSERT INTO tokens (token, student_name, grade, status, parent_name) VALUES (?, ?, ?, ?, ?)", test_tokens)
        
    conn.commit()
    conn.close()

def validate_token(token):
    conn = get_connection()
    c = conn.cursor()
    # Return details regardless of status so app can handle feedback
    c.execute("SELECT student_name, grade, status FROM tokens WHERE token=?", (token,))
    result = c.fetchone()
    conn.close()
    return result

def request_token(name, grade, parent_name, academic_year, status='pending'):
    conn = get_connection()
    c = conn.cursor()
    
    # Get the count
    c.execute("SELECT COUNT(*) FROM tokens")
    count = c.fetchone()[0]
    next_num = count + 1
    token = f"PSK{next_num:05d}"
    
    try:
        c.execute("INSERT INTO tokens (token, student_name, grade, status, parent_name, academic_year) VALUES (?, ?, ?, ?, ?, ?)",
                   (token, name, grade, status, parent_name, academic_year))
        conn.commit()
        return token
    except sqlite3.IntegrityError:
        return request_token_manual(name, grade, parent_name, academic_year, next_num + 1, status)
    finally:
        conn.close()

def request_token_manual(name, grade, parent_name, academic_year, forced_num, status='pending'):
    conn = get_connection()
    c = conn.cursor()
    token = f"PSK{forced_num:05d}"
    try:
        c.execute("INSERT INTO tokens (token, student_name, grade, status, parent_name, academic_year) VALUES (?, ?, ?, ?, ?, ?)",
                   (token, name, grade, status, parent_name, academic_year))
        conn.commit()
        return token
    except sqlite3.IntegrityError:
        return request_token_manual(name, grade, parent_name, academic_year, forced_num + 1, status)
    finally:
        conn.close()

def get_pending_requests():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT token, student_name, grade FROM tokens WHERE status='pending'")
    results = c.fetchall()
    conn.close()
    return results

def approve_token(token):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE tokens SET status='active' WHERE token=?", (token,))
    conn.commit()
    conn.close()

def save_result(token, module, score):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO results (token, module, score) VALUES (?, ?, ?)", (token, module, score))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
