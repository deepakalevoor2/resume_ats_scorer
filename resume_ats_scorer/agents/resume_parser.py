import logging
from typing import Dict, Any
from pathlib import Path
import PyPDF2
import docx
from bs4 import BeautifulSoup
from crewai import Agent
from ..models.schemas import ParsedResume, ResumeSection, FileType

logger = logging.getLogger(__name__)


class ResumeParser:
    """Agent responsible for parsing different resume file formats and extracting structured content."""
    
    def __init__(self):
        self.agent = Agent(
            role="Resume Parser",
            goal="Extract structured content from resume files",
            backstory="I am an expert at parsing resume files in various formats and extracting their content.",
            verbose=True,
            allow_delegation=False
        )
        
    async def parse_resume(self, file_path: str, file_type: FileType) -> ParsedResume:
        """Parse a resume file and extract structured content."""
        logger.info(f"Parsing resume from {file_path} of type {file_type}")
        
        try:
            raw_text = self._extract_text(file_path, file_type)
            sections = self._identify_sections(raw_text)
            keywords = self._extract_keywords(raw_text)
            
            return ParsedResume(
                raw_text=raw_text,
                sections=sections,
                keywords=keywords,
                metadata={"file_type": file_type, "file_path": file_path}
            )
        except Exception as e:
            logger.error(f"Error parsing resume: {str(e)}")
            raise
    
    def _extract_text(self, file_path: str, file_type: FileType) -> str:
        """Extract raw text from resume file based on file type."""
        if file_type == FileType.PDF:
            return self._extract_from_pdf(file_path)
        elif file_type == FileType.DOCX:
            return self._extract_from_docx(file_path)
        elif file_type == FileType.HTML:
            return self._extract_from_html(file_path)
        elif file_type == FileType.TXT:
            return self._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    
    def _extract_from_html(self, file_path: str) -> str:
        """Extract text from HTML file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            return soup.get_text(separator="\n")
    
    def _extract_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def _identify_sections(self, text: str) -> Dict[ResumeSection, str]:
        """Identify and extract different sections from resume text."""
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP techniques
        sections = {}
        
        # Simple keyword-based section identification
        if "EXPERIENCE" in text.upper() or "WORK EXPERIENCE" in text.upper():
            sections[ResumeSection.EXPERIENCE] = self._extract_section(text, ["EXPERIENCE", "WORK EXPERIENCE"])
        
        if "EDUCATION" in text.upper():
            sections[ResumeSection.EDUCATION] = self._extract_section(text, ["EDUCATION"])
        
        if "SKILLS" in text.upper() or "TECHNICAL SKILLS" in text.upper():
            sections[ResumeSection.SKILLS] = self._extract_section(text, ["SKILLS", "TECHNICAL SKILLS"])
        
        if "SUMMARY" in text.upper() or "PROFILE" in text.upper():
            sections[ResumeSection.SUMMARY] = self._extract_section(text, ["SUMMARY", "PROFILE"])
        
        return sections
    
    def _extract_section(self, text: str, section_headers: list) -> str:
        """Extract a specific section's content based on section headers."""
        # This is a simplified implementation
        # In a real system, this would be more robust
        for header in section_headers:
            if header.upper() in text.upper():
                start_idx = text.upper().find(header.upper())
                next_section_idx = float('inf')
                
                # Find the next section header
                for section in ResumeSection:
                    if section.value.upper() != header.upper():
                        next_idx = text.upper().find(section.value.upper(), start_idx + len(header))
                        if next_idx != -1 and next_idx < next_section_idx:
                            next_section_idx = next_idx
                
                if next_section_idx == float('inf'):
                    return text[start_idx:]
                else:
                    return text[start_idx:next_section_idx]
        
        return ""
    
    def _extract_keywords(self, text: str) -> list:
        """Extract key skills and keywords from resume text."""
        # This is a simplified implementation
        # In a real system, this would use NLP techniques like entity recognition
        # For demo purposes, we'll just split on common separators and filter
        words = text.replace(',', ' ').replace(';', ' ').split()
        keywords = [word.strip().lower() for word in words if len(word) > 3]
        return list(set(keywords))  # Remove duplicates
