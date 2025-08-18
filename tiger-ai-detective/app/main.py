import streamlit as st
import os
import sys
from pathlib import Path
import tempfile
import uuid
from datetime import datetime, timedelta
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import necessary components
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage
import operator
import functools
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.tools import BaseTool
from langchain_core.tools import tool
from typing import Dict, Optional

# Import our models
from app.models.database import SessionLocal, engine
from app.models.schemas import Base, Customer, Product, TigerTeamMember, SupportTicket, Case, Evidence

# Set page config
st.set_page_config(
    page_title="IBM Tiger Team Support",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0066cc;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0066cc;
        margin: 1rem 0;
    }
    .response-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .case-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
    .critical { border-left: 4px solid #dc3545; }
    .high { border-left: 4px solid #fd7e14; }
    .medium { border-left: 4px solid #ffc107; }
    .low { border-left: 4px solid #28a745; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'system_initialized' not in st.session_state:
    st.session_state.system_initialized = False
if 'current_case' not in st.session_state:
    st.session_state.current_case = None

def initialize_system():
    """Initialize the RAG system and database"""
    try:
        # Create database tables
        Base.metadata.create_all(bind=engine)
        
        # Initialize OpenAI components
        openai_chat_model = ChatOpenAI(model="gpt-4o-mini")
        embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
        
        # Create a simple RAG system for IBM documentation
        # In a real system, this would load actual IBM documentation
        ibm_docs = [
            "IBM WebSphere Application Server is an enterprise Java application server for building, deploying, and managing applications.",
            "Common WebSphere issues include memory leaks, performance degradation, and cluster communication failures.",
            "IBM Db2 Database is an enterprise database management system with advanced analytics capabilities.",
            "Db2 performance issues often relate to connection pooling, query optimization, and storage management.",
            "IBM MQ provides enterprise messaging middleware for reliable application integration.",
            "MQ issues typically involve message delivery, queue management, and security configuration.",
            "Tiger Team best practices include thorough research, evidence collection, and systematic problem-solving approaches."
        ]
        
        # Create vector store
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=750,
            chunk_overlap=0,
            length_function=lambda text: len(tiktoken.encoding_for_model("gpt-4o").encode(text))
        )
        
        from langchain_core.documents import Document
        documents = [Document(page_content=doc) for doc in ibm_docs]
        chunks = text_splitter.split_documents(documents)
        
        qdrant_vectorstore = Qdrant.from_documents(
            documents=chunks,
            embedding=embedding_model,
            location=":memory:"
        )
        qdrant_retriever = qdrant_vectorstore.as_retriever()
        
        # Create RAG chain
        HUMAN_TEMPLATE = """
        #CONTEXT:
        {context}

        QUERY:
        {query}

        You are an expert IBM Tiger Team specialist. Use the provided context to answer the query about IBM products and support issues. 
        Provide practical, actionable advice based on the context. If you don't know the answer, say "I don't have enough information to answer this question."
        """
        chat_prompt = ChatPromptTemplate.from_messages([("human", HUMAN_TEMPLATE)])
        
        class State(TypedDict):
            question: str
            context: List
            response: str

        def retrieve(state: State) -> State:
            retrieved_docs = qdrant_retriever.invoke(state["question"])
            return {"context": retrieved_docs}

        def generate(state: State) -> State:
            generator_chain = chat_prompt | openai_chat_model | StrOutputParser()
            response = generator_chain.invoke({"query": state["question"], "context": state["context"]})
            return {"response": response}

        graph_builder = StateGraph(State)
        graph_builder = graph_builder.add_sequence([retrieve, generate])
        graph_builder.add_edge(START, "retrieve")
        rag_graph = graph_builder.compile()
        
        # Store in session state
        st.session_state.rag_graph = rag_graph
        st.session_state.openai_chat_model = openai_chat_model
        st.session_state.system_initialized = True
        
        st.success("System initialized successfully!")
        return True
        
    except Exception as e:
        st.error(f"Error initializing system: {str(e)}")
        return False

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_ai_recommendations(case_description: str, product_name: str) -> str:
    """Get AI recommendations for a case"""
    try:
        if not st.session_state.system_initialized:
            return "System not initialized. Please check your API keys and try again."
        
        query = f"Case: {case_description}. Product: {product_name}. What are the key areas to research and potential solutions?"
        result = st.session_state.rag_graph.invoke({"question": query})
        return result.get("response", "No recommendations generated.")
        
    except Exception as e:
        return f"Error generating recommendations: {str(e)}"

def create_case_form():
    """Create a new case form"""
    st.markdown("### 📋 Create New Tiger Team Case")
    
    with st.form("new_case_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Get data from database
            db = SessionLocal()
            try:
                customers = db.query(Customer).all()
                products = db.query(Product).all()
                members = db.query(TigerTeamMember).filter(TigerTeamMember.is_available == True).all()
            finally:
                db.close()
            
            customer_id = st.selectbox(
                "Customer",
                options=[None] + customers,
                format_func=lambda x: "Select a customer..." if x is None else f"{x.company} - {x.name}"
            )
            
            product_id = st.selectbox(
                "IBM Product",
                options=[None] + products,
                format_func=lambda x: "Select a product..." if x is None else f"{x.name} {x.version}"
            )
            
            priority = st.selectbox("Priority", ["Select priority...", "Critical", "High", "Medium", "Low"], index=0)
            
        with col2:
            assigned_member_id = st.selectbox(
                "Assign to Tiger Team Member",
                options=[None] + members,
                format_func=lambda x: "Select a team member..." if x is None else f"{x.name} ({x.expertise_areas[0] if x.expertise_areas else 'General'})"
            )
            
            support_ticket = st.text_input("Support Ticket Number (PMR)", placeholder="e.g., PMR123456")
            desired_outcome = st.text_area("Desired Outcome", placeholder="Describe the desired resolution or outcome...")
        
        title = st.text_input("Case Title", placeholder="Enter a descriptive title for this case...")
        description = st.text_area("Case Description", height=150, placeholder="Provide a detailed description of the issue, including symptoms, error messages, and any relevant context...")
        
        submitted = st.form_submit_button("🚀 Create Case & Generate AI Research")
        
        if submitted:
            # Validate required fields
            if not title or title.strip() == "":
                st.error("Please enter a case title.")
                return
            if not description or description.strip() == "":
                st.error("Please enter a case description.")
                return
            if customer_id is None:
                st.error("Please select a customer.")
                return
            if product_id is None:
                st.error("Please select an IBM product.")
                return
            if assigned_member_id is None:
                st.error("Please select a team member.")
                return
            if priority == "Select priority...":
                st.error("Please select a priority level.")
                return
            try:
                db = SessionLocal()
                
                # Create case
                case_number = f"TT{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:4]}" # Changed to use uuid for uniqueness
                
                new_case = Case(
                    case_number=case_number,
                    support_ticket_id=None,  # Would link to actual ticket
                    customer_id=customer_id.id,
                    product_id=product_id.id,
                    assigned_member_id=assigned_member_id.id,
                    title=title.strip(),
                    description=description.strip(),
                    desired_outcome=desired_outcome.strip() if desired_outcome else None,
                    priority=priority,
                    status="Open"
                )
                
                db.add(new_case)
                db.commit()
                db.refresh(new_case)
                
                # Generate AI recommendations
                with st.spinner("🤖 Generating AI research recommendations..."):
                    recommendations = get_ai_recommendations(description, product_id.name)
                    new_case.ai_recommendations = recommendations
                    db.commit()
                
                st.success(f"✅ Case {case_number} created successfully!")
                st.session_state.current_case = new_case
                
                # Display recommendations
                st.markdown("### 🤖 AI Research Recommendations")
                st.markdown(f'<div class="response-box">{recommendations}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error creating case: {str(e)}")
            finally:
                db.close()

def display_cases():
    """Display existing cases"""
    st.markdown("### 📊 Active Tiger Team Cases")
    
    db = SessionLocal()
    try:
        # Get all cases (not just active ones) for better overview
        cases = db.query(Case).order_by(Case.created_at.desc()).all()
        
        if not cases:
            st.info("No cases found in the system.")
            return
        
        # Show summary statistics
        total_cases = len(cases)
        active_cases = len([c for c in cases if c.status != "Resolved"])
        critical_cases = len([c for c in cases if c.priority == "Critical"])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Cases", total_cases)
        with col2:
            st.metric("Active Cases", active_cases)
        with col3:
            st.metric("Critical Priority", critical_cases)
        
        st.markdown("---")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Open", "Research", "Customer Call", "Resolved"],
                index=0
            )
        with col2:
            priority_filter = st.selectbox(
                "Filter by Priority",
                ["All", "Critical", "High", "Medium", "Low"],
                index=0
            )
        with col3:
            show_resolved = st.checkbox("Show Resolved Cases", value=False)
        
        # Apply filters
        filtered_cases = cases
        if status_filter != "All":
            filtered_cases = [c for c in filtered_cases if c.status == status_filter]
        if priority_filter != "All":
            filtered_cases = [c for c in filtered_cases if c.priority == priority_filter]
        if not show_resolved:
            filtered_cases = [c for c in filtered_cases if c.status != "Resolved"]
        
        st.markdown(f"**Showing {len(filtered_cases)} of {total_cases} cases**")
        
        # Display cases
        for case in filtered_cases:
            # Get customer and product info
            customer = db.query(Customer).filter(Customer.id == case.customer_id).first()
            product = db.query(Product).filter(Product.id == case.product_id).first()
            assigned_member = db.query(TigerTeamMember).filter(TigerTeamMember.id == case.assigned_member_id).first()
            
            # Priority color coding
            priority_colors = {
                "Critical": "🔴",
                "High": "🟠", 
                "Medium": "🟡",
                "Low": "🟢"
            }
            priority_icon = priority_colors.get(case.priority, "⚪")
            
            with st.expander(f"{priority_icon} {case.case_number}: {case.title}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Status:** {case.status}")
                    st.markdown(f"**Priority:** {case.priority}")
                    st.markdown(f"**Customer:** {customer.company if customer else 'Unknown'}")
                    st.markdown(f"**Product:** {product.name if product else 'Unknown'} {product.version if product else ''}")
                    st.markdown(f"**Description:** {case.description}")
                    
                    if case.ai_recommendations:
                        st.markdown("**AI Recommendations:**")
                        st.markdown(f'<div class="response-box">{case.ai_recommendations}</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**Created:** {case.created_at.strftime('%Y-%m-%d %H:%M')}")
                    st.markdown(f"**Assigned:** {assigned_member.name if assigned_member else 'Unassigned'}")
                    if case.support_ticket_id:
                        st.markdown(f"**Support Ticket:** {case.support_ticket_id}")
                    if case.desired_outcome:
                        st.markdown(f"**Desired Outcome:** {case.desired_outcome}")
                    
                    if st.button(f"View Details", key=f"view_{case.id}"):
                        st.session_state.current_case = case
                        st.rerun()
    finally:
        db.close()

def research_assistant():
    """AI Research Assistant"""
    st.markdown("### 🔍 AI Research Assistant")
    
    if not st.session_state.system_initialized:
        st.warning("Please initialize the system first.")
        return
    
    user_question = st.text_area(
        "Ask about IBM products, support issues, or research strategies:",
        height=100,
        placeholder="e.g., How do I troubleshoot WebSphere memory leaks? What are common Db2 performance issues?"
    )
    
    if st.button("🔍 Get AI Research", type="primary"):
        if user_question.strip():
            with st.spinner("Researching..."):
                response = get_ai_recommendations(user_question, "General")
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "question": user_question,
                    "answer": response,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                
                # Display response
                st.markdown("### 📝 Research Results")
                st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)
        else:
            st.warning("Please enter a question.")

# Main app interface
def main():
    st.markdown('<h1 class="main-header">🦁 IBM Tiger Team Support</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered case management for critical IBM support issues</p>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Keys
        openai_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
        
        if openai_key:
            os.environ["OPENAI_API_KEY"] = openai_key
        
        # Initialize button
        if st.button("🚀 Initialize System", type="primary"):
            if not openai_key:
                st.error("Please enter OpenAI API key")
            else:
                with st.spinner("Initializing system..."):
                    initialize_system()
        
        st.markdown("---")
        st.markdown("### 📋 Quick Actions")
        
        if st.button("📊 View All Cases"):
            st.session_state.show_cases = True
            st.session_state.show_create = False
            st.session_state.show_research = False
        
        if st.button("➕ Create New Case"):
            st.session_state.show_create = True
            st.session_state.show_cases = False
            st.session_state.show_research = False
        
        if st.button("🔍 Research Assistant"):
            st.session_state.show_research = True
            st.session_state.show_cases = False
            st.session_state.show_create = False
    
    # Initialize session state for navigation
    if 'show_cases' not in st.session_state:
        st.session_state.show_cases = False
    if 'show_create' not in st.session_state:
        st.session_state.show_create = False
    if 'show_research' not in st.session_state:
        st.session_state.show_research = False
    
    # Main content area - use conditional rendering based on session state
    if st.session_state.show_cases:
        st.markdown("### 📊 View All Cases")
        display_cases()
        if st.button("← Back to Main Menu"):
            st.session_state.show_cases = False
            st.session_state.show_create = False
            st.session_state.show_research = False
            st.rerun()
    
    elif st.session_state.show_create:
        create_case_form()
        if st.button("← Back to Main Menu"):
            st.session_state.show_cases = False
            st.session_state.show_create = False
            st.session_state.show_research = False
            st.rerun()
    
    elif st.session_state.show_research:
        research_assistant()
        if st.button("← Back to Main Menu"):
            st.session_state.show_cases = False
            st.session_state.show_create = False
            st.session_state.show_research = False
            st.rerun()
    
    else:
        # Default view - show main dashboard
        st.markdown("### 🎯 Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 View All Cases", type="primary", use_container_width=True):
                st.session_state.show_cases = True
                st.rerun()
        
        with col2:
            if st.button("➕ Create New Case", type="primary", use_container_width=True):
                st.session_state.show_create = True
                st.rerun()
        
        with col3:
            if st.button("🔍 Research Assistant", type="primary", use_container_width=True):
                st.session_state.show_research = True
                st.rerun()
        
        st.markdown("---")
        
        # Show tabs for detailed access
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Create Case", "📊 View Cases", "🔍 Research Assistant", "📜 History"])
        
        with tab1:
            create_case_form()
        
        with tab2:
            display_cases()
        
        with tab3:
            research_assistant()
        
        with tab4:
            if st.session_state.chat_history:
                st.markdown("### 📜 Research History")
                for i, chat in enumerate(reversed(st.session_state.chat_history)):
                    with st.expander(f"Q: {chat['question'][:50]}..."):
                        st.markdown(f"**Question:** {chat['question']}")
                        st.markdown(f"**Answer:** {chat['answer']}")
                        st.caption(f"Asked: {chat['timestamp']}")
            else:
                st.info("No research history yet.")

if __name__ == "__main__":
    main()
