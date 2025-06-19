import re
import json
import requests
import time
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
from backend.job_fetching.init_tokens import refresh_token, validate_token

# the main project directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# file path where API tokens are stored
TOKEN_FILE = BASE_DIR / "config" / "tokens.json"
# A dictionary to help the AI understand abbreviations for skills
SKILL_SYNONYMS = { "machine learning": ["ml"], "data science": ["ds"], "python": ["py"] }


def compute_match_score(resume_text_embedding, job_embeddings, resume_skills, job_texts, user_experience_years: int, weights: dict):
    """
    This is the "brain" of the scoring process. It takes the numerical representations
    of the resume and jobs and calculates a final score based on a hybrid model.
    """
    # Safety check: if there are no job embeddings, return empty lists.
    if not hasattr(job_embeddings, 'any') or not job_embeddings.any(): return [], []

    # --- Step 1: Calculate the Raw Semantic Score ---
    # This line calculates the "cosine similarity" between the resume's vector and every job's vector.
    # The result is a raw score from 0 to 1 representing how similar their meanings are.
    semantic_scores = util.cos_sim(resume_text_embedding, job_embeddings).flatten().tolist()
    
    # Prepare empty lists to store the final calculated scores and matched skills for each job.
    final_scores, all_matched_skills = [], []

    # Loop through every job to calculate its unique final score.
    for i, job_text in enumerate(job_texts):
        
        # --- Step 2: Apply the Semantic Weight ---
        # Take the raw semantic score (e.g., 0.80) and multiply it by the weight we chose (e.g., 0.70).
        # This determines how much the "contextual meaning" contributes to the final score.
        base_score = semantic_scores[i] * weights['semantic']
        
        # --- Step 3: Calculate the Keyword Bonus ---
        keyword_bonus = 0.0
        matched_skills = []
        if resume_skills:
            job_text_lower = job_text.lower()
            # Loop through every skill found on the user's resume
            for skill in resume_skills:
                # Check if the skill (or its synonym) exists as a whole word in the job text
                if any(re.search(r'\b' + re.escape(syn) + r'\b', job_text_lower, re.I) for syn in SKILL_SYNONYMS.get(skill.lower(),[skill.lower()])):
                    # Add a small bonus for each skill that matches.
                    keyword_bonus += weights['keyword_multiplier']
                    matched_skills.append(skill.title())
        
        # --- Step 4: Calculate the Experience Penalty ---
        experience_penalty = 0.0
        # Use Regular Expressions to find phrases like "3-6 years", "more than 6 years", or "от 3 лет"
        exp_patterns = re.findall(r'(?:от|more than|from)\s*(\d+)|(\d+)-(\d+)\s*(?:лет|years)', job_text, re.I)
        if exp_patterns:
            for match in exp_patterns:
                # Extract the numbers from the found text
                required_years = [int(y) for y in match if y.isdigit()]
                # Find the minimum years required (e.g., for "3-6 years", the minimum is 3)
                min_required = min(required_years) if required_years else 0
                # If the job requires more experience than the user has, apply a penalty.
                if min_required > user_experience_years:
                    experience_penalty = weights['experience_penalty']
                    break  # Stop after finding the first requirement that doesn't match
    
        # --- Step 5: Calculate the Final Hybrid Score ---
        # The final score is: (Weighted Semantic Score + Keyword Bonus) - Experience Penalty
        final_score = (base_score + keyword_bonus) - experience_penalty
        
        # Ensure the final score stays between 0 and 1 (or 0% and 100%).
        final_scores.append(max(0, min(final_score, 1.0)))
        
        all_matched_skills.append(matched_skills)
        
    return final_scores, all_matched_skills


def _fetch_jobs_from_hh(access_token, params):
    """
    A helper function that handles the direct API call to hh.ru.
    """
    try:
        # Makes the API request to get the list of vacancies
        print(f"DEBUG: Making Simple Text Search request with params: {params}")
        response = requests.get("https://api.hh.ru/vacancies", params=params, headers={"Authorization": f"Bearer {access_token}"}, timeout=20)
        response.raise_for_status()  # Raise an error if the request was unsuccessful (e.g., 404, 500)
        return response.json().get("items", [])
    except requests.exceptions.RequestException as e:
        # If the network request fails, print an error and return an empty list.
        print(f"API request failed: {str(e)}"); return []


def match_resume_to_jobs(resume_data: dict, keyword: str) -> list:
    """
    This is the main orchestrator function. It manages the entire process from
    getting API tokens to returning a final, sorted list of matched jobs.
    """
    start_time = time.time()
    
    # --- Step 1: Get API Access Token ---
    # This section gets the access token needed to talk to the hh.ru API.

    # Make sure 'import os' is at the top of your file

