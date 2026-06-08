"""
AI Resume Analyzer - Main Application
Streamlit web interface for resume analysis
"""

import streamlit as st
import tempfile
import os
import sys
from datetime import datetime
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from utils.pdf_parser import PDFParser
    from utils.skill_extractor import SkillExtractor
    from utils.similarity import SimilarityMatcher
    from utils.ats_checker import ATSChecker
    from utils.ai_suggestions import AISuggester
    from utils.report_generator import ReportGenerator
except ImportError as e:
    st.error(f"Import Error: {str(e)}")
    st.error("Make sure all utility files are in the 'utils' folder")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0;
    }
    
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
    
    .success-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        margin: 10px 0;
    }
    
    .warning-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        margin: 10px 0;
    }
    
    .error-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        margin: 10px 0;
    }
    
    .skill-tag {
        display: inline-block;
        padding: 5px 10px;
        margin: 5px;
        border-radius: 20px;
        background-color: #007bff;
        color: white;
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state"""
    if "resume_text" not in st.session_state:
        st.session_state.resume_text = None
    if "jd_text" not in st.session_state:
        st.session_state.jd_text = None
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None


def display_header():
    """Display application header"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📄 AI Resume Analyzer")
        st.markdown("Optimize your resume to match job descriptions using AI-powered analysis")
    with col2:
        st.image("https://img.icons8.com/color/96/000000/resume.png", width=80)


