from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
database = 'names.db'

def init_db():
    if not os.path.exists(database):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute('''CREATE TABLE names (id INTEGER PRIMARY KEY, name TEXT)''')
        conn.commit()
        conn.close()

@app.route('/add_name', methods=['POST'])
def add_name():
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'success': False}), 400
    
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute('INSERT INTO names (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
