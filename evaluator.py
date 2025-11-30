import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "models/gemini-2.5-flash"
model = genai.GenerativeModel(MODEL)

EVAL_PROMPT = """
You are an expert interviewer and evaluator.

Return JSON:
{{
 "score": float (0-10),
 "feedback": "short feedback",
 "tags": [list]
}}

Question: {question}
Answer: {answer}
Role: {role}
Level: {level}
Persona: {persona}

If the answer is empty, give score 0.
"""

def evaluate_answer(question, answer, role, level, persona):
    if not answer.strip():
        return {
            "question": question,
            "score": 0,
            "feedback": "No answer provided.",
            "tags": ["empty"]
        }

    prompt = EVAL_PROMPT.format(
        question=question,
        answer=answer,
        role=role,
        level=level,
        persona=persona
    )

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Try to parse JSON safely
        start = text.find("{")
        end = text.rfind("}") + 1
        data_str = text[start:end]
        data = json.loads(data_str)

        return {
            "question": question,
            "score": float(data.get("score", 0)),
            "feedback": data.get("feedback", ""),
            "tags": data.get("tags", [])
        }

    except Exception as e:
        # Fallback if Gemini returns invalid JSON
        length_score = min(10, len(answer.split()) / 10)
        return {
            "question": question,
            "score": length_score,
            "feedback": "Fallback evaluation. Could not parse AI response.",
            "tags": ["fallback"]
        }


def aggregate_scores(results):
    total = sum(r["score"] for r in results)
    count = len(results)
    overall = (total / (count * 10)) * 100 if count > 0 else 0
    return {"overall_score": overall}
