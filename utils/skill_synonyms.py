"""
Skill Synonyms and Mappings
Maps various skill names to standardized categories
"""

# Skill synonyms dictionary
SKILL_SYNONYMS = {
    # Programming Languages
    'python': ['python', 'py', 'python3', 'python2'],
    'javascript': ['javascript', 'js', 'node.js', 'nodejs', 'typescript', 'ts'],
    'java': ['java', 'j2ee'],
    'c++': ['c++', 'cpp', 'cplusplus'],
    'c#': ['c#', 'csharp', 'dotnet', '.net'],
    'php': ['php', 'laravel'],
    'ruby': ['ruby', 'rails'],
    'go': ['go', 'golang'],
    'rust': ['rust'],
    'kotlin': ['kotlin'],
    'swift': ['swift'],
    'r': ['r programming', 'r language'],
    
    # Core CS Concepts
    'dsa': ['dsa', 'data structures', 'algorithms', 'algorithm design', 'competitive programming'],
    'oop': ['oop', 'object-oriented', 'object oriented programming', 'inheritance', 'polymorphism', 'encapsulation'],
    'design patterns': ['design patterns', 'mvc', 'mvvm', 'factory pattern', 'singleton'],
    'api': ['api', 'rest api', 'restful', 'graphql', 'soap', 'web services'],
    'sql': ['sql', 'mysql', 'postgresql', 'sqlite', 'pl/sql', 'tsql'],
    'database': ['database', 'dbms', 'nosql', 'mongodb', 'cassandra', 'redis', 'elasticsearch'],
    'database design': ['database design', 'schema design', 'normalization'],
    'system design': ['system design', 'scalability', 'microservices', 'distributed systems'],
    
    # Web Development
    'html': ['html', 'html5'],
    'css': ['css', 'css3', 'sass', 'scss', 'bootstrap', 'tailwind'],
    'react': ['react', 'react.js', 'reactjs'],
    'vue': ['vue', 'vue.js', 'vuejs'],
    'angular': ['angular', 'angularjs', 'angular.js'],
    'node.js': ['node.js', 'nodejs', 'node', 'express', 'express.js'],
    'django': ['django', 'python web'],
    'flask': ['flask', 'python framework'],
    'fastapi': ['fastapi', 'async python'],
    'asp.net': ['asp.net', 'asp net'],
    'spring': ['spring', 'spring boot'],
    
    # Databases & Caching
    'postgresql': ['postgresql', 'postgres', 'pg'],
    'mysql': ['mysql'],
    'mongodb': ['mongodb', 'mongo'],
    'redis': ['redis'],
    'elasticsearch': ['elasticsearch', 'elastic'],
    
    # DevOps & Tools
    'docker': ['docker', 'containerization', 'containers'],
    'kubernetes': ['kubernetes', 'k8s'],
    'git': ['git', 'github', 'gitlab', 'bitbucket', 'version control', 'scm'],
    'jenkins': ['jenkins', 'ci/cd', 'continuous integration'],
    'cicd': ['ci/cd', 'continuous integration', 'continuous deployment', 'pipeline'],
    'aws': ['aws', 'amazon web services', 'ec2', 's3', 'lambda'],
    'azure': ['azure', 'microsoft azure'],
    'gcp': ['gcp', 'google cloud', 'cloud platform'],
    'linux': ['linux', 'ubuntu', 'centos'],
    'bash': ['bash', 'shell scripting', 'shell'],
    
    # AI & ML Tools
    'chatgpt': ['chatgpt', 'chat gpt', 'openai'],
    'gemini': ['gemini', 'bard', 'google ai'],
    'copilot': ['copilot', 'github copilot', 'ai coding'],
    'ai tools': ['ai tools', 'generative ai', 'ai assistants', 'llm'],
    'machine learning': ['machine learning', 'ml', 'deep learning', 'neural networks'],
    'tensorflow': ['tensorflow', 'keras'],
    'pytorch': ['pytorch', 'torch'],
    'scikit-learn': ['scikit-learn', 'sklearn'],
    'nlp': ['nlp', 'natural language processing'],
    'computer vision': ['computer vision', 'cv', 'opencv'],
    
    # Testing
    'unit testing': ['unit testing', 'junit', 'pytest', 'jest', 'mocha'],
    'test automation': ['test automation', 'selenium', 'cypress'],
    'tdd': ['tdd', 'test-driven development'],
    
    # Authentication & Security
    'jwt': ['jwt', 'json web token', 'oauth', 'oauth2'],
    'authentication': ['authentication', 'auth', 'login'],
    'security': ['security', 'cryptography', 'ssl', 'https'],
    
    # Methodologies
    'agile': ['agile', 'scrum', 'kanban', 'sprint'],
    'jira': ['jira', 'project management'],
    
    # Cloud & Infrastructure
    'cloud': ['cloud', 'cloud computing'],
    'serverless': ['serverless', 'lambda'],
    
    # Other Tools
    'vs code': ['vs code', 'vscode', 'visual studio code'],
    'postman': ['postman', 'api testing'],
    'figma': ['figma', 'design'],
    'slack': ['slack', 'communication'],
}

