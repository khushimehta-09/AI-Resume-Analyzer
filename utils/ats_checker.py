"""
ATS Checker Module
Analyzes resume for ATS (Applicant Tracking System) compatibility
"""

import re
from typing import Dict, List, Tuple


class ATSChecker:
    """Check resume for ATS compatibility"""
    
    @staticmethod
    def check_contact_information(resume_text: str) -> Dict:
        """
        Check if resume contains proper contact information
        
        Args:
            resume_text: Resume text
            
        Returns:
            Analysis of contact information
        """
        score = 0
        issues = []
        
        # Check for email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        has_email = bool(re.search(email_pattern, resume_text))
        if has_email:
            score += 25
        else:
            issues.append("Missing email address")
        
        # Check for phone number
        phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b'
        has_phone = bool(re.search(phone_pattern, resume_text))
        if has_phone:
            score += 25
        else:
            issues.append("Missing phone number")
        
        # Check for LinkedIn URL
        linkedin_pattern = r'linkedin\.com'
        has_linkedin = bool(re.search(linkedin_pattern, resume_text, re.IGNORECASE))
        if has_linkedin:
            score += 25
        else:
            issues.append("Missing LinkedIn profile")
        
        # Check for location
        if re.search(r'\b(city|state|country|location)\b', resume_text, re.IGNORECASE):
            score += 25
        else:
            issues.append("Missing location information")
        
        return {
            "score": score,
            "has_email": has_email,
            "has_phone": has_phone,
            "has_linkedin": has_linkedin,
            "issues": issues
        }
    
    @staticmethod
    def check_formatting(resume_text: str) -> Dict:
        """
        Check if resume is properly formatted for ATS
        
        Args:
            resume_text: Resume text
            
        Returns:
            Formatting analysis
        """
        score = 0
        issues = []
        
        # Check for simple formatting (no fancy characters)
        fancy_chars = len(re.findall(r'[^\x00-\x7F]', resume_text))
        if fancy_chars == 0:
            score += 30
        else:
            issues.append(f"Contains {fancy_chars} non-ASCII characters (may cause ATS issues)")
        
        # Check for section headers
        section_keywords = ['experience', 'education', 'skills', 'project', 'summary']
        found_sections = sum(1 for keyword in section_keywords 
                           if re.search(rf'\b{keyword}\b', resume_text, re.IGNORECASE))
        
        section_score = (found_sections / len(section_keywords)) * 40
        score += section_score
        
        if found_sections < 3:
            issues.append("Missing important sections (Experience, Education, Skills)")
        
        # Check for tables or complex formatting indicators
        if '<' not in resume_text and '{' not in resume_text:
            score += 30
        else:
            issues.append("May contain HTML/complex formatting that ATS cannot parse")
        
        return {
            "score": min(score, 100),
            "section_count": found_sections,
            "issues": issues
        }
    
    @staticmethod
    def check_keyword_density(resume_text: str, jd_text: str = None) -> Dict:
        """
        Check keyword density and optimization
        
        Args:
            resume_text: Resume text
            jd_text: Job description text (optional)
            
        Returns:
            Keyword analysis
        """
        score = 0
        issues = []
        
        # Check for skills section
        if re.search(r'\b(skills?|technical|competencies)\b', resume_text, re.IGNORECASE):
            score += 20
        else:
            issues.append("No dedicated Skills section found")
        
        # Check for action verbs
        action_verbs = [
            'developed', 'designed', 'implemented', 'managed', 'led',
            'created', 'built', 'improved', 'optimized', 'enhanced',
            'increased', 'decreased', 'analyzed', 'demonstrated', 'achieved'
        ]
        
        verb_count = sum(1 for verb in action_verbs 
                        if re.search(rf'\b{verb}\b', resume_text, re.IGNORECASE))
        
        verb_score = min((verb_count / len(action_verbs)) * 30, 30)
        score += verb_score
        
        if verb_count < 5:
            issues.append("Resume lacks strong action verbs")
        
        # Check for quantifiable results
        numbers = re.findall(r'\b\d+[%$KM]?\b', resume_text)
        if len(numbers) >= 3:
            score += 20
        else:
            issues.append("Add more quantifiable achievements (numbers, percentages)")
        
        # Check for industry keywords if JD provided
        if jd_text:
            jd_keywords = re.findall(r'\b[a-z]{4,}\b', jd_text.lower())
            resume_keywords = re.findall(r'\b[a-z]{4,}\b', resume_text.lower())
            
            keyword_match = len(set(jd_keywords) & set(resume_keywords))
            keyword_score = min((keyword_match / max(len(set(jd_keywords)), 1)) * 30, 30)
            score += keyword_score
        else:
            score += 20
        
        return {
            "score": min(score, 100),
            "action_verb_count": verb_count,
            "quantifiable_results": len(numbers),
            "issues": issues
        }
    
    @staticmethod
    def calculate_ats_score(resume_text: str, jd_text: str = None) -> Dict:
        """
        Calculate overall ATS score
        
        Args:
            resume_text: Resume text
            jd_text: Job description text (optional)
            
        Returns:
            Comprehensive ATS analysis
        """
        contact_info = ATSChecker.check_contact_information(resume_text)
        formatting = ATSChecker.check_formatting(resume_text)
        keywords = ATSChecker.check_keyword_density(resume_text, jd_text)
        
        # Weighted average
        overall_score = (
            contact_info["score"] * 0.3 +
            formatting["score"] * 0.3 +
            keywords["score"] * 0.4
        )
        
        all_issues = (
            contact_info.get("issues", []) +
            formatting.get("issues", []) +
            keywords.get("issues", [])
        )
        
        return {
            "overall_ats_score": round(overall_score, 2),
            "contact_information_score": contact_info["score"],
            "formatting_score": round(formatting["score"], 2),
            "keyword_optimization_score": round(keywords["score"], 2),
            "breakdown": {
                "Contact Information": contact_info["score"],
                "Formatting": round(formatting["score"], 2),
                "Keywords & Content": round(keywords["score"], 2)
            },
            "issues": list(set(all_issues)),
            "action_verbs_count": keywords.get("action_verb_count", 0),
            "quantifiable_results": keywords.get("quantifiable_results", 0)
        }
    
    @staticmethod
    def get_improvement_suggestions(ats_analysis: Dict) -> List[str]:
        """
        Generate improvement suggestions based on ATS analysis
        
        Args:
            ats_analysis: ATS analysis dictionary
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        if ats_analysis["contact_information_score"] < 75:
            suggestions.append("✓ Add complete contact information (email, phone, LinkedIn, location)")
        
        if ats_analysis["formatting_score"] < 75:
            suggestions.append("✓ Use simple formatting (avoid tables, graphics, and special characters)")
        
        if ats_analysis["keyword_optimization_score"] < 75:
            suggestions.append("✓ Include a dedicated Skills section")
            suggestions.append("✓ Use more action verbs (Developed, Implemented, Managed, etc.)")
            suggestions.append("✓ Add quantifiable metrics to your achievements")
        
        if not suggestions:
            suggestions.append("✓ Your resume is well-optimized for ATS!")
        
        return suggestions
