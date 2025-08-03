"""
Research Team for Multi-Agent System
Implements Search Agent and RAG Agent with supervisor
Based on proven patterns from example code lesson 6
"""

import functools
import operator
from typing import Annotated, List, TypedDict
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from .helper_functions import agent_node, create_agent, create_team_supervisor, enter_chain
from .tools import create_tavily_search_tool
from langchain_core.tools import tool


class ResearchTeamState(TypedDict):
    """State for research team."""
    messages: Annotated[List[BaseMessage], operator.add]
    next: str


def create_research_team(llm: ChatOpenAI, rag_retriever, tavily_api_key: str = None):
    """Create the research team with Search and RAG agents.
    
    Based on proven pattern from example code lesson 6.
    """
    
    # Create tools
    tools = []
    
    # Add Tavily search tool if API key is provided
    if tavily_api_key:
        tavily_tool = create_tavily_search_tool()
        tools.append(tavily_tool)
    
    # Create RAG tool
    @tool
    def rag_search(query: str) -> str:
        """Search for information in the student loan knowledge base."""
        docs = rag_retriever.invoke(query)
        return "\n\n".join([doc.page_content for doc in docs])
    
    tools.append(rag_search)
    
    # Create Search Agent
    search_agent = create_agent(
        llm,
        [tavily_tool] if tavily_api_key else [],
        "You are a research assistant who can search for up-to-date info using the tavily search engine.",
    )
    search_node = functools.partial(agent_node, agent=search_agent, name="Search")
    
    # Create RAG Agent
    research_agent = create_agent(
        llm,
        [rag_search],
        "You are a research assistant who can provide specific information on the student loan policies from our knowledge base.",
    )
    research_node = functools.partial(agent_node, agent=research_agent, name="LoanRetriever")
    
    # Create Research Team Supervisor
    supervisor_agent = create_team_supervisor(
        llm,
        ("You are a supervisor tasked with managing a conversation between the"
        " following workers: Search, LoanRetriever. Given the following user request,"
        " determine the subject to be researched and respond with the worker to act next. Each worker will perform a"
        " task and respond with their results and status. When each team is finished,"
        " you must respond with FINISH."
        " You should never ask your team to do anything beyond research. They are not required to write content or posts."
        " You should only pass tasks to workers that are specifically research focused."),
        ["Search", "LoanRetriever"],
    )
    
    # Create Research Team Graph
    research_graph = StateGraph(ResearchTeamState)
    research_graph.add_node("Search", search_node)
    research_graph.add_node("LoanRetriever", research_node)
    research_graph.add_node("supervisor", supervisor_agent)
    
    # Add edges
    research_graph.add_edge("Search", "supervisor")
    research_graph.add_edge("LoanRetriever", "supervisor")
    research_graph.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        {
            "Search": "Search",
            "LoanRetriever": "LoanRetriever",
            "FINISH": END,
        },
    )
    
    research_graph.set_entry_point("supervisor")
    compiled_research_graph = research_graph.compile()
    
    # Create chain
    research_chain = enter_chain | compiled_research_graph
    
    return research_chain 