"""
Response Team for Multi-Agent System
Implements Document Writing Team with NoteTaker, DocWriter, CopyEditor, EmpathyEditor
Based on proven patterns from example code lesson 6
"""

import functools
import operator
from typing import Annotated, List, TypedDict
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from .helper_functions import agent_node, create_agent, create_team_supervisor, enter_chain
from .tools import (
    create_outline, read_document, write_document, edit_document,
    create_complaint_reference_tool, create_document_prelude_function
)


class DocWritingState(TypedDict):
    """State for document writing team."""
    messages: Annotated[List[BaseMessage], operator.add]
    team_members: str
    next: str
    current_files: str


def create_response_team(llm: ChatOpenAI, complaint_retriever):
    """Create the response team with direct answer agents.
    
    Based on proven pattern from example code lesson 6.
    """
    
    # Create tools
    document_tools = [create_outline, read_document, write_document, edit_document]
    complaint_tool = create_complaint_reference_tool(complaint_retriever)
    prelude = create_document_prelude_function()
    
    # Create Direct Answer Agent
    direct_answer_agent = create_agent(
        llm,
        [read_document],  # Give it at least one tool to avoid empty array error
        ("You are an expert student loan advisor who provides clear, direct answers to user questions."
        " Your role is to take the research information and provide a concise, accurate response."
        
        " CRITICAL INSTRUCTIONS:"
        " 1. If the research contains 'CURRENT INFORMATION FROM EXTERNAL SOURCES', prioritize that information"
        " 2. For interest rates, clearly state the academic year and source"
        " 3. Focus on answering the user's question directly with the specific information they requested"
        " 4. Be helpful, accurate, and concise"
        " 5. Do not create documents or outlines unless specifically requested"
        " 6. If you see current 2024-2025 rates, use those instead of any older information"
        " 7. If the research says 'I don't have current information available', be honest and say you don't have current information"
        " 8. Never make up information - if you don't have current data, say so clearly"),
    )
    direct_answer_node = functools.partial(
        agent_node, agent=direct_answer_agent, name="DirectAnswer"
    )
    
    # Create Document Writer Agent (for complex requests only)
    document_writer_agent = create_agent(
        llm,
        [write_document, edit_document, read_document, create_outline, complaint_tool],
        ("You are an expert document writer for complex student loan assistance requests."
        " Only create documents when the user specifically requests detailed documentation,"
        " outlines, or comprehensive guides. For simple questions, let the DirectAnswer agent handle it."
        "Below are files currently in your directory:\n{current_files}"),
    )
    context_aware_document_writer_agent = prelude | document_writer_agent
    document_writing_node = functools.partial(
        agent_node, agent=context_aware_document_writer_agent, name="DocumentWriter"
    )
    
    # Create Quality Check Agent
    quality_check_agent = create_agent(
        llm,
        [read_document],
        ("You are a quality assurance expert who reviews responses for accuracy, clarity, and completeness."
        " Ensure the response directly answers the user's question and is factually correct."
        "Below are files currently in your directory:\n{current_files}"),
    )
    context_aware_quality_check_agent = prelude | quality_check_agent
    quality_check_node = functools.partial(
        agent_node, agent=context_aware_quality_check_agent, name="QualityCheck"
    )
    
    # Create Response Team Supervisor
    response_supervisor = create_team_supervisor(
        llm,
        ("You are a supervisor managing a response team with two workers:"
        " DirectAnswer (provides direct answers to simple questions) and DocumentWriter (creates documents for complex requests)."
        
        " CRITICAL ROUTING RULES:"
        " 1. Use DirectAnswer for:"
        "    - Questions about rates, amounts, deadlines, updates, policies"
        "    - Information requests (what, when, how much, etc.)"
        "    - Simple factual questions"
        "    - Status updates and current information"
        
        " 2. Use DocumentWriter ONLY for:"
        "    - User explicitly requests 'create a document', 'write a guide', 'make an outline'"
        "    - User asks for 'detailed documentation' or 'comprehensive guide'"
        "    - User wants something saved to a file"
        
        " 3. DEFAULT: Always use DirectAnswer unless user specifically asks for document creation"
        " 4. When the response is complete, respond with FINISH"),
        ["DirectAnswer", "DocumentWriter"],
    )
    
    # Create Response Team Graph
    response_graph = StateGraph(DocWritingState)
    response_graph.add_node("DirectAnswer", direct_answer_node)
    response_graph.add_node("DocumentWriter", document_writing_node)
    response_graph.add_node("supervisor", response_supervisor)
    
    # Add edges
    response_graph.add_edge("DirectAnswer", "supervisor")
    response_graph.add_edge("DocumentWriter", "supervisor")
    
    response_graph.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        {
            "DirectAnswer": "DirectAnswer",
            "DocumentWriter": "DocumentWriter",
            "FINISH": END,
        },
    )
    
    response_graph.set_entry_point("supervisor")
    compiled_response_graph = response_graph.compile()
    
    # Create chain
    response_chain = (
        functools.partial(enter_chain, members=response_graph.nodes)
        | compiled_response_graph
    )
    
    return response_chain 