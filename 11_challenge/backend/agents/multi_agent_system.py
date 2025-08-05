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
    
    def __init__(self, rag_retriever, complaint_retriever, tavily_api_key: str = None, use_advanced_retrieval: bool = True, openai_api_key: str = None):
        """Initialize the multi-agent system.
        
        Args:
            rag_retriever: Retriever for student loan documents
            complaint_retriever: Retriever for complaint data
            tavily_api_key: Optional Tavily API key for real-time search
            use_advanced_retrieval: Whether to use advanced retrieval techniques
            openai_api_key: OpenAI API key for LLM access
        """
        self.rag_retriever = rag_retriever
        self.complaint_retriever = complaint_retriever
        self.tavily_api_key = tavily_api_key
        self.use_advanced_retrieval = use_advanced_retrieval
        
        # Get API key from parameter or environment
        import os
        api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key must be provided either as parameter or OPENAI_API_KEY environment variable")
        
        # Initialize LLM
        self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
        
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
    
    def process_query(self, query: str, max_iterations: int = 50) -> str:
        """Process a user query through the multi-agent system.
        
        Args:
            query: User's question about student loans
            max_iterations: Maximum number of agent iterations
            
        Returns:
            Final response from the multi-agent system
        """
        try:
            # Check if query is student loan related
            student_loan_keywords = [
                'student loan', 'loan', 'interest rate', 'federal', 'education', 
                'financial aid', 'fafsa', 'repayment', 'debt', 'borrower',
                'subsidized', 'unsubsidized', 'plus loan', 'pell grant'
            ]
            
            query_lower = query.lower()
            is_student_loan_related = any(keyword in query_lower for keyword in student_loan_keywords)
            
            if not is_student_loan_related:
                return "I'm a student loan assistant. I can help you with questions about federal student loans, financial aid, repayment options, and related topics. For other questions, please ask about student loans or financial aid."
            
            # Create initial state
            initial_state = {
                "messages": [HumanMessage(content=query)],
            }
            
            # Process through meta-supervisor
            final_response = None
            step_count = 0
            
            for step in self.meta_supervisor.stream(
                initial_state, 
                {"recursion_limit": max_iterations}
            ):
                step_count += 1
                if step_count > max_iterations:
                    print(f"Warning: Reached maximum iterations ({max_iterations})")
                    break
                    
                if "__end__" not in step:
                    # Extract the last message from each step
                    for key, value in step.items():
                        if key != "__end__" and isinstance(value, dict) and "messages" in value:
                            messages = value["messages"]
                            if messages and len(messages) > 0:
                                final_response = messages[-1].content
            
            return final_response if final_response else "I'm sorry, I couldn't process your request."
            
        except Exception as e:
            print(f"Error in multi-agent system: {e}")
            import traceback
            traceback.print_exc()
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