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
    """Create the response team with document writing agents.
    
    Based on proven pattern from example code lesson 6.
    """
    
    # Create tools
    document_tools = [create_outline, read_document, write_document, edit_document]
    complaint_tool = create_complaint_reference_tool(complaint_retriever)
    prelude = create_document_prelude_function()
    
    # Create DocWriter Agent
    doc_writer_agent = create_agent(
        llm,
        [write_document, edit_document, read_document],
        ("You are an expert writing customer assistance responses.\n"
        "Below are files currently in your directory:\n{current_files}"),
    )
    context_aware_doc_writer_agent = prelude | doc_writer_agent
    doc_writing_node = functools.partial(
        agent_node, agent=context_aware_doc_writer_agent, name="DocWriter"
    )
    
    # Create NoteTaker Agent
    note_taking_agent = create_agent(
        llm,
        [create_outline, read_document, complaint_tool],
        ("You are an expert senior researcher tasked with writing a customer assistance outline and"
        " taking notes to craft a customer assistance response.\n{current_files}"),
    )
    context_aware_note_taking_agent = prelude | note_taking_agent
    note_taking_node = functools.partial(
        agent_node, agent=context_aware_note_taking_agent, name="NoteTaker"
    )
    
    # Create CopyEditor Agent
    copy_editor_agent = create_agent(
        llm,
        [write_document, edit_document, read_document],
        ("You are an expert copy editor who focuses on fixing grammar, spelling, and tone issues\n"
        "Below are files currently in your directory:\n{current_files}"),
    )
    context_aware_copy_editor_agent = prelude | copy_editor_agent
    copy_editing_node = functools.partial(
        agent_node, agent=context_aware_copy_editor_agent, name="CopyEditor"
    )
    
    # Create EmpathyEditor Agent
    empathy_editor_agent = create_agent(
        llm,
        [write_document, edit_document, read_document],
        ("You are an expert in empathy, compassion, and understanding - you edit the document to make sure it's empathetic and compassionate."
        "Below are files currently in your directory:\n{current_files}"),
    )
    empathy_editor_agent = prelude | empathy_editor_agent
    empathy_node = functools.partial(
        agent_node, agent=empathy_editor_agent, name="EmpathyEditor"
    )
    
    # Create Document Writing Team Supervisor
    doc_writing_supervisor = create_team_supervisor(
        llm,
        ("You are a supervisor tasked with managing a conversation between the"
        " following workers: DocWriter, NoteTaker, EmpathyEditor, CopyEditor. You should always verify the technical"
        " contents after any edits are made. "
        "Given the following user request,"
        " respond with the worker to act next. Each worker will perform a"
        " task and respond with their results and status. When each team is finished,"
        " you must respond with FINISH."),
        ["DocWriter", "NoteTaker", "EmpathyEditor", "CopyEditor"],
    )
    
    # Create Document Writing Team Graph
    authoring_graph = StateGraph(DocWritingState)
    authoring_graph.add_node("DocWriter", doc_writing_node)
    authoring_graph.add_node("NoteTaker", note_taking_node)
    authoring_graph.add_node("CopyEditor", copy_editing_node)
    authoring_graph.add_node("EmpathyEditor", empathy_node)
    authoring_graph.add_node("supervisor", doc_writing_supervisor)
    
    # Add edges
    authoring_graph.add_edge("DocWriter", "supervisor")
    authoring_graph.add_edge("NoteTaker", "supervisor")
    authoring_graph.add_edge("CopyEditor", "supervisor")
    authoring_graph.add_edge("EmpathyEditor", "supervisor")
    
    authoring_graph.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        {
            "DocWriter": "DocWriter",
            "NoteTaker": "NoteTaker",
            "CopyEditor": "CopyEditor",
            "EmpathyEditor": "EmpathyEditor",
            "FINISH": END,
        },
    )
    
    authoring_graph.set_entry_point("supervisor")
    compiled_authoring_graph = authoring_graph.compile()
    
    # Create chain
    authoring_chain = (
        functools.partial(enter_chain, members=authoring_graph.nodes)
        | compiled_authoring_graph
    )
    
    return authoring_chain 