# Day 3: Job Fetching and Matching

## Tasks Completed
### 1. Job Fetching
- Implemented `backend/job_fetching/fetch_jobs.py` to fetch 100 jobs from hh.ru API.
- Saved jobs to `data/jobs.json`.
- Commands:
  ```bash
  python -m backend.job_fetching.fetch_jobs
  ls data/jobs.json

2. MySQL Storage for Jobs
Updated backend/job_fetching/fetch_jobs.py to save 100 jobs to MySQL jobs table.
Verified 100 rows in database.
Commands:
python -m backend.job_fetching.fetch_jobs
docker exec -it deployment-db-1 mysql -u user -ppassword -e "USE resume_matcher; SELECT COUNT(*) FROM jobs;"

3. Resume-Job Matching
Implemented backend/matching/match_algorithms.py for cosine similarity matching using sentence-transformers.
Generated 50 matches (5 resumes x 10 jobs) and saved to data/matches/matches.json.
Commands:
pip install sentence-transformers
python -m backend.matching.match_algorithms
ls data/matches/matches.json

4. MySQL Storage for Matches
Updated backend/matching/match_algorithms.py to save 50 matches to MySQL matches table.
Cleared duplicates and verified 50 rows.
Commands:
docker exec -it deployment-db-1 mysql -u user -ppassword -e "USE resume_matcher; TRUNCATE TABLE matches;"
python -m backend.matching.match_algorithms
docker exec -it deployment-db-1 mysql -u user -ppassword -e "USE resume_matcher; SELECT COUNT(*) FROM matches;"

5. Matching Accuracy Evaluation
Implemented backend/evaluate.py to evaluate 50 match scores for skills overlap.
Achieved 92% accuracy (46/50 correct).
Commands:
python -m backend.evaluate