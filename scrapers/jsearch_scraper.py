from dotenv import load_dotenv
import requests
import os
import pandas as pd

#loaded env
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

try:
    response.raise_for_status()
    data = response.json()
    print(data)
    print("SUCCESS")
except requests.HTTPError as h:
    print(f"Failed as {h}")
except ValueError as v:
    print(f"FAILED as {v}")

#Extracted skills from job desc.
skills_list = ['python', 'sql', 'aws', 'java', 'tableau', 'power bi', 'excel', 'r', 'spark', 'azure']

for job in data['data']:
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
