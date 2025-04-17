import logging
from typing import List, Dict
from crewai import Agent
from ..models.schemas import ParsedResume

logger = logging.getLogger(__name__)


class KeywordAnalyst:
    """Agent responsible for extracting and analyzing keywords from resumes."""
    
    def __init__(self):
        self.agent = Agent(
            role="Keyword Analyst",
            goal="Extract and analyze keywords from resumes to improve matching",
            backstory="I specialize in identifying key skills, technologies, and qualifications in resumes.",
            verbose=True,
            allow_delegation=False
        )
    
    async def analyze_keywords(self, resume: ParsedResume) -> Dict[str, List[str]]:
        """Analyze and categorize keywords from a parsed resume."""
        logger.info("Analyzing resume keywords")
        
        try:
            # Extract keywords from different sections
            skills_keywords = self._extract_skills_keywords(resume)
            experience_keywords = self._extract_experience_keywords(resume)
            education_keywords = self._extract_education_keywords(resume)
            
            # Combine all keywords
            all_keywords = list(set(skills_keywords + experience_keywords + education_keywords))
            
            return {
                "skills": skills_keywords,
                "experience": experience_keywords,
                "education": education_keywords,
                "all": all_keywords
            }
        except Exception as e:
            logger.error(f"Error analyzing keywords: {str(e)}")
            raise
    
    def _extract_skills_keywords(self, resume: ParsedResume) -> List[str]:
        """Extract skills-related keywords from the resume."""
        keywords = []
        
        # Extract from skills section if available
        if "skills" in resume.sections:
            skills_text = resume.sections["skills"].lower()
            
            # Common skill separators
            for separator in [",", ";", "\n", "•", "-"]:
                if separator in skills_text:
                    skills = [skill.strip() for skill in skills_text.split(separator) if skill.strip()]
                    keywords.extend(skills)
            
            # If no separators found, use the raw text
            if not keywords:
                words = skills_text.split()
                keywords = [word.strip() for word in words if len(word) > 3]
        
        # Look for skill keywords in the entire resume
        common_skills = [
            "python", "java", "javascript", "react", "angular", "vue", "node", "express",
            "django", "flask", "spring", "hibernate", "sql", "nosql", "mongodb", "postgresql",
            "mysql", "oracle", "aws", "azure", "gcp", "docker", "kubernetes", "ci/cd",
            "git", "agile", "scrum", "kanban", "api", "rest", "graphql", "microservices",
            "machine learning", "artificial intelligence", "data science", "data analysis",
            "deep learning", "nlp", "natural language processing", "computer vision"
        ]
        
        for skill in common_skills:
            if skill in resume.raw_text.lower() and skill not in keywords:
                keywords.append(skill)
        
        return list(set(keywords))  # Remove duplicates
    
    def _extract_experience_keywords(self, resume: ParsedResume) -> List[str]:
        """Extract experience-related keywords from the resume."""
        keywords = []
        
        # Extract from experience section if available
        if "experience" in resume.sections:
            exp_text = resume.sections["experience"].lower()
            
            # Look for action verbs
            action_verbs = [
                "led", "managed", "developed", "implemented", "created", "designed",
                "built", "enhanced", "improved", "reduced", "increased", "achieved",
                "coordinated", "delivered", "executed", "generated", "launched",
                "negotiated", "organized", "performed", "resolved", "streamlined",
                "supervised", "trained", "transformed", "established"
            ]
            
            for verb in action_verbs:
                if f" {verb} " in f" {exp_text} ":  # Add spaces to match whole words
                    keywords.append(verb)
            
            # Look for job titles
            job_titles = [
                "engineer", "developer", "manager", "director", "administrator",
                "analyst", "specialist", "consultant", "coordinator", "designer",
                "architect", "lead", "head", "chief", "officer", "president",
                "supervisor", "technician", "assistant", "associate", "senior"
            ]
            
            for title in job_titles:
                if f" {title} " in f" {exp_text} ":  # Add spaces to match whole words
                    keywords.append(title)
        
        return list(set(keywords))  # Remove duplicates
    
    def _extract_education_keywords(self, resume: ParsedResume) -> List[str]:
        """Extract education-related keywords from the resume."""
        keywords = []
        
        # Extract from education section if available
        if "education" in resume.sections:
            edu_text = resume.sections["education"].lower()
            
            # Look for degrees
            degrees = [
                "bachelor", "master", "doctorate", "phd", "bs", "ba", "ms", "ma", "mba",
                "btech", "mtech", "bsc", "msc", "associate", "certification"
            ]
            
            for degree in degrees:
                if f" {degree} " in f" {edu_text} " or f"{degree}'" in f" {edu_text} ":
                    keywords.append(degree)
            
            # Look for fields of study
            fields = [
                "computer science", "engineering", "business", "administration", "management",
                "information technology", "data science", "mathematics", "statistics",
                "physics", "chemistry", "biology", "economics", "finance", "accounting",
                "marketing", "communications", "psychology", "sociology", "liberal arts"
            ]
            
            for field in fields:
                if field in edu_text:
                    keywords.append(field)
        
        return list(set(keywords))