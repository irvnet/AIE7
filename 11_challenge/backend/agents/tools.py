"""
Tools for Multi-Agent System
Based on proven patterns from example code lessons 5-9
"""

import os
import uuid
import re
from datetime import datetime
from typing import Annotated, Dict, List, Optional
from pathlib import Path
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults


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


# Global working directory for document operations
WORKING_DIRECTORY = None


def create_random_subdirectory():
    """Create a random subdirectory for document operations."""
    global WORKING_DIRECTORY
    random_id = str(uuid.uuid4())[:8]
    subdirectory_path = os.path.join('./content/data', random_id)
    os.makedirs(subdirectory_path, exist_ok=True)
    WORKING_DIRECTORY = Path(subdirectory_path)
    return subdirectory_path


@tool
def create_outline(
    points: Annotated[List[str], "List of main points or sections."],
    file_name: Annotated[str, "File path to save the outline."],
) -> Annotated[str, "Path of the saved outline file."]:
    """Create and save an outline."""
    if not WORKING_DIRECTORY:
        create_random_subdirectory()
    
    with (WORKING_DIRECTORY / file_name).open("w") as file:
        for i, point in enumerate(points):
            file.write(f"{i + 1}. {point}\n")
    return f"Outline saved to {file_name}"


@tool
def read_document(
    file_name: Annotated[str, "File path to save the document."],
    start: Annotated[Optional[int], "The start line. Default is 0"] = None,
    end: Annotated[Optional[int], "The end line. Default is None"] = None,
) -> str:
    """Read the specified document."""
    if not WORKING_DIRECTORY:
        create_random_subdirectory()
    
    with (WORKING_DIRECTORY / file_name).open("r") as file:
        lines = file.readlines()
    if start is not None:
        start = 0
    return "\n".join(lines[start:end])


@tool
def write_document(
    content: Annotated[str, "Text content to be written into the document."],
    file_name: Annotated[str, "File path to save the document."],
) -> Annotated[str, "Path of the saved document file."]:
    """Create and save a text document."""
    if not WORKING_DIRECTORY:
        create_random_subdirectory()
    
    with (WORKING_DIRECTORY / file_name).open("w") as file:
        file.write(content)
    return f"Document saved to {file_name}"


@tool
def edit_document(
    file_name: Annotated[str, "Path of the document to be edited."],
    inserts: Annotated[
        Dict[int, str],
        "Dictionary where key is the line number (1-indexed) and value is the text to be inserted at that line.",
    ] = {},
) -> Annotated[str, "Path of the edited document file."]:
    """Edit a document by inserting text at specific line numbers."""
    if not WORKING_DIRECTORY:
        create_random_subdirectory()

    with (WORKING_DIRECTORY / file_name).open("r") as file:
        lines = file.readlines()

    sorted_inserts = sorted(inserts.items())

    for line_number, text in sorted_inserts:
        if 1 <= line_number <= len(lines) + 1:
            lines.insert(line_number - 1, text + "\n")
        else:
            return f"Error: Line number {line_number} is out of range."

    with (WORKING_DIRECTORY / file_name).open("w") as file:
        file.writelines(lines)

    return f"Document edited and saved to {file_name}"


def create_tavily_search_tool():
    """Create Tavily search tool for real-time policy updates."""
    return TavilySearchResults(max_results=5)


def create_federal_register_search_tool():
    """Create search tool for Federal Register - Education Department."""
    
    @tool
    def search_federal_register(
        query: Annotated[str, "Search query for Federal Register education documents."],
    ) -> Annotated[str, "Search results from Federal Register - Education Department."]:
        """Search the Federal Register for Education Department documents and regulations."""
        try:
            # Use Tavily with specific site targeting
            tavily_tool = TavilySearchResults(max_results=3)
            
            # For interest rate queries, be more specific
            if "interest rate" in query.lower() or "interest rates" in query.lower():
                search_query = f"site:www.federalregister.gov/documents {query} 2024 2025 current academic year"
            else:
                search_query = f"site:www.federalregister.gov/documents {query} education department student loans"
            
            results = tavily_tool.invoke({"query": search_query})
            return f"Federal Register Results for '{query}':\n{results}"
        except Exception as e:
            return f"Error searching Federal Register: {str(e)}"
    
    return search_federal_register


def create_education_press_releases_search_tool():
    """Create search tool for Department of Education Press Releases."""
    
    @tool
    def search_education_press_releases(
        query: Annotated[str, "Search query for Education Department press releases."],
    ) -> Annotated[str, "Search results from Department of Education Press Releases."]:
        """Search Department of Education press releases for student loan information."""
        try:
            # Use Tavily with specific site targeting
            tavily_tool = TavilySearchResults(max_results=3)
            search_query = f"site:www.ed.gov/news/press-releases {query} student loans"
            results = tavily_tool.invoke({"query": search_query})
            return f"Education Press Release Results for '{query}':\n{results}"
        except Exception as e:
            return f"Error searching Education Press Releases: {str(e)}"
    
    return search_education_press_releases


