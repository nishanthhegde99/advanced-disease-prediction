import sqlite3

conn = sqlite3.connect("disease.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS disease (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS symptom (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS disease_symptom (
    disease_id INTEGER,
    symptom_id INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS medicine (
    id INTEGER PRIMARY KEY,
    name TEXT,
    warning TEXT,
    requires_prescription INTEGER DEFAULT 0
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS disease_medicine (
    disease_id INTEGER,
    medicine_id INTEGER
)
""")
conn.commit()
conn.close()

print("Database created successfully")
print("Database created successfully")
