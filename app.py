from flask import Flask, render_template, request, redirect, jsonify
from database import Database

app = Flask(__name__)
db = Database("students.db")

@app.route("/")
def index():
    students = db.fetch_all()
    return render_template("index.html", students=students)

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        major = request.form["major"]
        db.insert_student(name, age, major)
        return redirect("/")
    return render_template("add_student.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
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
def delete_student(id):
    db.delete_student(id)
    return redirect("/")

# ---------------------------
# REST API ROUTES (JSON)
# ---------------------------

@app.route("/api/students", methods=["GET"])
def api_get_students():
    students = db.fetch_all()
    return jsonify(students)

@app.route("/api/student/<int:id>", methods=["GET"])
def api_get_student(id):
    student = db.fetch_by_id(id)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

@app.route("/api/student", methods=["POST"])
def api_add_student():
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")
    major = data.get("major")
    db.insert_student(name, age, major)
    return jsonify({"message": "Student added successfully"}), 201

@app.route("/api/student/<int:id>", methods=["PUT"])
def api_update_student(id):
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")
    major = data.get("major")
    db.update_student(id, name, age, major)
    return jsonify({"message": "Student updated successfully"})

@app.route("/api/student/<int:id>", methods=["DELETE"])
def api_delete_student(id):
    db.delete_student(id)
    return jsonify({"message": "Student deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)

