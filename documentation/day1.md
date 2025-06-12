# Day 1: Project Setup and MySQL Configuration

## Tasks Completed
### 1. WSL Environment
- Installed tools: `curl`, `git`, `python3-pip`, `python3-venv`, `net-tools`, `tree`.
- Commands:
  ```bash
  sudo apt update && sudo apt upgrade -y
  sudo apt install -y curl git python3-pip python3-venv net-tools tree
  python3 --version


2. Project Structure
Created directories and files for backend, api, frontend, config, data, documentation, thesis, uploads, utils, deployment.
Initialized virtual environment and Git in ~/all/AI-Resume-MVP.
Renamed project folder from AI-Resume to AI-Resume-MVP.
Commands:
cd ~/all/AI-Resume-MVP
python3 -m venv venv
source venv/bin/activate
mkdir -p backend/parsers backend/job_fetching backend/matching backend/database
git init


3. Docker Setup
Integrated Docker Desktop with WSL.
Commands:
docker --version
docker run hello-world

4. MySQL Setup
Configured MySQL 8.0 on port 3307 with resume_matcher database.
Defined tables: resumes, jobs, matches.
Commands:
cd deployment
docker-compose up -d
pip install sqlalchemy mysql-connector-python
python backend/database/test_db.py
docker exec -it deployment-db-1 mysql -u user -ppassword -e "USE resume_matcher; SHOW TABLES;"

5. Dependencies
Installed Python packages and spaCy models.
Commands:
pip install -r requirements.txt
python -m spacy download en_core_web_sm
pip install https://github.com/explosion/spacy-models/releases/download/ru_core_news_sm-3.7.1/ru_core_news_sm-3.7.1-py3-none-any.whl
python backend/test_setup.py

6. hh.ru API
Configured credentials in config/.env using provided CLIENT_ID, CLIENT_SECRET, APP_TOKEN, REDIRECT_URI.
Generated OAuth tokens, saved to config/tokens.json.
Commands:
nano config/.env
nano backend/job_fetching/init_tokens.py
python backend/job_fetching/init_tokens.py

