import os
import sqlite3

DATABASES_DIR = "./databases"
CSV_DIR = "./csv"
DB_NAMES = os.listdir(f"./{DATABASES_DIR}")
# DB_NAME = os.listdir(f"./{DATABASES_DIR}")[0]
DB_NAME = 'database.db'
CONN = sqlite3.connect(f"{DATABASES_DIR}/{DB_NAME}")
CONNECTION = CONN.cursor()

CONNECTION.execute(f"select tester_id from experiment")

TESTER_ID = [data for data in CONNECTION.fetchall()][-1][0]
