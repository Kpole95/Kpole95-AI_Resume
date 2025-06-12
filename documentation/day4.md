# Day 4: FastAPI Backend

## Tasks Completed
### 1. Initialize FastAPI Application
- Created `api/main.py` with a health check endpoint.
- Commands:
  ```bash
  pip install fastapi uvicorn
  uvicorn api.main:app --reload
  curl http://127.0.0.1:8000/health

2. Resume Upload Endpoint
Created api/routers/resumes.py to upload .docx resumes, extract text, and return parsed data.
Commands:
pip install python-multipart
uvicorn api.main:app --reload
curl -X POST -F "file=@data/resumes_raw/John Doe.docx" http://127.0.0.1:8000/resumes/upload

3. Job Listing Endpoint
Created api/routers/jobs.py to list jobs from MySQL with pagination.
Commands:
uvicorn api.main:app --reload
curl http://127.0.0.1:8000/jobs/?skip=0&limit=5

4. Resume-Job Matching Endpoint
Updated api/routers/matching.py to return top 5 job matches for a resume ID.
Commands:
uvicorn api.main:app --reload
curl http://127.0.0.1:8000/matches/0

