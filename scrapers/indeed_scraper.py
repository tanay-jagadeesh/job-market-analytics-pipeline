from dotenv import load_dotenv
import requests
import os

#loaded env
load_dotenv()


app_id = os.getenv('ADZUNA_APP_ID')
app_key = os.getenv('ADZUNA_API_KEY')

response = requests.get(url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={app_id}&app_key={app_key}")

try:
    response.raise_for_status()
    response.json()
    print("SUCCESS")
except ValueError:
    print("FAILED")
