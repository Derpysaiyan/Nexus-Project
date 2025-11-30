import sqlite3
# Creates the Database Tables using SQLite commands

DB = sqlite3.connect('Nexus Backend/Nexus.db')

cur = DB.cursor()
#User
cur.execute("""
        CREATE TABLE IF NOT EXISTS User (
        User_ID INTEGER PRIMARY KEY,
        Name TEXT,
        Email TEXT UNIQUE,
        Password TEXT,
        Role TEXT
    );""")

#Brand
cur.execute(""" 
        CREATE TABLE IF NOT EXISTS Brand(
        Brand_ID INTEGER PRIMARY KEY,
        Name TEXT
        );""")

#Product
cur.execute(""" 
        CREATE TABLE IF NOT EXISTS Product(
        Product_ID INTEGER PRIMARY KEY,
        Brand_ID INTEGER,
        Name TEXT,
        Description TEXT,
        Price REAL,
        Image TEXT,
        Stock_count INTEGER,
        Rating REAL,
        Review_Count INTEGER,
        FOREIGN KEY(Brand_ID) REFERENCES Brand(Brand_ID)
        );""")

#CartItems
cur.execute(""" 
        CREATE TABLE IF NOT EXISTS CartItem(
        CartItem_ID INTEGER PRIMARY KEY,
        User_ID INTEGER,
        Product_ID INTEGER,
        Quantity INTEGER,
        Price REAL,
        Added_At TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(User_ID) REFERENCES User(User_ID),
        FOREIGN KEY(Product_ID) REFERENCES Product(Product_ID)
        );""")

# Orders
cur.execute(""" 
        CREATE TABLE IF NOT EXISTS Orders(
            Order_ID INTEGER PRIMARY KEY,
            User_ID INTEGER,
            Order_date TEXT DEFAULT CURRENT_TIMESTAMP,
            Total_price REAL,
            Status TEXT,
            FOREIGN KEY(User_ID) REFERENCES User(User_ID)
        );""")

#OrderItems
cur.execute(""" 
        CREATE TABLE IF NOT EXISTS OrderItem(
        OrderItem_ID INTEGER PRIMARY KEY,
        Order_ID INTEGER,
        Product_ID INTEGER,
        Quantity INTEGER,
        Price REAL,
        FOREIGN KEY(Order_ID) REFERENCES Orders(Order_ID),
        FOREIGN KEY(Product_ID) REFERENCES Product(Product_ID)
        );""")

DB.commit()
DB.close()