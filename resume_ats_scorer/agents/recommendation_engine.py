import logging
from typing import List
from crewai import Agent
from ..models.schemas import ResumeScoreResponse, ParsedResume, ParsedJobDescription

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Agent responsible for providing detailed feedback and improvement suggestions."""
    
    def __init__(self):
        self.agent = Agent(
            role="Recommendation Engine",
            goal="Provide actionable feedback to improve resume ATS compatibility",
            backstory="I am an expert at improving resumes for better ATS system compatibility.",
            verbose=True,
            allow_delegation=False
        )
    
    async def generate_recommendations(
        self, 
        resume: ParsedResume, 
        job_description: ParsedJobDescription, 
        score_result: ResumeScoreResponse
    ) -> List[str]:
        """Generate detailed recommendations based on score analysis."""
        logger.info("Generating detailed recommendations")
        
        try:
            # Start with recommendations already in the score result
            recommendations = list(score_result.recommendations)
            
            # Add specific formatting recommendations
            formatting_recs = self._generate_formatting_recommendations(resume, score_result)
            recommendations.extend(formatting_recs)
            
            # Add specific content recommendations
            content_recs = self._generate_content_recommendations(resume, job_description, score_result)
            recommendations.extend(content_recs)
            
            # Add ATS-specific optimizations
            ats_recs = self._generate_ats_optimization_recommendations(resume, score_result)
            recommendations.extend(ats_recs)
            
            # Deduplicate and limit recommendations
            unique_recs = []
            for rec in recommendations:
                if rec not in unique_recs and len(unique_recs) < 10:  # Limit to top 10 recommendations
                    unique_recs.append(rec)
            
            return unique_recs
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            raise
    
    def _generate_formatting_recommendations(self, resume: ParsedResume, score_result: ResumeScoreResponse) -> List[str]:
        """Generate formatting-specific recommendations."""
        recommendations = []
        
        # Check for essential sections
        missing_sections = []
        for section in [
            ResumeSection.SKILLS, 
            ResumeSection.EXPERIENCE, 
            ResumeSection.EDUCATION, 
            ResumeSection.SUMMARY
        ]:
            if section not in resume.sections or not resume.sections[section]:
                missing_sections.append(section.value.title())
        
        if missing_sections:
            recommendations.append(f"Add these missing sections for better ATS compatibility: {', '.join(missing_sections)}")
        
        # Check resume length
        if len(resume.raw_text) < 500:
            recommendations.append("Your resume appears too short. Consider adding more detailed content to better showcase your qualifications.")
        elif len(resume.raw_text) > 5000:
            recommendations.append("Your resume may be too long. Consider focusing on the most relevant experience to make it more concise.")
        
        # Check section balance
        if len(resume.sections) >= 3:
            section_lengths = {section: len(content) for section, content in resume.sections.items()}
            total_length = sum(section_lengths.values())
            
            for section, length in section_lengths.items():
                if section == ResumeSection.SKILLS and length / total_length < 0.1:
                    recommendations.append("Your Skills section appears too brief. Consider expanding it to highlight more relevant skills.")
                elif section == ResumeSection.EXPERIENCE and length / total_length < 0.3:
                    recommendations.append("Your Experience section could be more detailed. Focus on quantifiable achievements and responsibilities.")
        
        return recommendations
    
    def _generate_content_recommendations(
        self, 
        resume: ParsedResume, 
        job_description: ParsedJobDescription, 
        score_result: ResumeScoreResponse
    ) -> List[str]:
        """Generate content-specific recommendations."""
        recommendations = []
        
        # Identify top missing keywords
        all_missing = []
        for section_score in score_result.section_scores:
            all_missing.extend(section_score.missing)
        
        if all_missing:
            top_missing = list(set(all_missing))[:5]  # Top 5 unique missing keywords
            recommendations.append(f"Consider incorporating these keywords in your resume: {', '.join(top_missing)}")
        
        # Check for skills alignment
        job_skills = set()
        for req in job_description.requirements:
            if "skill" in req.category.lower():
                job_skills.add(req.description)
        
        resume_skills = set()
        if ResumeSection.SKILLS in resume.sections:
            skills_text = resume.sections[ResumeSection.SKILLS].lower()
            for skill in job_skills:
                if skill.lower() in skills_text:
                    resume_skills.add(skill)
        
        missing_skills = job_skills - resume_skills
        if missing_skills:
            recommendations.append(f"Consider highlighting these skills if you have them: {', '.join(list(missing_skills)[:3])}")
        
        # Check for experience alignment
        if ResumeSection.EXPERIENCE in resume.sections:
            exp_text = resume.sections[ResumeSection.EXPERIENCE].lower()
            exp_keywords = ["led", "managed", "developed", "created", "implemented", "improved", "increased", "decreased", "reduced", "achieved"]
            
            if not any(keyword in exp_text for keyword in exp_keywords):
                recommendations.append("Use strong action verbs in your experience section (e.g., Led, Developed, Implemented) to highlight achievements.")
            
            if not any(char.isdigit() for char in exp_text):
                recommendations.append("Consider adding quantifiable achievements with numbers and percentages to strengthen your experience section.")
        
        return recommendations
    
    def _generate_ats_optimization_recommendations(self, resume: ParsedResume, score_result: ResumeScoreResponse) -> List[str]:
        """Generate ATS-specific optimization recommendations."""
        recommendations = []
        
        # Check for ATS-friendly formatting
        if score_result.format_compatibility_score < 15:
            recommendations.append("For better ATS compatibility:")
            recommendations.append("- Use standard section headings (e.g., 'Skills', 'Experience', 'Education')")
            recommendations.append("- Avoid tables, columns, headers/footers, and graphics")
            recommendations.append("- Use standard fonts like Arial, Calibri, or Times New Roman")
        
        # Keyword optimization
        if score_result.content_match_score < 35:
            recommendations.append("For better keyword matching:")
            recommendations.append("- Mirror the exact terminology from the job description")
            recommendations.append("- Include both spelled-out terms and acronyms (e.g., 'Artificial Intelligence (AI)')")
            recommendations.append("- Place important keywords near the beginning of bullet points")
        
        return recommendations