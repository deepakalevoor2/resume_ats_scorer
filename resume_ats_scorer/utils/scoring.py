import logging
import re
from typing import List, Dict, Any, Tuple
import datetime

from api.models.schemas import (
    ResumeScoreResponse,
    ContentMatch,
    FormatCompatibility,
    SectionAnalysis,
    OverallScore,
    SectionScore,
    KeywordAnalysis,
    JobRequirements
)

logger = logging.getLogger(__name__)

# Resume sections with max score allocations
RESUME_SECTIONS = {
    "contact_info": 5,
    "summary": 4,
    "experience": 8,
    "education": 5,
    "skills": 6,
    "certifications": 2,
}

# Format checking patterns
FORMAT_PATTERNS = {
    "bullet_points": r"•|\*|-|\+",
    "dates_consistent": r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\s*[-–—]\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}|Present",
    "action_verbs": r"\b(led|managed|developed|created|implemented|achieved|improved|increased|decreased|coordinated|designed)\b",
    "appropriate_length": lambda x: 300 <= len(x) <= 6000,
    "no_personal_pronouns": r"\b(I|me|my|mine|myself)\b",
    "consistent_tense": r"\b(ing|ed)\b"
}


def identify_resume_sections(resume_text: str) -> Dict[str, str]:
    """
    Identify different sections in the resume
    
    Args:
        resume_text: The text content of the resume
        
    Returns:
        Dictionary mapping section names to section content
    """
    sections = {}
    
    # Define patterns to identify common resume sections
    section_patterns = {
        "contact_info": r"(?:CONTACT|CONTACT INFORMATION|PERSONAL DETAILS).*?(?=\n\n|\n[A-Z])",
        "summary": r"(?:SUMMARY|PROFESSIONAL SUMMARY|PROFILE|OBJECTIVE).*?(?=\n\n|\n[A-Z])",
        "experience": r"(?:EXPERIENCE|WORK EXPERIENCE|EMPLOYMENT|PROFESSIONAL EXPERIENCE).*?(?=\n\n|\n[A-Z])",
        "education": r"(?:EDUCATION|EDUCATIONAL BACKGROUND|ACADEMIC).*?(?=\n\n|\n[A-Z])",
        "skills": r"(?:SKILLS|TECHNICAL SKILLS|CORE COMPETENCIES|EXPERTISE).*?(?=\n\n|\n[A-Z])",
        "certifications": r"(?:CERTIFICATIONS|CERTIFICATES|LICENSES|ACCREDITATIONS).*?(?=\n\n|\n[A-Z])",
    }
    
    # Extract each section using regex patterns
    for section_name, pattern in section_patterns.items():
        matches = re.findall(pattern, resume_text, re.IGNORECASE | re.DOTALL)
        if matches:
            sections[section_name] = matches[0]
        else:
            sections[section_name] = ""
    
    return sections


