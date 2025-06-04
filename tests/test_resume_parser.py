import pytest
from pathlib import Path
import tempfile
from resume_ats_scorer.agents.resume_parser import ResumeParser
from resume_ats_scorer.models.schemas import FileType, ResumeSection
from resume_ats_scorer.core.exceptions import (
    FileValidationError,
    ParsingError,
    UnsupportedFileTypeError,
    FileNotFoundError
)

@pytest.fixture
def resume_parser():
    return ResumeParser()

@pytest.fixture
def sample_pdf():
    # Create a temporary PDF file with sample content
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        f.write(b'%PDF-1.4\n1 0 obj\n<</Type /Catalog /Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type /Pages /Kids [3 0 R] /Count 1>>\nendobj\n3 0 obj\n<</Type /Page /Parent 2 0 R /Resources <<>> /Contents 4 0 R>>\nendobj\n4 0 obj\n<</Length 44>>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Hello World) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000010 00000 n\n0000000053 00000 n\n0000000102 00000 n\n0000000172 00000 n\ntrailer\n<</Size 5 /Root 1 0 R>>\nstartxref\n242\n%%EOF')
        return f.name

@pytest.fixture
def sample_docx():
    # Create a temporary DOCX file with sample content
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as f:
        f.write(b'PK\x03\x04\x14\x00\x00\x00\x00\x00\x00\x00!\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00[Content_Types].xml')
        return f.name

@pytest.fixture
def sample_html():
    # Create a temporary HTML file with sample content
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
        f.write(b'<html><body><h1>Hello World</h1></body></html>')
        return f.name

@pytest.fixture
def sample_txt():
    # Create a temporary TXT file with sample content
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
        f.write(b'Hello World')
        return f.name

class TestResumeParser:
    async def test_parse_pdf(self, resume_parser, sample_pdf):
        result = await resume_parser.parse_resume(sample_pdf, FileType.PDF)
        assert result.raw_text
        assert isinstance(result.sections, dict)
        assert isinstance(result.keywords, list)
        assert result.metadata["file_type"] == FileType.PDF

    async def test_parse_docx(self, resume_parser, sample_docx):
        result = await resume_parser.parse_resume(sample_docx, FileType.DOCX)
        assert result.raw_text
        assert isinstance(result.sections, dict)
        assert isinstance(result.keywords, list)
        assert result.metadata["file_type"] == FileType.DOCX

    async def test_parse_html(self, resume_parser, sample_html):
        result = await resume_parser.parse_resume(sample_html, FileType.HTML)
        assert result.raw_text
        assert isinstance(result.sections, dict)
        assert isinstance(result.keywords, list)
        assert result.metadata["file_type"] == FileType.HTML

    async def test_parse_txt(self, resume_parser, sample_txt):
        result = await resume_parser.parse_resume(sample_txt, FileType.TXT)
        assert result.raw_text
        assert isinstance(result.sections, dict)
        assert isinstance(result.keywords, list)
        assert result.metadata["file_type"] == FileType.TXT

    async def test_file_not_found(self, resume_parser):
        with pytest.raises(FileNotFoundError):
            await resume_parser.parse_resume("nonexistent.pdf", FileType.PDF)

    async def test_unsupported_file_type(self, resume_parser, sample_pdf):
        with pytest.raises(UnsupportedFileTypeError):
            await resume_parser.parse_resume(sample_pdf, "invalid_type")

    async def test_empty_file(self, resume_parser):
        with tempfile.NamedTemporaryFile(suffix='.txt') as f:
            with pytest.raises(ParsingError):
                await resume_parser.parse_resume(f.name, FileType.TXT)

    async def test_large_file(self, resume_parser):
        # Create a large file (>10MB)
        with tempfile.NamedTemporaryFile(suffix='.txt') as f:
            f.write(b'0' * (11 * 1024 * 1024))  # 11MB
            f.flush()
            with pytest.raises(FileValidationError):
                await resume_parser.parse_resume(f.name, FileType.TXT)

    async def test_section_identification(self, resume_parser):
        test_content = """
        PROFESSIONAL SUMMARY
        Experienced software developer
        
        WORK EXPERIENCE
        Senior Developer at Company
        
        EDUCATION
        BS in Computer Science
        
        SKILLS
        Python, Java, SQL
        """
        
        with tempfile.NamedTemporaryFile(suffix='.txt') as f:
            f.write(test_content.encode())
            f.flush()
            result = await resume_parser.parse_resume(f.name, FileType.TXT)
            
            assert ResumeSection.SUMMARY in result.sections
            assert ResumeSection.EXPERIENCE in result.sections
            assert ResumeSection.EDUCATION in result.sections
            assert ResumeSection.SKILLS in result.sections

    async def test_keyword_extraction(self, resume_parser):
        test_content = "Python developer with Java experience and SQL skills"
        
        with tempfile.NamedTemporaryFile(suffix='.txt') as f:
            f.write(test_content.encode())
            f.flush()
            result = await resume_parser.parse_resume(f.name, FileType.TXT)
            
            keywords = result.keywords
            assert "python" in keywords
            assert "java" in keywords
            assert "sql" in keywords
            assert "developer" in keywords
            assert "experience" in keywords
            assert "skills" in keywords

    async def test_metadata_inclusion(self, resume_parser, sample_pdf):
        result = await resume_parser.parse_resume(sample_pdf, FileType.PDF)
        
        assert "file_type" in result.metadata
        assert "file_path" in result.metadata
        assert "sections_found" in result.metadata
        assert "keyword_count" in result.metadata
        assert isinstance(result.metadata["sections_found"], list)
        assert isinstance(result.metadata["keyword_count"], int) 