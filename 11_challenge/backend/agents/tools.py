"""
Tools for Multi-Agent System
Based on proven patterns from example code lessons 5-9
"""

import os
import uuid
from typing import Annotated, Dict, List, Optional
from pathlib import Path
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults


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