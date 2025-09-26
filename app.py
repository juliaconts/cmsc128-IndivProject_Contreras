from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta, timezone
import sqlite3

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

app = Flask(__name__)
app.secret_key = "super-secret-key"  # needed for session + flash
DB_path = "task.db"

# --- Helper: get Manila timestamp ---
def get_manila_now():
    if ZoneInfo:
        try:
            return datetime.now(ZoneInfo("Asia/Manila"))
        except:
            return datetime.now(timezone(timedelta(hours=8)))
    else:
        return datetime.now(timezone(timedelta(hours=8)))


# --- Initialize database ---
def init_db():
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    # cursor.execute("DROP TABLE IF EXISTS tasks")
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
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()


# --- Get all tasks ---
def get_tasks(sort_by="priority"):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()

    if sort_by == "priority":
        cursor.execute('SELECT * FROM tasks ORDER BY priority ASC')
    elif sort_by == "due":
        cursor.execute('SELECT * FROM tasks ORDER BY date ASC, time ASC')
    elif sort_by == "timestamp":
        cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
    else:
        cursor.execute('SELECT * FROM tasks')

    tasks = cursor.fetchall()
    conn.close()
    return tasks


# --- Add task ---
def add_task(priority, label, task_name, date, time, task_desc, sub_todo):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()

    created_at = get_manila_now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        INSERT INTO tasks (priority, label, task_name, date, time, task_desc, sub_todo, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (priority, label, task_name, date, time, task_desc, sub_todo, created_at))

    conn.commit()
    conn.close()


# --- Edit task ---
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


# --- Delete task (and return deleted row for undo) ---
def delete_task(id):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    deleted = cursor.fetchone()
    if deleted:
        cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return deleted


# --- Restore task (undo delete) ---
def restore_task(task_data):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (id, priority, label, task_name, date, time, task_desc, sub_todo, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', task_data)
    conn.commit()
    conn.close()


# ------------------ Routes ------------------

@app.route('/')
def homepage():
    sort = request.args.get("sort", None)
    tasks = get_tasks(sort)
    return render_template('homepage.html', tasks=tasks, sort=sort)

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


@app.route('/delete/<int:task_id>')
def delete(task_id):
    deleted_task = delete_task(task_id)
    if deleted_task:
        session['last_deleted'] = deleted_task
        flash("Task Deleted")
    return redirect(url_for("homepage"))


@app.route('/undo_delete')
def undo_delete():
    if 'last_deleted' in session:
        restore_task(session['last_deleted'])
        session.pop('last_deleted')
        flash("Task Restored")
    return redirect(url_for("homepage"))


# --- Filters ---
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


@app.template_filter("format_timestamp")
def format_timestamp(value, format="%m-%d-%Y | %I:%M %p"):
    try:
        dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        return dt.strftime(format)
    except Exception as e:
        print("Timestamp parse error:", e, value)
        return value


if __name__ == "__main__":
    init_db()
    app.run(debug=True)