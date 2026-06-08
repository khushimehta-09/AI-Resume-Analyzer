"""
Similarity and Matching Module - Enhanced
Calculates resume-JD match score using intelligent NLP techniques
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Tuple, List, Dict
import re

class SimilarityMatcher:
    """Calculate similarity between resume and job description"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and preprocess text
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.lower().strip()
    
    @staticmethod
    def calculate_tfidf_similarity(resume_text: str, jd_text: str) -> float:
        """
        Calculate TF-IDF based cosine similarity
        
        Args:
            resume_text: Resume text
            jd_text: Job description text
            
        Returns:
            Similarity score (0-100)
        """
        try:
            resume_clean = SimilarityMatcher.clean_text(resume_text)
            jd_clean = SimilarityMatcher.clean_text(jd_text)
            
            vectorizer = TfidfVectorizer(
                max_features=1000,
                ngram_range=(1, 2),
                min_df=1
            )
            
            tfidf_matrix = vectorizer.fit_transform([resume_clean, jd_clean])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return round(similarity * 100, 2)
        except Exception as e:
            print(f"Error calculating TF-IDF similarity: {str(e)}")
            return 0.0
    
    @staticmethod
    def calculate_keyword_match_score(resume_text: str, jd_text: str) -> float:
        """
        Calculate match score based on keyword overlap
        
        Args:
            resume_text: Resume text
            jd_text: Job description text
            
        Returns:
            Match score (0-100)
        """
        try:
            resume_lower = resume_text.lower()
            jd_lower = jd_text.lower()
            
            resume_words = set(re.findall(r'\b\w+\b', resume_lower))
            jd_words = set(re.findall(r'\b\w+\b', jd_lower))
            
            stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
                'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are',
                'was', 'be', 'been', 'have', 'has', 'do', 'does', 'did',
                'will', 'would', 'could', 'should', 'may', 'might', 'can'
            }
            
            resume_words -= stop_words
            jd_words -= stop_words
            
            if not jd_words:
                return 0.0
            
            intersection = len(resume_words & jd_words)
            union = len(resume_words | jd_words)
            
            jaccard_similarity = intersection / union if union > 0 else 0
            
            return round(jaccard_similarity * 100, 2)
        except Exception as e:
            print(f"Error calculating keyword match score: {str(e)}")
            return 0.0
    
    @staticmethod
    def calculate_section_match(resume_text: str, jd_text: str) -> Dict[str, float]:
        """
        Calculate match score for different sections
        
        Args:
            resume_text: Resume text
            jd_text: Job description text
            
        Returns:
            Dictionary with section-wise match scores
        """
        sections = {
            "Overall": SimilarityMatcher.calculate_tfidf_similarity(resume_text, jd_text),
            "Keywords": SimilarityMatcher.calculate_keyword_match_score(resume_text, jd_text),
        }
        
        return sections
    
    @staticmethod
    def calculate_combined_score(resume_text: str, jd_text: str,
                                resume_skills: List[str],
                                jd_skills: List[str]) -> Dict:
        """
        Calculate combined match score with intelligent weighting
        
        Args:
            resume_text: Resume text
            jd_text: Job description text
            resume_skills: Skills found in resume
            jd_skills: Skills found in JD
            
        Returns:
            Dictionary with comprehensive match analysis
        """
        tfidf_score = SimilarityMatcher.calculate_tfidf_similarity(resume_text, jd_text)
        keyword_score = SimilarityMatcher.calculate_keyword_match_score(resume_text, jd_text)
        
        resume_skills_lower = set(s.lower() for s in resume_skills)
        jd_skills_lower = set(s.lower() for s in jd_skills)
        
        if jd_skills_lower:
            skill_match = len(resume_skills_lower & jd_skills_lower) / len(jd_skills_lower)
            skill_score = skill_match * 100
        else:
            skill_score = 0.0
        
        # Intelligent weighting - balance text and skill matching
        final_score = (tfidf_score * 0.3 + keyword_score * 0.2 + skill_score * 0.5)
        
        return {
            "overall_match_score": round(final_score, 2),
            "tfidf_score": tfidf_score,
            "keyword_score": keyword_score,
            "skill_match_score": round(skill_score, 2),
            "skills_matched": len(resume_skills_lower & jd_skills_lower),
            "total_jd_skills": len(jd_skills_lower),
            "match_percentage": f"{round(final_score, 1)}%"
        }
