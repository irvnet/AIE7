"""
Multi-Agent System for Student Loan Assistant
Main interface that brings together all agent teams
Based on proven patterns from example code lessons 5-9
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from .research_team import create_research_team
from .response_team import create_response_team
from .meta_supervisor import create_meta_supervisor
from .tools import create_random_subdirectory


class MultiAgentSystem:
    """Main multi-agent system for student loan assistance."""
    
    def __init__(self, rag_retriever, complaint_retriever, tavily_api_key: str = None, use_advanced_retrieval: bool = True):
        """Initialize the multi-agent system.
        
        Args:
            rag_retriever: Retriever for student loan documents
            complaint_retriever: Retriever for complaint data
            tavily_api_key: Optional Tavily API key for real-time search
            use_advanced_retrieval: Whether to use advanced retrieval techniques
        """
        self.rag_retriever = rag_retriever
        self.complaint_retriever = complaint_retriever
        self.tavily_api_key = tavily_api_key
        self.use_advanced_retrieval = use_advanced_retrieval
        
        # Initialize LLM
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        
        # Create agent teams
        self.research_chain = create_research_team(
            self.llm, 
            self.rag_retriever, 
            self.tavily_api_key,
            use_advanced_retrieval
        )
        self.response_chain = create_response_team(
            self.llm, 
            self.complaint_retriever
        )
        
        # Create meta-supervisor
        self.meta_supervisor = create_meta_supervisor(
            self.llm,
            self.research_chain,
            self.response_chain
        )
        
        # Initialize working directory
        create_random_subdirectory()
    
    def process_query(self, query: str, max_iterations: int = 30) -> str:
        """Process a user query through the multi-agent system.
        
        Args:
            query: User's question about student loans
            max_iterations: Maximum number of agent iterations
            
        Returns:
            Final response from the multi-agent system
        """
        try:
            # Create initial state
            initial_state = {
                "messages": [HumanMessage(content=query)],
            }
            
            # Process through meta-supervisor
            final_response = None
            for step in self.meta_supervisor.stream(
                initial_state, 
                {"recursion_limit": max_iterations}
            ):
                if "__end__" not in step:
                    # Extract the last message from each step
                    for key, value in step.items():
                        if key != "__end__" and "messages" in value:
                            messages = value["messages"]
                            if messages:
                                final_response = messages[-1].content
            
            return final_response if final_response else "I'm sorry, I couldn't process your request."
            
        except Exception as e:
            print(f"Error in multi-agent system: {e}")
            return f"I encountered an error while processing your request: {str(e)}"
    
    def get_system_status(self) -> dict:
        """Get the status of the multi-agent system."""
        return {
            "research_team_ready": self.research_chain is not None,
            "response_team_ready": self.response_chain is not None,
            "meta_supervisor_ready": self.meta_supervisor is not None,
            "tavily_available": self.tavily_api_key is not None,
            "rag_retriever_ready": self.rag_retriever is not None,
            "complaint_retriever_ready": self.complaint_retriever is not None,
        } 