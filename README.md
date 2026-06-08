````markdown
# 📄 AI Resume Analyzer

An AI-powered web application that helps job seekers optimize their resumes by analyzing them against job descriptions. Get detailed insights on skill matches, ATS compatibility, and actionable improvement suggestions.

## ✨ Features

### Core Features
- **📤 Resume Upload** - Upload PDF resumes (handles multi-page documents)
- **📝 Job Description Input** - Paste or load sample job descriptions
- **🎯 Skill Extraction** - Extract technical and soft skills from both resume and JD
- **📊 Resume-JD Matching** - Calculate match score using TF-IDF and cosine similarity
- **🤖 ATS Scoring** - Check Applicant Tracking System compatibility
- **❌ Missing Skills Detection** - Identify skills to add from job description
- **💡 AI Suggestions** - Get personalized improvement recommendations
- **📥 Report Generation** - Download analysis as PDF or text format

### Bonus Features
- **Dark/Light Mode** - Professional UI with theme support
- **Detailed Dashboard** - Visual analytics and metrics
- **Multi-section Analysis** - Analyze contact info, formatting, keywords, and content
- **Improvement Roadmap** - Prioritized suggestions for resume enhancement

## 🛠️ Tech Stack

### Frontend
- **Streamlit** - Web interface framework

### Backend
- **Python 3.8+** - Core language

### Libraries
- **PyPDF2 / pdfplumber** - PDF text extraction
- **pandas** - Data manipulation
- **nltk / spaCy** - NLP text processing
- **scikit-learn** - TF-IDF and similarity calculations
- **google-generativeai / openai** - AI-powered suggestions
- **reportlab** - PDF report generation
- **matplotlib / seaborn / plotly** - Data visualization

## 📋 Requirements

```
streamlit==1.28.1
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
nltk==3.8.1
spacy==3.6.1
PyPDF2==3.0.1
pdfplumber==0.10.3
google-generativeai==0.3.0
openai==1.3.0
reportlab==4.0.7
python-dotenv==1.0.0
matplotlib==3.7.2
seaborn==0.12.2
plotly==5.17.0
```

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### 2. Create Virtual Environment
```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download Required NLTK Data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 5. Configure Environment Variables
```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use your favorite editor
```

**Environment Variables:**
```
AI_PROVIDER=google  # or openai, or none
GOOGLE_API_KEY=your_api_key_here
OPENAI_API_KEY=your_api_key_here
```

### 6. Run the Application
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 📂 Project Structure

```
AI-Resume-Analyzer/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore file
├── README.md                       # Project documentation
│
├── utils/                          # Utility modules
│   ├── __init__.py                # Package initialization
│   ├── pdf_parser.py              # PDF text extraction
│   ├── skill_extractor.py         # Skill extraction engine
│   ├── similarity.py              # NLP similarity matching
│   ├── ats_checker.py             # ATS compatibility analysis
│   ├── ai_suggestions.py          # AI-powered suggestions
│   └── report_generator.py        # Report generation
│
├── assets/                         # Images and static files
├── data/                           # Data files and databases
│   └── skills_database.json       # Skill reference database
│
├── reports/                        # Generated reports output
└── docs/                           # Documentation
```

## 🎯 How to Use

### Step 1: Upload Resume
1. Navigate to "Resume Analyzer" page
2. Click on "Choose a PDF file" 
3. Select your resume PDF
4. Review the extracted text preview

### Step 2: Provide Job Description
1. Paste the job description in the text area, OR
2. Click "Sample JD" button to load an example
3. View character count

### Step 3: Run Analysis
1. Click "Analyze Resume" button
2. Wait for analysis to complete (typically 10-30 seconds)
3. Review all results

### Step 4: Review Results
1. **Match Score** - Overall resume-JD alignment (0-100%)
2. **ATS Score** - Compatibility with Applicant Tracking Systems
3. **Skills Analysis** - Your skills vs. required skills
4. **Suggestions** - AI-powered improvement recommendations

### Step 5: Download Report
1. Click "Download Text Report" or "Download PDF Report"
2. Save the file to your computer
3. Use for further resume improvements

## 📊 Analysis Metrics Explained

### Resume-JD Match Score (0-100%)
- **TF-IDF Score** (40%): Content similarity using term frequency
- **Keyword Score** (30%): Keyword overlap and relevance
- **Skill Match** (30%): Skill intersection from JD

**Interpretation:**
- 80-100% - Excellent match, highly qualified
- 60-79% - Good match, consider adding some skills
- 40-59% - Moderate match, significant improvements needed
- 0-39% - Poor match, major revisions recommended

### ATS Compatibility Score (0-100)
- **Contact Information** (30%): Email, phone, location, LinkedIn
- **Formatting** (30%): Structure, sections, ATS-friendly format
- **Keywords & Content** (40%): Skill keywords, action verbs, metrics

**Interpretation:**
- 80-100 - Excellent ATS compatibility
- 60-79 - Good, minor improvements suggested
- 40-59 - Fair, significant formatting needed
- 0-39 - Poor, major ATS issues found

## 🔑 API Setup Guide

### Google Generative AI (Recommended)

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the API key
4. Add to `.env` file:
   ```
   AI_PROVIDER=google
   GOOGLE_API_KEY=your_key_here
   ```

### OpenAI

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create new API key
3. Copy the key
4. Add to `.env` file:
   ```
   AI_PROVIDER=openai
   OPENAI_API_KEY=your_key_here
   ```

### Using Without AI
If you don't have API keys, the app still works with built-in suggestions:
```
AI_PROVIDER=none
```

## 🎓 Skills Database

The application includes an extensive database of:
- **Programming Languages** (20+): Python, Java, JavaScript, C++, Go, Rust, etc.
- **Web Frameworks** (15+): React, Django, FastAPI, Spring, Node.js, Laravel, etc.
- **Databases** (15+): PostgreSQL, MongoDB, MySQL, Redis, Elasticsearch, etc.
- **Cloud Platforms** (8+): AWS, Azure, Google Cloud, Heroku, DigitalOcean, etc.
- **DevOps Tools** (15+): Docker, Kubernetes, Jenkins, GitHub Actions, Terraform, etc.
- **Data Science** (12+): TensorFlow, PyTorch, Scikit-learn, Pandas, Spark, etc.
- **Soft Skills** (25+): Communication, Leadership, Problem Solving, Teamwork, etc.

## 📈 Example Workflow

```
Resume PDF (upload)
    ↓
