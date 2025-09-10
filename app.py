from flask import Flask, render_template, request
import os
import docx
import PyPDF2
import pandas as pd
import re
import io
from flask import send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import matplotlib.pyplot as plt
from reportlab.lib.utils import ImageReader


app = Flask(__name__)

# -------------------------
# Load Data from CSV files
# -------------------------
jobs_df = pd.read_csv("jobs.csv")
courses_df = pd.read_csv("course_recommendations.csv")

# Convert to dictionaries for easy access
career_data = {
    row["career"]: [s.strip() for s in str(row["skills"]).split(",")]
    for _, row in jobs_df.iterrows()
}

course_suggestions = {
    row["skill"]: row["course_link"]
    for _, row in courses_df.iterrows()
}

# -------------------------
# Helper functions
# -------------------------
def extract_text_from_docx(path):
    doc = docx.Document(path)
    return " ".join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def analyze_skills(user_skills):
    results = []
    user_skills = [u.lower() for u in user_skills]  # normalize once

    for career, required_skills in career_data.items():
        required_lower = [s.lower() for s in required_skills]

        matched = [s for s, s_low in zip(required_skills, required_lower) if s_low in user_skills]
        missing = [s for s, s_low in zip(required_skills, required_lower) if s_low not in user_skills]
        
        #Calculating matched percentage
        match_percent = round((len(matched) / len(required_skills)) * 100, 2) if required_skills else 0

        results.append({
            "career": career,
            "matched": matched,
            "missing": missing,
            "match_percent": match_percent,
            "courses": [course_suggestions.get(s, '#') for s in missing if s in course_suggestions]
        })
    return results

# -------------------------
# Routes
# -------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    skills = []
    text = ""

    # Resume Upload
    if "resume" in request.files and request.files["resume"].filename != "":
        file = request.files["resume"]
        filepath = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(filepath)

        if file.filename.endswith(".docx"):
            text = extract_text_from_docx(filepath)
        elif file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(filepath)
            
        #Clean text : lower and remove puncuations
        clean_text = re.sub(r"[^a-zA-Z0-9\s]", " ", text).lower().split()
        
        
        #Only keep word that are actual skills in our dataset
        all_skills = set(s.lower() for skills in career_data.values() for s in skills)
        skills = [w for w in clean_text if w in all_skills]

    # Manual Skills Entry
    elif "skills" in request.form and request.form["skills"].strip() != "":
        #Split by comma and clean spaces
        raw_input = request.form["skills"].lower()
        
        #Building a set of all skills in our dataset
        all_skills = set(s.lower() for skills in career_data.values() for s in skills)
        
        if "," in raw_input:
            #User separated by commas
            skills = [s.strip() for s in raw_input.split(",") if s.strip()]
        else:
            skills = []
            for known in all_skills:
                if known in raw_input:
                    skills.append(known)

    else:
        return render_template("results.html", jobs=[])

    # Run Analysis
    results = analyze_skills(skills)
    return render_template("results.html", jobs=results)

@app.route("/download_report", methods=["POST"])
def download_report():
    data = request.get_json()
    jobs = data.get("jobs", []) if data else []

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Career Guidance & Skill Gap Report")

    y = height - 100
    c.setFont("Helvetica", 12)

    for job in jobs:
        c.drawString(50, y, f"Career: {job['career']}")
        y -= 20
        c.drawString(70, y, f"Skill Match %: {job['match_percent']}%")
        y -= 20
        c.drawString(70, y, "Matched Skills: " + (", ".join(job['matched']) if job['matched'] else "None"))
        y -= 20
        c.drawString(70, y, "Missing Skills: " + (", ".join(job['missing']) if job['missing'] else "None"))
        y -= 20

        # Add pie chart for this job
        matched = len(job['matched'])
        missing = len(job['missing'])
        if matched + missing > 0:
            fig, ax = plt.subplots()
            ax.pie([matched, missing],
                   labels=["Matched", "Missing"],
                   colors=["#00d8ff", "#ff4d4d"],
                   autopct="%1.1f%%")
            ax.set_title(job['career'])

            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format="PNG", bbox_inches="tight")
            plt.close(fig)
            img_buffer.seek(0)

            img = ImageReader(img_buffer)
            c.drawImage(img, 70, y-200, width=200, height=200)  # place chart
            y -= 220

        if job['courses']:
            c.drawString(70, y, "Recommended Courses:")
            y -= 20
            for course in job['courses']:
                c.drawString(90, y, f"- {course}")
                y -= 20

        y -= 30
        if y < 200:  # new page if space runs out
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 12)

    c.save()
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="Career_Report.pdf",
        mimetype="application/pdf"
    )

        
if __name__ == "__main__":
    app.run(debug=True)
