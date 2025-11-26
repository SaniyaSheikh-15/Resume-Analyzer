# 🚀 AI Enabled Resume Analyzer

A smart resume screening tool built using Python + Gradio that analyses your resume against any Job Description and gives:
✔ ATS Score %
✔ Best-Fit Job Role Suggestions
✔ Missing & Matched Skills
✔ Pie-Chart Visualization
✔ Action-based improvement tips

Upload resume → paste JD → hit run → get instant evaluation.
Perfect for jobseekers, portfolio projects, and HR automation tools.

# ✨ Features

1.Extract resume text from PDF/Image 
2.OCR powered by Pytesseract & pdf2image 
3.Skill extraction + JD keyword parsing	
4.ATS Match Score Percentage 
5.Pie Chart Report Output 
6.Role Recommendations 
7.Improvement Suggestions 
8.Fully UI-based Gradio Web Interface	

# 🧠 Tech Stack

1. Python - Core logic
2. Gradio - Web UI
3. PyMuPDF / pdf2image -	PDF → image extraction
4. Pytesseract	OCR - text extraction
5. NLTK Tokenizer + Stopwords - JD keyword filtering
6. Matplotlib - ATS Pie Chart
7. PIL -	Image handling

# ⚙ Setup & Installation

1️⃣ Install Dependencies
pip install -r requirements.txt
Make sure Tesseract OCR is installed on your system

2️⃣ Run the Web App
python app.py

Auto-launches in browser.
Or deploy anywhere using HuggingFace/Render/Vercel.

# If you like this project → leave a ⭐ on GitHub, it’ll make my whole day ✨
