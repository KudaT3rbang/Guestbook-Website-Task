from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("guestbook.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        message TEXT NOT NULL
                      )''')
    conn.commit()
    conn.close()

@app.before_request
def before_request():
    init_db() 

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Number of messages per page
    offset = (page - 1) * per_page
    
    conn = sqlite3.connect("guestbook.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM entries")
    total_entries = cursor.fetchone()[0]
    
    cursor.execute("SELECT name, message FROM entries ORDER BY id DESC LIMIT ? OFFSET ?", (per_page, offset))
    entries = cursor.fetchall()
    conn.close()
    
    total_pages = (total_entries + per_page - 1) // per_page
    return render_template("index.html", entries=entries, page=page, total_pages=total_pages)

@app.route('/add', methods=['POST'])
def add_entry():
    name = request.form['name']
    message = request.form['message']
    if name and message:
        conn = sqlite3.connect("guestbook.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entries (name, message) VALUES (?, ?)", (name, message))
        conn.commit()
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
