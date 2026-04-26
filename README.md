# Student Portal 🏫

## Overview
A simple web application demonstrating CRUD operations using Flask and SQLite.  
This project connects backend (Flask), database (SQLite), and frontend (HTML + CSS).

## Features
- Add new students via form (`add_student.html`)
- Edit existing students (`edit_student.html`)
- Delete students directly from the list
- View all students in a table (`index.html`)

## Visual Representation
### Add Student Form
![Add Student](add_student.png)

### Edit Student Form
![Edit Student](edit_student.png)

### Student List
![Student List](index.png)

## Technologies Used
- Python 3.14
- Flask framework
- SQLite database
- HTML + CSS frontend

## Run the App
pip install flask
python app.py


Open in browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Example Output

               Student Portal

                Add Student
ID | Name     | Age | Major              | Actions

1  | Marko    | 18  | Computer Science   | Edit | Delete
2  | Marija   | 19  | Economics          | Edit | Delete 
3  | Petar    | 20  | Physics            | Edit | Delete 