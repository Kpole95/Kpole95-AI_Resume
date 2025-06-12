import json
import os

def evaluate_matches(match_file, resume_dir, job_file):
    with open(match_file, 'r', encoding='utf-8') as f:
        matches = json.load(f)
    
    with open(job_file, 'r', encoding='utf-8') as f:
        jobs = {str(job["id"]): job for job in json.load(f)}
    
    correct_matches = 0
    total_matches = len(matches)
    
    for match in matches:
        resume_file = match["resume"]
        job_id = str(match["job_id"])
        score = match["score"]
        
        with open(os.path.join(resume_dir, resume_file), 'r', encoding='utf-8') as f:
            resume_data = json.load(f)
        
        resume_skills = set(resume_data["skills"])
        job_requirements = jobs[job_id]["requirements"].lower()
        expected_skills = [skill for skill in resume_data["skills"] if skill.lower() in job_requirements]
        
        if expected_skills and score > 0.5:  # high score evaluate
            correct_matches += 1
        elif not expected_skills and score <= 0.5:  # low score for no overlap
            correct_matches += 1
    
    accuracy = (correct_matches / total_matches) * 100 if total_matches > 0 else 0
    print(f"Accuracy: {accuracy:.2f}% ({correct_matches}/{total_matches} correct)")
    return accuracy

if __name__ == "__main__":
    match_file = "data/matches/matches.json"
    resume_dir = "data/resumes_parsed"
    job_file = "data/jobs.json"
    evaluate_matches(match_file, resume_dir, job_file)