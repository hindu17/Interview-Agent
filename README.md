Interview Agent — AI-Powered Interview & Evaluation Tool

Overview

The Interview Agent is an AI-powered web application that automates the interview process for any role. It generates interview questions based on a job description, collects candidate answers, and provides AI-driven evaluation reports with scores, feedback, and insights.

This tool is designed for HR teams, recruiters, and hiring managers to save time, standardize interviews, and leverage AI for objective candidate evaluation.

Features

Job Description Parsing: Upload PDF, DOCX, TXT, or paste JD text.

Role & Level Customization: Tailor interview questions based on candidate role and experience level.

AI Question Generation: Automatically generates a mix of technical and behavioral interview questions using Google Gemini API.

Answer Input & Evaluation: Candidates can submit answers, and the AI evaluates them for quality, relevance, and completeness.

Score Aggregation: Provides overall score and detailed feedback for each question.


Persona Customization: Set the interviewer persona (e.g., strict HR, friendly tech lead).

Tech Stack

AI Model: Google Gemini 2.5 (Generative AI)

Framework: Python, Streamlit

Libraries: pandas, pdfminer.six, python-docx, dotenv

Hosting (optional): Streamlit Cloud or other hosting services

Environment Variables: .env for API keys (GEMINI_API_KEY)

Getting Started
Prerequisites

Python 3.10+

Git

Google Gemini API Key

Installation

Clone the repository:

git clone <https://github.com/hindu17/Interview-Agent>
cd interview-agent


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


Install dependencies:

pip install -r requirements.txt


Create a .env file with your Gemini API key:

GEMINI_API_KEY=your_google_gemini_api_key_here

Running Locally
streamlit run app.py


Open your browser at http://localhost:8501.

Upload a job description or paste it directly.

Set the role, level, and number of questions.

Generate questions, provide answers, and get an AI evaluation report.

Deploying Online

Push your code to GitHub.

Go to Streamlit Cloud
 and connect your GitHub repo.

Configure Secrets in Streamlit Cloud:

GEMINI_API_KEY=your_google_gemini_api_key_here


Select branch and app.py file, then click Deploy.

Share the generated public URL for your demo.

Project Architecture
app.py                  # Main Streamlit app
question_generator.py   # Generates interview questions via Gemini AI
evaluator.py            # Evaluates candidate answers using AI
utils.py                # JD parsing & CSV report utilities
.env                    # Environment variables (API keys)


Workflow:

Candidate uploads JD → Streamlit app parses it.

User selects role & level → AI generates interview questions.

Candidate answers questions → AI evaluates each answer.

Scores & feedback are displayed → Option to download CSV report.

Limitations

Depends on Google Gemini API availability.

Evaluation fallback logic used when API fails.

Large JDs or many questions may take longer to process.

Currently only supports English language.

Potential Improvements

Add multi-language support.

Include voice-to-text for answers.

Integrate with HR systems for automated candidate tracking.

Real-time collaborative interview sessions.

Demo

Local demo: Run streamlit run app.py

Online demo: [Your Streamlit Cloud link here]

Acknowledgements

Google Gemini AI for AI question generation and evaluation.

Streamlit for easy-to-build web app interface.

pdfminer.six & python-docx for document parsing.