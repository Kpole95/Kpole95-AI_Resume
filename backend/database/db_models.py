from sqlalchemy import Column, Integer, String, JSON, Enum, Float
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class Language(enum.Enum):
    en = "en"
    ru = "ru"

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    raw_text = Column(String)
    parsed_data = Column(JSON)
    language = Column(Enum(Language))

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    url = Column(String(255))
    description = Column(String)
    requirements = Column(JSON)
    language = Column(Enum(Language))

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer)
    job_id = Column(Integer)
    score = Column(Float)