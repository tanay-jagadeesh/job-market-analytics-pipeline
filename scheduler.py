import schedule
import time
from datetime import datetime
from src.analytics import run_all_queries
import requests
from dotenv import load_dotenv
import os
from src.db import insert_job, insert_skill, insert_job_skills, check_if_job_exists
import pandas as pd
import re
import logging
from logging.handlers import TimedRotatingFileHandler

# Set up log rotation (keeps last 30 days)
handler = TimedRotatingFileHandler(
    filename='logs/scheduler.log',
    when='midnight',      
    interval=1,          
    backupCount=30      
)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


# ETL (Extract, Transform, Load)
def fetch_jobs():
    try:
        load_dotenv()

        app_key = os.getenv('JSEARCH_API_KEY')

        url = "https://jsearch.p.rapidapi.com/search"

        headers = {
            "X-RapidAPI-Key": app_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }

        queries = [
            "data analyst Montreal",
            "business analyst Vancouver",
            "data engineer Toronto", 
            "remote data scientist Alberta",
            "junior data analyst British Columbia"
        ]

        all_jobs = []
        for query in queries:
            params = {
                "query": query,
                "num_pages": 1,
                "country": "ca",
            }

            response = requests.get(url = url, headers = headers, params = params)
            response.raise_for_status()
            data = response.json()

            for job in data['data']:
                all_jobs.append(job)

        # Log API call
            logging.info(f"API Call - Query: {params['query']}, Results: {len(data['data'])}")

        return all_jobs
    except Exception as e:
        logging.error(f"Error fetching jobs: {str(e)}")
        raise

def process_jobs(jobs):
    skills_list = ['python', 'r', 'java', 'scala', 'julia', 'c++', 'javascript', 'typescript', 'sql', 'mysql', 'postgresql', 'postgres', 'mongodb', 'redis', 'cassandra', 'oracle', 'snowflake', 'bigquery', 'aws', 'azure', 'gcp', 'google cloud', 'spark', 'hadoop', 'kafka', 'flink', 'hive', 'presto', 'tableau', 'power bi', 'looker', 'qlik', 'metabase', 'superset', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'keras', 'xgboost', 'excel', 'git', 'docker', 'kubernetes', 'k8s', 'airflow', 'dbt', 'databricks', 'etl', 'data pipeline', 'data warehouse', 'data lake', 'statistics', 'machine learning', 'deep learning', 'nlp', 'computer vision', 'sas', 'spss', 'matlab']

    for job in jobs:
        job_description = job.get('job_description')
        job_title = job.get("job_title")
        
        if job_description: 
            desc_lower = job_description.lower()
            
            for skill in skills_list:
                if skill.lower() in desc_lower:
                    print(f"NEEDS {skill}")
        
        if job_title:
            title_lower = job_title.lower()
        
            if "junior" in title_lower or "entry" in title_lower:
                print("Entry Level")
            elif "senior" in title_lower or "lead" in title_lower:
                print("Senior Level")
            else:
                print("Mid Level")

        if (job_title and "remote" in job_title.lower()) or (job_description and "remote" in job_description.lower()):
            print("This is a remote job")

def load_to_database(jobs):
    skills_list = ['python', 'r', 'java', 'scala', 'julia', 'c++', 'javascript', 'typescript', 'sql', 'mysql', 'postgresql', 'postgres', 'mongodb', 'redis', 'cassandra', 'oracle', 'snowflake', 'bigquery', 'aws', 'azure', 'gcp', 'google cloud', 'spark', 'hadoop', 'kafka', 'flink', 'hive', 'presto', 'tableau', 'power bi', 'looker', 'qlik', 'metabase', 'superset', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'keras', 'xgboost', 'excel', 'git', 'docker', 'kubernetes', 'k8s', 'airflow', 'dbt', 'databricks', 'etl', 'data pipeline', 'data warehouse', 'data lake', 'statistics', 'machine learning', 'deep learning', 'nlp', 'computer vision', 'sas', 'spss', 'matlab']

    skill_mapping = {
        'postgres': 'postgresql',
        'k8s': 'kubernetes',
        'sklearn': 'scikit-learn',
        'gcp': 'google cloud',
    }

    added_count = 0
    duplicate_count = 0

    try:
        for job in jobs:
            job_url = job.get('job_apply_link')

            if job_url and check_if_job_exists(job_url):
                duplicate_count += 1
                continue

            job_title = job.get('job_title')
            company_name = job.get('employer_name')
            city = job.get('job_city')
            province = job.get('job_state')
            salary_min = int(job.get('job_min_salary', 0))
            salary_max = int(job.get('job_max_salary', 0))

            job_id = insert_job(
                job_title=job_title,
                company_name=company_name,
                city=city,
                province=province,
                salary_min=salary_min,
                salary_max=salary_max,
                job_url=job_url,
            )

            job_description = job.get('job_description')
            if job_description:
                desc_lower = job_description.lower()
                found_skills = set()

                for skill in skills_list:
                    if re.search(rf'\b{re.escape(skill)}\b', desc_lower):
                        canonical_skill = skill_mapping.get(skill, skill)
                        found_skills.add(canonical_skill)

                for canonical_skill in found_skills:
                    skill_id = insert_skill(canonical_skill)
                    insert_job_skills(job_id, skill_id)

            added_count += 1

        # Log results
        logging.info(f"Database Load - Jobs added: {added_count}, Duplicates skipped: {duplicate_count}")

    except Exception as e:
        logging.error(f"Error loading to database: {str(e)}")
        raise

def job():
    jobs = fetch_jobs()
    process_jobs(jobs)
    load_to_database(jobs)
    run_all_queries()

#ensures that it runs at 6 am everyday
schedule.every().day.at("06:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
