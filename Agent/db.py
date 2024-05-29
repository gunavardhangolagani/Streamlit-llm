import sqlite3

# Connect to the SQLite database (create it if it doesn't exist)
conn = sqlite3.connect('inventory_management.db')
cursor = conn.cursor()

# Create tables
create_table_queries = [
    """
    CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        contact TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        price REAL NOT NULL,
        supplier_id INTEGER NOT NULL,
        FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        min_required INTEGER NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(id)
    );
    """
]

# Execute the table creation queries
for query in create_table_queries:
    cursor.execute(query)

# Data to be inserted
suppliers_data = [
    ("Samsung Electronics", "Seoul, South Korea", "800-726-7864"),
    ("Apple Inc.", "Cupertino, California, USA", "800–692–7753"),
    ("OnePlus Technology", "Shenzhen, Guangdong, China", "400-888-1111"),
    ("Google LLC", "Mountain View, California, USA", "855-836-3987"),
    ("Xiaomi Corporation", "Beijing, China", "1800-103-6286"),
]

products_data = [
    ("Samsung Galaxy S21", "Samsung flagship smartphone", 799.99, 1),
    ("Samsung Galaxy Note 20", "Samsung premium smartphone with stylus", 999.99, 1),
    ("iPhone 13 Pro", "Apple flagship smartphone", 999.99, 2),
    ("iPhone SE", "Apple budget smartphone", 399.99, 2),
    ("OnePlus 9", "High performance smartphone", 729.00, 3),
    ("OnePlus Nord", "Mid-range smartphone", 499.00, 3),
    ("Google Pixel 6", "Google's latest smartphone", 599.00, 4),
    ("Google Pixel 5a", "Affordable Google smartphone", 449.00, 4),
    ("Xiaomi Mi 11", "Xiaomi high-end smartphone", 749.99, 5),
    ("Xiaomi Redmi Note 10", "Xiaomi budget smartphone", 199.99, 5),
]

inventory_data = [
    (1, 150, 30),
    (2, 100, 20),
    (3, 120, 30),
    (4, 80, 15),
    (5, 200, 40),
    (6, 150, 25),
    (7, 100, 20),
    (8, 90, 18),
    (9, 170, 35),
    (10, 220, 45)
]

# Insert data into tables
cursor.executemany("INSERT INTO suppliers (name, address, contact) VALUES (?, ?, ?);", suppliers_data)
cursor.executemany("INSERT INTO products (name, description, price, supplier_id) VALUES (?, ?, ?, ?);", products_data)
cursor.executemany("INSERT INTO inventory (product_id, quantity, min_required) VALUES (?, ?, ?);", inventory_data)

# Commit the changes and close the connection
conn.commit()
conn.close()
