from typing import TypedDict, Optional, List, Dict, Any

class JobTrackerState(TypedDict, total=False):
    """
    This is our State - the data container that flows through all nodes.
    Each node will read from this and update it.
    """
    
    # Input (what we start with)
    job_url: str
    
    # After fetching the webpage
    raw_html: Optional[str]  # Optional because it doesn't exist at start
    fetch_status: Optional[str]  # "success" or "failed"
    
    # After parsing
    parsed_content: Optional[str]  # Cleaned text from HTML
    
    # After extraction
    extracted_details: Optional[Dict[str, Any]]  # Dict with job info
    
    # After LLM validation
    validation_result: Optional[Dict[str, Any]]  # LLM's judgment
    is_valid: Optional[bool]  # Did validation pass?
    
    # Final data ready for tracker
    final_details: Optional[Dict[str, Any]]  # Cleaned & validated data
    
    # After saving to tracker
    save_status: Optional[str]  # "success" or "failed"
    tracker_id: Optional[str]  # Row ID in tracker
    
    # For error handling
    error_message: Optional[str]  # If something goes wrong