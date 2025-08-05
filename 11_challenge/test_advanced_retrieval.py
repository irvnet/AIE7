#!/usr/bin/env python3
"""
Test script for Advanced Retrieval Techniques
Compares baseline vs advanced retrieval performance using LangChain techniques
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / "backend"))

from backend.core.advanced_retrieval import create_advanced_retriever
from backend.data.document_loader import DocumentLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
import time


def test_advanced_retrieval():
    """Test the advanced retrieval implementation"""
    
    print("🚀 Testing Advanced Retrieval Techniques")
    print("=" * 50)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in environment")
        return
    
    try:
        # Load documents
        print("📄 Loading documents...")
        document_loader = DocumentLoader()
        chunks = document_loader.load_documents("data")
        print(f"✅ Loaded {len(chunks)} chunks from {len(document_loader.documents)} documents")
        
        # Create embedding model
        print("🔧 Creating embedding model...")
        embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
        
        # Create vector store
        print("🗄️ Creating vector store...")
        vector_store = Qdrant.from_documents(
            documents=chunks,
            embedding=embedding_model,
            location=":memory:"
        )
        
        # Create advanced retriever
        print("⚡ Creating advanced retriever...")
        advanced_retriever = create_advanced_retriever(
            vector_store=vector_store,
            embedding_model=embedding_model,
            documents=chunks
        )
        
        # Get retriever info
        info = advanced_retriever.get_retriever_info()
        print(f"📊 Retriever Info:")
        print(f"   Optimized Ensemble: {'✅' if info['optimized_ensemble_available'] else '❌'}")
        print(f"   BM25: {'✅' if info['bm25_available'] else '❌'}")
        print(f"   Base Retriever: {'✅' if info['base_retriever_available'] else '❌'}")
        print(f"   Total Documents: {info['total_documents']}")
        print(f"   Performance: {info['performance']}")
        
        # Test queries
        test_queries = [
            "What is the maximum loan amount for dependent undergraduate students?",
            "What's the difference between subsidized and unsubsidized loans?",
            "How do I apply for income-based repayment?",
            "What are the current interest rates for federal student loans?",
            "How do I qualify for Public Service Loan Forgiveness?"
        ]
        
        print("\n🧪 Testing Advanced Retrieval vs Baseline")
        print("-" * 50)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Test {i}: {query}")
            print("-" * 30)
            
            # Test baseline retrieval
            print("🔍 Baseline retrieval:")
            start_time = time.time()
            baseline_results = vector_store.similarity_search(query, k=3)
            baseline_time = time.time() - start_time
            print(f"   ⏱️  Time: {baseline_time:.3f}s")
            print(f"   📊 Results: {len(baseline_results)} documents")
            
            # Test advanced retrieval
            print("🚀 Advanced retrieval:")
            start_time = time.time()
            advanced_results = advanced_retriever.search(query, k=3, use_advanced=True)
            advanced_time = time.time() - start_time
            print(f"   ⏱️  Time: {advanced_time:.3f}s")
            print(f"   📊 Results: {len(advanced_results)} documents")
            
            # Test with scores
            print("📈 Advanced retrieval with scores:")
            start_time = time.time()
            advanced_with_scores = advanced_retriever.search_with_scores(query, k=3, use_advanced=True)
            scores_time = time.time() - start_time
            print(f"   ⏱️  Time: {scores_time:.3f}s")
            print(f"   📊 Results: {len(advanced_with_scores)} documents")
            
            # Show top result scores
            if advanced_with_scores:
                print("   🏆 Top result scores:")
                for j, (doc, score) in enumerate(advanced_with_scores[:2]):
                    print(f"      {j+1}. Score: {score:.4f}")
                    print(f"         Preview: {doc.page_content[:100]}...")
            
            # Performance comparison
            print(f"   📊 Performance: Advanced is {baseline_time/advanced_time:.1f}x {'faster' if advanced_time < baseline_time else 'slower'}")
        
        print("\n✅ Advanced retrieval testing completed!")
        
        # Test individual retrievers
        print("\n🔍 Testing Individual Retrievers")
        print("-" * 30)
        
        if info['bm25_available']:
            print("📝 BM25 Retriever:")
            bm25_results = advanced_retriever.bm25_retriever.get_relevant_documents("loan amounts", k=2)
            print(f"   Results: {len(bm25_results)} documents")
            if bm25_results:
                print(f"   Preview: {bm25_results[0].page_content[:100]}...")
        
        if info['base_retriever_available']:
            print("📝 Base Semantic Retriever:")
            base_results = advanced_retriever.base_retriever.get_relevant_documents("loan amounts", k=2)
            print(f"   Results: {len(base_results)} documents")
            if base_results:
                print(f"   Preview: {base_results[0].page_content[:100]}...")
        
        if info['optimized_ensemble_available']:
            print("📝 Optimized Ensemble Retriever:")
            ensemble_results = advanced_retriever.ensemble_retriever.get_relevant_documents("loan amounts", k=2)
            print(f"   Results: {len(ensemble_results)} documents")
            if ensemble_results:
                print(f"   Preview: {ensemble_results[0].page_content[:100]}...")
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_advanced_retrieval() 