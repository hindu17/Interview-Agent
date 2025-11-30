import pandas as pd
import os
from pdfminer.high_level import extract_text
import docx

def parse_job_description(fileobj, text_box):
    """
    Parses job description from uploaded file or text area input.
    Supports txt, pdf, docx.
    """
    if fileobj is None and text_box:
        return text_box
    if fileobj is None:
        return ""

    fname = fileobj.name.lower()

    if fname.endswith(".txt"):
        return fileobj.getvalue().decode("utf-8")

    elif fname.endswith(".pdf"):
        with open("tmp_jd.pdf", "wb") as f:
            f.write(fileobj.getvalue())
        text = extract_text("tmp_jd.pdf")
        os.remove("tmp_jd.pdf")
        return text

    elif fname.endswith(".docx"):
        with open("tmp_jd.docx", "wb") as f:
            f.write(fileobj.getvalue())
        document = docx.Document("tmp_jd.docx")
        full = "\n".join([p.text for p in document.paragraphs])
        os.remove("tmp_jd.docx")
        return full

    return ""

def save_report_csv(role, level, rows, agg):
    """
    Saves the evaluation results to a CSV file.
    """
    df = pd.DataFrame(rows)
    df["Overall Score"] = agg.get("overall_score", 0)
    filename = f"interview_report_{role.replace(' ','_')}_{level}.csv"
    df.to_csv(filename, index=False)
    return os.path.abspath(filename)
