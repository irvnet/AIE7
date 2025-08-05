"""
FastAPI Backend for Student Loan Assistant
Provides WebSocket chat interface and REST API endpoints
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import json
import os
import sys
from pathlib import Path

# Add backend to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Import our existing components
from data.document_loader import DocumentLoader
from agents.multi_agent_system import MultiAgentSystem

# Pydantic models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None

class SystemStatus(BaseModel):
    initialized: bool
    vector_store_ready: bool
    agents_ready: bool
    documents_loaded: int
    total_chunks: int

class InitializeRequest(BaseModel):
    openai_api_key: str
    tavily_api_key: Optional[str] = None
    langsmith_api_key: Optional[str] = None

class EvaluateRequest(BaseModel):
    openai_api_key: str
    evaluation_type: str = "quick"  # "quick" or "full"
    langsmith_api_key: Optional[str] = None

# FastAPI app
app = FastAPI(
    title="Student Loan Assistant API",
    description="Multi-Agent RAG system for student loan guidance",
    version="1.0.0"
)

# CORS middleware for Vue.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Vue dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.system_initialized = False
        self.document_loader = None
        self.vector_store = None
        self.retriever = None
        self.complaint_retriever = None
        self.multi_agent_system = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# REST API Endpoints
@app.get("/")
async def root():
    return {"message": "Student Loan Assistant API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "initialized": manager.system_initialized}

@app.get("/status", response_model=SystemStatus)
async def get_system_status():
    """Get current system status"""
    return SystemStatus(
        initialized=manager.system_initialized,
        vector_store_ready=manager.vector_store is not None,
        agents_ready=manager.multi_agent_system is not None,
        documents_loaded=len(manager.document_loader.documents) if manager.document_loader else 0,
        total_chunks=len(manager.document_loader.chunks) if manager.document_loader else 0
    )

@app.post("/evaluate")
async def run_evaluation(request: EvaluateRequest):
    """Run the performance evaluation from the admin panel"""
    try:
        # Validate API keys first
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent.parent.parent))
        
        from api_key_manager import APIKeys, validate_api_keys
        
        # Create API keys object
        keys = APIKeys(
            openai_api_key=request.openai_api_key,
            langsmith_api_key=request.langsmith_api_key
        )
        
        # Validate keys
        errors = validate_api_keys(keys)
        if errors:
            return {
                "success": False,
                "error": f"API key validation failed: {'; '.join(errors)}"
            }
        
        # Set environment variables
        os.environ["OPENAI_API_KEY"] = request.openai_api_key
        if request.langsmith_api_key:
            os.environ["LANGCHAIN_API_KEY"] = request.langsmith_api_key
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_PROJECT"] = "student-loan-assistant-evaluation"
        
        # Run evaluation
        if request.evaluation_type == "quick":
            # Run quick evaluation
            from evaluation_with_langsmith import run_quick_evaluation
            results = run_quick_evaluation(request.openai_api_key, request.langsmith_api_key)
        else:
            # Run full evaluation
            from evaluation_with_langsmith import run_full_evaluation_with_progress
            results = run_full_evaluation_with_progress(request.openai_api_key, request.langsmith_api_key)
        
        # Check if results were returned
        if results is None:
            return {
                "success": False,
                "error": "Evaluation returned no results"
            }
        
        if results:
            return {
                "success": True,
                "evaluation_type": request.evaluation_type,
                "results": results
            }
        else:
            return {
                "success": False,
                "error": "Evaluation failed to complete"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/initialize")
async def initialize_system(request: InitializeRequest):
    """Initialize the RAG system with API keys"""
    try:
        # Validate API keys first
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent.parent.parent))
        
        from api_key_manager import APIKeys, validate_api_keys
        
        # Create API keys object
        keys = APIKeys(
            openai_api_key=request.openai_api_key,
            tavily_api_key=request.tavily_api_key,
            langsmith_api_key=request.langsmith_api_key
        )
        
        # Validate keys
        errors = validate_api_keys(keys)
        if errors:
            raise HTTPException(status_code=400, detail=f"API key validation failed: {'; '.join(errors)}")
        
        # Broadcast initialization start
        progress_message = json.dumps({
            "type": "initialization_progress",
            "step": "start",
            "message": "Starting system initialization...",
            "progress": 0
        })
        print(f"Broadcasting progress: {progress_message}")
        await manager.broadcast(progress_message)
        
        # Set environment variables
        os.environ["OPENAI_API_KEY"] = request.openai_api_key
        if request.tavily_api_key:
            os.environ["TAVILY_API_KEY"] = request.tavily_api_key
        if request.langsmith_api_key:
            os.environ["LANGCHAIN_API_KEY"] = request.langsmith_api_key
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_PROJECT"] = "student-loan-assistant-evaluation"

        # Initialize document loader using proven pattern
        try:
            await manager.broadcast(json.dumps({
                "type": "initialization_progress",
                "step": "loading_documents",
                "message": "Loading student loan documents...",
                "progress": 20
            }))
            
            manager.document_loader = DocumentLoader()
            chunks = manager.document_loader.load_documents("data")
            print(f"Loaded {len(chunks)} chunks from {len(manager.document_loader.documents)} documents")
            
            await manager.broadcast(json.dumps({
                "type": "initialization_progress",
                "step": "documents_loaded",
                "message": f"Loaded {len(manager.document_loader.documents)} documents ({len(chunks)} chunks)",
                "progress": 40
            }))
            
        except Exception as e:
            print(f"Document loader error: {e}")
            raise HTTPException(status_code=500, detail=f"Document loading failed: {str(e)}")
        
        # Initialize vector store using proven pattern from examples
        try:
            await manager.broadcast(json.dumps({
                "type": "initialization_progress",
                "step": "creating_vector_store",
                "message": "Creating vector database...",
                "progress": 60
            }))
            
            from langchain_openai.embeddings import OpenAIEmbeddings
            from langchain_community.vectorstores import Qdrant
            
            # Use the exact pattern from the examples
            embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
            manager.vector_store = Qdrant.from_documents(
                documents=chunks,
                embedding=embedding_model,
                location=":memory:"
            )
            manager.retriever = manager.vector_store.as_retriever()
            print("Vector store created successfully")
            
            await manager.broadcast(json.dumps({
                "type": "initialization_progress",
                "step": "vector_store_ready",
                "message": "Vector database created successfully",
                "progress": 80
            }))
            
        except Exception as e:
            print(f"Vector store error: {e}")
            raise HTTPException(status_code=500, detail=f"Vector store setup failed: {str(e)}")
        
        # Load complaint data for multi-agent system
        try:
            await manager.broadcast(json.dumps({
                "type": "initialization_progress",
                "step": "loading_complaints",
                "message": "Loading complaint data...",
                "progress": 85
            }))
            
            from langchain_community.document_loaders import CSVLoader
            complaint_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "complaints.csv")
            complaint_loader = CSVLoader(complaint_path, content_columns=["Consumer complaint narrative", "Company public response", "Company response to consumer"])
            complaints = complaint_loader.load()
            
            # Create complaint vector store
            complaint_vector_store = Qdrant.from_documents(
                documents=complaints,
                embedding=embedding_model,
                location=":memory:"
            )
            manager.complaint_retriever = complaint_vector_store.as_retriever()
            print("Complaint retriever created successfully")
            
        except Exception as e:
            print(f"Complaint retriever error: {e}")
            # Continue without complaint data
            manager.complaint_retriever = None
        
        # Initialize multi-agent system
        try:
            await manager.broadcast(json.dumps({
                "type": "initialization_progress",
                "step": "initializing_agents",
                "message": "Initializing multi-agent system...",
                "progress": 90
            }))
            
            # Create advanced retriever
            from core.advanced_retrieval import create_advanced_retriever
            advanced_retriever = create_advanced_retriever(
                vector_store=manager.vector_store,
                embedding_model=embedding_model,
                documents=manager.document_loader.chunks
            )
            
            manager.multi_agent_system = MultiAgentSystem(
                rag_retriever=advanced_retriever,
                complaint_retriever=manager.complaint_retriever,
                tavily_api_key=request.tavily_api_key,
                use_advanced_retrieval=True
            )
            print("Multi-agent system initialized successfully")
            
            await manager.broadcast(json.dumps({
                "type": "initialization_progress",
                "step": "complete",
                "message": "System ready! Multi-agent system initialized successfully.",
                "progress": 100
            }))
            
        except Exception as e:
            print(f"Multi-agent system error: {e}")
            raise HTTPException(status_code=500, detail=f"Multi-agent system setup failed: {str(e)}")
        
        # Mark system as initialized
        manager.system_initialized = True
        
        return {
            "success": True,
            "message": "System initialized successfully",
            "documents_loaded": len(manager.document_loader.documents),
            "chunks_created": len(manager.document_loader.chunks),
            "multi_agent_ready": manager.multi_agent_system is not None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"General initialization error: {e}")
        raise HTTPException(status_code=500, detail=f"Initialization failed: {str(e)}")

# WebSocket endpoint for real-time chat
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "chat_message":
                user_message = message_data["content"]
                
                # Send acknowledgment
                await manager.send_personal_message(
                    json.dumps({
                        "type": "message_received",
                        "content": user_message
                    }), 
                    websocket
                )
                
                # Process with RAG system (placeholder for now)
                # TODO: Integrate with multi-agent system
                response = await process_chat_message(user_message)
                
                # Send response
                await manager.send_personal_message(
                    json.dumps({
                        "type": "chat_response",
                        "content": response,
                        "timestamp": "now"
                    }), 
                    websocket
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def process_chat_message(message: str) -> str:
    """Process chat message with multi-agent system"""
    if not manager.system_initialized:
        return "System not initialized. Please initialize the system first."
    
    if not manager.multi_agent_system:
        return "Multi-agent system not available. Please check system initialization."
    
    try:
        # Use the multi-agent system to process the query
        response = manager.multi_agent_system.process_query(message)
        return response
        
    except Exception as e:
        print(f"Error processing chat message: {e}")
        return f"Error processing your question: {str(e)}"

# Run with: uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 