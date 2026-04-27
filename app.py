from flask import Flask, render_template, request, redirect, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from database import Database
import jwt
import datetime
from functools import wraps
import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env (lokalno)
load_dotenv()

app = Flask(__name__)

# Flask secret key (za sesije, CSRF, Flask-Login)
app.secret_key = os.environ.get("SECRET_KEY", "fallback_secret")

# JWT secret (za token autentikaciju)
JWT_SECRET = os.environ.get("JWT_SECRET", "fallback_jwt_secret")

db = Database("students.db")

# ---------------------------
# LOGIN MANAGER CONFIG
# ---------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    user = db.conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    if user:
        return User(user[0], user[1], user[3])
    return None

# ---------------------------
# JWT CONFIG
# ---------------------------
JWT_SECRET = "tajna_jwt_lozinka"  # promeni u nešto jače
JWT_ALGORITHM = "HS256"

def generate_token(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing"}), 401
        token = auth_header.split(" ")[1]
        payload = verify_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        request.user = payload
        return f(*args, **kwargs)
    return decorated

# ---------------------------
# VALIDATION HELPER
# ---------------------------
def validate_student_data(data):
    name = data.get("name")
    age = data.get("age")
    major = data.get("major")

    if not name or not isinstance(name, str) or name.strip() == "":
        return {"error": "Name is required and must be a non-empty string"}

    try:
        age = int(age)
    except (TypeError, ValueError):
        return {"error": "Age must be a valid integer"}

    if not major or not isinstance(major, str) or major.strip() == "":
        return {"error": "Major is required and must be a non-empty string"}

    return None

# ---------------------------
# WEB ROUTES (Flask-Login)
# ---------------------------
@app.route("/")
@login_required
def index():
    if current_user.role == "admin":
        students = db.fetch_all()
    else:
        # Student vidi samo svoj red (po username-u)
        students = db.conn.execute(
            "SELECT * FROM students WHERE name=?",
            (current_user.username,)
        ).fetchall()
    return render_template("index.html", students=students)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        major = request.form["major"]
        db.insert_student(name, age, major)
        return redirect("/")
    return render_template("add_student.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_student(id):
    student = db.fetch_by_id(id)
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        major = request.form["major"]
        db.update_student(id, name, age, major)
        return redirect("/")
    return render_template("edit_student.html", student=student)

@app.route("/delete/<int:id>")
@login_required
def delete_student(id):
    if current_user.role != "admin":
        return "Access denied", 403
    db.delete_student(id)
    return redirect("/")

# ---------------------------
# AUTH ROUTES (Flask-Login)
# ---------------------------

# ---------------------------
# CREATE ADMIN ROUTE (privremeno za Render)
# ---------------------------
@app.route("/create_admin")
def create_admin():
    cursor = db.conn.execute("SELECT * FROM users WHERE username=?", ("admin",))
    if cursor.fetchone():
        return "Admin already exists!"
    db.insert_user("admin", "admin123Arl11+", role="admin")
    return "Admin created: username=admin, password=admin123Arl11+"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db.insert_user(username, password)
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db.fetch_user(username)
        if user and check_password_hash(user[2], password):
            login_user(User(user[0], user[1], user[3]))
            return redirect("/")
        return "Invalid credentials"
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    user_id = current_user.id
    db.conn.execute("DELETE FROM users WHERE id=?", (user_id,))
    db.conn.commit()
    logout_user()
    return redirect("/register")

# ---------------------------
# AUTH ROUTE (JWT for API)
# ---------------------------
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = db.fetch_user(username)
    if user and check_password_hash(user[2], password):
        token = generate_token(user[0], user[3])
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401

# ---------------------------
# REST API ROUTES (JWT Protected)
# ---------------------------
@app.route("/students", methods=["GET"])
@jwt_required
def api_get_students():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    major = request.args.get("major")

    query = "SELECT * FROM students"
    params = []

    if major:
        query += " WHERE major=?"
        params.append(major)

    offset = (page - 1) * limit
    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    students = db.conn.execute(query, tuple(params)).fetchall()
    return jsonify(students)

@app.route("/student/<int:id>", methods=["GET"])
@jwt_required
def api_get_student(id):
    student = db.fetch_by_id(id)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

@app.route("/student", methods=["POST"])
@jwt_required
def api_add_student():
    data = request.get_json()
    error = validate_student_data(data)
    if error:
        return jsonify(error), 400

    name = data.get("name")
    age = int(data.get("age"))
    major = data.get("major")

    db.insert_student(name, age, major)
    return jsonify({"message": "Student added successfully"}), 201

@app.route("/student/<int:id>", methods=["PUT"])
@jwt_required
def api_update_student(id):
    data = request.get_json()
    error = validate_student_data(data)
    if error:
        return jsonify(error), 400

    name = data.get("name")
    age = int(data.get("age"))
    major = data.get("major")

    db.update_student(id, name, age, major)
    return jsonify({"message": "Student updated successfully"})

@app.route("/student/<int:id>", methods=["DELETE"])
@jwt_required
def api_delete_student(id):
    db.delete_student(id)
    return jsonify({"message": "Student deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
