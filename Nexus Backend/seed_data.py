import sqlite3

DB_PATH = "Nexus.db"

IMAGE_PATH = "Images/"   # frontend relative folder

def seed():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()


    brands = ["Apple", "Samsung"]
    for b in brands:
        cur.execute("INSERT OR IGNORE INTO Brand (Name) VALUES (?)", (b,))

    #brand IDs
    cur.execute("SELECT Brand_ID, Name FROM Brand")
    brand_map = {name: bid for bid, name in cur.fetchall()}

    products = [
        # Apple
        (brand_map["Apple"], "iPhone 15 128GB", "128GB model of iPhone 15", 
         899,  IMAGE_PATH + "Iphone15_128gb.jpg",   25, 4.8, 312),

        (brand_map["Apple"], "iPhone 15 256GB", "256GB model of iPhone 15", 
         999,  IMAGE_PATH + "Iphone15_256gb.jpg",   20, 4.7, 184),

        (brand_map["Apple"], "iPhone 15 Pro 128GB", "Premium 128GB iPhone 15 Pro",
         1099, IMAGE_PATH + "Iphone15Pro_128gb.jpg", 18, 4.9, 420),

        (brand_map["Apple"], "iPhone 15 Pro 256GB", "256GB model with Pro features",
         1199, IMAGE_PATH + "Iphone15Pro_256gb.jpg", 15, 4.9, 260),

        (brand_map["Apple"], "iPhone 14 128GB", "Classic iPhone 14 with 128GB",
         749, IMAGE_PATH + "Iphone14_128gb.jpg", 30, 4.6, 350),

        (brand_map["Apple"], "iPhone 14 Plus 128GB", "Larger 14 Plus model",
         829, IMAGE_PATH + "Iphone14Plus_128gb.jpg", 22, 4.6, 210),

        # Samsung
        (brand_map["Samsung"], "Galaxy S24 128GB", "Latest S24 with 128GB",
         799, IMAGE_PATH + "GalaxyS24_128gb.jpg", 25, 4.7, 198),

        (brand_map["Samsung"], "Galaxy S24+ 256GB", "S24+ 256GB edition",
         999, IMAGE_PATH + "GalaxyS24Plus_256gb.jpg", 20, 4.8, 155),

        (brand_map["Samsung"], "Galaxy S24 Ultra 256GB", "Flagship S24 Ultra",
         1199, IMAGE_PATH + "GalaxyS24Ultra_256gb.jpg", 18, 4.9, 402),

        (brand_map["Samsung"], "Galaxy A55 128GB", "Budget Samsung A55",
         449, IMAGE_PATH + "GalaxyA55_128gb.jpg", 40, 4.5, 120),

        (brand_map["Samsung"], "Galaxy A35 128GB", "Affordable Samsung A35",
         379, IMAGE_PATH + "GalaxyA35_128gb.jpg", 35, 4.4, 88),

        (brand_map["Samsung"], "Galaxy Z Flip 5 256GB", "Flip 5 foldable",
         999, IMAGE_PATH + "GalaxyZFlip5_256gb.jpg", 15, 4.6, 167)
    ]
    for prod in products:
        cur.execute("""
            INSERT INTO Product
            (Brand_ID, Name, Description, Price, Image, Stock_count, Rating, Review_Count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, prod)


    fake_users = [
        ("John Doe", "john@example.com", "password123", "Customer"),
        ("Alice Smith", "alice@example.com", "alicepass", "Customer"),
        ("Admin User", "admin@example.com", "admin123", "Admin")
    ]

    for u in fake_users:
        cur.execute("""
            INSERT OR IGNORE INTO User (Name, Email, Password, Role)
            VALUES (?, ?, ?, ?)
        """, u)

    conn.commit()
    conn.close()
    print("Database seeding complete.")

if __name__ == "__main__":
    seed()
