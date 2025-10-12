from typing import Dict, Any
from state import JobTrackerState
from datetime import datetime

def prepare_tracker_entry(state: JobTrackerState) -> Dict[str, Any]:
    """
    Node 5: Prepare data for tracker
    
    Formats validated job details into tracker-ready format
    """
    print(f"Preparing tracker entry...")
    
    # Check if we have extracted details
    if not state.get('extracted_details'):
        print("No extracted_details found!")
        return {
            "error_message": "No details to prepare"
        }
    
    try:
        details = state['extracted_details']
        
        # Create tracker entry with additional metadata
        tracker_entry = {
            # Core job info
            "Job Title": details.get('job_title', 'N/A'),
            "Company": details.get('company', 'N/A'),
            "Location": details.get('location', 'N/A'),
            "Job Type": details.get('job_type', 'N/A'),
            "Workplace Type": details.get('workplace_type', 'N/A'),
            "Salary": details.get('salary', 'Not mentioned'),
            "Experience Required": details.get('experience_required', 'Not mentioned'),
            
            # Skills as comma-separated string
            "Skills Required": ", ".join(details.get('skills_required', [])),
            
            # Dates
            "Posted Date": details.get('posted_date', 'N/A'),
            "Application Deadline": details.get('application_deadline', 'Not mentioned'),
            
            # Metadata (tracking info)
            "Date Added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Job URL": state['job_url'],
            "Notes": "",  # Empty for user to fill later
        }
        
        print("Tracker entry prepared!")

        return {
            "final_details": tracker_entry
        }
        
    except Exception as e:
        print(f"Error preparing tracker entry: {str(e)}")
        return {
            "error_message": f"Preparation error: {str(e)}"
        }