PDF Parser (extracts text)
    ↓
Skill Extractor (identifies 25+ skills)
    ↓
Job Description (paste)
    ↓
NLP Analysis (calculates similarities)
    ↓
ATS Checker (validates format)
    ↓
Results Dashboard
    ├─ Match Score: 78%
    ├─ ATS Score: 82/100
    ├─ Missing Skills: Docker, Kubernetes
    └─ Suggestions: 20+ actionable tips
    ↓
Report Generation (PDF/Text download)
```

## 🎨 UI Features

- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark/Light Mode** - Professional theme options
- **Progress Bars** - Visual score representations
- **Metric Cards** - Key statistics display
- **Expandable Sections** - Detailed content previews
- **Downloadable Reports** - PDF and text formats
- **Color-coded Results** - Easy-to-scan visual feedback

## 🔍 Analysis Categories

### Contact Information Check
- ✅ Email address
- ✅ Phone number
- ✅ LinkedIn profile
- ✅ Location

### Formatting Validation
- ✅ ASCII characters only
- ✅ Section headers
- ✅ No complex formatting
- ✅ Standard structure

### Content Analysis
- ✅ Skill section presence
- ✅ Action verbs usage
- ✅ Quantifiable achievements
- ✅ Industry keywords

### Skill Matching
- ✅ Technical skills alignment
- ✅ Soft skills presence
- ✅ Gap identification
- ✅ Priority ranking

## 💡 AI Improvement Suggestions

The app generates suggestions in 6 categories:

1. **Missing Keywords** - Add JD-specific terminology
2. **Project Improvements** - Enhance project descriptions
3. **Summary Enhancements** - Improve professional summary
4. **ATS Optimization** - Format for ATS systems
5. **Formatting Tips** - Improve visual structure
6. **Industry Specific** - Role-specific recommendations

## 🚨 Troubleshooting

### Issue: PDF parsing fails
**Solution:** Ensure PDF is text-based, not scanned image. Try using the alternative parser.

### Issue: No API response
**Solution:** Check API keys in `.env` file and ensure they have proper permissions.

### Issue: Skills not recognized
**Solution:** Skills database uses standard terminology. Use common industry terms.

### Issue: App runs slowly
**Solution:** Larger resumes take longer to process. This is normal for 5+ page resumes.

## 🔄 Future Improvements

- [ ] Multiple resume comparison
- [ ] Resume rewriter with AI
- [ ] Keyword heatmap visualization
- [ ] Interview preparation tips
- [ ] Cover letter optimizer
- [ ] Salary insights integration
- [ ] Job matching recommendations
- [ ] Profile strength scoring
- [ ] Export to multiple formats

## 📝 Sample JD

The app includes a sample Senior Python Developer job description that covers:
- Technical requirements (Python, Django, FastAPI, databases)
- DevOps skills (Docker, Kubernetes, CI/CD)
- Cloud experience (AWS)
- Soft skills expectations

## 🤝 Contributing

Contributions are welcome! Please feel free to:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👤 Author

Created for helping job seekers optimize their resumes using AI.

## 📧 Support

For issues, questions, or suggestions:
1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with detailed information

## 🙏 Acknowledgments

- Streamlit for the amazing web framework
- scikit-learn for NLP capabilities
- Google and OpenAI for AI models
- The open-source community

---

**Start optimizing your resume today!** 🚀

Built with ❤️ for job seekers
````
