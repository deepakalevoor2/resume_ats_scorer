import logging
from typing import Dict, Any
from crewai import Crew, Task
from ..agents.resume_parser import ResumeParser
from ..agents.keyword_analyst import KeywordAnalyst
from ..agents.job_description_parser import JobDescriptionParser
from ..agents.matching_algorithm import MatchingAlgorithm
from ..agents.recommendation_engine import RecommendationEngine
from ..models.schemas import ResumeUploadRequest, ResumeScoreResponse, ParsedResume, ParsedJobDescription

logger = logging.getLogger(__name__)


class ResumeCrewManager:
    """Manager class for orchestrating the CrewAI workflow for resume scoring."""
    
    def __init__(self):
        # Initialize agents
        self.resume_parser = ResumeParser()
        self.keyword_analyst = KeywordAnalyst()
        self.job_parser = JobDescriptionParser()
        self.matching_algorithm = MatchingAlgorithm()
        self.recommendation_engine = RecommendationEngine()
    
    async def score_resume(self, request: ResumeUploadRequest) -> ResumeScoreResponse:
        """Process a scoring request through the entire CrewAI workflow."""
        logger.info(f"Processing resume scoring request for file: {request.resume_file_path}")
        
        try:
            # Step 1: Parse the resume
            parsed_resume = await self.resume_parser.parse_resume(
                request.resume_file_path, 
                request.file_type
            )
            
            # Step 2: Parse the job description
            parsed_job = await self.job_parser.parse_job_description(
                request.job_description,
                request.job_platform
            )
            
            # Step 3: Generate the score
            score_result = await self.matching_algorithm.generate_score(
                parsed_resume,
                parsed_job
            )
            
            # Step 4: Generate detailed recommendations
            detailed_recommendations = await self.recommendation_engine.generate_recommendations(
                parsed_resume,
                parsed_job,
                score_result
            )
            
            # Update the score result with detailed recommendations
            score_result.recommendations = detailed_recommendations
            
            return score_result
        except Exception as e:
            logger.error(f"Error in resume scoring workflow: {str(e)}")
            raise
    
    def create_crew(self) -> Crew:
        """Create a CrewAI crew with all the agents and tasks."""
        # Create tasks
        parse_resume_task = Task(
            description="Parse the resume file and extract structured content",
            agent=self.resume_parser.agent,
            expected_output="Parsed resume content"
        )
        
        parse_job_task = Task(
            description="Parse the job description and extract key requirements",
            agent=self.job_parser.agent,
            expected_output="Parsed job requirements"
        )
        
        matching_task = Task(
            description="Compare resume content against job requirements and generate scores",
            agent=self.matching_algorithm.agent,
            expected_output="Resume score analysis"
        )
        
        recommendation_task = Task(
            description="Generate detailed recommendations for improving the resume",
            agent=self.recommendation_engine.agent,
            expected_output="Improvement recommendations"
        )
        
        # Create the crew
        crew = Crew(
            agents=[
                self.resume_parser.agent,
                self.job_parser.agent,
                self.matching_algorithm.agent,
                self.recommendation_engine.agent
            ],
            tasks=[
                parse_resume_task,
                parse_job_task,
                matching_task,
                recommendation_task
            ],
            verbose=True
        )
        
        return crew
