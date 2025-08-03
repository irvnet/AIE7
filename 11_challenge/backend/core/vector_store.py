"""
Vector Store Management Module
Second testable component for the student loan assistant
"""

import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_core.documents import Document


@dataclass
class VectorStoreConfig:
    """Configuration for vector store"""
    embedding_model: str = "text-embedding-3-small"
    collection_name: str = "student_loan_docs"
    location: str = ":memory:"  # Use in-memory for testing


@dataclass
class RetrievalResult:
    """Result of a retrieval operation"""
    documents: List[Document]
    scores: List[float]
    metadata: List[Dict[str, Any]]


class VectorStoreManager:
    """Manages vector store operations"""
    
    def __init__(self, config: VectorStoreConfig):
        self.config = config
        self.embedding_model = None
        self.vector_store = None
        self._initialized = False
    
    def initialize(self, api_key: Optional[str] = None) -> Dict[str, Any]:
        """Initialize the vector store with embeddings model"""
        try:
            # Set API key if provided
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
            
            # Check if API key is available
            if not os.getenv("OPENAI_API_KEY"):
                return {
                    "success": False,
                    "error": "OpenAI API key not found. Set OPENAI_API_KEY environment variable."
                }
            
            # Initialize embedding model
            self.embedding_model = OpenAIEmbeddings(model=self.config.embedding_model)
            
            # Test embedding model
            test_embedding = self.embedding_model.embed_query("test")
            if not test_embedding:
                return {
                    "success": False,
                    "error": "Failed to create test embedding"
                }
            
            self._initialized = True
            
            return {
                "success": True,
                "message": f"Vector store initialized with {self.config.embedding_model}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to initialize vector store: {str(e)}"
            }
    
    def create_vector_store(self, documents: List[Document]) -> Dict[str, Any]:
        """Create vector store from documents"""
        try:
            if not self._initialized:
                return {
                    "success": False,
                    "error": "Vector store not initialized. Call initialize() first."
                }
            
            if not documents:
                return {
                    "success": False,
                    "error": "No documents provided"
                }
            
            # Create vector store
            self.vector_store = Qdrant.from_documents(
                documents=documents,
                embedding=self.embedding_model,
                location=self.config.location,
                collection_name=self.config.collection_name
            )
            
            return {
                "success": True,
                "message": f"Vector store created with {len(documents)} documents",
                "document_count": len(documents)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create vector store: {str(e)}"
            }
    
    def add_documents(self, documents: List[Document]) -> Dict[str, Any]:
        """Add documents to existing vector store"""
        try:
            if not self.vector_store:
                return {
                    "success": False,
                    "error": "Vector store not created. Call create_vector_store() first."
                }
            
            # Add documents to existing store
            self.vector_store.add_documents(documents)
            
            return {
                "success": True,
                "message": f"Added {len(documents)} documents to vector store"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to add documents: {str(e)}"
            }
    
    def search(self, query: str, k: int = 5) -> RetrievalResult:
        """Search for similar documents"""
        try:
            if not self.vector_store:
                raise ValueError("Vector store not created")
            
            # Perform similarity search
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
            # Extract documents, scores, and metadata
            documents = [doc for doc, score in results]
            scores = [score for doc, score in results]
            metadata = [doc.metadata for doc, score in results]
            
            return RetrievalResult(
                documents=documents,
                scores=scores,
                metadata=metadata
            )
            
        except Exception as e:
            print(f"Search error: {e}")
            return RetrievalResult(documents=[], scores=[], metadata=[])
    
    def get_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None):
        """Get a retriever object for the vector store"""
        try:
            if not self.vector_store:
                raise ValueError("Vector store not created")
            
            retriever = self.vector_store.as_retriever()
            
            if search_kwargs:
                retriever.search_kwargs.update(search_kwargs)
            
            return retriever
            
        except Exception as e:
            print(f"Error creating retriever: {e}")
            return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        try:
            if not self.vector_store:
                return {
                    "success": False,
                    "error": "Vector store not created"
                }
            
            # Get collection info
            collection_info = self.vector_store.client.get_collection(
                collection_name=self.config.collection_name
            )
            
            return {
                "success": True,
                "collection_name": self.config.collection_name,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance,
                "points_count": collection_info.points_count
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get stats: {str(e)}"
            }


def test_vector_store():
    """Test function for the vector store manager"""
    print("Testing Vector Store Manager...")
    print("=" * 50)
    
    # Initialize manager
    config = VectorStoreConfig()
    manager = VectorStoreManager(config)
    
    # Test initialization
    print("1. Testing initialization...")
    init_result = manager.initialize()
    
    if init_result["success"]:
        print("✓ Vector store initialized successfully")
        print(f"  - Model: {config.embedding_model}")
    else:
        print(f"✗ Initialization failed: {init_result['error']}")
        return
    
    # Test with sample documents
    print("\n2. Testing document creation...")
    sample_docs = [
        Document(
            page_content="Federal student loans are available to eligible students.",
            metadata={"source": "test1.pdf", "page": 1}
        ),
        Document(
            page_content="Direct loans include subsidized and unsubsidized options.",
            metadata={"source": "test2.pdf", "page": 1}
        ),
        Document(
            page_content="Pell Grants provide need-based financial assistance.",
            metadata={"source": "test3.pdf", "page": 1}
        )
    ]
    
    create_result = manager.create_vector_store(sample_docs)
    
    if create_result["success"]:
        print("✓ Vector store created successfully")
        print(f"  - Documents: {create_result['document_count']}")
    else:
        print(f"✗ Creation failed: {create_result['error']}")
        return
    
    # Test search
    print("\n3. Testing search functionality...")
    test_queries = [
        "What are federal student loans?",
        "How do direct loans work?",
        "What is a Pell Grant?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = manager.search(query, k=2)
        
        if result.documents:
            print(f"  Found {len(result.documents)} documents:")
            for i, (doc, score) in enumerate(zip(result.documents, result.scores)):
                print(f"    {i+1}. Score: {score:.3f} - {doc.page_content[:50]}...")
        else:
            print("  No documents found")
    
    # Test retriever
    print("\n4. Testing retriever...")
    retriever = manager.get_retriever()
    if retriever:
        print("✓ Retriever created successfully")
        test_result = retriever.get_relevant_documents("student loans")
        print(f"  - Retrieved {len(test_result)} documents")
    else:
        print("✗ Failed to create retriever")
    
    # Get stats
    print("\n5. Testing statistics...")
    stats = manager.get_stats()
    if stats["success"]:
        print("✓ Statistics retrieved:")
        for key, value in stats.items():
            if key != "success":
                print(f"  - {key}: {value}")
    else:
        print(f"✗ Failed to get stats: {stats['error']}")
    
    print("\n" + "=" * 50)
    print("Vector store test complete!")


if __name__ == "__main__":
    test_vector_store() 