"""
Recruiter Scorer
Calculates intelligent recruitment-style scores
"""

from .job_level_detector import JobLevelDetector
from .intelligent_skill_matcher import IntelligentSkillMatcher
from .skill_synonyms import normalize_skill
from typing import Dict, List

class RecruiterScorer:
    """Calculate recruiter-style match scores"""
    
    def __init__(self):
        self.skill_matcher = IntelligentSkillMatcher()
        self.job_level_detector = JobLevelDetector()
    
    def calculate_overall_score(self, resume_data, jd_data):
        """
        Calculate overall match score (40% skill, 20% project, 15% education, 15% AI tools, 10% ATS)
        
        Args:
            resume_data: Dictionary with resume information
            jd_data: Dictionary with job description information
            
        Returns:
            Overall score and breakdown
        """
        # Detect job level
        job_level = self.job_level_detector.detect_level(jd_data.get('raw_jd', ''))
        is_fresher_role = job_level['level'] in ['Fresher', 'Internship']
        
        # Calculate component scores
        skill_score = self._calculate_skill_score(
            resume_data.get('skills', []),
            jd_data.get('skills', []),
            is_fresher_role
        )
        
        project_score = self._calculate_project_score(
            resume_data.get('projects', []),
            jd_data.get('keywords', []),
            is_fresher_role
        )
        
        education_score = self._calculate_education_score(
            resume_data.get('education', []),
            is_fresher_role
        )
        
        ai_tools_score = self._calculate_ai_tools_score(
            resume_data.get('skills', []),
            is_fresher_role
        )
        
        ats_score = resume_data.get('ats_score', 70)
        
        # Apply weights
        if is_fresher_role:
            # For freshers, projects and learning ability are more important
            weights = {
                'skill': 0.25,
                'project': 0.30,
                'education': 0.15,
                'ai_tools': 0.20,
                'ats': 0.10
            }
        else:
            # For experienced, skills are more important
            weights = {
                'skill': 0.40,
                'project': 0.15,
                'education': 0.10,
                'ai_tools': 0.15,
                'ats': 0.10
            }
        
        # Calculate overall
        overall_score = (
            skill_score * weights['skill'] +
            project_score * weights['project'] +
            education_score * weights['education'] +
            ai_tools_score * weights['ai_tools'] +
            ats_score * weights['ats']
        )
        
        return {
            'overall_score': round(overall_score),
            'skill_score': round(skill_score),
            'project_score': round(project_score),
            'education_score': round(education_score),
            'ai_tools_score': round(ai_tools_score),
            'ats_score': round(ats_score),
            'weights': weights,
            'job_level': job_level,
            'is_fresher_role': is_fresher_role,
            'breakdown': {
                'skill': f"{round(skill_score)}% × {weights['skill']:.0%}",
                'project': f"{round(project_score)}% × {weights['project']:.0%}",
                'education': f"{round(education_score)}% × {weights['education']:.0%}",
                'ai_tools': f"{round(ai_tools_score)}% × {weights['ai_tools']:.0%}",
                'ats': f"{round(ats_score)}% × {weights['ats']:.0%}"
            }
        }
    
    def _calculate_skill_score(self, resume_skills, jd_skills, is_fresher=False):
        """
        Calculate skill match score (intelligent matching)
        
        Args:
            resume_skills: List of resume skills
            jd_skills: List of JD skills
            is_fresher: Whether this is a fresher role
            
        Returns:
            Skill match score (0-100)
        """
        if not jd_skills:
            return 100
        
        match_result = self.skill_matcher.match_skills(resume_skills, jd_skills)
        
        matched = match_result['match_count']
        partial = match_result['partial_count']
        missing = match_result['missing_count']
        total = len(jd_skills)
        
        # For freshers, be more lenient
        if is_fresher:
            # Full match = 100 points, partial = 60 points, missing = 0 points
            score = ((matched * 100) + (partial * 60)) / total
        else:
            # Full match = 100 points, partial = 50 points, missing = 0 points
            score = ((matched * 100) + (partial * 50)) / total
        
        return min(100, max(0, score))
    
    def _calculate_project_score(self, projects, jd_keywords, is_fresher=False):
        """
        Calculate project relevance score
        
        Args:
            projects: List of projects with descriptions
            jd_keywords: Keywords from JD
            is_fresher: Whether this is a fresher role
            
        Returns:
            Project relevance score (0-100)
        """
        if not projects:
            return 50 if is_fresher else 30  # Freshers without projects get partial credit
        
        # Score based on number and relevance of projects
        base_score = min(100, len(projects) * 25)
        
        # Check relevance
        relevant_projects = 0
        if jd_keywords:
            jd_keywords_lower = [k.lower() for k in jd_keywords]
            for project in projects:
                project_text = (project.get('title', '') + ' ' + project.get('description', '')).lower()
                if any(kw in project_text for kw in jd_keywords_lower):
                    relevant_projects += 1
        
        # Adjust based on relevance
        if projects:
            relevance_bonus = (relevant_projects / len(projects)) * 30
        else:
            relevance_bonus = 0
        
        return min(100, base_score + relevance_bonus)
    
    def _calculate_education_score(self, education, is_fresher=False):
        """
        Calculate education match score
        
        Args:
            education: List of education entries
            is_fresher: Whether this is a fresher role
            
        Returns:
            Education score (0-100)
        """
        if not education:
            return 40 if is_fresher else 50
        
        score = 70  # Base score for having education
        
        # Bonus for higher education
        for edu_entry in education:
            degree = edu_entry.get('degree', '').lower()
            if 'bachelor' in degree or 'b.tech' in degree or 'b.e' in degree:
                score += 10
            elif 'master' in degree or 'm.tech' in degree:
                score += 20
        
        return min(100, score)
    
    def _calculate_ai_tools_score(self, resume_skills, is_fresher=False):
        """
        Calculate AI tools exposure score
        
        Args:
            resume_skills: List of resume skills
            is_fresher: Whether this is a fresher role
            
        Returns:
            AI tools score (0-100)
        """
        # Check for AI tool usage
        ai_tools = ['chatgpt', 'gemini', 'copilot', 'ai tools', 'machine learning', 'tensorflow', 'pytorch']
        
        resume_skills_lower = [normalize_skill(s) for s in resume_skills]
        ai_tool_count = sum(1 for skill in resume_skills_lower if any(tool in skill for tool in ai_tools))
        
        # Score based on AI tool presence
        if ai_tool_count > 0:
            return min(100, 70 + (ai_tool_count * 10))
        else:
            return 40 if is_fresher else 50  # Freshers without AI tools get partial credit
    
    def generate_recruiter_verdict(self, overall_score, job_level, strong_matches, missing_skills):
        """
        Generate a recruiter-style verdict
        
        Args:
            overall_score: Overall match score
            job_level: Detected job level
            strong_matches: List of strong matching skills
            missing_skills: List of missing skills
            
        Returns:
            Recruiter verdict text
        """
        level = job_level.get('level', 'Junior')
        
        if overall_score >= 85:
            strength = "excellent"
            recommendation = f"Highly recommended for {level} role"
        elif overall_score >= 70:
            strength = "good"
            recommendation = f"Strong candidate for {level} role"
        elif overall_score >= 50:
            strength = "moderate"
            recommendation = f"Suitable for {level} role with focused learning"
        else:
            strength = "limited"
            recommendation = f"May need additional skills for {level} role"
        
        verdict = f"This candidate is a {strength} match for a {level} software developer role."
        
        if strong_matches:
            verdict += f" Demonstrates strong knowledge in {', '.join(strong_matches[:2])}."
        
        if missing_skills:
            verdict += f" Should focus on learning {', '.join(missing_skills[:2])}."
        
        if overall_score >= 70:
            verdict += " Good interview candidate."
        
        return verdict
