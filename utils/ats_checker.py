"""
ATS Checker Module - Enhanced
Analyzes resume for ATS (Applicant Tracking System) compatibility with improved detection
"""

import re
from typing import Dict, List

class ATSChecker:
    """Enhanced ATS compatibility checker with better detection"""
    
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
        
        # Check for phone number (flexible)
        phone_pattern = r'\+?[0-9\s\-()]{10,}'
        has_phone = bool(re.search(phone_pattern, resume_text))
        if has_phone:
            score += 25
        else:
            issues.append("Missing phone number")
        
        # Check for LinkedIn URL
        linkedin_pattern = r'linkedin\.com|linkedin'
        has_linkedin = bool(re.search(linkedin_pattern, resume_text, re.IGNORECASE))
        if has_linkedin:
            score += 25
        else:
            pass  # LinkedIn is optional
        
        # Check for GitHub
        github_pattern = r'github\.com|github'
        has_github = bool(re.search(github_pattern, resume_text, re.IGNORECASE))
        if has_github:
            score += 15
        
        # Check for location (improved detection)
        location_pattern = r'\b(?:Delhi|Mumbai|Bangalore|Hyderabad|Pune|Chennai|Kolkata|Ahmedabad|Jaipur|Lucknow|USA|UK|Canada|Australia|Singapore|Berlin|London|New York|San Francisco|Remote)\b'
        has_location = bool(re.search(location_pattern, resume_text, re.IGNORECASE))
        if has_location:
            score += 10
        
        return {
            "score": min(score, 100),
            "has_email": has_email,
            "has_phone": has_phone,
            "has_linkedin": has_linkedin,
            "has_github": has_github,
            "has_location": has_location,
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
        
        # Check for simple formatting
        fancy_chars = len(re.findall(r'[^\x00-\x7F]', resume_text))
        if fancy_chars <= 5:
            score += 30
        else:
            issues.append(f"Contains {fancy_chars} special characters (may cause ATS issues)")
        
        # Check for section headers (improved detection)
        section_keywords = ['experience', 'education', 'skills', 'project', 'summary', 'work']
        found_sections = sum(1 for keyword in section_keywords 
                           if re.search(rf'\b{keyword}\b', resume_text, re.IGNORECASE))
        
        section_score = (found_sections / len(section_keywords)) * 40
        score += section_score
        
        if found_sections < 3:
            issues.append("Missing important sections (Experience, Education, Skills)")
        
        # Check for tables or complex formatting
        if '<' not in resume_text and '{' not in resume_text and '|' not in resume_text:
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
            'increased', 'decreased', 'analyzed', 'demonstrated', 'achieved',
            'built', 'deployed', 'tested', 'automated', 'integrated'
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
        
        # Check for industry keywords
        if jd_text:
            jd_keywords = re.findall(r'\b[a-z]{4,}\b', jd_text.lower())
            resume_keywords = re.findall(r'\b[a-z]{4,}\b', resume_text.lower())
            
            if jd_keywords:
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
        Calculate overall ATS score with balanced weighting
        
        Args:
            resume_text: Resume text
            jd_text: Job description text (optional)
            
        Returns:
            Comprehensive ATS analysis
        """
        contact_info = ATSChecker.check_contact_information(resume_text)
        formatting = ATSChecker.check_formatting(resume_text)
        keywords = ATSChecker.check_keyword_density(resume_text, jd_text)
        
        # Balanced weighted average
        overall_score = (
            contact_info["score"] * 0.25 +
            formatting["score"] * 0.25 +
            keywords["score"] * 0.50
        )
        
        all_issues = (
            contact_info.get("issues", []) +
            formatting.get("issues", []) +
            keywords.get("issues", [])
        )
        
        return {
            "overall_ats_score": round(overall_score),
            "contact_information_score": round(contact_info["score"]),
            "formatting_score": round(formatting["score"]),
            "keyword_optimization_score": round(keywords["score"]),
            "breakdown": {
                "Contact Information": round(contact_info["score"]),
                "Formatting": round(formatting["score"]),
                "Keywords & Content": round(keywords["score"])
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
            suggestions.append("✓ Add complete contact information (email, phone, LinkedIn)")
        
        if ats_analysis["formatting_score"] < 75:
            suggestions.append("✓ Use simple formatting (avoid tables, graphics, and special characters)")
        
        if ats_analysis["keyword_optimization_score"] < 75:
            suggestions.append("✓ Include a dedicated Skills section")
            suggestions.append("✓ Use more action verbs (Developed, Implemented, Managed, etc.)")
            suggestions.append("✓ Add quantifiable metrics to your achievements")
        
        if not suggestions:
            suggestions.append("✓ Your resume is well-optimized for ATS!")
        
        return suggestions
