# Day 2: Bilingual Resume Parsing

## Tasks Completed
### 1. Resume File Placement
- Placed 15 .docx resumes (10 English, 5 Russian) in `data/resumes_raw/`.
- Commands:
  ```bash
  mkdir -p data/resumes_raw
  ls data/resumes_raw/

  2. Text Extraction
Implemented backend/parsers/extract_files.py to extract text from .docx resumes, supporting .pdf and .txt for future use.
Saved extracted text as .txt in data/resumes_parsed/.
Commands:
pip install python-docx PyPDF2
python backend/parsers/extract_files.py
ls data/resumes_parsed/

3. Resume Parsing
Implemented backend/parsers/parse_resumes.py to parse 15 resumes for name, skills, experience, education, and language.
Saved structured data as JSON in data/resumes_parsed/.
Commands:
pip install spacy langdetect
python -m backend.parsers.parse_resumes
ls data/resumes_parsed/ | grep .json

4. MySQL Storage
Updated backend/parsers/parse_resumes.py to save parsed data to MySQL resumes table.
Verified 15 rows in database.
Commands:
python -m backend.parsers.parse_resumes
docker exec -it deployment-db-1 mysql -u user -ppassword -e "USE resume_matcher; SELECT COUNT(*) FROM resumes;"

5. Parsing Accuracy Test
Implemented test_resume_parsing.py to verify parsed JSON files contain required fields.
Commands:
python test_resume_parsing.py