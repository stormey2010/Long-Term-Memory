from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from memory import extract

app = Flask(__name__)

def get_db_connection():
    return sqlite3.connect('core/memory/long-term.db')

def create_table():
    with get_db_connection() as conn:
        db = conn.cursor()
        db.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            importance INTEGER,
            keywords TEXT
        )
        ''')
        conn.commit()

create_table()

@app.route('/')
def index():
    items = view_all_items()
    return render_template('index.html', items=items)

@app.route('/insert', methods=['POST'])
def insert():
    name = request.form['name']
    description = request.form['description']
    importance = int(request.form['importance'])
    keywords = request.form['keywords']
    
    # AI integration for new items
    ai_response = extract.extract_memories(name + ' ' + description + ' ' + keywords)
    if ai_response != "The generation failed.":
        # Process and insert new items based on AI response
        pass
    
    insert_item(name, description, importance, keywords)
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    keywords = request.args.get('keywords', '').split(',')
    results = search_items(keywords)
    return render_template('search_results.html', items=results)

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    delete_item(item_id)
    return redirect(url_for('index'))

@app.route('/delete_all', methods=['POST'])
def delete_all():
    delete_all_items()
    return redirect(url_for('index'))

@app.route('/item_details/<int:item_id>')
def item_details(item_id):
    item = get_item(item_id)
    if item:
        return render_template('item_details.html', item=item)
    return redirect(url_for('index'))

@app.route('/update_item/<int:item_id>', methods=['POST'])
def update_item(item_id):
    name = request.form['name']
    description = request.form['description']
    importance = int(request.form['importance'])
    keywords = request.form['keywords']
    update_item_details(item_id, name, description, importance, keywords)
    return redirect(url_for('item_details', item_id=item_id))

@app.route('/add_item')
def add_item():
    return render_template('add_item.html')

@app.route('/ai_add_item', methods=['GET', 'POST'])
def ai_add_item():
    if request.method == 'POST':
        text = request.form['text']
        extract.memory_set(text)
        return redirect(url_for('index'))
    return render_template('ai_add_item.html')



def insert_item(name, description, importance, keywords):
    with get_db_connection() as conn:
        db = conn.cursor()
        db.execute('''
        INSERT INTO items (name, description, importance, keywords)
        VALUES (?, ?, ?, ?)
        ''', (name, description, importance, keywords))
        conn.commit()

def update_item_details(item_id, name, description, importance, keywords):
    with get_db_connection() as conn:
        db = conn.cursor()
        db.execute('''
        UPDATE items
        SET name = ?, description = ?, importance = ?, keywords = ?
        WHERE id = ?
        ''', (name, description, importance, keywords, item_id))
        conn.commit()


def get_item(item_id):
    with get_db_connection() as conn:
        db = conn.cursor()
        db.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        return db.fetchone()

def search_items(keywords):
    with get_db_connection() as conn:
        db = conn.cursor()
        if not keywords:
            return []
        
        query = "SELECT * FROM items WHERE "
        conditions = []
        params = []
        for keyword in keywords:
            conditions.append("(name LIKE ? OR description LIKE ? OR keywords LIKE ?)")
            params.extend(['%' + keyword + '%'] * 3)
        query += " OR ".join(conditions)
        db.execute(query, params)
        return db.fetchall()

def view_all_items():
    with get_db_connection() as conn:
        db = conn.cursor()
        db.execute('SELECT * FROM items')
        return db.fetchall()

def delete_item(item_id):
    with get_db_connection() as conn:
        db = conn.cursor()
        db.execute('DELETE FROM items WHERE id = ?', (item_id,))
        conn.commit()

def delete_all_items():
    with get_db_connection() as conn:
        db = conn.cursor()
        db.execute('DELETE FROM items')
        conn.commit()

if __name__ == '__main__':
    app.run(debug=True)