def analyze_format_compatibility(resume_text: str, file_type: str) -> Tuple[float, List[str], str]:
    """
    Analyze how well the resume format is compatible with ATS systems
    
    Args:
        resume_text: The text content of the resume
        file_type: The file type of the resume
        
    Returns:
        Tuple containing score, list of issues, and feedback
    """
    issues = []
    max_score = 20.0
    score = max_score
    
    # Check for proper formatting according to FORMAT_PATTERNS
    if not re.search(FORMAT_PATTERNS["bullet_points"], resume_text):
        issues.append("No bullet points detected for listing experiences/skills")
        score -= 3
    
    if not re.search(FORMAT_PATTERNS["dates_consistent"], resume_text):
        issues.append("Inconsistent date formatting detected")
        score -= 3
    
    if not re.search(FORMAT_PATTERNS["action_verbs"], resume_text):
        issues.append("Few action verbs detected in experience descriptions")
        score -= 3
    
    if not FORMAT_PATTERNS["appropriate_length"](resume_text):
        issues.append("Resume length is not optimal (too short or too long)")
        score -= 3
    
    if re.search(FORMAT_PATTERNS["no_personal_pronouns"], resume_text, re.IGNORECASE):
        issues.append("Personal pronouns detected (avoid I, me, my)")
        score -= 2
    
    # Assess consistency in tense usage
    past_tense = len(re.findall(r"\b\w+ed\b", resume_text))
    present_tense = len(re.findall(r"\b\w+ing\b", resume_text))
    if past_tense > 0 and present_tense > 0 and min(past_tense, present_tense) / max(past_tense, present_tense) > 0.4:
        issues.append("Mixed tenses detected in experience descriptions")
        score -= 2
    
    # Check for file-specific issues
    if file_type == "pdf" and "could not extract" in resume_text.lower():
        issues.append("PDF might contain scanned images instead of text")
        score -= 4
    
    # Ensure score doesn't go below 0
    score = max(0, score)
    
    feedback = "Your resume format is "
    if score >= 16:
        feedback += "excellent and highly compatible with ATS systems."
    elif score >= 12:
        feedback += "good, but could be improved to better pass through ATS filters."
    elif score >= 8:
        feedback += "average and may be filtered out by some ATS systems."
    else:
        feedback += "poorly formatted for ATS systems and likely to be rejected."
    
    if issues:
        feedback += " Consider addressing these formatting issues: " + ", ".join(issues) + "."
    
    return score, issues, feedback


def evaluate_section_scores(sections: Dict[str, str]) -> Tuple[float, List[SectionScore], str]:
    """
    Evaluate each section of the resume and assign scores
    
    Args:
        sections: Dictionary of resume sections
        
    Returns:
        Tuple containing total section score, list of section scores, and feedback
    """
    section_scores = []
    total_score = 0
    max_total = sum(RESUME_SECTIONS.values())
    
    for section_name, max_score in RESUME_SECTIONS.items():
        section_content = sections.get(section_name, "")
        
        # Evaluate section quality
        if not section_content:
            score = 0
            feedback = f"Missing {section_name.replace('_', ' ')} section"
        else:
            content_length = len(section_content)
            if section_name == "contact_info":
                # Check for email, phone, LinkedIn
                has_email = bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', section_content))
                has_phone = bool(re.search(r'[\+\(]?[0-9][0-9 \-\(\)]{8,}[0-9]', section_content))
                has_linkedin = bool(re.search(r'linkedin\.com/in/[a-zA-Z0-9\-]+', section_content))
                
                score = 0
                if has_email:
                    score += max_score * 0.4
                if has_phone:
                    score += max_score * 0.3
                if has_linkedin:
                    score += max_score * 0.3
                
                feedback = "Contact information is "
                if score >= max_score * 0.9:
                    feedback += "complete and well-formatted."
                elif score >= max_score * 0.6:
                    feedback += "good but missing some elements."
                else:
                    feedback += "incomplete or poorly formatted."
            
            elif section_name == "summary":
                word_count = len(section_content.split())
                
                if 50 <= word_count <= 200:
                    score = max_score
                    feedback = "Summary is concise and effective."
                elif word_count < 50:
                    score = max_score * 0.6
                    feedback = "Summary may be too brief."
                else:
                    score = max_score * 0.7
                    feedback = "Summary is too long, consider condensing."
            
            elif section_name == "experience":
                has_dates = bool(re.search(FORMAT_PATTERNS["dates_consistent"], section_content))
                has_bullets = bool(re.search(FORMAT_PATTERNS["bullet_points"], section_content))
                has_action_verbs = bool(re.search(FORMAT_PATTERNS["action_verbs"], section_content))
                
                score = 0
                if has_dates:
                    score += max_score * 0.3
                if has_bullets:
                    score += max_score * 0.3
                if has_action_verbs:
                    score += max_score * 0.4
                
                feedback = "Experience section is "
                if score >= max_score * 0.9:
                    feedback += "well-structured with clear dates, bullet points, and action verbs."
                elif score >= max_score * 0.6:
                    feedback += "good but could use improvement in structure or content."
                else:
                    feedback += "poorly structured or missing key elements."
            
            elif section_name == "education":
                has_institution = bool(re.search(r'(University|College|Institute|School)', section_content, re.IGNORECASE))
                has_degree = bool(re.search(r'(Bachelor|Master|PhD|Doctorate|BSc|BA|MS|MA|MBA)', section_content, re.IGNORECASE))
                has_dates = bool(re.search(r'\b(19|20)\d{2}\b', section_content))
                
                score = 0
                if has_institution:
                    score += max_score * 0.4
                if has_degree:
                    score += max_score * 0.4
                if has_dates:
                    score += max_score * 0.2
                
                feedback = "Education section is "
                if score >= max_score * 0.9:
                    feedback += "complete with institutions, degrees, and dates."
                elif score >= max_score * 0.6:
                    feedback += "good but missing some details."
                else:
                    feedback += "incomplete or poorly structured."
            
            elif section_name == "skills":
                # Check for organized skills
                skill_count = len(re.findall(r',|\n|\•|\*|\-', section_content)) + 1
                
                if skill_count >= 10:
                    score = max_score
                    feedback = "Skills section is comprehensive and well-organized."
                elif skill_count >= 5:
                    score = max_score * 0.7
                    feedback = "Skills section is good but could be more comprehensive."
                else:
                    score = max_score * 0.4
                    feedback = "Skills section is limited or poorly organized."
            
            elif section_name == "certifications":
                if content_length > 50:
                    score = max_score
                    feedback = "Certifications section is present and detailed."
                elif content_length > 0:
                    score = max_score * 0.5
                    feedback = "Certifications section is present but limited."
                else:
                    score = 0
                    feedback = "No certifications listed."
        
        section_scores.append(SectionScore(
            name=section_name.replace('_', ' ').title(),
            score=round(score, 1),
            max_score=max_score,
            feedback=feedback
        ))
        
        total_score += score
    
    # Calculate percentage of max possible score and convert to a 0-30 scale
    normalized_score = (total_score / max_total) * 30
    
    overall_feedback = "Your resume sections are "
    if normalized_score >= 25:
        overall_feedback += "excellent, with all key sections well-developed."
    elif normalized_score >= 20:
        overall_feedback += "good, but some sections could be improved."
    elif normalized_score >= 15:
        overall_feedback += "average, with several sections needing improvement."
    else:
        overall_feedback += "below average, with significant room for improvement in most sections."
    
    return round(normalized_score, 1), section_scores, overall_feedback


