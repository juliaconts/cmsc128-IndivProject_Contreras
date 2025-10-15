from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
import sqlite3, hashlib

app = Flask(__name__)
app.secret_key = "super-secret-key"
DB_path = "task.db"

def init_db():
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(255) NOT NULL UNIQUE,
            username VARCHAR(255) NOT NULL UNIQUE,
            fname TEXT NOT NULL,
            lname TEXT NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    
init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_id(id):
    with sqlite3.connect("task.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Accounts WHERE id = ?", (id,))
        return cursor.fetchone()
    
def get_user_email(email):
    with sqlite3.connect("task.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Accounts WHERE email = ?", (email,))
        return cursor.fetchone()
    
def edit_profile(id, username, fname, lname, password):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    if password:
        password = hash_password(password)
        cursor.execute('''
            UPDATE Accounts
            SET username = ?, fname = ?, lname = ?, password = ?
            WHERE id = ?
        ''', (username, fname, lname, password, id))
    else:
        cursor.execute('''
            UPDATE Accounts
            SET username = ?, fname = ?, lname = ?
            WHERE id = ?
        ''', (username, fname, lname, id))

    conn.commit()
    conn.close()

    
@app.route('/')
def home():
    if "id" in session:
        return redirect(url_for('login'))
    return redirect(url_for("signup"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = hash_password(request.form["password"])
        fname = request.form["fname"]
        lname = request.form["lname"]

        conn = sqlite3.connect(DB_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Accounts WHERE username = ? OR email = ?", (username, email))
        existing_user = cursor.fetchone()
        if existing_user:
            flash("Username or email already exists.", "error")
            return redirect(url_for("signup"))
        
        cursor.execute("INSERT INTO Accounts (email, username, fname, lname, password) VALUES (?, ?, ?, ?, ?)",
                       (email, username, fname, lname, password))
        
        conn.commit()
        conn.close()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    get_flashed_messages()
    if request.method == "POST":
        email = request.form["email"]
        password = hash_password(request.form["password"])

        user = get_user_email(email)
        if not user:
            # Email not found
            flash("No account found with that email.", "error")
            return redirect(url_for("login"))

        hashed_password = hash_password(password)
        if user[5] != hashed_password:
            # Wrong password
            flash("Incorrect password.", "error")
            return redirect(url_for("login"))

        # Correct login
        session["id"] = user[0]
        flash("Login successful!", "success")
        return redirect(url_for("profile"))

    return render_template("login.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "id" not in session:
        return redirect(url_for("login"))

    user_id = session["id"]
    user = get_user_id(user_id)

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        fname = request.form.get("fname", "").strip()
        lname = request.form.get("lname", "").strip()
        password = request.form.get("password", "").strip()

        if password:
            password = hash_password(password)
        else:
            password = user[5]

        conn = sqlite3.connect(DB_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Accounts
            SET username = ?, fname = ?, lname = ?, password = ?
            WHERE id = ?
        """, (username, fname, lname, password, user_id))
        conn.commit()
        conn.close()

        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))

    return render_template("acctProfile.html", user=user)

@app.route("/logout")
def logout():
    get_flashed_messages()
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# @app.route('/edit/<int:id>', methods=['POST'])
# def edit(id):
#     username = request.form.get("username", "").strip()
#     fname = request.form.get("fname", "").strip()
#     lname = request.form.get("lname", "").strip()
#     password = request.form.get("password", "").strip()

#     edit_profile(id, username, fname, lname, password)
#     flash("Profile updated successfully!", "success")
#     return redirect(url_for("profile"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)