# Skill Categories
SKILL_CATEGORIES = {
    'Programming Languages': {
        'skills': ['python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'kotlin', 'swift', 'r'],
        'weight': 0.20,
        'priority': 'high'
    },
    'Core CS': {
        'skills': ['dsa', 'oop', 'design patterns', 'system design', 'api', 'sql', 'database', 'database design'],
        'weight': 0.20,
        'priority': 'high'
    },
    'Web Development': {
        'skills': ['html', 'css', 'react', 'vue', 'angular', 'node.js', 'django', 'flask', 'fastapi', 'asp.net', 'spring'],
        'weight': 0.15,
        'priority': 'medium'
    },
    'Databases': {
        'skills': ['postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch'],
        'weight': 0.10,
        'priority': 'medium'
    },
    'DevOps & Tools': {
        'skills': ['docker', 'kubernetes', 'git', 'jenkins', 'cicd', 'aws', 'azure', 'gcp', 'linux', 'bash'],
        'weight': 0.15,
        'priority': 'medium'
    },
    'AI & ML': {
        'skills': ['chatgpt', 'gemini', 'copilot', 'ai tools', 'machine learning', 'tensorflow', 'pytorch', 'scikit-learn', 'nlp', 'computer vision'],
        'weight': 0.10,
        'priority': 'high'
    },
    'Testing': {
        'skills': ['unit testing', 'test automation', 'tdd'],
        'weight': 0.05,
        'priority': 'medium'
    },
    'Tools': {
        'skills': ['vs code', 'postman', 'figma', 'jira'],
        'weight': 0.05,
        'priority': 'low'
    }
}

def normalize_skill(skill):
    """
    Normalize a skill name to its standard form
    
    Args:
        skill: Skill name (string)
        
    Returns:
        Normalized skill name
    """
    skill_lower = skill.lower().strip()
    
    for standard_skill, synonyms in SKILL_SYNONYMS.items():
        if skill_lower in synonyms:
            return standard_skill
    
    return skill_lower

def get_skill_category(skill):
    """
    Get the category of a skill
    
    Args:
        skill: Skill name (string)
        
    Returns:
        Category name or None
    """
    normalized = normalize_skill(skill)
    
    for category, data in SKILL_CATEGORIES.items():
        if normalized in data['skills']:
            return category
    
    return None

def get_related_skills(skill):
    """
    Get skills related to the given skill
    
    Args:
        skill: Skill name (string)
        
    Returns:
        List of related skills
    """
    normalized = normalize_skill(skill)
    category = get_skill_category(skill)
    
    if category:
        return SKILL_CATEGORIES[category]['skills']
    return []

def is_related_skill(skill1, skill2):
    """
    Check if two skills are related
    
    Args:
        skill1: First skill
        skill2: Second skill
        
    Returns:
        True if related, False otherwise
    """
    cat1 = get_skill_category(skill1)
    cat2 = get_skill_category(skill2)
    return cat1 == cat2 and cat1 is not None
