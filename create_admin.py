from database import Database

# Inicijalizuj bazu
db = Database("students.db")

# Kreiraj admin nalog (pokreni samo jednom!)
db.insert_user("admin", "adminpass", role="admin")

print("✅ Admin nalog kreiran: username='admin', password='adminpass'")