def calculate_content_match_score(
    resume_keywords: KeywordAnalysis,
    job_requirements: JobRequirements
) -> Tuple[float, List[str], List[str], str]:
    """
    Calculate how well the resume content matches job requirements
    
    Args:
        resume_keywords: Keywords extracted from resume
        job_requirements: Requirements extracted from job description
        
    Returns:
        Tuple containing score, matched keywords, missing keywords, and feedback
    """
    max_score = 40.0
    
    # Combine skills from resume
    resume_skills = resume_keywords.hard_skills + resume_keywords.soft_skills
    
    # Calculate matches
    matched_required = [skill for skill in job_requirements.required_skills if any(
        re.search(rf'\b{re.escape(skill)}\b', rs, re.IGNORECASE) for rs in resume_skills
    )]
    
    matched_preferred = [skill for skill in job_requirements.preferred_skills if any(
        re.search(rf'\b{re.escape(skill)}\b', rs, re.IGNORECASE) for rs in resume_skills
    )]
    
    # Calculate missing skills
    missing_required = [skill for skill in job_requirements.required_skills if skill not in matched_required]
    missing_preferred = [skill for skill in job_requirements.preferred_skills if skill not in matched_preferred]
    
    # Calculate experience match
    experience_match = 1.0
    if job_requirements.experience_required and resume_keywords.experience:
        max_exp = max(resume_keywords.experience.values()) if resume_keywords.experience else 0
        if max_exp < job_requirements.experience_required:
            experience_match = max_exp / job_requirements.experience_required
    
    # Calculate education match
    education_match = 0.0
    if job_requirements.education_required and resume_keywords.education:
        for edu_req in job_requirements.education_required:
            if any(re.search(rf'\b{re.escape(edu_req)}\b', edu, re.IGNORECASE) for edu in resume_keywords.education):
                education_match = 1.0
                break
    else:
        education_match = 1.0  # If no education requirements specified
    
    # Calculate weighted score
    required_weight = 0.6
    preferred_weight = 0.2
    experience_weight = 0.1
    education_weight = 0.1
    
    required_score = len(matched_required) / max(len(job_requirements.required_skills), 1) if job_requirements.required_skills else 1.0
    preferred_score = len(matched_preferred) / max(len(job_requirements.preferred_skills), 1) if job_requirements.preferred_skills else 1.0
    
    weighted_score = (
        required_score * required_weight +
        preferred_score * preferred_weight +
        experience_match * experience_weight +
        education_match * education_weight
    )
    
    # Scale to max score
    final_score = weighted_score * max_score
    final_score = round(min(final_score, max_score), 1)
    
    # All matched keywords
    all_matched = matched_required + matched_preferred
    all_missing = missing_required + missing_preferred
    
    # Generate feedback
    feedback = "Your resume "
    if final_score >= 30:
        feedback += "strongly matches the job requirements."
    elif final_score >= 20:
        feedback += "matches many of the job requirements but is missing some key elements."
    elif final_score >= 10:
        feedback += "only partially matches the job requirements."
    else:
        feedback += "has significant gaps compared to the job requirements."
    
    if missing_required:
        feedback += f" Critical missing skills include: {', '.join(missing_required[:3])}"
        if len(missing_required) > 3:
            feedback += f" and {len(missing_required) - 3} more"
        feedback += "."
    
    return final_score, all_matched, all_missing, feedback


