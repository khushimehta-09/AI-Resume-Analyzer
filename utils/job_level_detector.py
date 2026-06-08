"""
Job Level Detector
Detects job level from job description
"""

import re

class JobLevelDetector:
    """Detect job level from job description"""
    
    FRESHER_KEYWORDS = [
        'fresher', 'graduate', 'pass out', 'pass-out', 'recent graduate',
        'entry level', 'entry-level', 'no experience', '0 years',
        'junior developer', 'trainee', 'intern', 'internship',
        'newcomer', 'beginner', 'start your career'
    ]
    
    INTERNSHIP_KEYWORDS = [
        'internship', 'intern', 'summer intern', 'winter intern',
        'co-op', 'apprenticeship'
    ]
    
    JUNIOR_KEYWORDS = [
        'junior', 'entry level', 'entry-level', '1-2 years',
        '1+ years', '2 years', 'junior developer'
    ]
    
    MID_LEVEL_KEYWORDS = [
        'mid-level', 'mid level', '3-5 years', '3+ years',
        '4-5 years', 'senior developer', 'lead', 'architect'
    ]
    
    SENIOR_KEYWORDS = [
        'senior', '5+ years', '6+ years', '7+ years',
        'principal', 'staff', 'lead', 'technical lead',
        'architect', 'lead engineer', 'staff engineer'
    ]
    
    @staticmethod
    def detect_level(job_description):
        """
        Detect job level from JD
        
        Args:
            job_description: Job description text
            
        Returns:
            Dictionary with level and confidence
        """
        jd_lower = job_description.lower()
        
        # Count keyword matches
        fresher_count = sum(1 for kw in JobLevelDetector.FRESHER_KEYWORDS if kw in jd_lower)
        internship_count = sum(1 for kw in JobLevelDetector.INTERNSHIP_KEYWORDS if kw in jd_lower)
        junior_count = sum(1 for kw in JobLevelDetector.JUNIOR_KEYWORDS if kw in jd_lower)
        mid_count = sum(1 for kw in JobLevelDetector.MID_LEVEL_KEYWORDS if kw in jd_lower)
        senior_count = sum(1 for kw in JobLevelDetector.SENIOR_KEYWORDS if kw in jd_lower)
        
        counts = {
            'Fresher': fresher_count,
            'Internship': internship_count,
            'Junior': junior_count,
            'Mid-Level': mid_count,
            'Senior': senior_count
        }
        
        # Find the level with highest count
        max_level = max(counts, key=counts.get)
        max_count = counts[max_level]
        
        # If no clear match, default to Junior
        if max_count == 0:
            return {
                'level': 'Junior',
                'confidence': 'low',
                'reason': 'No specific level indicators found'
            }
        
        confidence = 'high' if max_count >= 2 else 'medium' if max_count == 1 else 'low'
        
        return {
            'level': max_level,
            'confidence': confidence,
            'keyword_count': max_count
        }
    
    @staticmethod
    def is_fresher_role(job_description):
        """
        Check if job is for freshers
        
        Args:
            job_description: Job description text
            
        Returns:
            True if fresher role, False otherwise
        """
        result = JobLevelDetector.detect_level(job_description)
        return result['level'] in ['Fresher', 'Internship']
    
    @staticmethod
    def get_expected_experience(job_description):
        """
        Extract expected years of experience
        
        Args:
            job_description: Job description text
            
        Returns:
            Tuple of (min_years, max_years)
        """
        # Pattern: "X+ years", "X-Y years"
        pattern = r'(\d+)[\s+]*(?:to|-)\s*(\d+)\s*years|([\d]+)\s*\+\s*years'
        matches = re.findall(pattern, job_description.lower())
        
        if matches:
            for match in matches:
                if match[0] and match[1]:  # Range format
                    return (int(match[0]), int(match[1]))
                elif match[2]:  # Plus format
                    return (int(match[2]), None)
        
        return (0, None)
