"""
Document Loading and Processing Module
Simplified version following proven patterns from course examples
"""

import os
from typing import List
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken


class DocumentLoader:
    """Handles loading and processing of PDF documents using proven patterns"""
    
    def __init__(self, chunk_size: int = 750, chunk_overlap: int = 0):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = self._create_text_splitter()
        self.documents = []
        self.chunks = []
    
    def _create_text_splitter(self) -> RecursiveCharacterTextSplitter:
        """Create text splitter with token-based length function"""
        def tiktoken_len(text: str) -> int:
            """Calculate token length using tiktoken"""
            try:
                tokens = tiktoken.encoding_for_model("gpt-4o").encode(text)
                return len(tokens)
            except Exception as e:
                print(f"Warning: Could not calculate token length: {e}")
                return len(text.split())  # Fallback to word count
        
        return RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=tiktoken_len,
        )
    
    def load_documents(self, directory: str = "data") -> List:
        """Load and process documents using the proven pattern from examples"""
        try:
            print(f"Loading documents from: {directory}")
            
            # Use the exact pattern from the examples
            directory_loader = DirectoryLoader(directory, glob="**/*.pdf", loader_cls=PyMuPDFLoader)
            self.documents = directory_loader.load()
            
            print(f"Loaded {len(self.documents)} documents")
            
            # Chunk documents using the exact pattern from examples
            self.chunks = self.text_splitter.split_documents(self.documents)
            
            print(f"Created {len(self.chunks)} chunks")
            
            return self.chunks
            
        except Exception as e:
            print(f"Error loading documents: {e}")
            return []


def test_document_loader():
    """Test function for the simplified document loader"""
    print("Testing Simplified Document Loader...")
    print("=" * 50)
    
    # Initialize loader
    loader = DocumentLoader(chunk_size=750, chunk_overlap=0)
    
    # Test loading documents
    chunks = loader.load_documents("data")
    
    if chunks:
        print("✓ Documents loaded successfully")
        print(f"  - Documents: {len(loader.documents)}")
        print(f"  - Chunks: {len(loader.chunks)}")
        
        # Show sample chunk
        if chunks:
            sample_chunk = chunks[0]
            print(f"  - Sample chunk: {sample_chunk.page_content[:100]}...")
    else:
        print("✗ Document loading failed")
    
    print("=" * 50)
    print("Document loader test complete!")


if __name__ == "__main__":
    test_document_loader() 