def calculate_overall_impression_score(
    content_match_score: float,
    format_score: float,
    section_score: float
) -> Tuple[float, str]:
    """
    Calculate an overall impression score based on other dimensions
    
    Args:
        content_match_score: Score for content matching
        format_score: Score for format compatibility
        section_score: Score for section quality
        
    Returns:
        Tuple containing overall score and feedback
    """
    # Calculate weighted average of other scores, normalized to a 0-10 scale
    max_score = 10.0
    weighted_sum = (
        (content_match_score / 40) * 0.5 +
        (format_score / 20) * 0.25 +
        (section_score / 30) * 0.25
    ) * max_score
    
    overall_score = round(min(weighted_sum, max_score), 1)
    
    # Generate feedback
    feedback = "Overall, your resume is "
    if overall_score >= 8:
        feedback += "excellent and likely to pass ATS screening with high marks."
    elif overall_score >= 6:
        feedback += "good and has a good chance of passing ATS screening."
    elif overall_score >= 4:
        feedback += "acceptable but may struggle with some ATS systems."
    else:
        feedback += "in need of significant improvement to pass ATS screening."
    
    return overall_score, feedback


def generate_improvement_suggestions(
    content_match: ContentMatch,
    format_compatibility: FormatCompatibility,
    section_analysis: SectionAnalysis
) -> List[str]:
    """
    Generate improvement suggestions based on scoring results
    
    Args:
        content_match: Content match results
        format_compatibility: Format compatibility results
        section_analysis: Section analysis results
        
    Returns:
        List of improvement suggestions
    """
    suggestions = []
    
    # Add content match suggestions
    if content_match.missing_keywords:
        suggestions.append(
            f"Add these key missing skills to your resume: {', '.join(content_match.missing_keywords[:5])}"
            + (f" and {len(content_match.missing_keywords) - 5} more" if len(content_match.missing_keywords) > 5 else "")
        )
    
    # Add format suggestions
    for issue in format_compatibility.issues[:3]:
        if "bullet points" in issue.lower():
            suggestions.append("Use bullet points to list your skills and achievements")
        elif "date" in issue.lower():
            suggestions.append("Use consistent date formatting throughout your resume (e.g., 'Month Year - Month Year')")
        elif "action verbs" in issue.lower():
            suggestions.append("Start achievement statements with strong action verbs (led, achieved, implemented, etc.)")
        elif "length" in issue.lower():
            suggestions.append("Adjust your resume length to be between 1-2 pages (around 600-1200 words)")
        elif "pronouns" in issue.lower():
            suggestions.append("Remove personal pronouns (I, me, my) from your resume")
        elif "tenses" in issue.lower():
            suggestions.append("Use consistent verb tense throughout your experience section")
        elif "pdf" in issue.lower():
            suggestions.append("Ensure your PDF contains searchable text rather than scanned images")
    
    # Add section-specific suggestions
    weak_sections = [s for s in section_analysis.sections if s.score < (s.max_score * 0.7)]
    for section in weak_sections[:3]:
        if "contact" in section.name.lower():
            suggestions.append("Include complete contact information: email, phone, and LinkedIn profile")
        elif "summary" in section.name.lower():
            suggestions.append("Add a concise professional summary (50-200 words) that highlights your relevant qualifications")
        elif "experience" in section.name.lower():
            suggestions.append("Enhance your experience section with clear dates, company names, and bullet points with measurable achievements")
        elif "education" in section.name.lower():
            suggestions.append("Include complete education details with institution names, degrees, and graduation dates")
        elif "skills" in section.name.lower():
            suggestions.append("Expand your skills section with more relevant technical and soft skills")
        elif "certification" in section.name.lower():
            suggestions.append("Add relevant certifications with names, issuing organizations, and dates")
    
    # Limit to top 10 suggestions
    return suggestions[:10]


