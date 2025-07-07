#!/usr/bin/env python3
"""
Example: Using Enhanced TextFileLoader with PDF files in RAG Pipeline
"""

import asyncio
from aimakerspace.text_utils import TextFileLoader, CharacterTextSplitter
from aimakerspace.vectordatabase import VectorDatabase

async def demonstrate_pdf_rag():
    """Demonstrate RAG pipeline with PDF support"""
    
    print("📚 PDF-Enhanced RAG Pipeline Demo")
    print("=" * 40)
    
    # Step 1: Load documents from PDF file
    print("1️⃣ Loading documents from PDF...")
    pdf_loader = TextFileLoader("data/PMarcaBlogs.pdf")
    pdf_documents = pdf_loader.load_documents()
    print(f"   ✅ Loaded {len(pdf_documents)} PDF document(s)")
    
    # Step 2: Split documents into chunks
    print("\n2️⃣ Splitting PDF documents into chunks...")
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_documents = splitter.split_texts(pdf_documents)
    print(f"   ✅ Created {len(split_documents)} chunks from PDF")
    
    # Step 3: Build vector database
    print("\n3️⃣ Building vector database from PDF chunks...")
    vector_db = VectorDatabase()
    vector_db = await vector_db.abuild_from_list(split_documents)
    print(f"   ✅ Vector database built with {len(split_documents)} embeddings from PDF")
    
    # Step 4: Test retrieval
    print("\n4️⃣ Testing retrieval from PDF-based vector DB...")
    test_query = "What is the Michael Eisner Memorial Weak Executive Problem?"
    results = vector_db.search_by_text(test_query, k=3)
    print(f"   ✅ Retrieved {len(results)} relevant chunks from PDF")
    
    # Display top result
    if results:
        top_result = results[0]
        print(f"   📄 Top result (first 200 chars): {top_result[0][:200]}...")
    
    print("\n🎉 PDF-enhanced RAG pipeline is working with your PDF file!")
    print("\n💡 To use with other PDF files:")
    print("   1. Place your PDF files in the data/ directory")
    print("   2. Use TextFileLoader('data/your_file.pdf')")
    print("   3. The pipeline will automatically extract text and create embeddings")

if __name__ == "__main__":
    asyncio.run(demonstrate_pdf_rag()) 