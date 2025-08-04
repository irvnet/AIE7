"""
Advanced Retrieval Techniques for Multi-Agent RAG System
Uses LangChain's built-in advanced retrieval techniques for improved performance.
Based on proven patterns from example code lesson 9.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.schema import Document
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import (
    EnsembleRetriever,
    MultiQueryRetriever,
    ParentDocumentRetriever
)
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain.storage import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient, models


@dataclass
class RetrievalResult:
    """Represents a retrieval result with metadata"""
    document: Document
    score: float
    retrieval_method: str
    rank: int


class AdvancedRetriever:
    """
    Advanced retriever that combines multiple LangChain retrieval techniques:
    - BM25 retrieval
    - Multi-query retrieval
    - Parent document retrieval
    - Contextual compression (reranking)
    - Ensemble retrieval
    """
    
    def __init__(
        self,
        vector_store: Qdrant,
        embedding_model: OpenAIEmbeddings,
        documents: List[Document],
        use_reranking: bool = True,
        use_ensemble: bool = True
    ):
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.documents = documents
        self.use_reranking = use_reranking
        self.use_ensemble = use_ensemble
        
        # Initialize retrievers
        self._setup_retrievers()
    
    def _setup_retrievers(self):
        """Initialize all advanced retrievers"""
        
        # 1. BM25 Retriever
        self.bm25_retriever = BM25Retriever.from_documents(self.documents)
        
        # 2. Multi-Query Retriever (using the base vector store retriever)
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4o-mini")
        base_retriever = self.vector_store.as_retriever()
        self.multi_query_retriever = MultiQueryRetriever.from_llm(
            retriever=base_retriever, 
            llm=llm
        )
        
        # 3. Parent Document Retriever
        self._setup_parent_document_retriever()
        
        # 4. Contextual Compression (Reranking)
        if self.use_reranking:
            self._setup_contextual_compression_retriever()
        
        # 5. Ensemble Retriever
        if self.use_ensemble:
            self._setup_ensemble_retriever()
    
    def _setup_parent_document_retriever(self):
        """Setup parent document retriever"""
        try:
            # Create child splitter
            child_splitter = RecursiveCharacterTextSplitter(chunk_size=750)
            
            # Create Qdrant client for parent documents
            client = QdrantClient(location=":memory:")
            
            # Create collection for parent documents
            client.create_collection(
                collection_name="parent_documents",
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE)
            )
            
            # Create vector store for parent documents
            parent_vector_store = Qdrant(
                collection_name="parent_documents", 
                embedding=self.embedding_model, 
                client=client
            )
            
            # Create in-memory store for parent documents
            store = InMemoryStore()
            
            # Create parent document retriever
            self.parent_document_retriever = ParentDocumentRetriever(
                vectorstore=parent_vector_store,
                docstore=store,
                child_splitter=child_splitter,
            )
            
            # Add documents
            self.parent_document_retriever.add_documents(self.documents, ids=None)
            
        except Exception as e:
            print(f"Error setting up parent document retriever: {e}")
            self.parent_document_retriever = None
    
    def _setup_contextual_compression_retriever(self):
        """Setup contextual compression retriever with reranking"""
        try:
            # Create base retriever
            base_retriever = self.vector_store.as_retriever()
            
            # Create compressor (reranker)
            compressor = CohereRerank(model="rerank-v3.5")
            
            # Create contextual compression retriever
            self.compression_retriever = ContextualCompressionRetriever(
                base_compressor=compressor, 
                base_retriever=base_retriever
            )
            
        except Exception as e:
            print(f"Error setting up contextual compression retriever: {e}")
            self.compression_retriever = None
    
    def _setup_ensemble_retriever(self):
        """Setup ensemble retriever combining all techniques"""
        try:
            # Collect all available retrievers
            retrievers = [self.bm25_retriever, self.multi_query_retriever]
            
            if self.parent_document_retriever:
                retrievers.append(self.parent_document_retriever)
            
            if self.compression_retriever:
                retrievers.append(self.compression_retriever)
            
            # Create equal weighting
            weights = [1/len(retrievers)] * len(retrievers)
            
            # Create ensemble retriever
            self.ensemble_retriever = EnsembleRetriever(
                retrievers=retrievers, 
                weights=weights
            )
            
        except Exception as e:
            print(f"Error setting up ensemble retriever: {e}")
            self.ensemble_retriever = None
    
    def search(
        self, 
        query: str, 
        k: int = 10,
        use_advanced: bool = True
    ) -> List[Document]:
        """
        Main search interface that returns documents
        """
        if use_advanced and self.ensemble_retriever:
            # Use ensemble retriever for best results
            return self.ensemble_retriever.get_relevant_documents(query)
        elif use_advanced and self.multi_query_retriever:
            # Fallback to multi-query retriever
            return self.multi_query_retriever.get_relevant_documents(query)
        else:
            # Fallback to simple vector search
            return self.vector_store.similarity_search(query, k=k)
    
    def search_with_scores(
        self, 
        query: str, 
        k: int = 10,
        use_advanced: bool = True
    ) -> List[tuple[Document, float]]:
        """
        Search interface that returns documents with scores
        """
        if use_advanced and self.ensemble_retriever:
            # For ensemble retriever, we need to simulate scores
            docs = self.ensemble_retriever.get_relevant_documents(query)
            return [(doc, 1.0 - i/len(docs)) for i, doc in enumerate(docs)]
        else:
            # Fallback to simple vector search with scores
            return self.vector_store.similarity_search_with_score(query, k=k)
    
    def get_retriever_info(self) -> Dict[str, Any]:
        """Get information about available retrievers"""
        return {
            "bm25_available": self.bm25_retriever is not None,
            "multi_query_available": self.multi_query_retriever is not None,
            "parent_document_available": self.parent_document_retriever is not None,
            "compression_available": self.compression_retriever is not None,
            "ensemble_available": self.ensemble_retriever is not None,
            "total_documents": len(self.documents),
            "use_reranking": self.use_reranking,
            "use_ensemble": self.use_ensemble
        }


def create_advanced_retriever(
    vector_store: Qdrant,
    embedding_model: OpenAIEmbeddings,
    documents: List[Document],
    **kwargs
) -> AdvancedRetriever:
    """Factory function to create an advanced retriever"""
    return AdvancedRetriever(vector_store, embedding_model, documents, **kwargs) 