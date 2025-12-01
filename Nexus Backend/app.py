# API for the Database and frontend
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

#test route 
@app.route("/")
def home():
    return "Nexus API is running!"


# products route for multiple 
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

# Product route for 1
@app.route("/Products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    conn = sqlite3.connect('Nexus.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()


    cur.execute("""
                SELECT Product.*, Brand.Name AS BrandName
                FROM Product
                JOIN Brand ON Product.Brand_ID = Brand.Brand_ID
                WHERE Product.Product_ID = ?
                """, (product_id,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Product is not Found"}), 404
    
    return jsonify(dict(row))


#  Post Product/creating product
@app.route("/Products", methods=["POST"])
def create_product():
    data = request.get_json()

    Brand_ID = data.get("Brand_ID")
    Name = data.get("Name")
    Description = data.get("Description")
    Price = data.get("Price")
    Image = data.get("Image")
    Stock_count = data.get("Stock_count")
    Rating = data.get("Rating")
    Review_Count = data.get("Review_Count")

    conn = sqlite3.connect("Nexus.db")
    cur = conn.cursor()

    cur.execute("""
            INSERT INTO Product (Brand_ID, Name, Description, Price, Image, Stock_count, Rating, Review_Count)
            VALUES(?,?,?,?,?,?,?,?)
             """, (Brand_ID, Name, Description, Price, Image, Stock_count, Rating, Review_Count))

    conn.commit()    
    conn.close()

    return jsonify({"message": "Product was Created succesfully"}), 201



# product update
@app.route("/Products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json()

    conn = sqlite3.connect('Nexus.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Check if product exists
    cur.execute("SELECT * FROM Product WHERE Product_ID = ?", (product_id,))
    if cur.fetchone() is None:
        return jsonify({"error": "Product not found"}), 404

    # Update the product
    cur.execute("""
        UPDATE Product
        SET Brand_ID = ?, Name = ?, Description = ?, Price = ?, Image = ?, Stock_count = ?, Rating = ?, Review_Count = ?
        WHERE Product_ID = ?
    """, (
        data.get("Brand_ID"),
        data.get("Name"),
        data.get("Description"),
        data.get("Price"),
        data.get("Image"),
        data.get("Stock_count"),
        data.get("Rating"),
        data.get("Review_Count"),
        product_id
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Product updated successfully"})


# delete products 
@app.route("/Products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    conn = sqlite3.connect('Nexus.db')
    cur = conn.cursor()

    # Check if product exists
    cur.execute("SELECT * FROM Product WHERE Product_ID = ?", (product_id,))
    if cur.fetchone() is None:
        return jsonify({"error": "Product not found"}), 404

    # Delete product
    cur.execute("DELETE FROM Product WHERE Product_ID = ?", (product_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Product deleted successfully"})

#TO DO LIST

#Brand
""""
GET /Brand

GET /Brand/<id>

POST /Brand

PUT /Brand/<id>

DELETE /Brand/<id>

"""
# get brands multiple
@app.route("/Brands")
def get_brands():
    conn = sqlite3.connect('Nexus.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM Brand")
    rows = cur.fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])

# get brand singular
@app.route("/Brands/<int:brand_id>", methods=["GET"])
def get_brand(brand_id):
    conn = sqlite3.connect('Nexus.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM Brand WHERE Brand_ID = ?", (brand_id,))
    row = cur.fetchone()

    conn.close()

    if row is None:
        return jsonify({"error": "Brand cannot be found"}), 404
    
    return jsonify(dict(row))

# post brands, create
@app.route("/Brands", methods = ["POST"])
def create_brand():
    data = request.get_json()

    name = data.get("Name")

    conn = sqlite3.connect("Nexus.db")
    cur = conn.cursor()

    cur.execute("""
            INSERT INTO Brand (Name)
            VALUES(?)
             """, (name,))

    conn.commit()    
    conn.close()

    return jsonify({"message": "Brand was Created succesfully"}), 201

# put in new data to update brand
@app.route("/Brands/<int:brand_id>", methods = ["PUT"])
def update_brands(brand_id):
    data = request.get_json()
    conn = sqlite3.connect('Nexus.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM Brand WHERE Brand_ID = ?",(brand_id))
    if cur.fetchone() is None:
        return jsonify({"error": "Brand not found"}), 404

    # Update the product
    cur.execute("""
        UPDATE Brand
        SET Name = ?
        WHERE Brand_ID = ?
    """, (
        data.get("Name"),
        brand_id
    ))
    conn.commit()
    conn.close()

    return jsonify({"message": "Brand updated successfully"})


# Delete the Brand
@app.route("/Brands/<int:brand_id>", methods = ["DELETE"])
def delete_brand(brand_id):
    conn = sqlite3.connect('Nexus.db')
    cur = conn.cursor()

    # Check if product exists
    cur.execute("SELECT * FROM Brand WHERE Brand_ID = ?", (brand_id,))
    if cur.fetchone() is None:
        return jsonify({"error": "Brand can not be found"}), 404

    # Delete product
    cur.execute("DELETE FROM Brand WHERE Brand_ID = ?", (brand_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Brand deleted successfully"})

#User
"""
POST /Users

POST /Login

GET /Users/<id>

PUT /Users/<id>

DELETE /Users/<id>
"""







#Orders
"""
POST /Orders

GET /Orders/<id>

GET /Orders/user/<user_id>

DELETE /Orders/<id>
"""
#History/order Items
"""
GET /History/<user_id>
(returns all orders + items)
"""









if __name__ == "__main__":
    # debug=True lets you see errors and auto-reloads on save
    app.run(debug=True)

