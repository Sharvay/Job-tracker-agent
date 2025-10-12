from typing import Dict, Any
from state import JobTrackerState
import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv

# Google Sheets configuration
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def save_to_tracker(state: JobTrackerState) -> Dict[str, Any]:
    """
    Node 6: Save job details to Google Sheets tracker
    
    Appends the job to a Google Sheet
    """
    print(f"Saving to Google Sheets tracker...")
    
    # Check if we have final details
    if not state.get('final_details'):
        print("No final_details found!")
        return {
            "error_message": "No details to save"
        }
    
    try:
        final_details = state['final_details']
        
        # Authenticate with Google Sheets
        creds = Credentials.from_service_account_file(
            'credentials.json',
            scopes=SCOPES
        )
        client = gspread.authorize(creds)
        
        # Open the sheet
        # REPLACE THIS WITH YOUR SHEET ID
        SHEET_ID = os.getenv("SHEET_ID")
        spreadsheet = client.open_by_key(SHEET_ID)
        worksheet = spreadsheet.sheet1  # First sheet
        
        # Prepare row data (must match column order in sheet)
        row_data = [
            final_details['Job Title'],
            final_details['Company'],
            final_details['Location'],
            final_details['Job Type'],
            final_details['Workplace Type'],
            final_details['Salary'],
            final_details['Experience Required'],
            final_details['Skills Required'],
            final_details['Posted Date'],
            final_details['Application Deadline'],
            final_details['Date Added'],
            final_details['Job URL'],
            final_details['Notes']
        ]
        
        # Append the row
        worksheet.append_row(row_data)
        
        # Get the row number (last row)
        tracker_id = str(len(worksheet.get_all_values()))
        
        print(f"Saved to Google Sheets! Row #{tracker_id}")
        print(f"View at: https://docs.google.com/spreadsheets/d/{SHEET_ID}")
        
        return {
            "save_status": "success",
            "tracker_id": tracker_id
        }
        
    except FileNotFoundError:
        print(f"credentials.json not found!")
        return {
            "save_status": "failed",
            "error_message": "credentials.json file not found"
        }
    
    except Exception as e:
        print(f"Error saving to Google Sheets: {str(e)}")
        return {
            "save_status": "failed",
            "error_message": f"Save error: {str(e)}"
        }