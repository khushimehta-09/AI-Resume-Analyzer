"""
Skill Extractor Module
Extracts technical and soft skills from resume and JD
"""

import json
import re
from typing import List, Dict, Set
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords


class SkillExtractor:
    """Extract technical and soft skills from text"""
    
    def __init__(self):
        """Initialize skill extractor with skill database"""
        self.technical_skills = self._load_technical_skills()
        self.soft_skills = self._load_soft_skills()
    
    @staticmethod
    def _load_technical_skills() -> Dict[str, List[str]]:
        """Load technical skills database"""
        return {
            "Programming Languages": [
                "Python", "Java", "C++", "C#", "JavaScript", "TypeScript",
                "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin", "Scala",
                "R", "MATLAB", "SQL", "HTML", "CSS", "Bash", "Shell"
            ],
            "Web Frameworks": [
                "React", "Angular", "Vue.js", "Django", "Flask", "FastAPI",
                "Express.js", "Spring", "ASP.NET", "Node.js", "Nest.js",
                "Laravel", "Ruby on Rails", "Next.js"
            ],
            "Databases": [
                "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra",
                "Firebase", "DynamoDB", "Oracle", "SQL Server", "SQLite",
                "Elasticsearch", "Neo4j", "CouchDB"
            ],
            "Cloud Platforms": [
                "AWS", "Azure", "Google Cloud", "GCP", "Heroku", "DigitalOcean",
                "Alibaba Cloud", "IBM Cloud", "Oracle Cloud"
            ],
            "DevOps & Tools": [
                "Docker", "Kubernetes", "Jenkins", "GitHub Actions", "GitLab CI",
                "Terraform", "Ansible", "Prometheus", "Grafana", "ELK Stack",
                "Git", "SVN", "Jira", "Confluence"
            ],
            "Data Science": [
                "Machine Learning", "TensorFlow", "PyTorch", "Scikit-learn",
                "Pandas", "NumPy", "Matplotlib", "Seaborn", "Keras",
                "XGBoost", "Spark", "Hadoop", "Big Data"
            ],
            "Mobile Development": [
                "iOS", "Android", "React Native", "Flutter", "Xamarin",
                "Swift", "Kotlin", "Objective-C"
            ],
            "Other Tools": [
                "Git", "Linux", "Windows", "macOS", "API", "REST",
                "GraphQL", "SOAP", "JWT", "OAuth", "Agile", "Scrum",
                "CI/CD", "Microservices", "AWS", "SSL/TLS"
            ]
        }
    
    @staticmethod
    def _load_soft_skills() -> List[str]:
        """Load soft skills database"""
        return [
            "Communication", "Leadership", "Teamwork", "Problem Solving",
            "Critical Thinking", "Creativity", "Time Management",
            "Organization", "Adaptability", "Collaboration", "Project Management",
            "Customer Service", "Negotiation", "Presentation", "Writing",
            "Public Speaking", "Mentoring", "Coaching", "Decision Making",
            "Conflict Resolution", "Attention to Detail", "Reliability",
            "Initiative", "Self-motivated", "Interpersonal Skills"
        ]
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """
        Extract both technical and soft skills from text
        
        Args:
            text: Input text (resume or JD)
            
        Returns:
            Dictionary with extracted skills
        """
        text_lower = text.lower()
        
        extracted_skills = {
            "technical_skills": self._extract_technical_skills(text_lower),
            "soft_skills": self._extract_soft_skills(text_lower),
            "all_skills": []
        }
        
        extracted_skills["all_skills"] = (
            extracted_skills["technical_skills"] + 
            extracted_skills["soft_skills"]
        )
        
        return extracted_skills
    
    def _extract_technical_skills(self, text: str) -> List[str]:
        """Extract technical skills from text"""
        found_skills = set()
        
        for category, skills in self.technical_skills.items():
            for skill in skills:
                # Case-insensitive search with word boundaries
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, text):
                    found_skills.add(skill)
        
        return sorted(list(found_skills))
    
    def _extract_soft_skills(self, text: str) -> List[str]:
        """Extract soft skills from text"""
        found_skills = set()
        
        for skill in self.soft_skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text):
                found_skills.add(skill)
        
        return sorted(list(found_skills))
    
    def get_missing_skills(self, resume_skills: List[str], 
                          jd_skills: List[str]) -> Dict[str, List[str]]:
        """
        Find missing skills in resume compared to JD
        
        Args:
            resume_skills: Skills found in resume
            jd_skills: Skills found in JD
            
        Returns:
            Dictionary with missing and present skills
        """
        resume_set = set(skill.lower() for skill in resume_skills)
        jd_set = set(skill.lower() for skill in jd_skills)
        
        missing = list(jd_set - resume_set)
        present = list(resume_set & jd_set)
        
        return {
            "missing_skills": sorted(missing),
            "present_skills": sorted(present),
            "missing_count": len(missing),
            "present_count": len(present)
        }
    
    def get_skill_categories(self, skills: List[str]) -> Dict[str, List[str]]:
        """
        Categorize skills
        
        Args:
            skills: List of skills
            
        Returns:
            Skills organized by category
        """
        categorized = {
            "Technical": [],
            "Soft": [],
            "Other": []
        }
        
        skills_lower = [s.lower() for s in skills]
        
        for category, tech_skills in self.technical_skills.items():
            for skill in skills:
                if skill.lower() in [s.lower() for s in tech_skills]:
                    if skill not in categorized["Technical"]:
                        categorized["Technical"].append(skill)
        
        for skill in skills:
            if skill.lower() in [s.lower() for s in self.soft_skills]:
                if skill not in categorized["Soft"]:
                    categorized["Soft"].append(skill)
        
        # Skills not found in any category
        found_in_categories = (
            set(s.lower() for s in categorized["Technical"]) |
            set(s.lower() for s in categorized["Soft"])
        )
        
        for skill in skills:
            if skill.lower() not in found_in_categories:
                categorized["Other"].append(skill)
        
        return categorized
