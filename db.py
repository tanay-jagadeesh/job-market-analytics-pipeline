import psycopg2
import pandas as pd

DB_NAME = "job_market_db"
DB_USER = "User123"
DB_PASS = "Helloworld123"
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    conn = psycopg2.connect(database = DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST, port = DB_PORT)
    print("SUCCESSFUL DATABASE CONNECTION")
except Exception as e:
    print(f"UNSUCCESSFUL DATABASE CONNECTION: {e}")