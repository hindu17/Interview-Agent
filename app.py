import streamlit as st
from question_generator import generate_questions
from evaluator import evaluate_answer, aggregate_scores
from utils import parse_job_description, save_report_csv
from dotenv import load_dotenv
import google.generativeai as genai
import os

# --------------------
# LOAD ENV + CONFIGURE GEMINI
# --------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ ERROR: GEMINI_API_KEY not found in .env file!")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# --------------------
# STREAMLIT UI CONFIG
# --------------------
st.set_page_config(page_title="Interview Agent", layout="centered")

st.title("🧑‍💼 Interview Agent — Automated Interview + AI Scoring")
st.markdown(
    "Upload a job description, choose role & level, generate interview questions, "
    "answer them, and get an AI-powered evaluation report."
)

# --------------------
# SECTION 1 — JOB DESCRIPTION
# --------------------
with st.expander("1 — Job description / Role"):
    jd_input = st.file_uploader("Upload Job Description (txt, pdf, docx)", type=["txt", "pdf", "docx"])
    jd_text_box = st.text_area("Or paste Job Description here", height=150)
    role = st.text_input("Role", value="Frontend Developer")
    level = st.selectbox("Level", ["Intern/Entry", "Mid", "Senior", "Lead"])

    if st.button("Parse JD"):
        jd_text = parse_job_description(jd_input, jd_text_box)
        st.success("Parsed JD:")
        st.write(jd_text[:1500] + ("..." if len(jd_text) > 1500 else ""))

st.markdown("---")

# --------------------
# SECTION 2 — QUESTION GENERATION CONFIG
# --------------------
with st.form("config_form"):
    num_questions = st.slider("Number of questions", 3, 12, 6)
    mix = st.checkbox("Mix: Technical + Behavioral", value=True)
    persona = st.text_input("Interviewer Persona", value="Friendly, strict HR Manager")

    submitted = st.form_submit_button("Generate Questions")

if submitted:
    jd_text = parse_job_description(jd_input, jd_text_box)
    questions = generate_questions(jd_text, role, level, num_questions, mix, persona)
    st.session_state["questions"] = questions
    st.session_state["answers"] = [""] * len(questions)
    st.success(f"Generated {len(questions)} interview questions!")

# --------------------
# SECTION 3 — DISPLAY QUESTIONS + ANSWER INPUT
# --------------------
if "questions" in st.session_state:
    st.header("Interview Section")

    for i, q in enumerate(st.session_state["questions"]):
        st.subheader(f"Q{i+1}: {q['text']}")
        ans = st.text_area(
            f"Your Answer {i+1}",
            key=f"ans_{i}",
            value=st.session_state["answers"][i],
            height=120
        )
        st.session_state["answers"][i] = ans
        st.caption(f"Type: {q['type']} | Difficulty: {q['difficulty']}")

    if st.button("Evaluate Answers"):
        results = []

        with st.spinner("Evaluating your answers with Gemini AI..."):
            for i, q in enumerate(st.session_state["questions"]):
                answer = st.session_state["answers"][i].strip()
                result = evaluate_answer(q["text"], answer, role, level, persona)
                results.append(result)

        st.session_state["results"] = results
        agg = aggregate_scores(results)

        st.success("Evaluation Completed!")
        st.metric("Overall Score (0–100)", f"{agg['overall_score']:.1f}")

        st.write("### Detailed AI Feedback")
        rows = []
        for i, r in enumerate(results):
            st.markdown(f"**Q{i+1}: {r['question']}**")
            st.write(f"🔹 **Score:** {r['score']}/10")
            st.write(f"💬 **Feedback:** {r['feedback']}")
            st.write("---")
            rows.append(r)

        # if st.button("Download Report as CSV"):
        #     file_path = save_report_csv(role, level, rows, agg)
        #     st.success(f"📄 Report Saved: `{file_path}`")

st.markdown("---")
st.info("💡 Powered by Google Gemini AI — Supports question generation, evaluation, JD parsing & CSV reports.")
