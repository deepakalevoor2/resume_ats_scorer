import logging
from crewai import Crew, Agent, Task
from typing import Dict, Any
from ..agents.resume_parser import ResumeParserAgent
from ..agents.keyword_analyst import KeywordAnalyst
from ..agents.job_description_parser import JobDescriptionParserAgent
from ..agents.matching_algorithm import MatchingAlgorithm
from ..agents.recommendation_engine import RecommendationEngine

logger = logging.getLogger(__name__)

def create_crew_for_analysis() -> Crew:
    """
    Creates a CrewAI crew for resume analysis.
    
    Returns:
        Crew: A configured CrewAI crew with agents and tasks for resume analysis.
    """
    try:
        # Initialize agents
        resume_parser = ResumeParserAgent()
        keyword_analyst = KeywordAnalyst()
        job_description_parser = JobDescriptionParserAgent()
        matching_algorithm = MatchingAlgorithm()
        recommendation_engine = RecommendationEngine()

        # Create CrewAI agents
        parser_agent = Agent(
            role="Resume Parser",
            goal="Extract text from resumes",
            backstory="Expert in parsing resumes of various formats",
            verbose=True,
            allow_delegation=False
        )

        keyword_agent = Agent(
            role="Keyword Analyst",
            goal="Extract and analyze keywords from resumes",
            backstory="Expert in identifying key skills and qualifications",
            verbose=True,
            allow_delegation=False
        )

        job_parser_agent = Agent(
            role="Job Description Parser",
            goal="Extract requirements from job descriptions",
            backstory="Expert in analyzing job descriptions",
            verbose=True,
            allow_delegation=False
        )

        matcher_agent = Agent(
            role="Matcher",
            goal="Match resume content to job requirements",
            backstory="Expert in comparing resumes with job descriptions",
            verbose=True,
            allow_delegation=False
        )

        recommender_agent = Agent(
            role="Recommender",
            goal="Generate improvement recommendations",
            backstory="Expert in providing actionable resume improvement suggestions",
            verbose=True,
            allow_delegation=False
        )

        # Define tasks
        parse_resume_task = Task(
            description="Parse the resume and extract text content",
            agent=parser_agent
        )

        extract_keywords_task = Task(
            description="Extract and analyze keywords from the resume",
            agent=keyword_agent,
            context=parse_resume_task
        )

        parse_job_task = Task(
            description="Parse the job description and extract requirements",
            agent=job_parser_agent
        )

        matching_task = Task(
            description="Compare resume content with job requirements",
            agent=matcher_agent,
            context=[extract_keywords_task, parse_job_task]
        )

        recommendation_task = Task(
            description="Generate recommendations for improvement",
            agent=recommender_agent,
            context=matching_task
        )

        # Create and return the crew
        crew = Crew(
            agents=[
                parser_agent,
                keyword_agent,
                job_parser_agent,
                matcher_agent,
                recommender_agent
            ],
            tasks=[
                parse_resume_task,
                extract_keywords_task,
                parse_job_task,
                matching_task,
                recommendation_task
            ],
            verbose=True
        )

        return crew

    except Exception as e:
        logger.error(f"Error creating analysis crew: {str(e)}")
        raise 