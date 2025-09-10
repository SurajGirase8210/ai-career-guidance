# AI Career Guidance & Skill Gap Analyzer

🚀 A Flask-based web app that analyzes resumes or manually entered skills, compares them with industry job roles, and provides:
- ✅ Career match percentage
- ✅ Matched & missing skills
- ✅ Recommended courses for missing skills
- ✅ Visual career analysis with donut charts
- ✅ Downloadable PDF career report

---

## ✨ Features
- Upload **resume (PDF/DOCX)** or enter skills manually
- Detects **multi-word skills** (e.g., Machine Learning, Deep Learning)
- Suggests **career options** from a job dataset
- Identifies **skill gaps** for each career
- Provides **recommended courses** from top platforms (Coursera, Udemy, etc.)
- Generates **interactive donut charts** per career
- Export a **Career Report as PDF** (with cover page and charts)

---

## 🛠 Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Chart.js
- **Data**: jobs.csv, course_recommendations.csv
- **PDF Reports**: ReportLab, Matplotlib
- **Resume Parsing**: python-docx, PyPDF2

---

## 📂 Project Structure
AI-Career-Guidance/
│── app.py # Main Flask app
│── requirements.txt # Dependencies
│── jobs.csv # Job roles and required skills
│── course_recommendations.csv # Skill → Course mapping
│── templates/
│ ├── index.html # Homepage (resume/manual input)
│ ├── results.html # Career analysis results
│── static/
│ ├── style.css # Styling (dark theme)
│── uploads/ # Uploaded resumes (ignored in Git)


---

## ⚙️ Setup & Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/SurajGirase8210/ai-career-guidance.git
   cd ai-career-guidance

2.Create virtual envirnoment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3.Install dependencies:
pip install -r requirements.txt

4.Run The app
python app.py

5.Open in browser
http://127.0.0.1:5000/

📊 Example Careers Included

Data Scientist
Web Developer
AI Engineer
Cybersecurity Analyst
Cloud Engineer
Mobile App Developer
DevOps Engineer
Business Analyst
Data Engineer
UI/UX Designer
Game Developer
Machine Learning Engineer
