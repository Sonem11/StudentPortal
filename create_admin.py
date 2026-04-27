from database import Database

# inicijalizuj bazu
db = Database("students.db")

# ubaci admin nalog
db.insert_user("admin", "admin123Arl11+", role="admin")

print("Admin user created: username=admin, password=admin123Arl11+")

