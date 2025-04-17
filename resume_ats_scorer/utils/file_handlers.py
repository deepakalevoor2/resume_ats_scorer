import os
import logging
import tempfile
from typing import BinaryIO, Optional
from pathlib import Path
import shutil

import PyPDF2
import docx
import html2text
from fastapi import UploadFile, HTTPException

logger = logging.getLogger(__name__)


async def save_upload_file(upload_file: UploadFile, destination: str) -> None:
    """
    Save an uploaded file to the specified destination
    
    Args:
        upload_file: The uploaded file
        destination: The path where the file should be saved
    """
    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    except Exception as e:
        logger.error(f"Error saving uploaded file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")
    finally:
        upload_file.file.close()
        
    logger.info(f"File saved to {destination}")


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text as a string
    """
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not extract text from PDF: {str(e)}")
    
    return text


def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from a DOCX file
    
    Args:
        file_path: Path to the DOCX file
        
    Returns:
        Extracted text as a string
    """
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not extract text from DOCX: {str(e)}")
    
    return text


def extract_text_from_txt(file_path: str) -> str:
    """
    Extract text from a TXT file
    
    Args:
        file_path: Path to the TXT file
        
    Returns:
        Extracted text as a string
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()
    except Exception as e:
        logger.error(f"Error extracting text from TXT: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not extract text from TXT: {str(e)}")
    
    return text


def extract_text_from_html(file_path: str) -> str:
    """
    Extract text from an HTML file
    
    Args:
        file_path: Path to the HTML file
        
    Returns:
        Extracted text as a string
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            html_content = file.read()
        
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        text = h.handle(html_content)
    except Exception as e:
        logger.error(f"Error extracting text from HTML: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not extract text from HTML: {str(e)}")
    
    return text


def extract_text_from_file(file_path: str, file_type: str) -> str:
    """
    Extract text from a file based on its type
    
    Args:
        file_path: Path to the file
        file_type: Type of the file (pdf, docx, txt, html)
        
    Returns:
        Extracted text as a string
    """
    if file_type.lower() == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_type.lower() == 'docx':
        return extract_text_from_docx(file_path)
    elif file_type.lower() == 'txt':
        return extract_text_from_txt(file_path)
    elif file_type.lower() == 'html':
        return extract_text_from_html(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")