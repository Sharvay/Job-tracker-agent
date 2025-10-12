from bs4 import BeautifulSoup
from typing import Dict, Any
from state import JobTrackerState
from utils.content_cleaner import clean_content_by_site

def parse_content(state: JobTrackerState) -> Dict[str, Any]:
    """
    Node 2: Parse HTML and extract clean text content
    
    Takes raw_html from state and returns parsed_content
    """
    print(f"Parsing HTML content...")
    
    # Check if we have HTML to parse
    if not state.get('raw_html'):
        print("No raw_html found in state!")
        return {
            "error_message": "No HTML content to parse"
        }
    
    try:
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(state['raw_html'], 'lxml')
        
        # Remove script and style elements
        for script in soup(['script', 'style', 'nav', 'footer', 'header']):
            script.decompose()
        
        # Get text content
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up: remove excessive whitespace
        lines = [line.strip() for line in text.splitlines()]
        lines = [line for line in lines if line]  # Remove empty lines
        parsed_text = '\n'.join(lines)
        
        # Apply site-specific cleaning
        # print(f"   Applying site-specific cleaning...")
        cleaned_text = clean_content_by_site(parsed_text, state['job_url'])
        
        # print(f"Final cleaned text: {len(cleaned_text)} characters")
        
        return {
            "parsed_content": cleaned_text
        }

    except Exception as e:
        print(f"Error parsing HTML: {str(e)}")
        return {
            "error_message": f"Parsing error: {str(e)}"
        }