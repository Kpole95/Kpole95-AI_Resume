# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from backend.database.db_session import get_db
# from backend.database.db_models import Match
# from typing import List
# from pydantic import BaseModel

# router = APIRouter(prefix="/matches", tags=["matches"])

# class MatchResponse(BaseModel):
#     id: int
#     resume_id: int
#     job_id: int
#     score: float

#     class Config:
#         from_attributes = True

# @router.get("/{resume_id}", response_model=List[MatchResponse])
# def get_matches(resume_id: int, db: Session = Depends(get_db)):
#     matches = db.query(Match).filter(Match.resume_id == resume_id).order_by(Match.score.desc()).limit(5).all()
#     if not matches:
#         raise HTTPException(status_code=404, detail="No matches found for this resume")
#     return matches