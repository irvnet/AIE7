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
        "You are a supervisor tasked with managing a conversation between the"
        " following teams: Research team, Response team. Given the following user request,"
        " respond with the worker to act next. Each worker will perform a"
        " task and respond with their results and status. When all workers are finished,"
        " you must respond with FINISH.",
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