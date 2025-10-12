from langgraph.graph import StateGraph, END
from state import JobTrackerState
from nodes import (
    fetch_job_page,
    parse_content,
    extract_details,
    prepare_tracker_entry,
    save_to_tracker
)

def create_job_tracker_graph():
    """
    Creates the LangGraph workflow for job tracking
    """
    
    # Create the graph with our State
    graph = StateGraph(JobTrackerState)
    
    # Add all nodes to the graph
    graph.add_node("fetch", fetch_job_page)
    graph.add_node("parse", parse_content)
    graph.add_node("extract", extract_details)
    graph.add_node("prepare", prepare_tracker_entry)
    graph.add_node("save", save_to_tracker)
    
    # Define the flow (edges between nodes)
    graph.set_entry_point("fetch")  # Start here
    graph.add_edge("fetch", "parse")       # fetch → parse
    graph.add_edge("parse", "extract")     # parse → extract
    graph.add_edge("extract", "prepare")   # extract → prepare
    graph.add_edge("prepare", "save")      # prepare → save
    graph.add_edge("save", END)            # save → END
    
    # Compile the graph into a runnable app
    app = graph.compile()
    
    return app

# Create the app
job_tracker_app = create_job_tracker_graph()
