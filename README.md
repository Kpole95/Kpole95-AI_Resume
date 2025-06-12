AI Resume Job Matcher: Project Documentation

Course: Advanced Python, M.Sc. in Artificial Intelligence, MIPT
1. The Project's Goal & Philosophy
As a student pursuing an M.Sc. in Artificial Intelligence at MIPT, I wanted my project for the advanced Python course to tackle a real-world problem that required a sophisticated, machine learning-centric solution. I chose the challenge of job searching.

The core problem is that resumes and job descriptions are written in natural language, full of context and nuance. A simple script checking for the keyword "Python" might incorrectly match a data scientist with a junior web developer role. The goal of this application was to overcome that by building a system that understands the meaning and context of a person's entire professional profile.

The result is an intelligent, full-stack web application that uses a hybrid AI model to parse any resume and find the most relevant job opportunities from thousands of real-world listings on the hh.ru job portal.

2. The User's Journey: From Resume to Job Match
The application is designed to be simple and intuitive. Here is a step-by-step look at what happens when a user interacts with the system:

The Search Begins: The user opens the web app and is greeted by a clean interface. They perform two simple actions: upload their .docx resume and type in the job title they're looking for (e.g., "Machine Learning Engineer").

The Frontend Calls for Help: When the user clicks "Find Job Matches," the Streamlit frontend packages up the resume file and the search term and sends a secure request to the backend API.

The Backend Takes Over: The FastAPI backend acts as the application's central nervous system. It receives the request and immediately begins the two-stage process.

The Parser Understands the Resume: First, the request goes to the Universal Parser. This module's job is to read the unstructured text of the resume and convert it into clean, structured data, identifying key sections like "Work Experience," "Education," and, most importantly, "Skills".

The AI Engine Finds and Ranks Jobs: The structured resume data is then passed to the AI Matching Engine. This is where the core "magic" happens:

Fetching: The engine makes a live call to the hh.ru API, requesting a list of up to 100 jobs that match the user's search term.

Scoring: For every single job returned, the AI performs a deep analysis, calculating a "Match Score" based on how well it aligns with the user's resume.

Ranking: Once all jobs are scored, they are sorted from the highest match to the lowest.

The Results Are In: The final, ranked list of jobs is sent back to the frontend, which then displays the results dashboard, showing the user the most relevant opportunities for their unique profile.

3. How the AI "Thinks": A Deep Dive
This application's intelligence comes from a custom Hybrid Ranking Model. Instead of relying on a single technique, it combines two different AI approaches to get a more accurate and nuanced result.

The Semantic Model: Understanding the Meaning
This is the core of the AI. It uses a state-of-the-art, multilingual sentence-transformer model. This deep learning model doesn't just look at words; it understands the context and meaning of entire sentences.

It reads the user's full resume profile and converts it into a complex numerical "fingerprint" (called an embedding).

It does the same thing for every job description.

By calculating the mathematical closeness of these fingerprints, the AI can understand that a resume talking about "building financial forecasts" is a great match for a job asking for "financial modeling," even if the exact keywords aren't the same.

The Keyword Model: Checking the Details
To ground the AI's understanding in reality, the system also rewards jobs for matching the specific, important keywords from the user's resume.

After the semantic score is calculated, the system performs a second pass.

It checks the job description for each of the specific skills listed in the resume (e.g., "PyTorch", "Scrum", "SQL").

For every skill it finds, it adds a bonus to the job's total match score.

The final score is a smart blend of the AI's contextual understanding and the concrete keyword matches, creating a result that is both context-aware and accurate.