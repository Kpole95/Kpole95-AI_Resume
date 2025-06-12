# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from backend.database.db_session import get_db
# from backend.database.db_models import Job
# from typing import List
# from pydantic import BaseModel

# router = APIRouter(prefix="/jobs", tags=["jobs"])

# class JobResponse(BaseModel):
#     id: int
#     title: str
#     url: str
#     description: str
#     requirements: dict
#     language: str

#     class Config:
#         from_attributes = True

# @router.get("/", response_model=List[JobResponse])
# def list_jobs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     jobs = db.query(Job).offset(skip).limit(limit).all()
#     return jobs