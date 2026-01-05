import schedule
import time
from datetime import datetime
from analytics import run_all_queries
import requests
from dotenv import load_dotenv
import os
from db import insert_job, insert_skill, insert_job_skills, check_if_job_exists
import pandas as pd
import re
import logging

# At the top after imports
logging.basicConfig(
    filename='logs/scheduler.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


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

        params = {
            "query": "data analyst",
            "num_pages": 1,
            "country": "ca"
        }

        response = requests.get(url = url, headers = headers, params = params)
        response.raise_for_status()
        data = response.json()

        # Log API call
        logging.info(f"API Call - Query: {params['query']}, Results: {len(data['data'])}")

        return data['data']
    except Exception as e:
        logging.error(f"Error fetching jobs: {str(e)}")
        raise

def process_jobs(jobs):
    skills_list = ['python', 'sql', 'aws', 'java', 'tableau', 'power bi', 'excel', 'r', 'spark', 'azure']

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
    skills_list = ['python', 'sql', 'aws', 'java', 'tableau', 'power bi', 'excel', 'r', 'spark', 'azure']

    added_count = 0
    duplicate_count = 0

    try:
        for job in jobs:
            job_url = job.get('job_apply_link')

            # Check for duplicates
            if job_url and check_if_job_exists(job_url):
                duplicate_count += 1
                continue  # Skip this job

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

            # Link skills to job
            job_description = job.get('job_description')
            if job_description:
                desc_lower = job_description.lower()
                for skill in skills_list:
                    # Use word boundaries to match whole words only
                    if re.search(rf'\b{re.escape(skill)}\b', desc_lower):
                        skill_id = insert_skill(skill)
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
schedule.every().day.at("6:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)