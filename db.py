import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

try:
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, port=DB_PORT)
    print("SUCCESSFUL DATABASE CONNECTION")
except Exception as e:
    print(f"UNSUCCESSFUL DATABASE CONNECTION: {e}")