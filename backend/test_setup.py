import spacy
import sentence_transformers
import fastapi
import sqlalchemy
import streamlit
import langdetect
import PyPDF2
import docx
import requests
import mysql.connector

print("spaCy English:", spacy.load("en_core_web_sm").pipe_names)
print("spaCy Russian:", spacy.load("ru_core_news_sm").pipe_names)
print("Setup verified successfully!")