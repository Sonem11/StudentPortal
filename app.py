from flask import Flask, render_template, request, redirect
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

if __name__ == "__main__":
    app.run(debug=True)
