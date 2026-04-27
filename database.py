import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        # Students tabela
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            major TEXT
        )
        """)
        # Users tabela
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT
        )
        """)
        self.conn.commit()

    # ---------------- STUDENTS ----------------
    def insert_student(self, name, age, major):
        self.conn.execute("INSERT INTO students (name, age, major) VALUES (?, ?, ?)", (name, age, major))
        self.conn.commit()

    def fetch_all(self):
        return self.conn.execute("SELECT * FROM students").fetchall()

    def fetch_by_id(self, student_id):
        return self.conn.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()

    def update_student(self, student_id, name, age, major):
        self.conn.execute("UPDATE students SET name=?, age=?, major=? WHERE id=?", (name, age, major, student_id))
        self.conn.commit()

    def delete_student(self, student_id):
        self.conn.execute("DELETE FROM students WHERE id=?", (student_id,))
        self.conn.commit()

    # ---------------- USERS ----------------
    def insert_user(self, username, password, role="student"):
        """Dodaje korisnika sa default role='student', osim ako se ručno prosledi 'admin'."""
        password_hash = generate_password_hash(password)
        self.conn.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                          (username, password_hash, role))
        self.conn.commit()

    def fetch_user(self, username):
        return self.conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()

    def verify_user(self, username, password):
        user = self.fetch_user(username)
        if user and check_password_hash(user[2], password):
            return user
        return None
