"""
AI Suggestions Module
Generates improvement suggestions using AI APIs
"""

import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()


class AISuggester:
    """Generate AI-powered suggestions for resume improvement"""
    
    def __init__(self):
        """Initialize AI suggester with API keys"""
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.api_provider = os.getenv("AI_PROVIDER", "google")
    
    def generate_suggestions(self, resume_text: str, jd_text: str,
                           missing_skills: List[str] = None,
                           ats_issues: List[str] = None) -> Dict:
        """
        Generate comprehensive improvement suggestions
        
        Args:
            resume_text: Resume text
            jd_text: Job description text
            missing_skills: List of missing skills
            ats_issues: List of ATS issues
            
        Returns:
            Dictionary with AI suggestions
        """
        suggestions = {
            "missing_keywords": self._suggest_missing_keywords(resume_text, jd_text),
            "project_improvements": self._suggest_project_improvements(resume_text),
            "summary_improvements": self._suggest_summary_improvements(resume_text, jd_text),
            "ats_optimization": self._suggest_ats_optimization(ats_issues or []),
            "formatting_suggestions": self._suggest_formatting(),
            "industry_specific": self._suggest_industry_specific(jd_text)
        }
        
        return suggestions
    
    def _suggest_missing_keywords(self, resume_text: str, jd_text: str) -> List[str]:
        """Suggest missing keywords from JD"""
        suggestions = [
            "Review the job description and identify core technical keywords",
            "Incorporate industry-specific terminology used in the JD",
            "Use the exact keywords from the 'Required Skills' section",
            "Add relevant tools and technologies mentioned in the JD"
        ]
        return suggestions
    
    def _suggest_project_improvements(self, resume_text: str) -> List[str]:
        """Suggest improvements for project descriptions"""
        suggestions = [
            "Add quantifiable metrics (e.g., 'improved performance by 30%')",
            "Describe the impact and business value of your projects",
            "Use strong action verbs (Developed, Implemented, Optimized, etc.)",
            "Include technologies and tools used in each project",
            "Mention team size and your specific role/responsibilities"
        ]
        return suggestions
    
    def _suggest_summary_improvements(self, resume_text: str, jd_text: str) -> List[str]:
        """Suggest improvements for resume summary"""
        suggestions = [
            "Create a targeted professional summary matching the JD",
            "Highlight years of experience and key expertise areas",
            "Include 2-3 major achievements with quantifiable results",
            "Align your summary with the job title and role requirements",
            "Keep it concise (2-3 sentences) but impactful"
        ]
        return suggestions
    
    @staticmethod
    def _suggest_ats_optimization(ats_issues: List[str]) -> List[str]:
        """Suggest ATS optimization tips"""
        suggestions = [
            "Use standard font (Arial, Calibri, or Times New Roman)",
            "Avoid tables, graphics, and complex formatting",
            "Include a dedicated 'Skills' section with relevant keywords",
            "Use standard section headers (Experience, Education, Skills, Projects)",
            "Save and submit as PDF to preserve formatting",
            "Keep file size under 5MB",
            "Avoid headers and footers with important information"
        ]
        return suggestions
    
    @staticmethod
    def _suggest_formatting() -> List[str]:
        """Suggest formatting improvements"""
        suggestions = [
            "Use consistent date formats throughout",
            "Align text to the left for better ATS parsing",
            "Use bullet points for easy readability",
            "Maintain 0.5-1 inch margins",
            "Use 10-12 pt font size for body text",
            "Keep it to 1-2 pages maximum",
            "Use clear section dividers"
        ]
        return suggestions
    
    @staticmethod
    def _suggest_industry_specific(jd_text: str) -> List[str]:
        """Suggest industry-specific improvements"""
        suggestions = [
            "Research industry trends and incorporate relevant terminology",
            "Highlight experience with current technologies in your field",
            "Mention certifications relevant to the position",
            "Include metrics relevant to your industry",
            "Showcase problem-solving approach aligned with industry standards"
        ]
        return suggestions
    
    def generate_ai_powered_content(self, text: str, context: str) -> str:
        """
        Generate AI-powered content rewrite (requires API setup)
        
        Args:
            text: Original text to improve
            context: Context for improvement
            
        Returns:
            Improved text
        """
        try:
            if self.api_provider == "google" and self.google_api_key:
                return self._google_ai_rewrite(text, context)
            elif self.api_provider == "openai" and self.openai_api_key:
                return self._openai_rewrite(text, context)
            else:
                return f"Enhanced: {text}"
        except Exception as e:
            print(f"Error generating AI content: {str(e)}")
            return text
    
    def _google_ai_rewrite(self, text: str, context: str) -> str:
        """Rewrite using Google Generative AI"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.google_api_key)
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"""Rewrite the following resume text to be more impactful and ATS-optimized:
            
Original: {text}
Context: {context}

Provide only the rewritten text without explanations."""
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error with Google AI: {str(e)}")
            return text
    
    def _openai_rewrite(self, text: str, context: str) -> str:
        """Rewrite using OpenAI API"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"""Rewrite the following resume text to be more impactful and ATS-optimized:
                        
Original: {text}
Context: {context}

Provide only the rewritten text without explanations."""
                    }
                ]
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error with OpenAI: {str(e)}")
            return text
