from dotenv import load_dotenv
import requests
import os
import pandas as pd

#loaded env
load_dotenv()

app_key = os.getenv('JSEARCH_API_KEY')

response = requests.get(url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={app_id}&app_key={app_key}")

try:
    response.raise_for_status()
    data = response.json()
    print("SUCCESS")
except requests.HTTPError as h:
    print(f"Failed as {h}")
except ValueError as v:
    print(f"FAILED as {v}")

for job in response:
    