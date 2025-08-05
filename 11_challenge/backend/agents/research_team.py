"""
Research Team for Multi-Agent System
Implements Search Agent and RAG Agent with supervisor
Based on proven patterns from example code lesson 6
"""

import functools
import operator
import re
from typing import Annotated, List, TypedDict
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph


def _is_current_information(text: str, current_year: int, current_month: int) -> bool:
    """Check if information is current (within 12 months)."""
    # Look for year patterns
    year_pattern = r'\b(20\d{2})\b'
    years = re.findall(year_pattern, text)
    
    if not years:
        return True  # If no year found, assume current
    
    # Count current vs old years
    current_years = [y for y in years if int(y) >= current_year - 1]
    old_years = [y for y in years if int(y) < current_year - 1]
    
    # If there are more old years than current years, reject
    if len(old_years) > len(current_years):
        print(f"    ⚠️  Rejecting: {len(old_years)} old years vs {len(current_years)} current years")
        return False
    
    # Additional check: if text contains old years prominently, reject it
    old_year_patterns = [
        r'\b2023\b',  # Reject 2023 information
        r'\b2022\b',  # Reject 2022 information
        r'\b2021\b',  # Reject 2021 information
        r'\b2020\b',  # Reject 2020 information
        r'\b2019\b',  # Reject 2019 information
        r'\b2018\b',  # Reject 2018 information
        r'\b2017\b',  # Reject 2017 information
        r'\b2016\b',  # Reject 2016 information
        r'\b2015\b',  # Reject 2015 information
        r'\b2014\b',  # Reject 2014 information
    ]
    
    for pattern in old_year_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            # Check if the old year is mentioned prominently (not just in passing)
            old_year_matches = re.findall(pattern, text, re.IGNORECASE)
            if len(old_year_matches) > 1:  # If old year appears more than once, likely outdated
                print(f"    ⚠️  Rejecting: {len(old_year_matches)} instances of old year pattern")
                return False
    
    return True

from .helper_functions import agent_node, create_agent, create_team_supervisor, enter_chain
from .tools import create_tavily_search_tool, create_targeted_external_search_tool
from langchain_core.tools import tool


class ResearchTeamState(TypedDict):
    """State for research team."""
    messages: Annotated[List[BaseMessage], operator.add]
    next: str


def create_research_team(llm: ChatOpenAI, rag_retriever, tavily_api_key: str = None, use_advanced_retrieval: bool = True):
    """Create the research team with Search and RAG agents.
    
    Based on proven pattern from example code lesson 6.
    """
    
    # Create tools
    tools = []
    
    # Add targeted external search tool if API key is provided
    if tavily_api_key:
        external_search_tool = create_targeted_external_search_tool()
        tools.append(external_search_tool)
    
    # Create RAG tool with advanced retrieval
    @tool
    def rag_search(query: str) -> str:
        """Search for information in the student loan knowledge base using advanced retrieval techniques."""
        print(f"📚 RAG SEARCH CALLED: {query}")
        
        # Check if this is a time-sensitive query that needs current information
        time_sensitive_keywords = ['2024', '2025', 'latest', 'today', 'now', 'deadlines', 'recent', 'updated']
        query_lower = query.lower()
        is_time_sensitive = any(keyword in query_lower for keyword in time_sensitive_keywords)
        
        # Special case: interest rate queries should always use external search for current data
        if 'interest rate' in query_lower or 'interest rates' in query_lower:
            is_time_sensitive = True
        
        if is_time_sensitive and tavily_api_key:
            print(f"  ⏰ Time-sensitive query detected - redirecting to external search")
            external_search_tool = create_targeted_external_search_tool()
            external_result = external_search_tool.invoke(query)
            print(f"  📋 External search result length: {len(external_result)} characters")
            print(f"  📋 External search result preview: {external_result[:200]}...")
            return external_result
        
        try:
            if use_advanced_retrieval and hasattr(rag_retriever, 'search'):
                # Use advanced retriever if available
                print(f"  🔧 Using advanced retrieval...")
                docs = rag_retriever.search(query, k=5, use_advanced=True)
            else:
                # Fallback to standard retriever
                print(f"  🔧 Using standard retrieval...")
                docs = rag_retriever.invoke(query)
            
            if not docs:
                print(f"  ❌ No documents found in knowledge base")
                return "No relevant information found in the knowledge base."
            
            print(f"  ✅ Found {len(docs)} documents in knowledge base")
            content = "\n\n".join([doc.page_content for doc in docs])
            print(f"  📄 Content length: {len(content)} characters")
            
            # Check if content is current (within 12 months)
            current_year = 2025
            current_month = 1
            if not _is_current_information(content, current_year, current_month):
                print(f"  ⚠️  Knowledge base content is outdated (more than 12 months old)")
                return "The information in our knowledge base is outdated (more than 12 months old). Please use external search for current information."
            
            return content
        except Exception as e:
            print(f"  ❌ RAG search error: {e}")
            return f"Error searching knowledge base: {str(e)}"
    
    tools.append(rag_search)
    
    # Create External Search Agent
    external_search_agent = create_agent(
        llm,
        [external_search_tool] if tavily_api_key else [],
        "You are a research assistant who can search trusted external sources for student loan information: Federal Register, Education Press Releases, and NerdWallet.",
    )
    external_search_node = functools.partial(agent_node, agent=external_search_agent, name="ExternalSearch")
    
    # Create RAG Agent
    research_agent = create_agent(
        llm,
        [rag_search],
        ("You are a research assistant who can provide specific information on student loan policies."
        " You can search both our knowledge base and external sources for current information."
        " When you receive external search results, extract the key information and provide it clearly."
        " For interest rates, always specify the academic year and source of the information."
        " Be accurate and helpful in your responses."),
    )
    research_node = functools.partial(agent_node, agent=research_agent, name="LoanRetriever")
    
    # Create Research Team Supervisor
    supervisor_agent = create_team_supervisor(
        llm,
        ("You are a supervisor managing research for student loan questions."
        " You have two workers: LoanRetriever (searches our knowledge base) and ExternalSearch (searches trusted external sources)."
        
        " CRITICAL RULES - FOLLOW EXACTLY:"
        " 1. If the question contains ANY of these words: 'current', 'latest', 'today', 'now', 'interest rate', 'interest rates', 'deadlines', 'recent', 'updated', '2024', '2025' - ALWAYS respond with 'ExternalSearch'"
        " 2. For all other questions, respond with 'LoanRetriever'"
        " 3. When research is complete, respond with 'FINISH'"),
        ["LoanRetriever", "ExternalSearch"],
    )
    
    # Create Research Team Graph
    research_graph = StateGraph(ResearchTeamState)
    research_graph.add_node("LoanRetriever", research_node)
    research_graph.add_node("ExternalSearch", external_search_node)
    research_graph.add_node("supervisor", supervisor_agent)
    
    # Add edges
    research_graph.add_edge("LoanRetriever", "supervisor")
    research_graph.add_edge("ExternalSearch", "supervisor")
    research_graph.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        {
            "LoanRetriever": "LoanRetriever",
            "ExternalSearch": "ExternalSearch",
            "FINISH": END,
        },
    )
    
    research_graph.set_entry_point("supervisor")
    compiled_research_graph = research_graph.compile()
    
    # Create chain
    research_chain = enter_chain | compiled_research_graph
    
    return research_chain 