def display_sidebar():
    """Display sidebar navigation"""
    with st.sidebar:
        st.markdown("## Navigation")
        page = st.radio(
            "Select Page",
            ["Home", "Resume Analyzer", "ATS Checker", "Reports", "About"],
            index=1
        )
        
        st.markdown("---")
        st.markdown("## Settings")
        
        ai_provider = st.selectbox(
            "AI Provider",
            ["Google Gemini", "OpenAI", "None"]
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.info(
            "AI Resume Analyzer helps you optimize your resume "
            "to match job descriptions and improve ATS compatibility."
        )
        
        return page


def upload_and_parse_resume():
    """Handle resume upload and parsing"""
    st.markdown("### Step 1: Upload Your Resume")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload your resume in PDF format"
    )
    
    if uploaded_file is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                tmp_path = tmp_file.name
            
            # Parse resume
            with st.spinner("Parsing resume..."):
                resume_text = PDFParser.extract_text(tmp_path, method="pdfplumber")
            
            st.session_state.resume_text = resume_text
            
            # Display preview
            with st.expander("📋 Resume Content Preview"):
                st.text_area(
                    "Extracted Resume Text",
                    resume_text,
                    height=200,
                    disabled=True
                )
            
            st.success("✓ Resume uploaded and parsed successfully!")
            
            # Cleanup
            os.unlink(tmp_path)
            
            return True
        except Exception as e:
            st.error(f"Error parsing resume: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
            return False
    
    return False


def input_job_description():
    """Handle job description input"""
    st.markdown("### Step 2: Paste Job Description")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("📝 Sample JD", help="Load a sample job description"):
            sample_jd = """Senior Python Developer

We are looking for an experienced Python Developer to join our team.

Requirements:
- 5+ years of Python development experience
- Strong knowledge of Django and FastAPI
- Experience with PostgreSQL and MongoDB
- AWS cloud platform experience
- Docker and Kubernetes knowledge
- REST API design and implementation
- CI/CD pipeline setup (Jenkins, GitHub Actions)
- SQL optimization
- Git version control

Nice to have:
- Machine Learning experience with TensorFlow/PyTorch
- Microservices architecture
- Redis caching
- Elasticsearch
- Agile/Scrum methodology

Responsibilities:
- Develop and maintain Python applications
- Design and implement APIs
- Optimize database queries
- Implement CI/CD pipelines
- Code review and mentoring

Salary: $100k - $150k
Location: Remote"""
            st.session_state.jd_text = sample_jd
    
    with col1:
        jd_text = st.text_area(
            "Job Description",
            value=st.session_state.jd_text or "",
            height=200,
            placeholder="Paste the job description here..."
        )
    
    if jd_text:
        st.session_state.jd_text = jd_text
        char_count = len(jd_text)
        st.caption(f"Characters: {char_count}")
        return True
    
    return False


def analyze_resume():
    """Perform comprehensive resume analysis"""
    if not st.session_state.resume_text or not st.session_state.jd_text:
        st.warning("Please upload resume and provide job description first")
        return None
    
    st.markdown("### Step 3: Analysis Results")
    
    with st.spinner("Analyzing resume..."):
        try:
            # Extract skills
            skill_extractor = SkillExtractor()
            resume_skills = skill_extractor.extract_skills(st.session_state.resume_text)
            jd_skills = skill_extractor.extract_skills(st.session_state.jd_text)
            
            # Calculate match score
            match_data = SimilarityMatcher.calculate_combined_score(
                st.session_state.resume_text,
                st.session_state.jd_text,
                resume_skills["all_skills"],
                jd_skills["all_skills"]
            )
            
            # Calculate ATS score
            ats_data = ATSChecker.calculate_ats_score(
                st.session_state.resume_text,
                st.session_state.jd_text
            )
            
            # Get missing skills
            missing_skills_info = skill_extractor.get_missing_skills(
                resume_skills["all_skills"],
                jd_skills["all_skills"]
            )
            
            # Generate suggestions
            suggester = AISuggester()
            suggestions = suggester.generate_suggestions(
                st.session_state.resume_text,
                st.session_state.jd_text,
                missing_skills_info["missing_skills"],
                ats_data["issues"]
            )
            
            results = {
                "match_score": match_data,
                "ats_score": ats_data,
                "resume_skills": resume_skills,
                "jd_skills": jd_skills,
                "missing_skills": missing_skills_info,
                "suggestions": suggestions
            }
            
            st.session_state.analysis_results = results
            return results
            
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
            return None


def display_match_score(results):
    """Display resume-JD match score"""
    if not results or "match_score" not in results:
        return
    
    st.markdown("## 📊 Resume-JD Match Score")
    
    match = results["match_score"]
    overall_score = match["overall_match_score"]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Overall Match",
            f"{overall_score}%",
            delta=f"{overall_score - 50}% from average"
        )
    
    with col2:
        st.metric(
            "TF-IDF Score",
            f"{match['tfidf_score']}%"
        )
    
    with col3:
        st.metric(
            "Keyword Score",
            f"{match['keyword_score']}%"
        )
    
    with col4:
        st.metric(
            "Skill Match",
            f"{match['skill_match_score']}%"
        )
    
    # Progress bar
    st.progress(overall_score / 100)
    
    # Interpretation
    if overall_score >= 80:
        st.success("✓ Excellent match! Your resume aligns well with the job description.")
    elif overall_score >= 60:
        st.info("⚠ Good match. Consider adding some missing skills.")
    else:
        st.warning("✗ Limited match. Significant improvements needed.")


def display_ats_score(results):
    """Display ATS compatibility score"""
    if not results or "ats_score" not in results:
        return
    
    st.markdown("## 🤖 ATS Compatibility Score")
    
    ats = results["ats_score"]
    overall_ats = ats["overall_ats_score"]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "ATS Score",
            f"{overall_ats}/100"
        )
    
    with col2:
        st.metric(
            "Contact Info",
            f"{ats['contact_information_score']}/100"
        )
    
    with col3:
        st.metric(
            "Formatting",
            f"{ats['formatting_score']}/100"
        )
    
    with col4:
        st.metric(
            "Keywords",
            f"{ats['keyword_optimization_score']}/100"
        )
    
    st.progress(overall_ats / 100)
    
    # Issues
    if ats["issues"]:
        st.markdown("### ⚠️ ATS Issues Found")
        for issue in ats["issues"]:
            st.markdown(f"• {issue}")


