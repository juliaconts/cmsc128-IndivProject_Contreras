from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, os, hashlib

app = Flask(__name__)
app.secret_key = "super-secret-key"
DB_path = "accounts.db"

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
    with sqlite3.connect("accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Accounts WHERE id = ?", (id,))
        return cursor.fetchone()
    
def get_user_email(email):
    with sqlite3.connect("accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Accounts WHERE email = ?", (email,))
        return cursor.fetchone()
    
@app.route('/')
def home():
    if "id" in session:
        return redirect(url_for('profile'))
    return redirect(url_for("login"))

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
    if request.method == "POST":
        email = request.form["email"]
        password = hash_password(request.form["password"])

        user = get_user_email(email)
        if user and user[5] == password:
            session["id"] = user[0]
            flash("Login successfull!", "success")
            return redirect(url_for("profile"))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/profile")
def profile():
    if "id" not in session:
        return redirect(url_for("login"))
    
    user = get_user_id(session["id"])
    return render_template("acctProfile.html", user=user)

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)