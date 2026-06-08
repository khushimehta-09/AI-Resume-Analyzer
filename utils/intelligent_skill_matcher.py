"""
Intelligent Skill Matcher
Maps and matches skills intelligently using synonyms and categories
"""

from .skill_synonyms import (
    normalize_skill, get_skill_category, is_related_skill,
    SKILL_SYNONYMS, SKILL_CATEGORIES
)
from typing import Dict, List, Tuple

class IntelligentSkillMatcher:
    """Match skills intelligently considering synonyms and categories"""
    
    def __init__(self):
        self.skill_synonyms = SKILL_SYNONYMS
        self.skill_categories = SKILL_CATEGORIES
    
    def match_skills(self, resume_skills, jd_skills):
        """
        Match resume skills with JD skills
        
        Args:
            resume_skills: List of skills from resume
            jd_skills: List of skills from JD
            
        Returns:
            Dictionary with matched, partial, and missing skills
        """
        # Normalize all skills
        resume_normalized = [normalize_skill(s) for s in resume_skills]
        jd_normalized = [normalize_skill(s) for s in jd_skills]
        
        # Remove duplicates
        resume_set = set(resume_normalized)
        jd_set = set(jd_normalized)
        
        matched = set()
        partial_matches = {}
        missing = set()
        
        for jd_skill in jd_set:
            if jd_skill in resume_set:
                matched.add(jd_skill)
            else:
                # Check for category-level matches
                category = get_skill_category(jd_skill)
                category_matches = [s for s in resume_set if get_skill_category(s) == category]
                
                if category_matches:
                    partial_matches[jd_skill] = category_matches
                else:
                    missing.add(jd_skill)
        
        return {
            'matched': list(matched),
            'partial_matches': partial_matches,
            'missing': list(missing),
            'match_count': len(matched),
            'partial_count': len(partial_matches),
            'missing_count': len(missing)
        }
    
    def get_skill_priority(self, skill):
        """
        Get priority level of a skill
        
        Args:
            skill: Skill name
            
        Returns:
            Priority level: 'high', 'medium', 'low'
        """
        category = get_skill_category(skill)
        if category:
            return self.skill_categories[category].get('priority', 'low')
        return 'low'
    
    def categorize_skills(self, skills):
        """
        Categorize skills by type
        
        Args:
            skills: List of skills
            
        Returns:
            Dictionary with skills grouped by category
        """
        categorized = {}
        uncategorized = []
        
        for skill in skills:
            normalized = normalize_skill(skill)
            category = get_skill_category(normalized)
            
            if category:
                if category not in categorized:
                    categorized[category] = []
                categorized[category].append(normalized)
            else:
                uncategorized.append(normalized)
        
        if uncategorized:
            categorized['Other'] = uncategorized
        
        return categorized
    
    def get_high_priority_missing_skills(self, all_missing_skills, max_skills=5):
        """
        Get high-priority missing skills only
        
        Args:
            all_missing_skills: List of all missing skills
            max_skills: Maximum number of skills to return
            
        Returns:
            List of high-priority missing skills
        """
        # Prioritize based on skill priority
        prioritized = []
        
        for skill in all_missing_skills:
            priority = self.get_skill_priority(skill)
            if priority == 'high':
                prioritized.append((skill, 0))  # 0 = highest priority
            elif priority == 'medium':
                prioritized.append((skill, 1))
            else:
                prioritized.append((skill, 2))
        
        # Sort by priority
        prioritized.sort(key=lambda x: x[1])
        
        # Return only the top N
        return [skill for skill, _ in prioritized[:max_skills]]
    
    def calculate_category_match_score(self, resume_skills, jd_skills):
        """
        Calculate match score by category
        
        Args:
            resume_skills: List of resume skills
            jd_skills: List of JD skills
            
        Returns:
            Dictionary with per-category scores
        """
        # Normalize and categorize
        resume_normalized = [normalize_skill(s) for s in resume_skills]
        jd_normalized = [normalize_skill(s) for s in jd_skills]
        
        resume_set = set(resume_normalized)
        jd_set = set(jd_normalized)
        
        # Group JD skills by category
        category_scores = {}
        
        for category in self.skill_categories:
            category_skills = self.skill_categories[category]['skills']
            
            # Find JD skills in this category
            jd_cat_skills = [s for s in jd_set if s in category_skills]
            
            if jd_cat_skills:
                # Find matches in resume
                matched = [s for s in jd_cat_skills if s in resume_set]
                
                # Calculate score
                score = (len(matched) / len(jd_cat_skills)) * 100
                category_scores[category] = {
                    'score': score,
                    'matched': len(matched),
                    'required': len(jd_cat_skills),
                    'weight': self.skill_categories[category]['weight']
                }
        
        return category_scores
