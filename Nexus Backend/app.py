# API for the Database and frontend
from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

#test route 
@app.route("/")
def home():
    return "Nexus API is running!"


#products route 
@app.route("/Products")
def get_products():
    conn = sqlite3.connect('Nexus.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""SELECT Product.*, Brand.Name AS BrandName
                FROM Product
                JOIN Brand ON Product.Brand_ID = Brand.Brand_ID""")
    rows = cur.fetchall()

    conn.close()

    products = [dict(row) for row in rows]

    return jsonify(products)


if __name__ == "__main__":
    # debug=True lets you see errors and auto-reloads on save
    app.run(debug=True)
