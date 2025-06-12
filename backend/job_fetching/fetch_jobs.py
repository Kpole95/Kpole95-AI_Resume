import requests
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from backend.database.db_session import get_db
from backend.database.db_models import Job

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TOKEN_FILE = BASE_DIR / "config" / "tokens.json"
OUTPUT_FILE = BASE_DIR / "data" / "jobs.json"

def fetch_jobs():
    with open(TOKEN_FILE, 'r') as f:
        tokens = json.load(f)
    access_token = tokens["access_token"]
    
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://api.hh.ru/vacancies"
    params = {
        "per_page": 100,
        "area": 1,
        "text": "developer",
    }
    
    jobs = []
    db = next(get_db())
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        for item in data.get("items", []):
            job_data = {
                "id": item["id"],
                "title": item["name"],
                "description": item.get("description", ""),
                "requirements": item.get("snippet", {}).get("requirement", ""),
                "language": "ru" if "ru" in item.get("name", "").lower() else "en"
            }
            jobs.append(job_data)
            
            # Save t MySQL
            job = Job(
                id=int(item["id"]),
                title=item["name"],
                url=item.get("alternate_url", ""),
                description=item.get("description", ""),
                requirements={"snippet": item.get("snippet", {}).get("requirement", "")},
                language="ru" if "ru" in item.get("name", "").lower() else "en"
            )
            db.add(job)
        db.commit()
    else:
        print(f"Error: {response.status_code} - {response.text}")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=4, ensure_ascii=False)
    
    return len(jobs)

if __name__ == "__main__":
    job_count = fetch_jobs()
    print(f"Fetched {job_count} jobs")