from fastapi import FastAPI
from api.routers import resumes, jobs, matching

app = FastAPI(title="Resume Job Matcher API")

app.include_router(resumes.router)
app.include_router(jobs.router)
app.include_router(matching.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}