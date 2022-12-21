import os
import sqlite3

DATABASES_DIR = "./databases"
CSV_DIR = "./csv"
DB_NAMES = os.listdir(f"{DATABASES_DIR}")

for db in DB_NAMES:
    if not db.endswith(".db"):
        os.remove(f"./{DATABASES_DIR}/{db}")

DB_NAMES = os.listdir(f"{DATABASES_DIR}")

# DB_NAME = os.listdir(f"./{DATABASES_DIR}")[0]
DB_NAME = 'database.db'
CONN = sqlite3.connect(f"{DATABASES_DIR}/{DB_NAME}")
CONNECTION = CONN.cursor()

CONNECTION.execute(f"select tester_id from experiment")

TESTERS_ID = []

for data in CONNECTION.fetchall():
    TESTERS_ID.append(data[0])

SENIORS = [217, 218, 219, 220, 221, 222, 224, 225]
