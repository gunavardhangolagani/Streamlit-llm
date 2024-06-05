from langchain.utilities import SQLDatabase
import sqlite3
import os
db = SQLDatabase.from_uri('sqlite:///sql_lite_database.db')
# File path
database_file_path = './sql_lite_database.db'

# Check if database file exists and delete if it does
if os.path.exists(database_file_path):
    os.remove(database_file_path)
    message = "File 'sql_lite_database.db' found and deleted."
else:
    message = "File 'sql_lite_database.db' does not exist."

# Step 1: Connect to the database or create it if it doesn't exist
conn = sqlite3.connect(database_file_path)

cursor = conn.cursor()

# Create tables
create_table_querie1 = """

                      CREATE TABLE IF NOT EXISTS suppliers (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name CHAR(20),
                          address CHAR(20),
                          contact VARCHAR2(25)
    );
    """
create_table_querie2 = """
                          CREATE TABLE IF NOT EXISTS products (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name CHAR(20),
                          description CHAR(100),
                          price INTEGER,
                          supplier_id INTEGER ,
                          FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
                      );
    """
create_table_querie3 = """
                            CREATE TABLE  inventory (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            product_id INTEGER ,
                            quantity INTEGER ,
                            min_required INTEGER ,
                            FOREIGN KEY (product_id) REFERENCES products(id)
                        );
                        """
queries = [create_table_querie1, create_table_querie2, create_table_querie3]

for query in queries:
    cursor.execute(query)

insert_query = """
INSERT INTO suppliers (name, address, contact) VALUES ('Samsung Electronics', 'Seoul, South Korea', '800-726-7864');
INSERT INTO suppliers (name, address, contact) VALUES ('Apple Inc.', 'Cupertino, California, USA', '800–692–7753');
INSERT INTO suppliers (name, address, contact) VALUES ('OnePlus Technology', 'Shenzhen, Guangdong, China', '400-888-1111');
INSERT INTO suppliers (name, address, contact) VALUES ('Google LLC', 'Mountain View, California, USA', '855-836-3987');
INSERT INTO suppliers (name, address, contact) VALUES ('Xiaomi Corporation', 'Beijing, China', '1800-103-6286');


INSERT INTO products (name, description, price, supplier_id) VALUES ('Samsung Galaxy S21', 'Samsung flagship smartphone', 799.99, 1);
INSERT INTO products (name, description, price, supplier_id) VALUES ('Samsung Galaxy Note 20', 'Samsung premium smartphone with stylus', 999.99, 1);
INSERT INTO products (name, description, price, supplier_id) VALUES ('iPhone 13 Pro', 'Apple flagship smartphone', 999.99, 2);
INSERT INTO products (name, description, price, supplier_id) VALUES ('iPhone SE', 'Apple budget smartphone', 399.99, 2);
INSERT INTO products (name, description, price, supplier_id) VALUES ('OnePlus 9', 'High performance smartphone', 729.00, 3);
INSERT INTO products (name, description, price, supplier_id) VALUES ('OnePlus Nord', 'Mid-range smartphone', 499.00, 3);
INSERT INTO products (name, description, price, supplier_id) VALUES ('Google Pixel 6', 'Google''s latest smartphone', 599.00, 4);
INSERT INTO products (name, description, price, supplier_id) VALUES ('Google Pixel 5a', 'Affordable Google smartphone', 449.00, 4);
INSERT INTO products (name, description, price, supplier_id) VALUES ('Xiaomi Mi 11', 'Xiaomi high-end smartphone', 749.99, 5);
INSERT INTO products (name, description, price, supplier_id) VALUES ('Xiaomi Redmi Note 10', 'Xiaomi budget smartphone', 199.99, 5);


INSERT INTO inventory (product_id, quantity, min_required) VALUES (1, 150, 30);
INSERT INTO inventory (product_id, quantity, min_required) VALUES (2, 100, 20);
INSERT INTO inventory (product_id, quantity, min_required) VALUES (3, 120, 30);
INSERT INTO inventory (product_id, quantity, min_required) VALUES (4, 80, 15);
INSERT INTO inventory (product_id, quantity, min_required) VALUES (5, 200, 40);
INSERT INTO inventory (product_id, quantity, min_required) VALUES (6, 150, 25);
INSERT INTO inventory (product_id, quantity, min_required) VALUES (7, 100, 20);
INSERT INTO inventory (product_id, quantity, min_required) VALUES (8, 90, 18);
INSERT INTO inventory (product_id, quantity, min_required) VALUES (9, 170, 35);
INSERT INTO inventory (product_id, quantity, min_required) VALUES (10, 220, 45);
"""

for row in insert_query.splitlines():
    try:
        cursor.execute(row)
    except:
        print(f"An error occurred")
        print(row)

# Step 5: Fetch data from tables
list_of_queries = []
list_of_queries.append("SELECT * FROM products")
list_of_queries.append("SELECT * FROM suppliers")
list_of_queries.append("SELECT * FROM inventory")

for query in list_of_queries:
    cursor.execute(query)
    data = cursor.fetchall()

    print(f"--- Data from tables ({query}) ---")
    for row in data:
        print(row)

# Step 7: Close the cursor and connection
cursor.close()
conn.commit()
conn.close()