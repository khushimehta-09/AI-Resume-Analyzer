"""
Enhanced ATS Checker
Improved ATS compatibility checking
"""

import re

class EnhancedATSChecker:
    """Enhanced ATS compatibility checker with better detection"""
    
    def __init__(self):
        self.issues = []
        self.scores = {}
    
    def calculate_ats_score(self, resume_text, jd_text=""):
        """
        Calculate comprehensive ATS score
        
        Args:
            resume_text: Resume text
            jd_text: Job description text (optional)
            
        Returns:
            Dictionary with ATS scores and issues
        """
        self.issues = []
        
        # Check each component
        contact_score = self._check_contact_info(resume_text)
        formatting_score = self._check_formatting(resume_text)
        structure_score = self._check_structure(resume_text)
        keyword_score = self._check_keywords(resume_text, jd_text)
        
        # Calculate overall
        overall_score = (
            contact_score * 0.25 +
            formatting_score * 0.25 +
            structure_score * 0.25 +
            keyword_score * 0.25
        )
        
        return {
            'overall_ats_score': round(overall_score),
            'contact_information_score': round(contact_score),
            'formatting_score': round(formatting_score),
            'structure_score': round(structure_score),
            'keyword_optimization_score': round(keyword_score),
            'issues': self.issues,
            'recommendation': self._get_recommendation(overall_score)
        }
    
    def _check_contact_info(self, resume_text):
        """
        Check for contact information
        
        Returns:
            Score 0-100
        """
        score = 100
        found_contact = 0
        
        # Check for email
        if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resume_text):
            found_contact += 1
        else:
            self.issues.append("No email address found")
            score -= 25
        
        # Check for phone
        if re.search(r'\+?[0-9\s\-()]{10,}', resume_text):
            found_contact += 1
        else:
            self.issues.append("No phone number found")
            score -= 25
        
        # Check for location/city
        if re.search(r'\b(?:Delhi|Mumbai|Bangalore|Hyderabad|Pune|Chennai|Kolkata|Ahmedabad|Jaipur|Lucknow|USA|UK|Canada|Australia|Singapore|Berlin|London|New York|San Francisco|Remote)\b', resume_text, re.IGNORECASE):
            found_contact += 1
        else:
            self.issues.append("Location information unclear")
            score -= 15
        
        # Check for LinkedIn/GitHub
        if re.search(r'linkedin\.com/in|github\.com/|github\.io', resume_text, re.IGNORECASE):
            found_contact += 1
        else:
            # Not critical
            pass
        
        return max(0, min(100, score))
    
    def _check_formatting(self, resume_text):
        """
        Check resume formatting
        
        Returns:
            Score 0-100
        """
        score = 100
        
        # Check for excessive symbols/emojis
        emoji_count = len([c for c in resume_text if ord(c) > 127])
        if emoji_count > 5:
            score -= 30
            self.issues.append("Too many special characters/emojis detected")
        
        # Check line length (should be readable)
        lines = resume_text.split('\n')
        very_long_lines = sum(1 for line in lines if len(line) > 200)
        if very_long_lines > 5:
            score -= 15
            self.issues.append("Some lines are too long (may cause formatting issues)")
        
        # Check for consistent spacing
        if resume_text.count('\n\n') < 5:  # Should have some section breaks
            score -= 10
            self.issues.append("Consider using section breaks for better readability")
        
        return max(0, min(100, score))
    
    def _check_structure(self, resume_text):
        """
        Check resume structure and sections
        
        Returns:
            Score 0-100
        """
        score = 100
        text_lower = resume_text.lower()
        
        # Check for common sections
        sections = {
            'experience': ['experience', 'work experience', 'professional experience'],
            'education': ['education', 'academic', 'degree'],
            'skills': ['skills', 'technical skills', 'competencies'],
            'projects': ['projects', 'work', 'portfolio']
        }
        
        found_sections = 0
        for section, keywords in sections.items():
            if any(kw in text_lower for kw in keywords):
                found_sections += 1
            else:
                if section in ['experience', 'education', 'skills']:
                    self.issues.append(f"Missing '{section}' section")
                    score -= 20
        
        # Projects section is optional
        if found_sections < 3:
            score -= 10
        
        return max(0, min(100, score))
    
    def _check_keywords(self, resume_text, jd_text=""):
        """
        Check keyword optimization
        
        Returns:
            Score 0-100
        """
        score = 80  # Default good score
        
        # Extract keywords from JD if provided
        if jd_text:
            # Look for technical terms
            technical_terms = ['python', 'java', 'javascript', 'sql', 'aws', 'docker',
                             'api', 'database', 'react', 'node', 'git', 'linux']
            
            resume_lower = resume_text.lower()
            found_terms = sum(1 for term in technical_terms if term in resume_lower)
            
            if found_terms >= 5:
                score = 95
            elif found_terms >= 3:
                score = 85
            else:
                score = 70
                self.issues.append("Limited technical keywords found")
        
        return max(0, min(100, score))
    
    def _get_recommendation(self, score):
        """
        Get ATS recommendation based on score
        """
        if score >= 90:
            return "Excellent ATS compatibility"
        elif score >= 75:
            return "Good ATS compatibility"
        elif score >= 60:
            return "Moderate ATS compatibility - consider improvements"
        else:
            return "Poor ATS compatibility - needs significant improvements"
