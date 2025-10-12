from typing import Dict, Any
from state import JobTrackerState
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def extract_details(state: JobTrackerState) -> Dict[str, Any]:
    """
    Node 3: Extract job details using LLM
    
    Uses an LLM to extract structured information from parsed content
    """
    print(f"Extracting job details using LLM...")
    
    # Check if we have parsed content
    if not state.get('parsed_content'):
        print("No parsed_content found in state!")
        return {
            "error_message": "No parsed content to extract from"
        }
    
    try:
        # Initialize the LLM
        llm = ChatOpenAI(
            model="gpt-4o-mini",  # Cheaper and faster model
            temperature=0,  # Deterministic output
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Create the prompt
        system_prompt = """You are a job posting analyzer. Extract the following information from the job posting text:

1. job_title: The position title
2. company: Company name
3. location: Job location (city/state or "Remote")
4. job_type: Full-time, Part-time, Contract, Internship, etc.
5. workplace_type: Remote, Hybrid, or Onsite
6. salary: Salary range if mentioned, otherwise "Not mentioned"
7. experience_required: Years of experience needed (e.g., "2-4 years")
8. skills_required: List of top 5-7 required skills
9. posted_date: When the job was posted, if available
10. application_deadline: Deadline if mentioned

Return ONLY a valid JSON object with these fields. If information is not found, use "Not mentioned" or an empty list for skills.

Example format:
{
    "job_title": "Senior Software Engineer",
    "company": "Tech Corp",
    "location": "San Francisco, CA",
    "job_type": "Full-time",
    "workplace_type": "Hybrid",
    "salary": "$120k-$180k",
    "experience_required": "5+ years",
    "skills_required": ["Python", "AWS", "Docker", "React", "PostgreSQL"],
    "posted_date": "2 days ago",
    "application_deadline": "Not mentioned"
}"""
        
        # Truncate content if too long (to save tokens)
        content = state['parsed_content']
        max_chars = 8000  # Limit content size
        if len(content) > max_chars:
            content = content[:max_chars] + "\n\n[Content truncated...]"
            print(f"Content truncated to {max_chars} characters")
        
        # Create messages
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Job Posting Content:\n\n{content}")
        ]
        
        # Call the LLM
        print("Calling LLM...")
        response = llm.invoke(messages)
        
        # Parse the JSON response
        extracted_data = json.loads(response.content)
        
        print("Successfully extracted job details!")

        return {
            "extracted_details": extracted_data
        }
        
    except json.JSONDecodeError as e:
        print(f"Error parsing LLM response as JSON: {str(e)}")
        print(f"Response was: {response.content[:200]}...")
        return {
            "error_message": f"JSON parsing error: {str(e)}"
        }
    
    except Exception as e:
        print(f"Error extracting details: {str(e)}")
        return {
            "error_message": f"Extraction error: {str(e)}"
        }