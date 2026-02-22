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
    
    # Tokens table - with school_type and specialized IDs
    c.execute('''CREATE TABLE IF NOT EXISTS tokens
                 (token TEXT PRIMARY KEY, student_name TEXT, grade INTEGER, status TEXT, 
                  parent_name TEXT, academic_year TEXT, school_type TEXT)''')
    
    # Results table
    c.execute('''CREATE TABLE IF NOT EXISTS results
                 (token TEXT, module TEXT, score INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Feedback/Message table
    c.execute('''CREATE TABLE IF NOT EXISTS feedback
                 (token TEXT, message TEXT, status TEXT DEFAULT 'unread', timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Check for missing columns (Migrations)
    c.execute("PRAGMA table_info(tokens)")
    columns = [col[1] for col in c.fetchall()]
    if 'school_type' not in columns:
        c.execute("ALTER TABLE tokens ADD COLUMN school_type TEXT DEFAULT 'Primary'")
    if 'parent_name' not in columns:
        c.execute("ALTER TABLE tokens ADD COLUMN parent_name TEXT")
    if 'academic_year' not in columns:
        c.execute("ALTER TABLE tokens ADD COLUMN academic_year TEXT")
    
    # Check if table needs migration (adding columns if necessary in future, but for now it's okay)
    
    # Pre-populate with specialized admins individually
    admins = [
        ('ADMIN100', 'Primary Admin', 0, 'admin', 'N/A', '2024-25', 'Primary'),
        ('GHSADMIN01', 'High School Admin', 0, 'admin', 'N/A', '2024-25', 'High School'),
        ('GHT00001', 'HS Super Admin', 0, 'admin', 'N/A', '2024-25', 'High School')
    ]
    
    for admin in admins:
        c.execute("SELECT COUNT(*) FROM tokens WHERE token=?", (admin[0],))
        if c.fetchone()[0] == 0:
            c.execute("INSERT INTO tokens (token, student_name, grade, status, parent_name, academic_year, school_type) VALUES (?, ?, ?, ?, ?, ?, ?)", admin)
        
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

def request_token(name, grade, parent_name, academic_year, school_type='Primary', status='pending'):
    conn = get_connection()
    c = conn.cursor()
    
    # Get the count for specific school type
    c.execute("SELECT COUNT(*) FROM tokens WHERE school_type=?", (school_type,))
    count = c.fetchone()[0]
    next_num = count + 1
    
    prefix = "PSK" if school_type == 'Primary' else "GHS"
    token = f"{prefix}{next_num:05d}"
    
    try:
        c.execute("INSERT INTO tokens (token, student_name, grade, status, parent_name, academic_year, school_type) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (token, name, grade, status, parent_name, academic_year, school_type))
        conn.commit()
        return token
    except sqlite3.IntegrityError:
        return request_token_manual(name, grade, parent_name, academic_year, school_type, next_num + 1, status)
    finally:
        conn.close()

def request_token_manual(name, grade, parent_name, academic_year, school_type, forced_num, status='pending'):
    conn = get_connection()
    c = conn.cursor()
    prefix = "PSK" if school_type == 'Primary' else "GHS"
    token = f"{prefix}{forced_num:05d}"
    try:
        c.execute("INSERT INTO tokens (token, student_name, grade, status, parent_name, academic_year, school_type) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (token, name, grade, status, parent_name, academic_year, school_type))
        conn.commit()
        return token
    except sqlite3.IntegrityError:
        return request_token_manual(name, grade, parent_name, academic_year, school_type, forced_num + 1, status)
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

def save_feedback(token, message):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO feedback (token, message) VALUES (?, ?)", (token, message))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
