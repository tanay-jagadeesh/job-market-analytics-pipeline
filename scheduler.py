import schedule
import time
from datetime import datetime
from analytics import run_all_queries
import requests
from dotenv import load_dotenv
import os

# ETL (Extract, Transform, Load)
def fetch_jobs():
    
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
    return data['data']

def process_jobs(jobs):


def job():
    run_all_queries()

#ensures that it runs at 6 am everyday
schedule.every().day.at("6:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)