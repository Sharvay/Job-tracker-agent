from typing import Optional
import re

def clean_content_by_site(content: str, url: str) -> str:
    """
    Clean parsed content based on the job site
    
    Args:
        content: The parsed text content
        url: The job posting URL (to detect which site)
    
    Returns:
        Cleaned content with irrelevant sections removed
    """
    
    # Detect which site we're dealing with
    if 'linkedin.com' in url:
        return clean_linkedin_content(content)
    elif 'indeed.com' in url:
        return clean_indeed_content(content)
    elif 'glassdoor.com' in url:
        return clean_glassdoor_content(content)
    else:
        # Generic cleaning for unknown sites
        return clean_generic_content(content)


def clean_linkedin_content(content: str) -> str:
    """
    Clean LinkedIn-specific content
    """
    # Find the cutoff point
    cutoff_phrases = [
        "Sign in to create job alert",
        "Create job alert",
        "Similar jobs",
        "People also viewed",
        "Show more jobs like this"
    ]
    
    # Find the earliest occurrence of any cutoff phrase
    earliest_index = len(content)
    found_phrase = None
    
    for phrase in cutoff_phrases:
        index = content.find(phrase)
        if index != -1 and index < earliest_index:
            earliest_index = index
            found_phrase = phrase
    
    # Cut content if we found a cutoff phrase
    if found_phrase:
        content = content[:earliest_index]
    
    return content.strip()


def clean_indeed_content(content: str) -> str:
    """
    Clean Indeed-specific content
    """
    cutoff_phrases = [
        "Report job",
        "Not interested",
        "People also searched",
        "Jobs you might be interested in"
    ]
    
    earliest_index = len(content)
    found_phrase = None
    
    for phrase in cutoff_phrases:
        index = content.find(phrase)
        if index != -1 and index < earliest_index:
            earliest_index = index
            found_phrase = phrase
    
    if found_phrase:
        content = content[:earliest_index]
    
    return content.strip()


def clean_glassdoor_content(content: str) -> str:
    """
    Clean Glassdoor-specific content
    """
    cutoff_phrases = [
        "Sign In to see similar jobs",
        "Jobs You Might Like",
        "Similar Jobs"
    ]
    
    earliest_index = len(content)
    found_phrase = None
    
    for phrase in cutoff_phrases:
        index = content.find(phrase)
        if index != -1 and index < earliest_index:
            earliest_index = index
            found_phrase = phrase
    
    if found_phrase:
        content = content[:earliest_index]
    
    return content.strip()


def clean_generic_content(content: str) -> str:
    """
    Generic cleaning for unknown sites
    
    Removes common footer/navigation patterns
    """
    # Common patterns to remove
    patterns = [
        r'Follow us on.*',
        r'Subscribe to.*',
        r'Copyright \d{4}.*',
        r'Privacy Policy.*',
        r'Terms of Service.*'
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    return content.strip()