def display_skills_analysis(results):
    """Display skills analysis"""
    if not results:
        return
    
    st.markdown("## 🎯 Skills Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Your Resume Skills")
        resume_skills = results["resume_skills"]
        
        if resume_skills["technical_skills"]:
            st.markdown("**Technical Skills:**")
            for skill in resume_skills["technical_skills"]:
                st.markdown(f"🔹 {skill}")
        
        if resume_skills["soft_skills"]:
            st.markdown("**Soft Skills:**")
            for skill in resume_skills["soft_skills"]:
                st.markdown(f"🔹 {skill}")
    
    with col2:
        st.markdown("### Missing Skills")
        missing = results["missing_skills"]
        
        if missing["missing_skills"]:
            st.markdown("**Skills to Add:**")
            for skill in missing["missing_skills"][:10]:
                st.markdown(f"❌ {skill}")
            
            if len(missing["missing_skills"]) > 10:
                st.info(f"... and {len(missing['missing_skills']) - 10} more")
        else:
            st.success("✓ All skills present!")


def display_suggestions(results):
    """Display AI suggestions"""
    if not results or "suggestions" not in results:
        return
    
    st.markdown("## 💡 AI Improvement Suggestions")
    
    suggestions = results["suggestions"]
    
    tabs = st.tabs([
        "Missing Keywords",
        "Project Improvements",
        "Summary",
        "ATS Optimization",
        "Formatting",
        "Industry Specific"
    ])
    
    categories = [
        "missing_keywords",
        "project_improvements",
        "summary_improvements",
        "ats_optimization",
        "formatting_suggestions",
        "industry_specific"
    ]
    
    for tab, category in zip(tabs, categories):
        with tab:
            if category in suggestions:
                for i, suggestion in enumerate(suggestions[category], 1):
                    st.markdown(f"{i}. {suggestion}")


def display_download_report(results):
    """Display report download option"""
    if not results:
        return
    
    st.markdown("## 📥 Download Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Download Text Report"):
            try:
                report_text = ReportGenerator.generate_text_report(results)
                st.download_button(
                    label="Download Text Report",
                    data=report_text,
                    file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
                st.success("Report generated successfully!")
            except Exception as e:
                st.error(f"Error generating text report: {str(e)}")
    
    with col2:
        if st.button("📊 Download PDF Report"):
            try:
                pdf_path = f"/tmp/resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                ReportGenerator.generate_pdf_report(results, pdf_path)
                
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_file.read(),
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf"
                    )
                st.success("PDF report generated successfully!")
                os.unlink(pdf_path)
            except Exception as e:
                st.error(f"Error generating PDF report: {str(e)}")


