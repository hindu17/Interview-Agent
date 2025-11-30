import google.generativeai as genai
import random
import json
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "models/gemini-2.5-flash"
model = genai.GenerativeModel(MODEL)

DEFAULT_PROMPT = """
You are an expert interviewer. Given the job description and role information, 
produce a list of {n} interview questions.
Return JSON array where each item has:
- text
- type (technical|behavioral|system-design|case)
- difficulty (easy|medium|hard)
"""

def generate_questions(jd_text, role, level, n=6, mix=True, persona="Professional interviewer"):
    prompt = DEFAULT_PROMPT.format(n=n) + f"""

Job Description:
{jd_text}

Role: {role}
Level: {level}
Mix behavioral with technical: {mix}
Persona: {persona}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Try to extract JSON array from the text
        data = []
        try:
            start = text.find("[")
            end = text.rfind("]") + 1
            if start != -1 and end != -1:
                data = json.loads(text[start:end])
        except json.JSONDecodeError:
            data = []

        # Ensure we always return exactly n questions
        while len(data) < n:
            data.append({
                "text": f"Example question {len(data)+1} for {role} at {level}",
                "type": random.choice(["technical", "behavioral", "system-design", "case"]),
                "difficulty": random.choice(["easy", "medium", "hard"])
            })

        return data[:n]

    except Exception as e:
        # Fallback if Gemini API fails
        print("FALLBACK QUESTION GENERATION:", e)
        return [
            {
                "text": f"Example question {i+1} for {role} at {level}",
                "type": random.choice(["technical", "behavioral", "system-design", "case"]),
                "difficulty": random.choice(["easy", "medium", "hard"])
            }
            for i in range(n)
        ]
