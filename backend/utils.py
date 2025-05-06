import fitz  # PyMuPDF
import pdfplumber
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import os
from typing import List, Optional

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF using PyMuPDF
    """
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def extract_text_from_pdf_plumber(file_path: str) -> str:
    """
    Extract text from PDF using pdfplumber (alternative method)
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF using pdfplumber: {str(e)}")

def scrape_url_content(url: str, use_playwright: bool = False) -> str:
    """
    Scrape content from a URL using either requests+BeautifulSoup or Playwright
    """
    if use_playwright:
        return scrape_with_playwright(url)
    else:
        return scrape_with_requests(url)

def scrape_with_requests(url: str) -> str:
    """
    Scrape content using requests and BeautifulSoup
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        raise Exception(f"Error scraping URL with requests: {str(e)}")

def scrape_with_playwright(url: str) -> str:
    """
    Scrape content using Playwright (for JavaScript-heavy sites)
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            # Wait for the content to load
            page.wait_for_load_state('networkidle')
            
            # Get the page content
            content = page.content()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
                
            # Get text
            text = soup.get_text()
            
            # Clean up the text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            browser.close()
            return text
    except Exception as e:
        raise Exception(f"Error scraping URL with Playwright: {str(e)}")

def save_uploaded_file(file_content: bytes, filename: str) -> str:
    """
    Save uploaded file to disk
    """
    try:
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save file
        file_path = os.path.join("uploads", filename)
        with open(file_path, "wb") as f:
            f.write(file_content)
            
        return file_path
    except Exception as e:
        raise Exception(f"Error saving file: {str(e)}") 