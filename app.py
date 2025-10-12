import streamlit as st
from graph import job_tracker_app
import json
from datetime import datetime
import pandas as pd

# Page config
st.set_page_config(
    page_title="Job Tracker Agent",
    # page_icon="💼",
    layout="wide"
)

# Title
st.title("Job Tracker Agent")
st.markdown("Automatically extract job details and save to Google Sheets using LangGraph")

# Sidebar for settings
st.sidebar.header("Settings")
mode = st.sidebar.radio(
    "Processing Mode",
    ["Single Job", "Batch Jobs"],
    help="Process one job or multiple jobs at once"
)

# Initialize session state for logs
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'results' not in st.session_state:
    st.session_state.results = []

# Main content
if mode == "Single Job":
    st.header("Single Job Processing")
    
    # Input
    job_url = st.text_input(
        "Enter Job URL",
        placeholder="https://www.linkedin.com/jobs/view/...",
        help="Paste the full job posting URL"
    )
    
    # Process button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        process_button = st.button("Process Job", use_container_width=True, type="primary")
    
    if process_button and job_url:
        # Clear previous logs
        st.session_state.logs = []
        
        # Progress container
        progress_container = st.container()
        
        with progress_container:
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Log container
            log_container = st.expander("Processing Logs", expanded=True)
            
            try:
                # Prepare input
                initial_input = {"job_url": job_url}
                
                # Capture stdout to show real logs
                import io
                import sys
                from contextlib import redirect_stdout
                
                log_capture = io.StringIO()
                
                # Show initial progress
                status_text.text("Running LangGraph workflow...")
                progress_bar.progress(10)
                
                # Run the graph and capture logs
                with redirect_stdout(log_capture):
                    final_state = job_tracker_app.invoke(initial_input)
                
                # Display captured logs
                logs = log_capture.getvalue()
                with log_container:
                    st.code(logs, language=None)
                
                # Update progress
                progress_bar.progress(100)
                status_text.text("Complete!")
                
                # Check results and display
                if final_state.get('save_status') == 'success':
                    st.success("Job Added to Tracker!")
                  
                
                else:
                    status_text.text("Failed")
                    st.error(f"Error: {final_state.get('error_message', 'Unknown error')}")
                
            except Exception as e:
                progress_bar.progress(0)
                status_text.text("Error occurred")
                st.error(f"An error occurred: {str(e)}")
                with log_container:
                    st.error(f"Exception: {str(e)}")
    
    elif process_button and not job_url:
        st.warning("Please enter a job URL")

else:  # Batch mode
    st.header("Batch Job Processing")
    
    # Input method
    input_method = st.radio(
        "Input Method",
        ["Paste URLs", "Upload File"],
        horizontal=True
    )
    
    job_urls = []
    
    if input_method == "Paste URLs":
        urls_text = st.text_area(
            "Enter Job URLs (one per line)",
            height=200,
            placeholder="https://www.linkedin.com/jobs/view/...\nhttps://www.linkedin.com/jobs/view/...\nhttps://www.linkedin.com/jobs/view/..."
        )
        if urls_text:
            job_urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
    
    else:  # Upload file
        uploaded_file = st.file_uploader(
            "Upload a text file with URLs (one per line)",
            type=['txt']
        )
        if uploaded_file:
            content = uploaded_file.read().decode('utf-8')
            job_urls = [url.strip() for url in content.split('\n') if url.strip()]
    
    # Show count
    if job_urls:
        st.info(f"{len(job_urls)} jobs to process")
    
    # Process button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        batch_button = st.button(
            f"Process {len(job_urls)} Jobs" if job_urls else "Process Batch",
            use_container_width=True,
            type="primary",
            disabled=len(job_urls) == 0
        )
    
    if batch_button and job_urls:
        st.markdown("---")
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_container = st.empty()
        
        # Results tracking
        results = []
        successful = 0
        duplicates = 0
        failed = 0
        
        # Process each job
        for i, url in enumerate(job_urls):
            progress = (i + 1) / len(job_urls)
            progress_bar.progress(progress)
            status_container.info(f"Processing job {i+1}/{len(job_urls)}: {url[:50]}...")
            
            try:
                final_state = job_tracker_app.invoke({"job_url": url})
                
                if final_state.get('save_status') == 'success':
                    successful += 1
                    details = final_state['final_details']
                    results.append({
                        'Status': 'Success',
                        'Job Title': details['Job Title'],
                        'Company': details['Company'],
                        'Location': details['Location'],
                        'Row': final_state.get('tracker_id'),
                        'URL': url
                    })

                else:
                    failed += 1
                    results.append({
                        'Status': 'Failed',
                        'Job Title': '-',
                        'Company': '-',
                        'Location': '-',
                        'Row': '-',
                        'URL': url
                    })
            
            except Exception as e:
                failed += 1
                results.append({
                    'Status': f'Error',
                    'Job Title': '-',
                    'Company': '-',
                    'Location': '-',
                    'Row': '-',
                    'URL': url
                })
        
        # Complete
        progress_bar.progress(1.0)
        status_container.success("Batch processing complete!")
        
        # Summary
        st.markdown("---")
        st.header("Batch Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Successful", successful)
        with col2:
            st.metric("Failed", failed)
        with col3:
            st.metric("Total", len(job_urls))
        
        # Results table
        st.markdown("### Detailed Results")
        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)
        
        # Download results
        csv = df.to_csv(index=False)
        st.download_button(
            label=" Download Results CSV",
            data=csv,
            file_name=f"job_tracker_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built with LangGraph | Powered by OpenAI & Google Sheets</p>
    </div>
    """,
    unsafe_allow_html=True
)

