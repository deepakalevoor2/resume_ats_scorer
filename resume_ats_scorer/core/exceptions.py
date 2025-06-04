class ResumeATSException(Exception):
    """Base exception class for Resume ATS Scorer."""
    pass

class FileValidationError(ResumeATSException):
    """Raised when file validation fails."""
    pass

class ParsingError(ResumeATSException):
    """Raised when there's an error parsing the resume content."""
    pass

class UnsupportedFileTypeError(ResumeATSException):
    """Raised when an unsupported file type is provided."""
    pass

class FileNotFoundError(ResumeATSException):
    """Raised when the specified file cannot be found."""
    pass

class ScoringError(ResumeATSException):
    """Raised when there's an error in the scoring process."""
    pass

class JobDescriptionError(ResumeATSException):
    """Raised when there's an error processing the job description."""
    pass

class RecommendationError(ResumeATSException):
    """Raised when there's an error generating recommendations."""
    pass 