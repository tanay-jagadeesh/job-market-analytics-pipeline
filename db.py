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


def get_connection():
    return psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, port=DB_PORT)

"""CONVERTED COMPANY NAME TO ID"""
def insert_company(company_name):
    conn = get_connection()

    c = conn.cursor()

    c.execute("SELECT company_id FROM companies WHERE company_name = %s", (company_name,))

    result = c.fetchone()

    if result:
        company_id = result[0]
        return company_id
    else:
        c.execute(
            "INSERT INTO companies (company_name) VALUES (%s) RETURNING company_id",
            (company_name,)
        )
        company_id = c.fetchone()[0]
        conn.commit()
        c.close()
        conn.close()
        return company_id

"""CONVERTED LOCATION (CITY, PROVINCE) TO ID"""
def insert_location(city, province):
    conn = get_connection()
    c = conn.cursor()

    # Check if location already exists (matching BOTH city AND province)
    c.execute("SELECT location_id FROM locations WHERE city = %s AND province = %s", (city, province))

    result = c.fetchone()

    if result:
        location_id = result[0]
        c.close()
        conn.close()
        return location_id
    else:
        c.execute(
            "INSERT INTO locations (city, province) VALUES (%s, %s) RETURNING location_id",
            (city, province)
        )
        location_id = c.fetchone()[0]
        conn.commit()
        c.close()
        conn.close()
        return location_id

"""CONVERTED SKILLS TO ID"""
def insert_skill(skill_name):
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT skill_id FROM skills WHERE skill_name = %s", (skill_name,))

    result = c.fetchone()

    if result:
        skill_id = result[0]
        c.close()
        conn.close()
        return skill_id
    else:
        c.execute(
            "INSERT INTO skills (skill_name) VALUES (%s) RETURNING skill_id",
            (skill_name,)
        )
        skill_id = c.fetchone()[0]
        conn.commit()
        c.close()
        conn.close()
        return skill_id