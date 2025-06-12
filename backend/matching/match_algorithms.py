import re
import json
import requests
import time
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
from backend.job_fetching.init_tokens import refresh_token, validate_token

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TOKEN_FILE = BASE_DIR / "config" / "tokens.json"
SKILL_SYNONYMS = { "machine learning": ["ml"], "data science": ["ds"], "python": ["py"] }

def compute_match_score(resume_text_embedding, job_embeddings, resume_skills, job_texts):
    if not hasattr(job_embeddings, 'any') or not job_embeddings.any(): return [], []
    semantic_scores = util.cos_sim(resume_text_embedding, job_embeddings).flatten().tolist()
    final_scores, all_matched_skills = [], []
    for i, job_text in enumerate(job_texts):
        base_score = semantic_scores[i] * 0.60
        keyword_bonus = 0.0
        matched_skills = []
        if resume_skills:
            job_text_lower = job_text.lower()
            for skill in resume_skills:
                if any(re.search(r'\b' + re.escape(syn) + r'\b', job_text_lower, re.I) for syn in SKILL_SYNONYMS.get(skill.lower(),[skill.lower()])):
                    keyword_bonus += 0.04
                    matched_skills.append(skill.title())
        final_scores.append(min(base_score + keyword_bonus, 1.0))
        all_matched_skills.append(matched_skills)
    return final_scores, all_matched_skills

def _fetch_jobs_from_hh(access_token, params):
    try:
        print(f"DEBUG: Making Simple Text Search request with params: {params}")
        response = requests.get("https://api.hh.ru/vacancies", params=params, headers={"Authorization": f"Bearer {access_token}"}, timeout=20)
        response.raise_for_status()
        return response.json().get("items", [])
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {str(e)}"); return []

def match_resume_to_jobs(resume_data: dict, keyword: str) -> list:
    start_time = time.time()
    try:
        with open(TOKEN_FILE, 'r') as f: tokens = json.load(f)
        access_token = tokens.get("access_token")
        if not access_token or not validate_token(access_token): access_token = refresh_token()
    except Exception as e:
        print(f"Failed to get API token: {e}"); return []
        
    params = { "per_page": 100, "text": keyword, "order_by": "relevance" }
    fetched_jobs = _fetch_jobs_from_hh(access_token, params)
    if not fetched_jobs: return []

    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    resume_text = " ".join(resume_data.get('found_skills', [])) + " " + resume_data.get('experience', '')
    resume_embedding = model.encode(resume_text, show_progress_bar=False)
    
    # create two lists: one for scoring, and the other one with the full description for display
    job_texts_for_scoring = []
    job_full_descriptions = []
    for job in fetched_jobs:
        requirement = job.get("snippet", {}).get("requirement") or ""
        responsibility = job.get("snippet", {}).get("responsibility") or ""
        job_texts_for_scoring.append(f"{job.get('name', '')} {requirement}")
        job_full_descriptions.append(f"**Requirements:**\n{requirement}\n\n**Responsibilities:**\n{responsibility}")

    job_embeddings = model.encode(job_texts_for_scoring, show_progress_bar=False)
    all_scores, all_matched_skills = compute_match_score(resume_embedding, job_embeddings, resume_data.get("found_skills"), job_texts_for_scoring)
    
    job_matches = []
    for i, job_item in enumerate(fetched_jobs):
        salary = job_item.get('salary'); salary_str = "Not specified"
        if salary:
            s_from, s_to, currency = salary.get('from'), salary.get('to'), salary.get('currency', '')
            if s_from and s_to: salary_str = f"{s_from} - {s_to} {currency}"
            elif s_from: salary_str = f"From {s_from} {currency}"
            elif s_to: salary_str = f"Up to {s_to} {currency}"
            
        job_matches.append({
            "job_title": job_item.get("name"),
            "company": job_item.get("employer", {}).get("name"),
            "url": job_item.get("alternate_url"),
            "score": all_scores[i],
            "matched_skills": all_matched_skills[i],
            "experience": job_item.get("experience", {}).get("name", "N/A"),
            "salary": salary_str,
            # New data added
            "location": job_item.get("area", {}).get("name", "N/A"),
            "description": job_full_descriptions[i]
        })

    sorted_matches = sorted(job_matches, key=lambda x: x['score'], reverse=True)
    print(f"Process completed in {time.time() - start_time:.2f} seconds.")
    return sorted_matches