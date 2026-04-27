# Student Portal 🏫

## Overview
A simple web application demonstrating CRUD operations using **Flask** and **SQLite**.  
This project connects backend (Flask), database (SQLite), and frontend (HTML + CSS).  
Extended with **REST API endpoints** for JSON access, **JWT authentication**, and **pytest test coverage**.

---

## Features
- Add new students via form (`add_student.html`)
- Edit existing students (`edit_student.html`)
- Delete students directly from the list
- View all students in a table (`index.html`)
- REST API for programmatic access (CRUD)
- JWT authentication for API routes
- UML diagram showing project structure
- Pytest test suite (`tests/`) for authentication and CRUD

---

## UML Diagram
The following diagram illustrates the structure of the Student Portal:

![Class Diagram](images/class_diagram.png)

---

## Visual Representation

### Add Student Form
![Add Student](images/add_student.png)

### Edit Student Form
![Edit Student](images/edit_student.png)

### Student List
![Student List](images/index.png)

---

## Technologies Used
- Python 3.14
- Flask framework
- SQLite database
- HTML + CSS frontend
- PyJWT for authentication
- Pytest for testing
- Gunicorn for deployment

---

## Run the App Locally
```bash
pip install -r requirements.txt
python app.py
Open in browser: http://127.0.0.1:5000

REST API Endpoints
All REST routes are implemented in app.py.
Responses are returned in JSON format.

Method	Endpoint	Description	Example Response
✅ GET	/students	Get all students	[{"id":1,"name":"Marko","age":18,"major":"Computer Science"}]
✅ GET	/student/	Get student by ID	{"id":1,"name":"Marko","age":18,"major":"Computer Science"}
➕ POST	/student	Add new student (JSON body)	{"message":"Student added successfully"}
✏️ PUT	/student/	Update student by ID	{"message":"Student updated successfully"}
❌ DELETE	/student/	Delete student by ID	{"message":"Student deleted successfully"}


Example Usage (Windows CMD)
bash
# Get all students
curl http://127.0.0.1:5000/students

# Get student by ID
curl http://127.0.0.1:5000/student/1

# Add new student
curl -X POST http://127.0.0.1:5000/student -H "Content-Type: application/json" -d "{\"name\":\"Petar\",\"age\":20,\"major\":\"Physics\"}"

# Update student
curl -X PUT http://127.0.0.1:5000/student/1 -H "Content-Type: application/json" -d "{\"name\":\"Marko Updated\",\"age\":19,\"major\":\"Math\"}"

# Delete student
curl -X DELETE http://127.0.0.1:5000/student/1
🧪 Running Tests
Test files are located in tests/.

Run all tests:

bash
pytest -v
Run a single file:

bash
pytest tests/test_auth.py
Run a single test:

bash
pytest tests/test_students.py::test_add_student_api
🚀 Deployment (Render.com)
Create an account on Render.

Connect your GitHub repository.

Add Procfile and requirements.txt in the project root.

Procfile:

Code
web: gunicorn app:app
requirements.txt:

Code
Flask
Flask-Login
Werkzeug
PyJWT
gunicorn
pytest
Render automatically installs dependencies and runs the app with:

Build Command: pip install -r requirements.txt

Start Command: gunicorn app:app

The application will be available at:

Code
https://student-portal.onrender.com
Project Structure
Code
StudentPortal/
│── app.py
│── database.py
│── students.db
│── templates/
│   ├── index.html
│   ├── add_student.html
│   ├── edit_student.html
│   ├── login.html
│   └── register.html
│── static/
│   └── style.css
│── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_students.py
│── images/
│   ├── add_student.png
│   ├── edit_student.png
│   ├── index.png
│   └── class_diagram.png
│── Procfile
│── requirements.txt
│── .gitignore
│── README.md