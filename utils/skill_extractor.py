"""
Skill Extractor Module - Enhanced
Extracts technical and soft skills from resume and JD with intelligent mapping
"""

import json
import re
from typing import List, Dict, Set
from .skill_synonyms import normalize_skill, get_skill_category, SKILL_SYNONYMS

class SkillExtractor:
    """Extract technical and soft skills from text with intelligent mapping"""
    
    def __init__(self):
        """Initialize skill extractor with skill database"""
        self.technical_skills = self._load_technical_skills()
        self.soft_skills = self._load_soft_skills()
        self.ai_tools = ['chatgpt', 'gemini', 'copilot', 'ai tools', 'machine learning', 'tensorflow', 'pytorch', 'openai', 'bard']
    
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
                "Git", "SVN", "Jira", "Confluence", "CI/CD"
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
                "Microservices", "AWS", "SSL/TLS"
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
        Extract both technical and soft skills from text with normalization
        
        Args:
            text: Input text (resume or JD)
            
        Returns:
            Dictionary with extracted skills
        """
        text_lower = text.lower()
        
        # Extract all skills
        technical = self._extract_technical_skills(text_lower)
        soft = self._extract_soft_skills(text_lower)
        ai_tools = self._extract_ai_tools(text_lower)
        
        # Normalize skills
        technical_normalized = [normalize_skill(s) for s in technical]
        ai_tools_normalized = [normalize_skill(s) for s in ai_tools]
        
        extracted_skills = {
            "technical_skills": list(set(technical)),
            "soft_skills": list(set(soft)),
            "ai_tools": list(set(ai_tools)),
            "all_skills": list(set(technical + soft + ai_tools)),
            "normalized_skills": list(set(technical_normalized + [normalize_skill(s) for s in soft] + ai_tools_normalized))
        }
        
        return extracted_skills
    
    def _extract_technical_skills(self, text: str) -> List[str]:
        """Extract technical skills from text"""
        found_skills = set()
        
        for category, skills in self.technical_skills.items():
            for skill in skills:
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
    
    def _extract_ai_tools(self, text: str) -> List[str]:
        """Extract AI tools usage from text"""
        found_tools = set()
        
        for tool in self.ai_tools:
            pattern = r'\b' + re.escape(tool.lower()) + r'\b'
            if re.search(pattern, text):
                found_tools.add(tool.title())
        
        return list(found_tools)
    
    def get_missing_skills(self, resume_skills: List[str], jd_skills: List[str]) -> Dict:
        """
        Find missing skills using intelligent matching
        
        Args:
            resume_skills: Skills found in resume
            jd_skills: Skills found in JD
            
        Returns:
            Dictionary with missing and present skills
        """
        resume_normalized = [normalize_skill(s) for s in resume_skills]
        jd_normalized = [normalize_skill(s) for s in jd_skills]
        
        resume_set = set(resume_normalized)
        jd_set = set(jd_normalized)
        
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
            "AI Tools": [],
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
        
        for skill in skills:
            if any(tool in skill.lower() for tool in self.ai_tools):
                if skill not in categorized["AI Tools"]:
                    categorized["AI Tools"].append(skill)
        
        found_in_categories = (
            set(s.lower() for s in categorized["Technical"]) |
            set(s.lower() for s in categorized["Soft"]) |
            set(s.lower() for s in categorized["AI Tools"])
        )
        
        for skill in skills:
            if skill.lower() not in found_in_categories:
                categorized["Other"].append(skill)
        
        return categorized