def main():
    """Main application logic"""
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Sidebar navigation
    page = display_sidebar()
    
    if page == "Home":
        st.markdown("""
        ## Welcome to AI Resume Analyzer! 👋
        
        This tool helps you optimize your resume to match job descriptions using AI-powered analysis.
        
        ### Features:
        
        ✅ **Resume Upload** - Upload your PDF resume  
        ✅ **Job Description Input** - Paste or load sample JD  
        ✅ **Skill Extraction** - Extract technical and soft skills  
        ✅ **Match Analysis** - Get detailed resume-JD match score  
        ✅ **ATS Scoring** - Check ATS compatibility  
        ✅ **Missing Skills** - Identify skills to add  
        ✅ **AI Suggestions** - Get improvement recommendations  
        ✅ **Report Generation** - Download detailed analysis reports  
        
        ### Getting Started:
        
        1. Go to **Resume Analyzer** page
        2. Upload your resume (PDF)
        3. Paste or load a job description
        4. Click "Analyze" to get comprehensive results
        5. Download your analysis report
        
        ---
        """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("💼 **Analyze Match** - See how well your resume matches the job")
        
        with col2:
            st.info("🤖 **ATS Check** - Ensure your resume passes ATS screening")
        
        with col3:
            st.info("📊 **Get Report** - Download detailed analysis as PDF/Text")
    
    elif page == "Resume Analyzer":
        col1, col2 = st.columns([1, 1])
        
        with col1:
            resume_uploaded = upload_and_parse_resume()
        
        with col2:
            jd_provided = input_job_description()
        
        st.markdown("---")
        
        if resume_uploaded and jd_provided:
            if st.button("🔍 Analyze Resume", key="analyze_btn", use_container_width=True):
                results = analyze_resume()
                
                if results:
                    st.success("✓ Analysis complete!")
                    
                    st.markdown("---")
                    display_match_score(results)
                    st.markdown("---")
                    display_ats_score(results)
                    st.markdown("---")
                    display_skills_analysis(results)
                    st.markdown("---")
                    display_suggestions(results)
                    st.markdown("---")
                    display_download_report(results)
    
    elif page == "ATS Checker":
        st.markdown("## ATS Compatibility Checker")
        
        uploaded_file = st.file_uploader(
            "Upload your resume",
            type="pdf",
            key="ats_upload"
        )
        
        if uploaded_file:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    tmp_path = tmp_file.name
                
                resume_text = PDFParser.extract_text(tmp_path)
                ats_analysis = ATSChecker.calculate_ats_score(resume_text)
                
                st.markdown("### ATS Analysis Results")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("ATS Score", f"{ats_analysis['overall_ats_score']}/100")
                
                with col2:
                    st.metric("Contact Info", f"{ats_analysis['contact_information_score']}/100")
                
                with col3:
                    st.metric("Formatting", f"{ats_analysis['formatting_score']}/100")
                
                with col4:
                    st.metric("Keywords", f"{ats_analysis['keyword_optimization_score']}/100")
                
                st.progress(ats_analysis['overall_ats_score'] / 100)
                
                if ats_analysis['issues']:
                    st.markdown("### Issues Found:")
                    for issue in ats_analysis['issues']:
                        st.markdown(f"⚠️ {issue}")
                
                os.unlink(tmp_path)
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
                import traceback
                st.error(traceback.format_exc())
    
    elif page == "Reports":
        st.markdown("## Analysis Reports")
        
        if st.session_state.analysis_results:
            st.success("✓ Analysis results available")
            display_download_report(st.session_state.analysis_results)
        else:
            st.info("Complete an analysis on the 'Resume Analyzer' page to generate reports.")
    
    elif page == "About":
        st.markdown("""
        ## About AI Resume Analyzer
        
        ### Project Overview
        
        AI Resume Analyzer is a comprehensive tool designed to help job seekers optimize their resumes
        for both human recruiters and Applicant Tracking Systems (ATS).
        
        ### Technology Stack
        
        - **Frontend**: Streamlit
        - **Backend**: Python
        - **NLP**: scikit-learn, NLTK, spaCy
        - **PDF Processing**: PyPDF2, pdfplumber
        - **AI**: Google Gemini / OpenAI API
        - **Reporting**: ReportLab
        
        ### Features
        
        1. **PDF Resume Parsing** - Extract text from multi-page PDFs
        2. **Skill Extraction** - Identify technical and soft skills
        3. **Resume-JD Matching** - TF-IDF and cosine similarity based matching
        4. **ATS Scoring** - Check ATS compatibility
        5. **Missing Skills Detection** - Identify gaps
        6. **AI Suggestions** - Get personalized recommendations
        7. **Report Generation** - Download analysis as PDF/Text
        
        ### How It Works
        
        1. **Upload Resume** - PDF parsing extracts text
        2. **Provide JD** - Job description input
        3. **Skill Analysis** - Extract and compare skills
        4. **Match Scoring** - Calculate resume-JD alignment
        5. **ATS Check** - Verify formatting and structure
        6. **AI Suggestions** - Generate improvement recommendations
        7. **Report** - Download comprehensive analysis
        
        ### Contact & Support
        
        For questions or feedback, please reach out to the development team.
        
        ---
        
        Built with ❤️ for job seekers
        """)


if __name__ == "__main__":
    main()
