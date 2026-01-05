import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os
import re

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

def get_connection():
    return psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    )

"""CONVERTED COMPANY NAME TO ID"""
def insert_company(company_name):
    conn = get_connection()

    c = conn.cursor()

    c.execute("SELECT company_id FROM companies WHERE company_name = %s", (company_name,))

    result = c.fetchone()

    if result:
        company_id = result[0]
        c.close()
        conn.close()
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

"""gets company/location ids, inserts jobs, returns job_id"""
def insert_job(job_title, company_name, city, province, salary_min, salary_max, posted_date=None, is_remote=None, experience_level=None, job_description=None):
    company_id = insert_company(company_name)

    location_id = insert_location(city, province)

    conn = get_connection()

    c = conn.cursor()

    c.execute(
    "INSERT INTO job_postings (job_title, company_id, location_id, salary_min, salary_max, posted_date, is_remote, experience_level, job_description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING job_id",
    (job_title, company_id, location_id, salary_min, salary_max, posted_date, is_remote, experience_level, job_description)
)
    job_id = c.fetchone()[0]
    conn.commit()
    c.close()
    conn.close()
    return job_id

"""links jobs to multiple skills in junction table"""
def insert_job_skills(job_id, skill_id):
    conn = get_connection()
    c = conn.cursor()
    
    c.execute(
        "INSERT INTO job_skills (job_id, skill_id) VALUES (%s, %s)",
        (job_id, skill_id)
    )
    
    conn.commit()
    c.close()
    conn.close()

df = pd.read_csv('jobs_info.csv').head(50)

skills_list = ['python', 'sql', 'aws', 'java', 'tableau', 'power bi', 'excel', 'r', 'spark', 'azure']

for i, row in df.iterrows():
    # Parse posted_date
    posted_date = None
    if pd.notna(row['job_posted_at']):
        try:
            posted_date = pd.to_datetime(row['job_posted_at']).date()
        except:
            posted_date = None

    # Insert job with all parameters, handling missing values
    job_id = insert_job(
        job_title=row['job_title'],
        company_name=row['employer_name'],
        city=row['job_city'] if pd.notna(row['job_city']) else 'Unknown',
        province=row['job_state'] if pd.notna(row['job_state']) else 'Unknown',
        salary_min=int(row['job_min_salary']) if pd.notna(row['job_min_salary']) else 0,
        salary_max=int(row['job_max_salary']) if pd.notna(row['job_max_salary']) else 0,
        posted_date=posted_date,
        is_remote=bool(row['job_is_remote']) if pd.notna(row['job_is_remote']) else False,
        experience_level=None,
        job_description=row['job_description'] if pd.notna(row['job_description']) else None
    )

    # Link skills to job
    if pd.notna(row['job_description']):
        desc_lower = row['job_description'].lower()
        for skill in skills_list:
            # Use word boundaries to match whole words only (prevents 'r' from matching 'programmer')
            if re.search(rf'\b{re.escape(skill)}\b', desc_lower):
                skill_id = insert_skill(skill)
                insert_job_skills(job_id, skill_id)

    print(f"Inserted job {i+1}: {row['job_title']}")

print(f"\nSuccessfully loaded {len(df)} jobs into the database")

#Check for duplicates (if job_url exists then skip)

def check_if_job_exists(job_url):
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT job_id FROM job_postings WHERE job_url = %s", (job_url,))
    result = c.fetchone()

    c.close()
    conn.close()

    if result:
        return True
    else:
        return False
       