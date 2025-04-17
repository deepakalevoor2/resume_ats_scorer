import logging
from typing import List
from crewai import Agent
from ..models.schemas import ParsedJobDescription, JobRequirement, JobPlatform

logger = logging.getLogger(__name__)


class JobDescriptionParser:
    """Agent responsible for parsing job descriptions and extracting key requirements."""
    
    def __init__(self):
        self.agent = Agent(
            role="Job Description Parser",
            goal="Extract structured requirements from job postings",
            backstory="I specialize in analyzing job descriptions to identify key skills, qualifications, and requirements.",
            verbose=True,
            allow_delegation=False
        )
    
    async def parse_job_description(self, job_description: str, platform: JobPlatform) -> ParsedJobDescription:
        """Parse a job description and extract structured requirements."""
        logger.info(f"Parsing job description from {platform}")
        
        try:
            title = self._extract_job_title(job_description)
            company = self._extract_company(job_description)
            requirements = self._extract_requirements(job_description)
            keywords = self._extract_keywords(job_description)
            
            return ParsedJobDescription(
                title=title,
                company=company,
                description=job_description,
                requirements=requirements,
                keywords=keywords,
                metadata={"platform": platform}
            )
        except Exception as e:
            logger.error(f"Error parsing job description: {str(e)}")
            raise
    
    def _extract_job_title(self, job_description: str) -> str:
        """Extract job title from job description."""
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP techniques
        lines = job_description.split('\n')
        for line in lines[:5]:  # Check first few lines for title
            if len(line.strip()) < 50 and any(word in line.lower() for word in ["engineer", "developer", "manager", "specialist", "analyst"]):
                return line.strip()
        
        return "Unknown Position"
    
    def _extract_company(self, job_description: str) -> str:
        """Extract company name from job description."""
        # This is a simplified implementation
        lines = job_description.split('\n')
        for line in lines[:10]:  # Check first few lines for company
            if "company" in line.lower() or "organization" in line.lower() or "at" in line.lower():
                return line.strip()
        
        return "Unknown Company"
    
    def _extract_requirements(self, job_description: str) -> List[JobRequirement]:
        """Extract requirements from job description."""
        # This is a simplified implementation
        requirements = []
        
        # Look for common requirement patterns in job descriptions
        skill_keywords = ["skills", "requirements", "qualifications", "proficient in", "experience with"]
        description_lines = job_description.split('\n')
        
        for i, line in enumerate(description_lines):
            if any(keyword in line.lower() for keyword in skill_keywords):
                # This might be a requirements section header
                # Collect the next few lines as requirements
                req_count = 0
                j = i + 1
                while j < len(description_lines) and req_count < 10:
                    if description_lines[j].strip() and len(description_lines[j].strip()) > 10:
                        # Determine if this is likely a required or preferred skill
                        is_required = not any(word in description_lines[j].lower() for word in ["preferred", "nice to have", "plus", "advantage"])
                        
                        requirements.append(
                            JobRequirement(
                                category="skill" if "skill" in line.lower() else "experience",
                                description=description_lines[j].strip(),
                                importance=1.0 if is_required else 0.5,
                                required=is_required
                            )
                        )
                        req_count += 1
                    j += 1
        
        # If no requirements found, try a different approach
        if not requirements:
            # Look for bullet points or numbered lists
            for line in description_lines:
                if (line.strip().startswith("-") or line.strip().startswith("•") or 
                    (len(line.strip()) > 0 and line.strip()[0].isdigit() and "." in line.strip()[:3])):
                    # This is likely a bullet point in a requirements list
                    is_required = not any(word in line.lower() for word in ["preferred", "nice to have", "plus", "advantage"])
                    
                    requirements.append(
                        JobRequirement(
                            category="general",
                            description=line.strip().lstrip("-•0123456789. "),
                            importance=1.0 if is_required else 0.5,
                            required=is_required
                        )
                    )
        
        return requirements
    
    def _extract_keywords(self, job_description: str) -> List[str]:
        """Extract key skills and keywords from job description."""
        # This is a simplified implementation
        # Extract common technical terms, programming languages, tools, etc.
        tech_keywords = [
            "python", "java", "javascript", "react", "angular", "vue", "node", "express",
            "django", "flask", "spring", "hibernate", "sql", "nosql", "mongodb", "postgresql",
            "mysql", "oracle", "aws", "azure", "gcp", "docker", "kubernetes", "ci/cd",
            "git", "agile", "scrum", "kanban", "api", "rest", "graphql", "microservices"
        ]
        
        found_keywords = []
        words = job_description.lower().replace(',', ' ').replace(';', ' ').replace('.', ' ').split()
        
        for keyword in tech_keywords:
            if keyword in job_description.lower():
                found_keywords.append(keyword)
        
        # Add other potentially important keywords
        for word in words:
            if (len(word) > 3 and word not in found_keywords and 
                any(term in word for term in ["skill", "experience", "year", "degree", "qualification"])):
                found_keywords.append(word)
        
        return list(set(found_keywords))