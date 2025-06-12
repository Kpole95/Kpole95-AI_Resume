from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import shutil, uuid, os
from backend.parsers.parse_resumes import extract_resume_data
from backend.matching.match_algorithms import match_resume_to_jobs

router = APIRouter(prefix="/resumes", tags=["Resume Matching"])

@router.post("/search-and-score")
async def search_and_score_jobs(file: UploadFile = File(...), keyword: str = Form(...)):
    temp_dir = "temp_uploads"; os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
    try:
        with open(temp_file_path, "wb") as buffer: shutil.copyfileobj(file.file, buffer)
        parsed_resume_data = extract_resume_data(temp_file_path)
        job_matches = match_resume_to_jobs(resume_data=parsed_resume_data, keyword=keyword)
        return {"matches": job_matches}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected server error: {str(e)}")
    finally:
        if os.path.exists(temp_file_path): os.remove(temp_file_path)