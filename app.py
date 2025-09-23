from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)
DB_path = "task.db"

# --- Initialize database ---
def init_db():
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS tasks")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            priority INTEGER NOT NULL,
            label TEXT NOT NULL,
            task_name TEXT NOT NULL,
            date TEXT,
            time TEXT,
            task_desc TEXT,
            sub_todo TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

def edit_task(id, priority, label, task_name, date, time, task_desc, sub_todo):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks
        SET priority = ?, label = ?, task_name = ?, date = ?, time = ?, task_desc = ?, sub_todo = ?
        WHERE id = ?
    ''', (priority, label, task_name, date, time, task_desc, sub_todo, id))
    conn.commit()
    conn.close()

# --- Routes ---
@app.route('/')
def homepage():
    tasks = get_tasks()
    return render_template('homepage.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():

    try:
        priority = int(request.form.get("priority", 3))
    except ValueError:
        priority = 3

    label = request.form.get("label", "").strip()
    task_name = request.form.get("task_name", "").strip()
    date = request.form.get("date") or ""
    time = request.form.get("time") or ""
    task_desc = request.form.get("task_desc") or ""
    sub_todo = request.form.get("sub_todo") or ""

    add_task(priority, label, task_name, date, time, task_desc, sub_todo)
    return redirect(url_for("homepage"))

    # priority = request.form.get("priority")
    # label = request.form.get("label")
    # task_name = request.form.get("task_name")
    # date = request.form.get("date")
    # time = request.form.get("time")
    # task_desc = request.form.get("task_desc")
    # sub_todo = request.form.get("sub_todo")

    # add_task(priority, label, task_name, date, time, task_desc, sub_todo)
    # return redirect(url_for("homepage"))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    try:
        priority = int(request.form.get("priority", 3))
    except ValueError:
        priority = 3

    label = request.form.get("label", "").strip()
    task_name = request.form.get("task_name", "").strip()
    date = request.form.get("date") or ""
    time = request.form.get("time") or ""
    task_desc = request.form.get("task_desc") or ""
    sub_todo = request.form.get("sub_todo") or ""

    edit_task(task_id, priority, label, task_name, date, time, task_desc, sub_todo)
    return redirect(url_for("homepage"))

@app.template_filter("format_date")
def format_date(value, format="%B %d, %Y"):
    try:
        date_obj = datetime.strptime(value, "%Y-%m-%d")
        return date_obj.strftime(format)
    except Exception:
        return value

@app.template_filter("format_time")   
def format_time(value, format="%I:%M %p"):
    try:
        return datetime.strptime(value, "%H:%M").strftime(format)
    except Exception:
        return value

if __name__ == "__main__":
    init_db()
    app.run(debug=True)