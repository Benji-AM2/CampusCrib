from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to connect to the database
def init_sqlite_db():
    conn = sqlite3.connect('campuspad.db')
    conn.execute('CREATE TABLE IF NOT EXISTS rooms (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, price TEXT, location TEXT)')
    conn.close()

init_sqlite_db()

@app.route('/')
def home():
    search_query = request.args.get('search', '')
    conn = sqlite3.connect('campuspad.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if search_query:
        cursor.execute("SELECT * FROM rooms WHERE location LIKE ? OR title LIKE ?", ('%' + search_query + '%', '%' + search_query + '%'))
    else:
        cursor.execute("SELECT * FROM rooms")
        
    rooms = cursor.fetchall()
    conn.close()
    return render_template('index.html', rooms=rooms, search=search_query)

@app.route('/add', methods=['POST'])
def add_room():
    title = request.form['title']
    price = request.form['price']
    location = request.form['location']
    
    conn = sqlite3.connect('campuspad.db')
    conn.execute("INSERT INTO rooms (title, price, location) VALUES (?, ?, ?)", (title, price, location))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/delete/<int:room_id>', methods=['POST'])
def delete_room(room_id):
    conn = sqlite3.connect('campuspad.db')
    conn.execute("DELETE FROM rooms WHERE id = ?", (room_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)