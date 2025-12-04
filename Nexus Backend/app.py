# API for the Database and frontend
import os 
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


# 200 is good
# 400 is bad request
# 401 is unathorized 
# 402 is payment req
# 404 is Not found error
# 409 is conflict
# 500 is internal server

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
ADMIN_RESET_KEY = os.environ.get("ADMIN_RESET_KEY", "dev-reset-key")


# make the databse when booting up the live server
def init_database():
    db_path = "Nexus.db"

    # If DB exists, do nothing
    if os.path.exists(db_path):
        print("Database already exists. Skipping initialization.")
        return

    print("Initializing database...")

    import Nexus_db   # creates tables
    import seed_data  # defines seed()

    seed_data.seed()

    print("Database created and seeded.")


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
    
    cur.execute("SELECT * FROM Brand WHERE Brand_ID = ?",(brand_id,))
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

    # Check if Brand exists
    cur.execute("SELECT * FROM Brand WHERE Brand_ID = ?", (brand_id,))
    if cur.fetchone() is None:
        return jsonify({"error": "Brand can not be found"}), 404

    # Delete BRand
    cur.execute("DELETE FROM Brand WHERE Brand_ID = ?", (brand_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Brand deleted successfully"})


#User
# create users
@app.route("/Users", methods = ["POST"])
def create_user():
    data = request.get_json()

    name = data.get("Name")
    email = data.get("Email")
    password = data.get("Password")
    role = data.get("Role")

    hashed_pw = generate_password_hash(password)

    conn = sqlite3.connect("Nexus.db")
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO User (Name, Email, Password, Role) 
            VALUES(?,?,?,?)
            """, (name,email,hashed_pw,role,))
        conn.commit()

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already in use"}), 400
    

    finally:
        conn.close()

    return jsonify({"message": "User was Created succesfully"}), 201


#login information
@app.route("/Login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("Email")
    password = data.get("Password")

    conn = sqlite3.connect("Nexus.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM User WHERE Email = ?", (email,))
    user = cur.fetchone()
    conn.close()

    if user is None:
        return jsonify({"error": "Email or Password is Invalid"}), 401

    # Secure password check
    if not check_password_hash(user["Password"], password):
        return jsonify({"error": "Email or Password is Invalid"}), 401

    return jsonify({
        "message": "Login successful",
        "User_ID": user["User_ID"],
        "Name": user["Name"],
        "Role": user["Role"]
    }), 200




# get Users multiple
@app.route("/Users", methods = ["GET"])
def get_users():
    conn = sqlite3.connect("Nexus.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""SELECT * FROM User""")
    rows = cur.fetchall()

    conn.close()
    return jsonify([dict(row) for row in rows])

# Get User singular

@app.route("/Users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = sqlite3.connect("Nexus.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""SELECT * FROM User WHERE User_ID = ?""",(user_id,))
    row = cur.fetchone()

    conn.close()

    if row is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(dict(row))

# update user information 
@app.route("/Users/<int:user_id>", methods = ["PUT"])
def update_user(user_id):
    data = request.get_json()
    conn = sqlite3.connect('Nexus.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    

    cur.execute("SELECT * FROM User WHERE User_ID = ?",(user_id,))
    if cur.fetchone() is None:
        conn.close()
        return jsonify({"error": "User can not be found"}), 404

    hashed_pw = generate_password_hash(data.get("Password"))
    # Update
    try:
        cur.execute("""
            UPDATE User
            SET Name = ?, Email = ?, Password = ?, Role = ?
            WHERE User_ID = ?
        """, (
            data.get("Name"),
            data.get("Email"),
            hashed_pw,
            data.get("Role"),
            user_id
        ))
        conn.commit()
        conn.close()
        
        return jsonify({"message": "User updated successfully"}),200
    
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Email is already in use"}),400

# dete the User
@app.route("/Users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = sqlite3.connect('Nexus.db')
    cur = conn.cursor()

    # Check if user exists
    cur.execute("SELECT * FROM User WHERE User_ID = ?", (user_id,))
    if cur.fetchone() is None:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    # Delete user
    cur.execute("DELETE FROM User WHERE User_ID = ?", (user_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "User deleted successfully"})

"""
expecting order data to look like
{
  "User_ID": 3,
  "Total": 2499.97,
  "Items": [
    { "Product_ID": 1, "Quantity": 2, "Price": 999.99 },
    { "Product_ID": 4, "Quantity": 1, "Price": 499.99 }
  ]
}
makes a order row and take the ID to put in the OrderItems
"""
# Create an order
@app.route("/Orders", methods=["POST"])
def create_order():
    data = request.get_json()

    user_id = data.get("User_ID")
    items = data.get("Items") #list of phones[iphone2,samsung4]
    total = data.get("Total")

    if not user_id or not items or total is None:
        return jsonify({"error": "Missing order fields"}), 400

    conn = sqlite3.connect("Nexus.db")
    cur = conn.cursor()

    try:
        # 1. Insert into Orders table
        cur.execute("""
            INSERT INTO Orders (User_ID, Total_price, Status)
            VALUES (?, ?, ?)
        """, (user_id, total, "Completed"))

        order_id = cur.lastrowid  # GET the generated Order_ID for OrderItems

        # 2. Insert each order into orderItens
        for item in items:
            cur.execute("""
                INSERT INTO OrderItem (Order_ID, Product_ID, Quantity, Price)
                VALUES (?, ?, ?, ?)
            """, (
                order_id,
                item["Product_ID"],
                item["Quantity"],
                item["Price"]
            ))
            cur.execute("""
                UPDATE Product
                SET Stock_count = Stock_count - ?
                WHERE Product_ID = ?""", 
                (item["Quantity"], item["Product_ID"]))

        conn.commit()

    finally:
        conn.close()

    return jsonify({
        "message": "Order created successfully",
        "Order_ID": order_id
    }), 201


# get a singular order's items
@app.route("/Orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    conn = sqlite3.connect("Nexus.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM Orders WHERE Order_ID = ?
    """, (order_id,))
    order = cur.fetchone()

    if order is None:
        conn.close()
        return jsonify({"error": "Order not found"}), 404

    # Get order items and products
    cur.execute("""
        SELECT OI.*, P.Name, P.Image 
        FROM OrderItem OI
        JOIN Product P ON OI.Product_ID = P.Product_ID
        WHERE OI.Order_ID = ?
    """, (order_id,))
    items = [dict(row) for row in cur.fetchall()]

    conn.close()

    order_dict = dict(order)
    order_dict["Items"] = items

    return jsonify(order_dict), 200

# All orders on a user
@app.route("/Orders/user/<int:user_id>", methods=["GET"])
def get_orders_by_user(user_id):
    conn = sqlite3.connect("Nexus.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get all orders for user
    cur.execute("""
        SELECT * FROM Orders WHERE User_ID = ?
    """, (user_id,))
    orders = cur.fetchall()
    #empty
    if not orders:
        conn.close()
        return jsonify([]), 200

    # Build list including items
    results = []

    for order in orders:
        order_id = order["Order_ID"]

        # Get each item's product details
        cur.execute("""
            SELECT OI.*, P.Name, P.Image 
            FROM OrderItem OI
            JOIN Product P ON OI.Product_ID = P.Product_ID
            WHERE OI.Order_ID = ?
        """, (order_id,))
        items = [dict(row) for row in cur.fetchall()]

        order_dict = dict(order)
        order_dict["Items"] = items
        results.append(order_dict)

    conn.close()
    return jsonify(results), 200

# Delete an order entirely
@app.route("/Orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    conn = sqlite3.connect("Nexus.db")
    cur = conn.cursor()

    # Check if order exists
    cur.execute("SELECT * FROM Orders WHERE Order_ID = ?", (order_id,))
    if cur.fetchone() is None:
        conn.close()
        return jsonify({"error": "Order not found"}), 404

    # Remove order items first
    cur.execute("DELETE FROM OrderItem WHERE Order_ID = ?", (order_id,))
    
    # Remove order
    cur.execute("DELETE FROM Orders WHERE Order_ID = ?", (order_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Order deleted successfully"}), 200



# Order history
@app.route("/History/<int:user_id>", methods=["GET"])
def get_history(user_id):
    return get_orders_by_user(user_id)

@app.route("/Signup", methods=["POST"])
def signup():
    data = request.get_json()

    name = data.get("Name")
    email = data.get("Email")
    password = data.get("Password")

    conn = sqlite3.connect("Nexus.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    hashed_ps = generate_password_hash(password)

    # check if email already exists
    cur.execute("SELECT * FROM User WHERE Email = ?", (email,))
    existing = cur.fetchone()

    if existing:
        conn.close()
        return jsonify({"error": "Email already registered"}), 400

    # insert new user
    cur.execute("""
        INSERT INTO User (Name, Email, Password, Role)
        VALUES (?, ?, ?, 'customer')
    """, (name, email, hashed_ps))

    conn.commit()

    # return user info
    new_id = cur.lastrowid

    conn.close()

    return jsonify({
        "User_ID": new_id,
        "Name": name,
        "Role": "customer"
    }), 200


@app.route("/admin/reset-db", methods=["POST"])
def reset_database():
    data = request.get_json() or {}

    key = data.get("key")
    if key != ADMIN_RESET_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    db_path = "Nexus.db"

    # delete the existing DB
    if os.path.exists(db_path):
        os.remove(db_path)

    # force recreation + seeding
    import importlib
    import Nexus_db
    import seed_data

    importlib.reload(Nexus_db)
    importlib.reload(seed_data)

    # table creation runs at import time
    seed_data.seed()

    return jsonify({"message": "Database has been RESET and RESEEDED."}), 200




# Run DB initialization ONLY on Render and only once if it's doesn't exist
if os.environ.get("RENDER") == "true":
    init_database()

if __name__ == "__main__":
    init_database()
    app.run(debug=True)



