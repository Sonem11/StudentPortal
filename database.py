import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    major TEXT
                )"""
        self.conn.execute(query)
        self.conn.commit()

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