# ... inside the match_resume_to_jobs function ...
    try:
    # Read the access token from the environment variable provided by Yandex Cloud
        access_token = os.getenv("HH_RU_ACCESS_TOKEN")
        if not access_token:
        # This error will show up in the Yandex Cloud logs if the secret isn't set
            raise ValueError("HH_RU_ACCESS_TOKEN secret not found in the environment.")

    # You can still add your token validation/refresh logic here if needed
    # if not validate_token(access_token): access_token = refresh_token()

    except Exception as e:
        print(f"Failed to get API token: {e}"); return []
        

    # --- Step 2: Fetch Raw Job Postings ---
    # Prepare the parameters for the API call (get 100 jobs matching the keyword).
    params = { "per_page": 100, "text": keyword, "order_by": "relevance" }
    fetched_jobs = _fetch_jobs_from_hh(access_token, params)
    # If no jobs are found, stop here and return an empty list.
    if not fetched_jobs: return []

    # --- Step 3: Set Up the AI Model and Scoring Rules ---
    # Load the pre-trained SentenceTransformer AI model.
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

    # This is the "universal" part. Get the user's experience from the parsed resume data.
    # If it's not found, default to 0.
    user_experience_years = resume_data.get("total_experience_years", 0)
    
    # This is the "Control Panel" for the AI. You can tune these values to change the scoring behavior.
    weights = {
        'semantic': 0.70,           # The weight for contextual meaning
        'keyword_multiplier': 0.05, # The bonus for each matching skill
        'experience_penalty': 0.15  # The penalty for not having enough experience
    }
    
    # --- Step 4: Prepare Texts and Convert to Embeddings ---
    # Create a clean string of text from the resume's skills and experience.
    resume_text = " ".join(resume_data.get('found_skills', [])) + " " + resume_data.get('experience', '')
    # Convert the resume text into its numerical "DNA" (embedding/vector).
    resume_embedding = model.encode(resume_text, show_progress_bar=False)
    
    # Prepare lists to hold the job texts for scoring and for display.
    job_texts_for_scoring = []
    job_full_descriptions = []
    for job in fetched_jobs:
        requirement = job.get("snippet", {}).get("requirement") or ""
        responsibility = job.get("snippet", {}).get("responsibility") or ""
        # Create a clean string of text for each job for the AI to analyze.
        job_texts_for_scoring.append(f"{job.get('name', '')} {requirement} {responsibility}")
        # Create a nicely formatted description for the user to see.
        job_full_descriptions.append(f"**Requirements:**\n{requirement}\n\n**Responsibilities:**\n{responsibility}")

    # Convert all the job texts into their numerical "DNA" (embeddings/vectors).
    job_embeddings = model.encode(job_texts_for_scoring, show_progress_bar=False)

    # --- Step 5: Calculate Scores ---
    # Call the main scoring function with all the prepared data.
    all_scores, all_matched_skills = compute_match_score(
        resume_embedding, job_embeddings, resume_data.get("found_skills"),
        job_texts_for_scoring, user_experience_years, weights
    )
    
    # --- Step 6: Format and Sort the Final Results ---
    # This section takes the calculated scores and formats them into a nice, clean list
    # of dictionaries that the API can send to the frontend.
    job_matches = []
    for i, job_item in enumerate(fetched_jobs):
        # ... (formatting logic for salary, company name, etc.)
        salary = job_item.get('salary'); salary_str = "Not specified"
        if salary:
            s_from, s_to, currency = salary.get('from'), salary.get('to'), salary.get('currency', '')
            if s_from and s_to: salary_str = f"{s_from} - {s_to} {currency}"
            elif s_from: salary_str = f"From {s_from} {currency}"
            elif s_to: salary_str = f"Up to {s_to} {currency}"
            
        job_matches.append({
            "job_title": job_item.get("name"), "company": job_item.get("employer", {}).get("name"),
            "url": job_item.get("alternate_url"), "score": all_scores[i],
            "matched_skills": all_matched_skills[i], "experience": job_item.get("experience", {}).get("name", "N/A"),
            "salary": salary_str, "location": job_item.get("area", {}).get("name", "N/A"),
            "description": job_full_descriptions[i]
        })

    # Sort the final list of jobs from the highest score to the lowest.
    sorted_matches = sorted(job_matches, key=lambda x: x['score'], reverse=True)
    
    print(f"Process completed in {time.time() - start_time:.2f} seconds.")
    return sorted_matches