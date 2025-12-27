from dotenv import load_dotenv
import requests
import os
import pandas as pd

#loaded env
load_dotenv()

app_key = os.getenv('JSEARCH_API_KEY')

url = "https://jsearch.p.rapidapi.com/search"

headers = {
    "X-RapidAPI_Key": app_key,
    "X_RapidAPI_Host": "jsearch.p.rapidapi.com"
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
    print("SUCCESS")
except requests.HTTPError as h:
    print(f"Failed as {h}")
except ValueError as v:
    print(f"FAILED as {v}")

    