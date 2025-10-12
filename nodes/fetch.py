import requests
from typing import Dict, Any
from state import JobTrackerState

def fetch_job_page(state: JobTrackerState) -> Dict[str, Any]:
    """
    Node 1: Fetch the job posting webpage
    """
    print(f"Fetching job page: {state['job_url']}")
    
    try:
        response = requests.get(state['job_url'], timeout=10)
        
        if response.status_code == 200:
            print("Page fetched successfully!")
            return {
                "raw_html": response.text,
                "fetch_status": "success"
            }
        else:
            print(f"Failed to fetch. Status code: {response.status_code}")
            return {
                "fetch_status": "failed",
                "error_message": f"HTTP {response.status_code}"
            }
            
    except Exception as e:
        print(f"Error fetching page: {str(e)}")
        return {
            "fetch_status": "failed",
            "error_message": str(e)
        }