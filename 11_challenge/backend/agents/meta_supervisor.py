"""
Meta-Supervisor for Multi-Agent System
Orchestrates Research Team and Response Team
Based on proven patterns from example code lesson 6
"""

import operator
from typing import Annotated, List, TypedDict
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from .helper_functions import create_team_supervisor, get_last_message, join_graph


class State(TypedDict):
    """State for meta-supervisor."""
    messages: Annotated[List[BaseMessage], operator.add]
    next: str


def create_meta_supervisor(llm: ChatOpenAI, research_chain, response_chain):
    """Create the meta-supervisor that orchestrates research and response teams.
    
    Based on proven pattern from example code lesson 6.
    """
    
    # Create Meta-Supervisor Node
    supervisor_node = create_team_supervisor(
        llm,
        ("You are a supervisor managing a student loan assistance system with two teams:"
        " Research team (finds information) and Response team (formats responses)."
        
        " IMPORTANT RULES:"
        " 1. ALWAYS start with Research team to gather information"
        " 2. Then use Response team to format the information into a clear answer"
        " 3. For time-sensitive questions (current rates, recent changes), ensure Research team gets current information"
        " 4. When both teams have completed their work, respond with FINISH"
        " 5. Never skip the Research team - information gathering is always needed first"),
        ["Research team", "Response team"],
    )
    
    # Create Super Graph
    super_graph = StateGraph(State)
    super_graph.add_node("Research team", get_last_message | research_chain | join_graph)
    super_graph.add_node("Response team", get_last_message | response_chain | join_graph)
    super_graph.add_node("supervisor", supervisor_node)
    
    # Add edges
    super_graph.add_edge("Research team", "supervisor")
    super_graph.add_edge("Response team", "supervisor")
    super_graph.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        {
            "Response team": "Response team",
            "Research team": "Research team",
            "FINISH": END,
        },
    )
    
    super_graph.set_entry_point("supervisor")
    compiled_super_graph = super_graph.compile()
    
    return compiled_super_graph 