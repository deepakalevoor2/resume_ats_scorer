import logging
from typing import Dict, List, Tuple
from crewai import Agent
from ..models.schemas import ParsedResume, ParsedJobDescription, ResumeScoreResult, SectionScore, ResumeSection

logger = logging.getLogger(__name__)


class MatchingAlgorithm:
    """Agent responsible for comparing resume content against job requirements and generating scores."""
    
    def __init__(self):
        self.agent = Agent(
            role="Matching Algorithm",
            goal="Compare resumes against job requirements and generate accurate scores",
            backstory="I am an expert at analyzing the relevance of resume content to job requirements.",
            verbose=True,
            allow_delegation=False
        )
    
    async def generate_score(self, resume: ParsedResume, job_description: ParsedJobDescription) -> ResumeScoreResult:
        """Generate a comprehensive score based on resume and job description."""
        logger.info("Generating resume score")
        
        try:
            # Calculate various score components
            content_match_score, content_matches, content_missing = self._calculate_content_match(resume, job_description)
            format_score = self._calculate_format_compatibility(resume)
            section_scores = self._calculate_section_scores(resume, job_description)
            
            # Calculate total score
            total_score = content_match_score + format_score + sum(section.score for section in section_scores)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                resume, job_description, content_match_score, format_score, section_scores, content_missing
            )
            
            return ResumeScoreResult(
                total_score=total_score,
                content_match_score=content_match_score,
                format_compatibility_score=format_score,
                section_scores=section_scores,
                recommendations=recommendations
            )
        except Exception as e:
            logger.error(f"Error generating score: {str(e)}")
            raise
    
    def _calculate_content_match(self, resume: ParsedResume, job_description: ParsedJobDescription) -> Tuple[float, List[str], List[str]]:
        """Calculate the content match score (0-50)."""
        # Extract all keywords and important phrases from job description
        job_keywords = set(job_description.keywords)
        resume_keywords = set(resume.keywords)
        
        # Calculate keyword match percentage
        matched_keywords = job_keywords.intersection(resume_keywords)
        match_percentage = len(matched_keywords) / max(len(job_keywords), 1)
        
        # Calculate requirement match percentage
        matched_requirements = 0
        missing_requirements = []
        
        for req in job_description.requirements:
            req_description = req.description.lower()
            if any(keyword in req_description for keyword in resume_keywords):
                matched_requirements += 1
            else:
                missing_requirements.append(req.description)
        
        req_match_percentage = matched_requirements / max(len(job_description.requirements), 1)
        
        # Calculate overall content match score (0-50)
        content_score = (match_percentage * 25) + (req_match_percentage * 25)
        content_score = min(50, content_score)  # Cap at 50
        
        return content_score, list(matched_keywords), missing_requirements
    
    def _calculate_format_compatibility(self, resume: ParsedResume) -> float:
        """Calculate the format compatibility score (0-20)."""
        format_score = 0
        
        # Check if resume has essential sections
        essential_sections = [ResumeSection.SKILLS, ResumeSection.EXPERIENCE, ResumeSection.EDUCATION]
        for section in essential_sections:
            if section in resume.sections and resume.sections[section]:
                format_score += 3  # 3 points per essential section
        
        # Check if resume has good structure
        if len(resume.sections) >= 4:  # Has a good number of sections
            format_score += 3
        
        # Check for overall text length and content density
        if len(resume.raw_text) > 200:  # Not too short
            format_score += 3
        
        # Check for keyword density
        keyword_density = len(resume.keywords) / max(len(resume.raw_text.split()), 1) * 100
        if 5 <= keyword_density <= 15:  # Good keyword density
            format_score += 5
        
        return min(20, format_score)  # Cap at 20
    
    def _calculate_section_scores(self, resume: ParsedResume, job_description: ParsedJobDescription) -> List[SectionScore]:
        """Calculate scores for individual resume sections."""
        section_scores = []
        
        # Score skills section
        skills_score = 0
        skills_feedback = "Skills section not found or insufficient."
        skills_matches = []
        skills_missing = []
        
        if ResumeSection.SKILLS in resume.sections and resume.sections[ResumeSection.SKILLS]:
            skills_text = resume.sections[ResumeSection.SKILLS].lower()
            skills_score = 0
            
            for keyword in job_description.keywords:
                if keyword.lower() in skills_text:
                    skills_score += 1
                    skills_matches.append(keyword)
                else:
                    skills_missing.append(keyword)
            
            skills_score = min(10, skills_score)  # Cap at 10
            
            if skills_score >= 7:
                skills_feedback = "Excellent skills match with job requirements."
            elif skills_score >= 5:
                skills_feedback = "Good skills match, but could be improved."
            else:
                skills_feedback = "Skills section needs improvement to better match job requirements."
        
        section_scores.append(SectionScore(
            section=ResumeSection.SKILLS,
            score=skills_score,
            feedback=skills_feedback,
            matches=skills_matches,
            missing=skills_missing
        ))
        
        # Score experience section
        exp_score = 0
        exp_feedback = "Experience section not found or insufficient."
        exp_matches = []
        exp_missing = []
        
        if ResumeSection.EXPERIENCE in resume.sections and resume.sections[ResumeSection.EXPERIENCE]:
            exp_text = resume.sections[ResumeSection.EXPERIENCE].lower()
            exp_score = 0
            
            # Check for relevant experience keywords
            for req in job_description.requirements:
                if req.category.lower() == "experience":
                    req_keywords = req.description.lower().split()
                    matched = any(keyword in exp_text for keyword in req_keywords if len(keyword) > 3)
                    
                    if matched:
                        exp_score += 1
                        exp_matches.append(req.description)
                    else:
                        exp_missing.append(req.description)
            
            exp_score = min(10, exp_score)  # Cap at 10
            
            if exp_score >= 7:
                exp_feedback = "Excellent experience match with job requirements."
            elif exp_score >= 5:
                exp_feedback = "Good experience match, but could be improved."
            else:
                exp_feedback = "Experience section needs improvement to better match job requirements."
        
        section_scores.append(SectionScore(
            section=ResumeSection.EXPERIENCE,
            score=exp_score,
            feedback=exp_feedback,
            matches=exp_matches,
            missing=exp_missing
        ))
        
        # Score education section
        edu_score = 0
        edu_feedback = "Education section not found or insufficient."
        edu_matches = []
        edu_missing = []
        
        if ResumeSection.EDUCATION in resume.sections and resume.sections[ResumeSection.EDUCATION]:
            edu_text = resume.sections[ResumeSection.EDUCATION].lower()
            edu_score = 0
            
            # Check for education requirements
            education_reqs = [req for req in job_description.requirements if any(term in req.description.lower() for term in ["degree", "education", "university", "college", "bachelor", "master", "phd"])]
            
            for req in education_reqs:
                req_keywords = req.description.lower().split()
                matched = any(keyword in edu_text for keyword in req_keywords if len(keyword) > 3)
                
                if matched:
                    edu_score += 2
                    edu_matches.append(req.description)
                else:
                    edu_missing.append(req.description)
            
            # Basic education section present
            edu_score += 3
            
            edu_score = min(5, edu_score)  # Cap at 5
            
            if edu_score >= 4:
                edu_feedback = "Education section meets job requirements."
            else:
                edu_feedback = "Education section could be improved to better match job requirements."
        
        section_scores.append(SectionScore(
            section=ResumeSection.EDUCATION,
            score=edu_score,
            feedback=edu_feedback,
            matches=edu_matches,
            missing=edu_missing
        ))
        
        # Score overall formatting
        format_score = 0
        format_feedback = "Resume formatting needs improvement for ATS compatibility."
        
        # Check for number of sections
        if len(resume.sections) >= 4:
            format_score += 2
        
        # Check for content density
        if 200 <= len(resume.raw_text) <= 5000:
            format_score += 2
        
        # Basic formatting check
        format_score += 1
        
        format_score = min(5, format_score)  # Cap at 5
        
        if format_score >= 4:
            format_feedback = "Resume formatting is well-suited for ATS systems."
        else:
            format_feedback = "Resume formatting could be improved for better ATS compatibility."
        
        section_scores.append(SectionScore(
            section=ResumeSection.OTHER,  # Using OTHER for formatting
            score=format_score,
            feedback=format_feedback,
            matches=[],
            missing=[]
        ))
        
        return section_scores
    
    def _generate_recommendations(
        self, 
        resume: ParsedResume, 
        job_description: ParsedJobDescription,
        content_score: float,
        format_score: float,
        section_scores: List[SectionScore],
        missing_requirements: List[str]
    ) -> List[str]:
        """Generate recommendations for improving the resume."""
        recommendations = []
        
        # Content match recommendations
        if content_score < 25:
            recommendations.append("Your resume has low keyword matching with the job description. Try incorporating more relevant keywords.")
            recommendations.append(f"Consider adding these missing keywords: {', '.join(missing_requirements[:5])}")
        elif content_score < 40:
            recommendations.append("Your resume has moderate keyword matching. Consider enhancing the following areas:")
            recommendations.append(f"Add these important missing keywords: {', '.join(missing_requirements[:3])}")
        
        # Format recommendations
        if format_score < 10:
            recommendations.append("Your resume format needs significant improvement for better ATS compatibility.")
            recommendations.append("Ensure your resume has clearly defined sections for Skills, Experience, and Education.")
        elif format_score < 15:
            recommendations.append("Your resume format could be improved for better ATS compatibility.")
            
        # Section-specific recommendations
        for section_score in section_scores:
            if section_score.score < section_score.max_score * 0.7:
                if section_score.section == ResumeSection.SKILLS:
                    recommendations.append(f"Improve your Skills section: {section_score.feedback}")
                    if section_score.missing:
                        recommendations.append(f"Add these missing skills: {', '.join(section_score.missing[:5])}")
                elif section_score.section == ResumeSection.EXPERIENCE:
                    recommendations.append(f"Improve your Experience section: {section_score.feedback}")
                    if section_score.missing:
                        recommendations.append(f"Add experiences that demonstrate: {', '.join(section_score.missing[:3])}")
                elif section_score.section == ResumeSection.EDUCATION:
                    recommendations.append(f"Enhance your Education section: {section_score.feedback}")
                    if section_score.missing:
                        recommendations.append(f"Consider highlighting education relevant to: {', '.join(section_score.missing[:2])}")
        
        # Overall recommendations
        if len(recommendations) == 0:
            recommendations.append("Your resume is well-optimized for this job position. Consider making minor tweaks to further emphasize your relevant experience.")
        
        return recommendations