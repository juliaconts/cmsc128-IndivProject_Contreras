from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_path = "task.db"

# --- Initialize database ---
def init_db():
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            priority INTEGER NOT NULL,
            label TEXT NOT NULL,
            task_name TEXT NOT NULL,
            date TEXT,
            time TEXT,
            task_desc TEXT,
            sub_todo TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- Get all tasks ---
def get_tasks():
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# --- Add a new task ---
def add_task(priority, label, task_name, date, time, task_desc, sub_todo):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (priority, label, task_name, date, time, task_desc, sub_todo)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (priority, label, task_name, date, time, task_desc, sub_todo))
    conn.commit()
    conn.close()

# --- Routes ---
@app.route('/')
def homepage():
    tasks = get_tasks()
    return render_template('homepage.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    priority = request.form.get("priority")
    label = request.form.get("label")
    task_name = request.form.get("task_name")
    date = request.form.get("date")
    time = request.form.get("time")
    task_desc = request.form.get("task_desc")
    sub_todo = request.form.get("sub_todo")

    add_task(priority, label, task_name, date, time, task_desc, sub_todo)
    return redirect(url_for("homepage"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)