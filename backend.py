import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#example items in our store
items = [
    {'title': 'Comb',
    'price': 2,
    'inventory_count': 4},
    {'title': 'Watch',
    'price': 50,
    'inventory_count': 40},
    {'title': 'Orange juice',
    'price': 2,
    'inventory_count': 3}
]

DATABASE = 'sample_items.db'

#get dictionary of our store
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/backend/v1/resources/items/all', methods=['GET'])
def get_all_items():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_items = cur.execute('SELECT * FROM items;').fetchall()

    return jsonify(all_items)


#get the specified item
@app.route('/backend/v1/resources/items', methods=['GET'])
def get_item():
    query_parameters = request.args

    title = query_parameters.get('title')

    query = "SELECT * FROM items WHERE"
    query_content = []

    query += ' title=?'
    query_content.append(title)

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, query_content).fetchall()

    return jsonify(results)


#decrement item's inventory_count by 1 if inventory_count is not already 0
@app.route('/backend/v1/resources/items/purchase/<item_title>', methods=['POST'])
def purchase_item():
    title = item_title

    query= 'UPDATE items SET inventory_count = inventory_count - 1 WHERE title = {} and inventory_count > 0'.format(title)

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    cur.execute(query).fetchall()

app.run()
