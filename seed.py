import os
import sqlite3

DB_PATH = "data/receipts.db"

# create folder if it doesn't exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create tables
cur.execute("""
CREATE TABLE IF NOT EXISTS receipts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        store TEXT,
        date TEXT,
        total REAL,
        raw_text TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS receipt_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        receipt_id INTEGER,
        item TEXT,
        price REAL,
        FOREIGN KEY(receipt_id) REFERENCES receipts(id)
)
""")

receipts = [
    ("Warteg Simpang", "2025/10/17", 55000, ""),
    ("Bakso Solo Joko", "2025/10/17", 40000, ""),
    ("Kopi Kina", "2025/10/17", 65000, ""),
    ("Warkop Mawar", "2025/10/07", 80000, "")
]

for store, date, total, text in receipts:
    cur.execute("INSERT INTO receipts (store, date, total, raw_text) VALUES (?, ?, ?, ?)",
                (store, date, total, text))

receipt_items = [
    (1, "Nasi Goreng Teri", 40000),
    (1, "Es Teh Manis", 15000),
    (2, "Bakso Urat", 30000),
    (2, "Teh Hangat", 10000),
    (3, "Amerikano", 35000),
    (3, "Roti Bakar Keju", 30000),
    (4, "Sate Ayam", 60000),
    (4, "Indomie", 20000),
]

for rid, item, price in receipt_items:
    cur.execute("INSERT INTO receipt_items (receipt_id, item, price) VALUES (?, ?, ?)",
                (rid, item, price))

conn.commit()
conn.close()

print("Success insert dummy data")