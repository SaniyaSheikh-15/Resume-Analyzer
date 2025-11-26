import gradio as gr
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import re
import nltk
import tempfile
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from pdf2image import convert_from_bytes

nltk.download("punkt")
nltk.download("stopwords")

RECOMMENDED_SKILLS = {
    "AI/ML Intern": ["python", "tensorflow", "pandas", "deep learning", "machine learning"],
    "Data Analyst": ["excel", "sql", "power bi", "python", "data visualization"],
    "Web Developer": ["html", "css", "javascript", "react", "flask"],
    "Backend Developer": ["python", "django", "rest api", "sql"],
    "Cloud Engineer": ["aws", "azure", "docker", "kubernetes"],
}

def extract_text_from_resume(resume_bytes):
    try:
        images = convert_from_bytes(resume_bytes)
        text = "\n".join([pytesseract.image_to_string(img) for img in images])
        return text
    except Exception as e:
        return f"[ERROR] Unable to extract resume text: {str(e)}"

def extract_keywords_from_jd(jd_text):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(jd_text.lower())
    stop_words = set(stopwords.words("english"))
    keywords = [word for word in tokens if word.isalnum() and word not in stop_words]
    return list(set(keywords))

def extract_skills(text):
    all_skills = set()
    for skills in RECOMMENDED_SKILLS.values():
        all_skills.update(skills)
    found = [skill.lower() for skill in all_skills if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE)]
    return list(set(found))

def match_roles(skills_found):
    matched_roles = []
    total_possible = set().union(*RECOMMENDED_SKILLS.values())
    for role, req_skills in RECOMMENDED_SKILLS.items():
        matched = list(set(skills_found) & set(req_skills))
        if matched:
            score = int((len(matched) / len(req_skills)) * 100)
            matched_roles.append({
                "Role": role,
                "Matched Skills": matched,
                "Missing Skills": list(set(req_skills) - set(matched)),
                "Score": score
            })
    ats_score = int((len(skills_found) / len(total_possible)) * 100)
    return matched_roles, ats_score

def plot_ats_score_pie(score):
    fig, ax = plt.subplots()
    labels = [f"Match ({score}%)", f"Missing ({100 - score}%)"]
    colors = ["#00C9A7", "#F67280"]
    ax.pie([score, 100 - score], labels=labels, colors=colors, startangle=90, autopct='%1.1f%%')
    ax.axis("equal")
    plt.title("ATS Match Score", fontsize=14)
    tmpfile = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    plt.savefig(tmpfile.name, bbox_inches='tight')
    plt.close(fig)
    return tmpfile.name

def analyze_resume(resume_file, jd_text):
    resume_bytes = resume_file
    resume_text = extract_text_from_resume(resume_bytes)
    if resume_text.startswith("[ERROR]"):
        return resume_text, None

    jd_keywords = extract_keywords_from_jd(jd_text)
    resume_skills = extract_skills(resume_text)
    matched_roles, ats_score = match_roles(resume_skills)

    # 🥧 Generate Pie Chart
    pie_chart_path = plot_ats_score_pie(ats_score)

    # 📋 Generate Message
    if ats_score < 60:
        message = f"😕 Your ATS score is *{ats_score}%*, which is a bit low.\n\n"
        message += "🔍 To improve your chances, try refining your resume to highlight more relevant skills."
    else:
        best_fit = sorted(matched_roles, key=lambda x: x['Score'], reverse=True)[0]
        message = f"✅ Your ATS score is *{ats_score}%* — you're a strong match!\n\n"
        message += f"💼 You’re well-suited for the *{best_fit['Role']}* role."
        other_roles = [r for r in matched_roles if r['Role'] != best_fit['Role']]
        if other_roles:
            message += "\n\n📌 You might also explore roles like:\n"
            for r in other_roles[:2]:
                message += f"- *{r['Role']}* ({r['Score']}%)\n"

    return pie_chart_path, message
demo = gr.Interface(
    fn=analyze_resume,
    inputs=[
        gr.File(type="binary", label="📄 Upload Resume (PDF/Image)"),
        gr.Textbox(label="📝 Paste Job Description", lines=8, placeholder="Paste JD here...")
    ],
    outputs=[
        gr.Image(type="filepath", label="🎯 ATS Score"),
        gr.Markdown(label="💡 Suggestions & Best Fit Role")
    ],
    title="🚀 Resume Analyzer based on JD",
    description="Upload your resume and paste the job description. Get your ATS score as a chart and improve your chances!",
    theme="default"
)

if __name__ == "__main__":
    demo.launch(share=True)