#!/usr/bin/env python3
"""
Example: Using Enhanced TextFileLoader with PDF files in RAG Pipeline
"""

import asyncio
from aimakerspace.text_utils import TextFileLoader, CharacterTextSplitter
from aimakerspace.vectordatabase import VectorDatabase
from aimakerspace.openai_utils.prompts import SystemRolePrompt, UserRolePrompt
from aimakerspace.openai_utils.chatmodel import ChatOpenAI

RAG_SYSTEM_TEMPLATE = """You are a knowledgeable assistant that answers questions strictly based on the provided context.
Instructions:
- Only answer using information from the context below.
- If the context does not contain the answer, respond with \"I don't know.\"
- Be accurate and cite specific parts of the context when possible.
- Explain your answer step by step.
- When possible, cite the source number or quote the relevant passage.
- Keep your response {response_style} and {response_length}.
- Do not use any external knowledge.
"""

RAG_USER_TEMPLATE = """<<<CONTEXT_START>>>
{context}
<<<CONTEXT_END>>>

Number of relevant sources found: {context_count}
{similarity_scores}

Question: {user_query}

Please provide your answer based solely on the context above.
"""

rag_system_prompt = SystemRolePrompt(
    RAG_SYSTEM_TEMPLATE,
    strict=True,
    defaults={
        "response_style": "concise",
        "response_length": "brief"
    }
)

rag_user_prompt = UserRolePrompt(
    RAG_USER_TEMPLATE,
    strict=True,
    defaults={
        "context_count": "",
        "similarity_scores": ""
    }
)

async def demonstrate_pdf_rag():
    """Demonstrate RAG pipeline with PDF support and notebook-style prompts"""
    
    print("📚 PDF-Enhanced RAG Pipeline Demo (Notebook-Style Prompts)")
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
    
    # Build context and similarity scores for prompt
    context_list = results  # List of (chunk, score)
    context_prompt = ""
    similarity_scores = []
    for i, (context, score) in enumerate(context_list, 1):
        context_prompt += f"[Source {i}]: {context}\n\n"
        similarity_scores.append(f"Source {i}: {score:.3f}")

    system_params = {
        "response_style": "detailed",
        "response_length": "comprehensive"
    }
    formatted_system_prompt = rag_system_prompt.create_message(**system_params)

    user_params = {
        "user_query": test_query,
        "context": context_prompt.strip(),
        "context_count": len(context_list),
        "similarity_scores": f"Relevance scores: {', '.join(similarity_scores)}"
    }
    formatted_user_prompt = rag_user_prompt.create_message(**user_params)

    # Use ChatOpenAI to get the final answer
    chat_openai = ChatOpenAI()
    response = chat_openai.run([formatted_system_prompt, formatted_user_prompt])
    print(f"\nLLM Response:\n{response}")
    
    print("\n🎉 PDF-enhanced RAG pipeline is working with your PDF file and notebook-style prompts!")
    print("\n💡 To use with other PDF files:")
    print("   1. Place your PDF files in the data/ directory")
    print("   2. Use TextFileLoader('data/your_file.pdf')")
    print("   3. The pipeline will automatically extract text and create embeddings")

if __name__ == "__main__":
    try:
        asyncio.run(demonstrate_pdf_rag())
    except Exception as e:
        import traceback
        print("\n❌ An error occurred while running the RAG pipeline:")
        traceback.print_exc() 