def calculate_resume_score(
    resume_text: str,
    resume_filename: str,
    resume_keywords: KeywordAnalysis,
    job_requirements: JobRequirements,
    job_title: str,
    file_type: str
) -> ResumeScoreResponse:
    """
    Calculate the complete resume score across all dimensions
    
    Args:
        resume_text: The text content of the resume
        resume_filename: The name of the resume file
        resume_keywords: Keywords extracted from the resume
        job_requirements: Requirements extracted from the job description
        job_title: The job title
        file_type: The file type of the resume
        
    Returns:
        Complete resume score response
    """
    logger.info(f"Calculating score for resume: {resume_filename}")
    
    # Identify sections in the resume
    sections = identify_resume_sections(resume_text)
    
    # Calculate content match score
    content_score, matched_keywords, missing_keywords, content_feedback = calculate_content_match_score(
        resume_keywords, job_requirements
    )
    content_match = ContentMatch(
        score=content_score,
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords,
        feedback=content_feedback
    )
    
    # Calculate format compatibility score
    format_score, format_issues, format_feedback = analyze_format_compatibility(
        resume_text, file_type
    )
    format_compatibility = FormatCompatibility(
        score=format_score,
        issues=format_issues,
        feedback=format_feedback
    )
    
    # Calculate section scores
    section_score, section_scores, section_feedback = evaluate_section_scores(sections)
    section_analysis = SectionAnalysis(
        score=section_score,
        sections=section_scores,
        feedback=section_feedback
    )
    
    # Calculate overall impression score
    overall_score, overall_feedback = calculate_overall_impression_score(
        content_score, format_score, section_score
    )
    overall = OverallScore(
        score=overall_score,
        feedback=overall_feedback
    )
    
    # Calculate total score
    total_score = content_score + format_score + section_score + overall_score
    
    # Generate improvement suggestions
    suggestions = generate_improvement_suggestions(
        content_match, format_compatibility, section_analysis
    )
    
    # Create response
    response = ResumeScoreResponse(
        timestamp=datetime.datetime.now(),
        filename=resume_filename,
        content_match=content_match,
        format_compatibility=format_compatibility,
        section_analysis=section_analysis,
        overall_score=overall,
        total_score=total_score,
        keyword_analysis=resume_keywords,
        job_requirements=job_requirements,
        improvement_suggestions=suggestions
    )
    
    logger.info(f"Resume score calculated: {total_score}/100")
    return response