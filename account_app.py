from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "super-secret-key"
DB_path = "accounts.db"

def init_db():
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Accounts (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,
            fname TEXT NOT NULL,
            lname TEXT NOT NULL,
            password VARCHAR(255) NOT NULL DEFAULT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def signup():
    
    

if __name__ == "__main__":
    init_db()
    app.run(debug=True)