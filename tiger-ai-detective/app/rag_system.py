"""
RAG System for IBM Tiger Team Support
Provides AI-powered recommendations based on IBM documentation and support cases
"""

import os
import logging
from typing import List, Dict, Optional, Any
from pathlib import Path
from dataclasses import dataclass

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, START, END
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import TypedDict, List
import tiktoken

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RAGConfig:
    """Configuration for the Tiger Team RAG system"""
    embedding_model: str = "text-embedding-3-large"  # Use large model for better performance
    collection_name: str = "ibm_tiger_team_docs"
    location: str = ":memory:"  # Use in-memory for development
    chunk_size: int = 750
    chunk_overlap: int = 0

@dataclass
class RetrievalResult:
    """Result of a retrieval operation"""
    documents: List
    scores: List[float]
    metadata: List[Dict[str, Any]]

class RAGState(TypedDict):
    """State for the RAG system"""
    question: str
    context: List
    response: str
    case_info: Optional[Dict]

class TigerTeamRAGSystem:
    """RAG system for IBM Tiger Team Support - Based on proven patterns"""
    
    def __init__(self, config: Optional[RAGConfig] = None):
        self.config = config or RAGConfig()
        self.embedding_model = None
        self.vectorstore = None
        self.rag_graph = None
        self.llm = None
        self.tavily_tool = None
        self.is_initialized = False
        
    def initialize(self, openai_api_key: str, progress_callback=None) -> Dict[str, Any]:
        """Initialize the RAG system with IBM documentation and optional progress callback"""
        try:
            logger.info("Initializing Tiger Team RAG system...")
            
            if progress_callback:
                progress_callback(0.05, "🔧 Setting up OpenAI API...")
            
            # Set OpenAI API key
            os.environ["OPENAI_API_KEY"] = openai_api_key
            
            # Check if API key is available
            if not os.getenv("OPENAI_API_KEY"):
                return {
                    "success": False,
                    "error": "OpenAI API key not found. Set OPENAI_API_KEY environment variable."
                }
            
            if progress_callback:
                progress_callback(0.1, "🧠 Initializing embedding model...")
            
            # Initialize embedding model
            self.embedding_model = OpenAIEmbeddings(model=self.config.embedding_model)
            
            # Test embedding model
            test_embedding = self.embedding_model.embed_query("test")
            if not test_embedding:
                return {
                    "success": False,
                    "error": "Failed to create test embedding"
                }
            
            if progress_callback:
                progress_callback(0.15, "🤖 Initializing language model...")
            
            # Initialize LLM
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
            
            if progress_callback:
                progress_callback(0.2, "🔍 Setting up web search tools...")
            
            # Initialize web search tool (optional)
            self.tavily_tool = None
            try:
                # Check if Tavily API key is available
                tavily_api_key = os.getenv("TAVILY_API_KEY")
                if tavily_api_key:
                    self.tavily_tool = TavilySearchResults(max_results=5, api_key=tavily_api_key)
                    logger.info("Tavily web search tool initialized")
                else:
                    logger.warning("Tavily API key not found - web search will be disabled")
            except Exception as e:
                logger.warning(f"Failed to initialize Tavily tool: {str(e)} - web search will be disabled")
            
            if progress_callback:
                progress_callback(0.25, "📚 Loading IBM documentation PDFs...")
            
            # Load and process IBM documentation
            logger.info("Loading IBM documentation PDFs...")
            docs_path = Path("data/documentation")
            if not docs_path.exists():
                return {
                    "success": False,
                    "error": f"Documentation path not found: {docs_path}"
                }
                
            directory_loader = DirectoryLoader(
                str(docs_path), 
                glob="**/*.pdf", 
                loader_cls=PyMuPDFLoader
            )
            documents = directory_loader.load()
            
            if not documents:
                return {
                    "success": False,
                    "error": "No documents loaded from documentation directory"
                }
                
            logger.info(f"Loaded {len(documents)} documents")
            
            if progress_callback:
                progress_callback(0.4, f"📄 Processing {len(documents)} documents...")
            
            # Chunk documents with proven strategy
            def tiktoken_len(text):
                tokens = tiktoken.encoding_for_model("gpt-4o").encode(text)
                return len(tokens)
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.config.chunk_size,
                chunk_overlap=self.config.chunk_overlap,
                length_function=tiktoken_len,
            )
            chunks = text_splitter.split_documents(documents)
            logger.info(f"Created {len(chunks)} chunks from documents")
            
            if progress_callback:
                progress_callback(0.6, f"✂️ Created {len(chunks)} text chunks...")
            
            # Create vector store
            logger.info("Creating vector database...")
            if progress_callback:
                progress_callback(0.7, "🗄️ Creating vector database...")
            
            self.vectorstore = Qdrant.from_documents(
                documents=chunks,
                embedding=self.embedding_model,
                location=self.config.location,
                collection_name=self.config.collection_name
            )
            
            if progress_callback:
                progress_callback(0.85, "🔗 Setting up RAG processing graph...")
            
            # Create RAG graph
            self._create_rag_graph()
            
            if progress_callback:
                progress_callback(0.95, "✅ Finalizing system setup...")
            
            self.is_initialized = True
            logger.info("Tiger Team RAG system initialized successfully!")
            
            if progress_callback:
                progress_callback(1.0, "🎉 System initialization complete!")
            
            return {
                "success": True,
                "message": f"RAG system initialized with {len(chunks)} chunks from {len(documents)} documents"
            }
            
        except Exception as e:
            logger.error(f"Error initializing RAG system: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to initialize RAG system: {str(e)}"
            }
    
    def _create_rag_graph(self):
        """Create the RAG processing graph"""
        
        # Create prompt template for Tiger Team recommendations
        TIGER_TEAM_TEMPLATE = """
        You are an IBM Tiger Team specialist providing expert recommendations for support cases.
        
        CONTEXT FROM IBM DOCUMENTATION:
        {context}
        
        CASE INFORMATION:
        {case_info}
        
        USER QUERY:
        {query}
        
        Based on the IBM documentation context and case information, provide:
        1. **Technical Analysis**: What the issue likely involves based on IBM best practices
        2. **Recommended Actions**: Specific steps the Tiger Team should take
        3. **Documentation References**: Key IBM guides and sections to consult
        4. **Risk Assessment**: Potential impact and urgency considerations
        5. **Next Steps**: Immediate actions and follow-up recommendations
        
        Focus on practical, actionable advice that leverages IBM's official documentation and best practices.
        If the context doesn't contain relevant information, say so and suggest general troubleshooting approaches.
        """
        
        chat_prompt = ChatPromptTemplate.from_messages([("human", TIGER_TEAM_TEMPLATE)])
        
        def retrieve(state: RAGState) -> RAGState:
            """Retrieve relevant documentation"""
            try:
                retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
                retrieved_docs = retriever.invoke(state["question"])
                return {"context": retrieved_docs}
            except Exception as e:
                logger.error(f"Error in retrieve: {str(e)}")
                return {"context": []}
        
        def generate(state: RAGState) -> RAGState:
            """Generate recommendations"""
            try:
                # Format context for the prompt
                context_text = ""
                if state.get("context"):
                    context_text = "\n\n".join([doc.page_content for doc in state["context"]])
                
                # Format case info
                case_info_text = ""
                if state.get("case_info"):
                    case_info_text = f"""
                    Product: {state['case_info'].get('product', 'Unknown')}
                    Priority: {state['case_info'].get('priority', 'Unknown')}
                    Description: {state['case_info'].get('description', 'No description')}
                    """
                
                generator_chain = chat_prompt | self.llm | StrOutputParser()
                response = generator_chain.invoke({
                    "query": state["question"],
                    "context": context_text,
                    "case_info": case_info_text
                })
                return {"response": response}
            except Exception as e:
                logger.error(f"Error in generate: {str(e)}")
                return {"response": f"Error generating recommendations: {str(e)}"}
        
        # Build the graph
        graph_builder = StateGraph(RAGState)
        graph_builder.add_node("retrieve", retrieve)
        graph_builder.add_node("generate", generate)
        graph_builder.add_edge(START, "retrieve")
        graph_builder.add_edge("retrieve", "generate")
        graph_builder.add_edge("generate", END)
        
        self.rag_graph = graph_builder.compile()
    
    def get_recommendations(self, case_description: str, product_name: str = "General", 
                          priority: str = "Medium", additional_context: str = "") -> str:
        """Get AI recommendations for a support case using multiple tools"""
        if not self.is_initialized:
            return "RAG system not initialized. Please check your OpenAI API key and try again."
        
        try:
            # Prepare case information
            case_info = {
                "product": product_name,
                "priority": priority,
                "description": case_description,
                "additional_context": additional_context
            }
            
            # Create comprehensive query
            query = f"""
            IBM Product: {product_name}
            Priority: {priority}
            Issue Description: {case_description}
            Additional Context: {additional_context}
            
            Please provide comprehensive recommendations for this Tiger Team support case.
            """
            
            # Use multiple tools for comprehensive research
            recommendations = self._get_comprehensive_recommendations(query, case_info)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            return f"Error generating recommendations: {str(e)}"
    
    def get_architecture_guidance(self, architecture_question: str) -> str:
        """Get specialized IBM architecture and integration guidance"""
        if not self.is_initialized:
            return "RAG system not initialized. Please check your OpenAI API key and try again."
        
        try:
            # Create specialized architecture query
            query = f"""
            IBM Architecture Question: {architecture_question}
            
            Focus on:
            - Enterprise architecture patterns
            - System integration best practices
            - Performance optimization strategies
            - Deployment and scalability patterns
            - Security and compliance considerations
            """
            
            # Use specialized architecture research
            guidance = self._get_architecture_recommendations(query, architecture_question)
            
            return guidance
            
        except Exception as e:
            logger.error(f"Error getting architecture guidance: {str(e)}")
            return f"Error generating architecture guidance: {str(e)}"
    
    def _get_comprehensive_recommendations(self, query: str, case_info: Dict) -> str:
        """Get recommendations using multiple tools"""
        try:
            # 1. Search local IBM documentation
            local_results = self.search_documentation(query, max_results=3)
            
            # 2. Search web for current information
            web_results = self.search_web(query)
            
            # 3. Search IBM-specific resources
            ibm_results = self.search_ibm_resources(query, case_info["product"])
            
            # 4. Combine and synthesize results
            combined_context = self._combine_search_results(local_results, web_results, ibm_results)
            
            # 5. Generate final recommendations
            final_prompt = f"""
            Based on the following comprehensive research, provide detailed Tiger Team recommendations:

            LOCAL IBM DOCUMENTATION:
            {combined_context['local']}

            WEB SEARCH RESULTS:
            {combined_context['web']}

            IBM-SPECIFIC RESOURCES:
            {combined_context['ibm']}

            CASE INFORMATION:
            Product: {case_info['product']}
            Priority: {case_info['priority']}
            Description: {case_info['description']}

            Please provide:
            1. Technical Analysis
            2. Recommended Actions
            3. Documentation References
            4. Risk Assessment
            5. Next Steps
            """
            
            # Use LLM to generate final recommendations
            response = self.llm.invoke(final_prompt)
            return response.content
            
        except Exception as e:
            logger.error(f"Error in comprehensive recommendations: {str(e)}")
            return f"Error generating comprehensive recommendations: {str(e)}"
    
    def _get_architecture_recommendations(self, query: str, architecture_question: str) -> str:
        """Get specialized architecture and integration guidance"""
        try:
            # 1. Search local IBM documentation for architecture patterns
            local_results = self.search_documentation(query, max_results=5)
            
            # 2. Search web for current IBM architecture best practices
            web_results = self.search_web(f"IBM enterprise architecture {architecture_question}")
            
            # 3. Search IBM-specific architecture resources
            ibm_results = self.search_ibm_resources(f"IBM architecture patterns {architecture_question}", "Architecture")
            
            # 4. Combine and synthesize results
            combined_context = self._combine_search_results(local_results, web_results, ibm_results)
            
            # 5. Generate specialized architecture guidance
            architecture_prompt = f"""
            As an IBM Enterprise Architecture Specialist, provide comprehensive guidance for this architecture question:

            QUESTION: {architecture_question}

            RESEARCH CONTEXT:
            LOCAL IBM DOCUMENTATION:
            {combined_context['local']}

            WEB SEARCH RESULTS:
            {combined_context['web']}

            IBM-SPECIFIC RESOURCES:
            {combined_context['ibm']}

            Please provide a structured architecture guidance response with:

            🏗️ **ARCHITECTURAL OVERVIEW**
            - High-level architectural approach
            - Key components and their relationships
            - Integration patterns to consider

            🔗 **INTEGRATION STRATEGY**
            - How to connect the IBM products
            - Communication patterns and protocols
            - Data flow and messaging architecture

            ⚡ **PERFORMANCE CONSIDERATIONS**
            - Scalability patterns
            - Performance optimization strategies
            - Resource allocation recommendations

            ☁️ **DEPLOYMENT ARCHITECTURE**
            - Deployment patterns (on-prem, cloud, hybrid)
            - Infrastructure requirements
            - High availability and disaster recovery

            🔒 **SECURITY & COMPLIANCE**
            - Security architecture patterns
            - Authentication and authorization strategies
            - Compliance considerations

            📋 **IMPLEMENTATION ROADMAP**
            - Phased implementation approach
            - Key milestones and deliverables
            - Risk mitigation strategies

            📚 **REFERENCE ARCHITECTURES**
            - Relevant IBM reference architectures
            - Best practice documentation
            - Additional resources for implementation

            Focus on enterprise-grade, production-ready architectural patterns that follow IBM best practices.
            """
            
            # Use LLM to generate specialized architecture guidance
            response = self.llm.invoke(architecture_prompt)
            return response.content
            
        except Exception as e:
            logger.error(f"Error in architecture recommendations: {str(e)}")
            return f"Error generating architecture recommendations: {str(e)}"
    
    def search_web(self, query: str) -> List[str]:
        """Search the web for current information"""
        try:
            if not self.tavily_tool:
                return ["Web search not available"]
            
            results = self.tavily_tool.invoke(query)
            # Handle both list and dict responses from Tavily
            if isinstance(results, list):
                return [str(result.get("content", result)) for result in results[:3]]
            else:
                return [str(results)]
        except Exception as e:
            logger.error(f"Error searching web: {str(e)}")
            return [f"Web search error: {str(e)}"]
    
    def search_ibm_resources(self, query: str, product_name: str) -> List[str]:
        """Search IBM-specific resources"""
        try:
            if not self.tavily_tool:
                return ["IBM search not available"]
            
            # Search IBM-specific resources
            ibm_query = f"IBM {product_name} {query} site:ibm.com"
            results = self.tavily_tool.invoke(ibm_query)
            # Handle both list and dict responses from Tavily
            if isinstance(results, list):
                return [str(result.get("content", result)) for result in results[:3]]
            else:
                return [str(results)]
        except Exception as e:
            logger.error(f"Error searching IBM resources: {str(e)}")
            return [f"IBM search error: {str(e)}"]
    
    def _combine_search_results(self, local_results: List[str], web_results: List[str], ibm_results: List[str]) -> Dict[str, str]:
        """Combine search results from different sources"""
        return {
            "local": "\n\n".join(local_results) if local_results else "No local documentation found",
            "web": "\n\n".join(web_results) if web_results else "No web results found",
            "ibm": "\n\n".join(ibm_results) if ibm_results else "No IBM-specific results found"
        }
    
    def search_documentation(self, query: str, max_results: int = 5) -> List[str]:
        """Search IBM documentation for specific information"""
        if not self.is_initialized:
            return ["RAG system not initialized"]
        
        try:
            retriever = self.vectorstore.as_retriever(search_kwargs={"k": max_results})
            results = retriever.invoke(query)
            return [doc.page_content for doc in results]
        except Exception as e:
            logger.error(f"Error searching documentation: {str(e)}")
            return [f"Error searching documentation: {str(e)}"]
    
    def get_system_status(self) -> Dict:
        """Get the current status of the RAG system"""
        return {
            "initialized": self.is_initialized,
            "has_vectorstore": self.vectorstore is not None,
            "has_llm": self.llm is not None,
            "has_embeddings": self.embedding_model is not None
        }