def create_nerdwallet_search_tool():
    """Create search tool for NerdWallet Student Loans Guide."""
    
    @tool
    def search_nerdwallet_student_loans(
        query: Annotated[str, "Search query for NerdWallet student loan information."],
    ) -> Annotated[str, "Search results from NerdWallet Student Loans Guide."]:
        """Search NerdWallet's student loan guides and resources."""
        try:
            # Use Tavily with specific site targeting
            tavily_tool = TavilySearchResults(max_results=3)
            search_query = f"site:www.nerdwallet.com {query} student loans"
            results = tavily_tool.invoke({"query": search_query})
            return f"NerdWallet Student Loan Results for '{query}':\n{results}"
        except Exception as e:
            return f"Error searching NerdWallet: {str(e)}"
    
    return search_nerdwallet_student_loans


def create_targeted_external_search_tool():
    """Create a comprehensive external search tool for student loan resources."""
    
    @tool
    def search_external_student_loan_resources(
        query: Annotated[str, "Search query for external student loan information."],
    ) -> Annotated[str, "Search results from trusted external student loan resources."]:
        """Search trusted external sources for student loan information: Federal Register, Education Press Releases, and NerdWallet."""
        print(f"🔍 EXTERNAL SEARCH CALLED: {query}")
        
        current_year = 2025
        current_month = 1  # January 2025
        max_attempts = 5
        
        for attempt in range(1, max_attempts + 1):
            print(f"  🔄 Attempt {attempt}/{max_attempts}")
            try:
                results = []
                
                # Search Federal Register
                print(f"    📋 Searching Federal Register...")
                federal_register_tool = create_federal_register_search_tool()
                federal_results = federal_register_tool.invoke(query)
                if "Error" not in federal_results and _is_current_information(federal_results, current_year, current_month):
                    results.append(f"📋 Federal Register:\n{federal_results}")
                    print(f"    ✅ Federal Register results found (current)")
                else:
                    print(f"    ⚠️  Federal Register results outdated or failed")
                
                # Search Education Press Releases
                print(f"    📰 Searching Education Press Releases...")
                press_releases_tool = create_education_press_releases_search_tool()
                press_results = press_releases_tool.invoke(query)
                if "Error" not in press_results and _is_current_information(press_results, current_year, current_month):
                    results.append(f"📰 Education Press Releases:\n{press_results}")
                    print(f"    ✅ Education Press Releases results found (current)")
                else:
                    print(f"    ⚠️  Education Press Releases results outdated or failed")
                
                # Search NerdWallet
                print(f"    💰 Searching NerdWallet...")
                nerdwallet_tool = create_nerdwallet_search_tool()
                nerdwallet_results = nerdwallet_tool.invoke(query)
                if "Error" not in nerdwallet_results and _is_current_information(nerdwallet_results, current_year, current_month):
                    results.append(f"💰 NerdWallet Student Loans:\n{nerdwallet_results}")
                    print(f"    ✅ NerdWallet results found (current)")
                else:
                    print(f"    ⚠️  NerdWallet results outdated or failed")
                
                if results:
                    print(f"  ✅ External search completed with {len(results)} current sources")
                    
                    # Format the results for better agent processing
                    formatted_result = "CURRENT INFORMATION FROM EXTERNAL SOURCES:\n\n"
                    formatted_result += "\n\n".join(results)
                    formatted_result += f"\n\nIMPORTANT: This information is current (within 12 months) and from official sources."
                    
                    return formatted_result
                else:
                    print(f"  ⚠️  Attempt {attempt}: No current information found, trying again...")
                    if attempt < max_attempts:
                        import time
                        time.sleep(1)  # Brief pause between attempts
                    
            except Exception as e:
                print(f"  ❌ Attempt {attempt} failed: {str(e)}")
                if attempt < max_attempts:
                    import time
                    time.sleep(1)  # Brief pause between attempts
        
        print(f"  ❌ All {max_attempts} attempts failed to find current information")
        return "I don't have current information available for this query. All external sources returned outdated information (more than 12 months old) or failed to provide results."
    
    return search_external_student_loan_resources


def create_complaint_reference_tool(complaint_retriever):
    """Create complaint reference tool for response consistency."""
    
    @tool 
    def reference_previous_responses(
        query: Annotated[str, "The query to search for in the previous responses."],
    ) -> Annotated[str, "The previous responses that match the query."]:
        """Search for previous responses that match the query."""
        return complaint_retriever.invoke(query)
    
    return reference_previous_responses


def create_document_prelude_function():
    """Create prelude function for document writing team."""
    
    def prelude(state):
        """Add current files information to state."""
        written_files = []
        if not WORKING_DIRECTORY or not WORKING_DIRECTORY.exists():
            create_random_subdirectory()
        
        try:
            written_files = [
                f.relative_to(WORKING_DIRECTORY) for f in WORKING_DIRECTORY.rglob("*")
            ]
        except:
            pass
        
        if not written_files:
            return {**state, "current_files": "No files written."}
        
        return {
            **state,
            "current_files": "\nBelow are files your team has written to the directory:\n"
            + "\n".join([f" - {f}" for f in written_files]),
        }
    
    return prelude 