import re
import string
import logging
from typing import Dict, List, Set, Tuple, Optional
import spacy
from pdfminer.high_level import extract_text as pdf_extract_text
import docx2txt
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Configure logging
logger = logging.getLogger(__name__)

# Download required NLTK resources
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except Exception as e:
    logger.warning(f"Error downloading NLTK resources: {e}")

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    logger.warning(f"Error loading spaCy model: {e}. Installing now...")
    import subprocess
    subprocess.run([
        "python", "-m", "spacy", "download", "en_core_web_sm"
    ], check=True)
    nlp = spacy.load("en_core_web_sm")


class TextExtractor:
    """Extract text from various file formats."""
    
    @staticmethod
    def extract_from_pdf(file_path: str) -> str:
        """Extract text from PDF files."""
        try:
            logger.info(f"Extracting text from PDF: {file_path}")
            text = pdf_extract_text(file_path)
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {e}")
            return ""
    
    @staticmethod
    def extract_from_docx(file_path: str) -> str:
        """Extract text from DOCX files."""
        try:
            logger.info(f"Extracting text from DOCX: {file_path}")
            text = docx2txt.process(file_path)
            return text
        except Exception as e:
            logger.error(f"Error extracting text from DOCX {file_path}: {e}")
            return ""
    
    @staticmethod
    def extract_from_html(file_path: str) -> str:
        """Extract text from HTML files."""
        try:
            logger.info(f"Extracting text from HTML: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()
            
            text = soup.get_text()
            # Break into lines and remove leading and trailing space
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            return text
        except Exception as e:
            logger.error(f"Error extracting text from HTML {file_path}: {e}")
            return ""
    
    @staticmethod
    def extract_from_file(file_path: str) -> str:
        """Extract text from a file based on its extension."""
        if file_path.lower().endswith('.pdf'):
            return TextExtractor.extract_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            return TextExtractor.extract_from_docx(file_path)
        elif file_path.lower().endswith(('.html', '.htm')):
            return TextExtractor.extract_from_html(file_path)
        else:
            logger.error(f"Unsupported file format: {file_path}")
            return ""


class KeywordExtractor:
    """Extract keywords from text."""
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        # Add common words that aren't useful for ATS matching
        self.stop_words.update([
            'resume', 'curriculum', 'vitae', 'cv', 'page', 'contact',
            'email', 'phone', 'address', 'linkedin', 'github'
        ])
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for keyword extraction."""
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def extract_keywords(self, text: str, max_keywords: int = 50) -> List[str]:
        """Extract keywords from text."""
        preprocessed_text = self.preprocess_text(text)
        
        # Tokenize
        tokens = word_tokenize(preprocessed_text)
        
        # Remove stopwords and lemmatize
        filtered_tokens = [
            self.lemmatizer.lemmatize(token) for token in tokens
            if token not in self.stop_words and len(token) > 2
        ]
        
        # Use spaCy for named entity recognition and noun chunks
        doc = nlp(preprocessed_text)
        
        # Extract named entities
        entities = [ent.text.lower() for ent in doc.ents]
        
        # Extract noun chunks (potential technical skills and job titles)
        noun_chunks = [chunk.text.lower() for chunk in doc.noun_chunks]
        
        # Combine all potential keywords
        all_keywords = filtered_tokens + entities + noun_chunks
        
        # Count frequencies
        keyword_freq = {}
        for keyword in all_keywords:
            if keyword in keyword_freq:
                keyword_freq[keyword] += 1
            else:
                keyword_freq[keyword] = 1
        
        # Sort by frequency
        sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Return top keywords
        return [keyword for keyword, _ in sorted_keywords[:max_keywords]]
    
    def extract_technical_skills(self, text: str) -> List[str]:
        """Extract technical skills from text."""
        # Common programming languages, tools, frameworks, etc.
        tech_keywords = {
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php',
            'html', 'css', 'sql', 'nosql', 'react', 'angular', 'vue',
            'node.js', 'express', 'django', 'flask', 'spring', 'hibernate',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'terraform',
            'jenkins', 'git', 'github', 'gitlab', 'bitbucket', 'jira',
            'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'rest', 'graphql',
            'machine learning', 'deep learning', 'ai', 'data science',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas',
            'numpy', 'scipy', 'matplotlib', 'seaborn', 'tableau', 'power bi',
            'hadoop', 'spark', 'kafka', 'elasticsearch', 'mongodb', 'mysql',
            'postgresql', 'oracle', 'sqlserver', 'redis', 'rabbitmq',
            'react native', 'flutter', 'swift', 'kotlin', 'objective-c',
            'android', 'ios', 'typescript', 'redux', 'vuex', 'webpack',
            'sass', 'less', 'tailwind', 'bootstrap', 'material-ui',
            'linux', 'bash', 'powershell', 'aws lambda', 'serverless',
            'microservices', 'restful api', 'oauth', 'jwt', 'authentication',
            'authorization', 'cybersecurity', 'blockchain', 'ethereum'
        }
        
        # Preprocess text
        preprocessed_text = self.preprocess_text(text)
        
        # Find technical skills in text
        found_skills = []
        for skill in tech_keywords:
            if re.search(r'\b' + re.escape(skill) + r'\b', preprocessed_text):
                found_skills.append(skill)
        
        return found_skills


class SectionExtractor:
    """Extract sections from resume text."""
    
    SECTION_HEADERS = {
        'education': ['education', 'academic background', 'academic history', 'degrees', 'qualifications'],
        'experience': ['experience', 'work experience', 'employment history', 'work history', 'professional experience'],
        'skills': ['skills', 'technical skills', 'competencies', 'expertise', 'proficiencies'],
        'projects': ['projects', 'personal projects', 'academic projects', 'professional projects'],
        'certifications': ['certifications', 'certificates', 'accreditations', 'professional development'],
        'summary': ['summary', 'professional summary', 'profile', 'objective', 'professional objective'],
        'achievements': ['achievements', 'accomplishments', 'honors', 'awards']
    }
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extract sections from resume text."""
        logger.info("Extracting resume sections")
        sections = {}
        
        # Preprocess text - normalize line breaks and spacing
        text = re.sub(r'\r\n', '\n', text)  # Normalize newlines
        text = re.sub(r'\n+', '\n', text)   # Remove multiple consecutive newlines
        
        # Create a list of section header patterns
        section_patterns = {}
        for section_name, headers in self.SECTION_HEADERS.items():
            patterns = [re.escape(header) for header in headers]
            # Match full words with variations in capitalization and optional following characters
            section_patterns[section_name] = re.compile(
                r'(?i)^(?:' + '|'.join(patterns) + r')[\s:]*$',
                re.MULTILINE
            )
        
        # Find the positions of all section headers
        matches = []
        for section_name, pattern in section_patterns.items():
            for match in pattern.finditer(text):
                matches.append((match.start(), match.end(), section_name))
        
        # Sort matches by position
        matches.sort()
        
        # Extract text between section headers
        for i, (start, end, section_name) in enumerate(matches):
            # Section text goes from the end of this header to the start of the next one
            section_start = end
            if i < len(matches) - 1:
                section_end = matches[i + 1][0]
            else:
                section_end = len(text)
            
            section_text = text[section_start:section_end].strip()
            sections[section_name] = section_text
        
        return sections


class JobDescriptionParser:
    """Parse job descriptions from various sources."""
    
    def __init__(self):
        self.keyword_extractor = KeywordExtractor()
    
    def extract_requirements(self, job_description: str) -> Dict[str, List[str]]:
        """Extract requirements from a job description."""
        logger.info("Extracting job requirements")
        
        requirements = {
            'skills': [],
            'education': [],
            'experience': []
        }
        
        # Extract technical skills
        requirements['skills'] = self.keyword_extractor.extract_technical_skills(job_description)
        
        # Extract education requirements
        edu_patterns = [
            r'(?i)bachelor[\'s]* degree',
            r'(?i)master[\'s]* degree',
            r'(?i)phd',
            r'(?i)doctorate',
            r'(?i)bs[c]?\.?\s+in',
            r'(?i)ms[c]?\.?\s+in',
            r'(?i)b\.?a\.?',
            r'(?i)m\.?a\.?',
            r'(?i)b\.?s\.?',
            r'(?i)m\.?s\.?',
            r'(?i)degree in'
        ]
        
        for pattern in edu_patterns:
            matches = re.findall(pattern + r'[^.;:]*[.;:]?', job_description)
            for match in matches:
                requirements['education'].append(match.strip())
        
        # Extract experience requirements
        exp_patterns = [
            r'(?i)(\d+[\+]?\s+years?(?:\s+of)?(?:\s+experience)?)',
            r'(?i)(minimum\s+of\s+\d+\s+years?(?:\s+of)?(?:\s+experience)?)',
            r'(?i)(at\s+least\s+\d+\s+years?(?:\s+of)?(?:\s+experience)?)'
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern + r'[^.;:]*[.;:]?', job_description)
            for match in matches:
                requirements['experience'].append(match.strip())
        
        return requirements
    
    def parse_linkedin_job(self, job_text: str) -> Dict[str, List[str]]:
        """Parse a LinkedIn job description."""
        # Currently uses the generic parser
        # Could be extended with LinkedIn-specific patterns
        return self.extract_requirements(job_text)
    
    def parse_naukri_job(self, job_text: str) -> Dict[str, List[str]]:
        """Parse a Naukri job description."""
        # Currently uses the generic parser
        # Could be extended with Naukri-specific patterns
        return self.extract_requirements(job_text)


class MatchingAlgorithm:
    """Compare resume content against job requirements."""
    
    def __init__(self):
        self.nlp = nlp
    
    def calculate_similarity(self, resume_text: str, job_description: str) -> float:
        """Calculate similarity between resume and job description."""
        # Use spaCy to calculate similarity
        resume_doc = self.nlp(resume_text)
        job_doc = self.nlp(job_description)
        
        # Calculate similarity score (0-1)
        similarity = resume_doc.similarity(job_doc)
        return similarity
    
    def keyword_match_score(self, resume_keywords: List[str], job_keywords: List[str]) -> float:
        """Calculate keyword match score."""
        if not job_keywords:
            return 0.0
        
        # Convert to sets for faster lookup
        resume_keywords_set = set(resume_keywords)
        job_keywords_set = set(job_keywords)
        
        # Calculate matches
        matches = resume_keywords_set.intersection(job_keywords_set)
        
        # Calculate score as percentage of job keywords found in resume
        score = len(matches) / len(job_keywords_set)
        return score
    
    def section_match_score(self, resume_sections: Dict[str, str], 
                            job_requirements: Dict[str, List[str]]) -> Dict[str, float]:
        """Calculate match score for each section."""
        section_scores = {}
        
        # Check skills match
        if 'skills' in resume_sections and 'skills' in job_requirements:
            resume_skills = set(self.nlp(resume_sections['skills']).text.lower().split())
            job_skills = set(' '.join(job_requirements['skills']).lower().split())
            if job_skills:
                matches = resume_skills.intersection(job_skills)
                section_scores['skills'] = len(matches) / len(job_skills)
            else:
                section_scores['skills'] = 0.0
        else:
            section_scores['skills'] = 0.0
        
        # Check education match
        if 'education' in resume_sections and 'education' in job_requirements:
            resume_edu = resume_sections['education'].lower()
            edu_score = 0.0
            for edu_req in job_requirements['education']:
                if edu_req.lower() in resume_edu:
                    edu_score += 1.0
            section_scores['education'] = min(1.0, edu_score / max(1, len(job_requirements['education'])))
        else:
            section_scores['education'] = 0.0
        
        # Check experience match
        if 'experience' in resume_sections and 'experience' in job_requirements:
            resume_exp = resume_sections['experience'].lower()
            exp_score = 0.0
            for exp_req in job_requirements['experience']:
                if exp_req.lower() in resume_exp:
                    exp_score += 1.0
            section_scores['experience'] = min(1.0, exp_score / max(1, len(job_requirements['experience'])))
        else:
            section_scores['experience'] = 0.0
        
        return section_scores


class ATSFormatChecker:
    """Check resume format for ATS compatibility."""
    
    def check_format(self, resume_text: str) -> Dict[str, float]:
        """Check resume format and return scores for ATS compatibility."""
        format_scores = {}
        
        # Check for bullet points (preferred by ATS)
        bullet_patterns = [r'•', r'■', r'○', r'►', r'✓', r'✔', r'-', r'\*']
        has_bullets = any(re.search(pattern, resume_text) for pattern in bullet_patterns)
        format_scores['bullet_points'] = 1.0 if has_bullets else 0.0
        
        # Check for consistent formatting of dates
        date_patterns = [
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s\.]+ \d{4}\b',
            r'\b\d{2}/\d{2}/\d{4}\b',
            r'\b\d{4}-\d{2}-\d{2}\b',
            r'\b\d{4}-\d{2}\b',
            r'\b\d{2}/\d{4}\b'
        ]
        
        date_formats = [set() for _ in range(len(date_patterns))]
        for i, pattern in enumerate(date_patterns):
            matches = re.findall(pattern, resume_text)
            date_formats[i] = set(matches)
        
        # Check if dates are consistent (using only one format)
        non_empty_formats = sum(1 for format_set in date_formats if format_set)
        format_scores['date_consistency'] = 1.0 if non_empty_formats <= 1 else 0.5
        
        # Check for appropriate section headers
        section_headers = SectionExtractor.SECTION_HEADERS
        section_patterns = []
        for headers in section_headers.values():
            section_patterns.extend([re.escape(header) for header in headers])
        
        section_pattern = r'(?i)^(?:' + '|'.join(section_patterns) + r')[\s:]*$'
        sections_found = len(re.findall(section_pattern, resume_text, re.MULTILINE))
        format_scores['section_headers'] = min(1.0, sections_found / 4.0)  # At least 4 sections is ideal
        
        # Check for appropriate line spacing
        newline_count = resume_text.count('\n')
        text_length = len(resume_text)
        newline_ratio = newline_count / max(1, text_length)
        format_scores['line_spacing'] = 1.0 if 0.01 <= newline_ratio <= 0.05 else 0.5
        
        # Check for common ATS issues
        issues = []
        # Check for tables
        if '|' in resume_text or '\t' in resume_text:
            issues.append('tables')
        
        # Check for headers/footers (approximate)
        lines = resume_text.split('\n')
        if len(lines) > 10:
            repeated_first_line = lines[0] == lines[-1]
            if repeated_first_line:
                issues.append('headers_footers')
        
        # Check for images (can't really detect in text, but we can check if text is too sparse)
        if text_length / max(1, newline_count) < 20:  # Average less than 20 chars per line
            issues.append('possibly_image_heavy')
        
        format_scores['no_common_issues'] = 1.0 if not issues else 0.5 if len(issues) <= 1 else 0.0
        
        return format_scores