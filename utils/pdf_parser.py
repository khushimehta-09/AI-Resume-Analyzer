"""
PDF Parser Module
Extracts text from PDF resumes
"""

import PyPDF2
import pdfplumber
from typing import List, Dict


class PDFParser:
    """Parse and extract text from PDF files"""
    
    @staticmethod
    def extract_text_pdfplumber(pdf_path: str) -> str:
        """
        Extract text from PDF using pdfplumber
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text from PDF
        """
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            return text if text.strip() else "No text found in PDF"
        except Exception as e:
            raise Exception(f"Error extracting PDF with pdfplumber: {str(e)}")
    
    @staticmethod
    def extract_text_pypdf2(pdf_path: str) -> str:
        """
        Extract text from PDF using PyPDF2
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text from PDF
        """
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            return text if text.strip() else "No text found in PDF"
        except Exception as e:
            raise Exception(f"Error extracting PDF with PyPDF2: {str(e)}")
    
    @staticmethod
    def extract_text(pdf_path: str, method: str = "pdfplumber") -> str:
        """
        Extract text from PDF using specified method
        
        Args:
            pdf_path: Path to PDF file
            method: "pdfplumber" or "pypdf2"
            
        Returns:
            Extracted text from PDF
        """
        if method == "pdfplumber":
            return PDFParser.extract_text_pdfplumber(pdf_path)
        elif method == "pypdf2":
            return PDFParser.extract_text_pypdf2(pdf_path)
        else:
            raise ValueError(f"Unknown method: {method}")
    
    @staticmethod
    def extract_pages_info(pdf_path: str) -> Dict:
        """
        Extract detailed page information from PDF
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with page information
        """
        try:
            pages_info = {
                "total_pages": 0,
                "pages": []
            }
            
            with pdfplumber.open(pdf_path) as pdf:
                pages_info["total_pages"] = len(pdf.pages)
                for idx, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    tables = page.extract_tables()
                    pages_info["pages"].append({
                        "page_number": idx + 1,
                        "text": text if text else "",
                        "tables": tables if tables else []
                    })
            
            return pages_info
        except Exception as e:
            raise Exception(f"Error extracting page info: {str(e)}")
