from database import Database

db = Database("students.db")

db.conn.execute("DELETE FROM users WHERE username=?", ("admin",))
db.conn.commit()

print("User 'admin' deleted.")
