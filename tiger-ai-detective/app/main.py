import streamlit as st
import os
import sys
from pathlib import Path
import tempfile
import uuid
from datetime import datetime, timedelta
import json
import logging

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

# Import RAG system
from app.rag_system import TigerTeamRAGSystem

# Import admin module
from app.admin import AdminManager

# Set page config
st.set_page_config(
    page_title="IBM Tiger Team Support",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# IBM Carbon Design System - Gray 10 Theme
st.markdown("""
<link rel="stylesheet" href="https://unpkg.com/@carbon/styles/css/styles-g10.css">
<style>
    /* IBM Carbon Design System - Gray 10 Theme */
    /* Using official Carbon tokens - no hardcoded hex values */
    
    /* Global styles - Body text on ui-background */
    .main .block-container {
        background-color: var(--cds-ui-background);
        color: var(--cds-text-01);
    }
    
    .stApp {
        background-color: var(--cds-ui-background);
    }
    
    /* Headers - text-01 for hierarchy */
    .main-header {
        font-size: 2.5rem;
        color: var(--cds-text-01);
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: var(--cds-text-01);
        margin-bottom: 1rem;
    }
    
    /* Content boxes - layer-01 with borders */
    .info-box {
        background-color: var(--cds-layer-01);
        color: var(--cds-text-01);
        padding: 1rem;
        border-radius: 0.25rem;
        border: 1px solid var(--cds-border-subtle-01);
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
    }
    
    .response-box {
        background-color: var(--cds-layer-01);
        color: var(--cds-text-01);
        padding: 1.5rem;
        border-radius: 0.25rem;
        border: 1px solid var(--cds-border-subtle-01);
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
    }
    
    .case-card {
        background-color: var(--cds-layer-01);
        color: var(--cds-text-01);
        padding: 1rem;
        border-radius: 0.25rem;
        border: 1px solid var(--cds-border-subtle-01);
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
    }
    
    /* Priority indicators - semantic colors */
    .critical { border-left: 4px solid var(--cds-support-01); }
    .high { border-left: 4px solid var(--cds-support-03); }
    .medium { border-left: 4px solid var(--cds-support-04); }
    .low { border-left: 4px solid var(--cds-support-02); }
    
    /* Case details - layer-01 for content */
    .case-details {
        color: var(--cds-text-01);
        background-color: var(--cds-layer-01);
        padding: 1rem;
        border-radius: 0.25rem;
        border: 1px solid var(--cds-border-subtle-01);
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
    }
    
    /* Fix field visibility issues - use explicit dark grey for better contrast */
    .case-description-field {
        background-color: #393939 !important;
        color: #ffffff !important;
        border: 1px solid #525252 !important;
        border-radius: 0.25rem;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }
    
    .ai-recommendations-field {
        background-color: #393939 !important;
        color: #ffffff !important;
        border: 1px solid #525252 !important;
        border-radius: 0.25rem;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }
    
    .research-data-field {
        background-color: #393939 !important;
        color: #ffffff !important;
        border: 1px solid #525252 !important;
        border-radius: 0.25rem;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }
    
    /* Text visibility - body text uses text-01 */
    .stMarkdown, .stText, .stMarkdown p, .stMarkdown div {
        color: var(--cds-text-01);
    }
    
    /* Streamlit elements - proper interactive states */
    .stButton > button {
        background-color: var(--cds-interactive-01);
        color: var(--cds-text-on-color);
        border: 1px solid var(--cds-interactive-01);
        border-radius: 0.25rem;
        outline: none;
    }
    
    .stButton > button:hover {
        background-color: var(--cds-hover-primary);
        color: var(--cds-text-on-color);
    }
    
    .stButton > button:focus {
        outline: 2px solid var(--cds-focus);
        outline-offset: 2px;
    }
    
    /* Sidebar - ui-01 for secondary area */
    .css-1d391kg {
        background-color: var(--cds-ui-01);
    }
    
    /* Metrics - layer-02 for data display */
    .stMetric {
        background-color: var(--cds-layer-02);
        color: var(--cds-text-01);
        border-radius: 0.25rem;
        border: 1px solid var(--cds-border-subtle-01);
    }
    
    /* Expanders - layer-02 for collapsible content */
    .streamlit-expanderHeader {
        background-color: var(--cds-layer-02);
        color: var(--cds-text-01);
        border-radius: 0.25rem;
        border: 1px solid var(--cds-border-subtle-01);
    }
    
    /* Form elements - layer-01 with borders */
    .stTextInput > div > div > input {
        background-color: var(--cds-layer-01);
        color: var(--cds-text-01);
        border: 1px solid var(--cds-border-subtle-01);
        border-radius: 0.25rem;
    }
    
    .stTextInput > div > div > input:focus {
        outline: 2px solid var(--cds-focus);
        outline-offset: 2px;
    }
    
    .stSelectbox > div > div > div {
        background-color: var(--cds-layer-01);
        color: var(--cds-text-01);
        border-radius: 0.25rem;
        border: 1px solid var(--cds-border-subtle-01);
    }
    
    .stSelectbox > div > div > div:focus {
        outline: 2px solid var(--cds-focus);
        outline-offset: 2px;
    }
    
    /* Textarea */
    .stTextArea > div > div > textarea {
        background-color: var(--cds-layer-01);
        color: var(--cds-text-01);
        border: 1px solid var(--cds-border-subtle-01);
        border-radius: 0.25rem;
    }
    
    .stTextArea > div > div > textarea:focus {
        outline: 2px solid var(--cds-focus);
        outline-offset: 2px;
    }
    
    /* Checkbox */
    .stCheckbox > div > div {
        background-color: var(--cds-layer-01);
        color: var(--cds-text-01);
    }
    
    /* Links */
    a {
        color: var(--cds-interactive-01);
    }
    
    a:hover {
        color: var(--cds-hover-primary);
    }
    
    /* Tables */
    .stTable {
        background-color: var(--cds-layer-02);
        color: var(--cds-text-01);
        border: 1px solid var(--cds-border-subtle-01);
        border-radius: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'system_initialized' not in st.session_state:
    st.session_state.system_initialized = False
if 'current_case' not in st.session_state:
    st.session_state.current_case = None

# Add debug logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_system():
    """Initialize the RAG system and database"""
    try:
        # Create database tables
        Base.metadata.create_all(bind=engine)
        
        # Get API keys from admin manager
        admin = AdminManager()
        openai_api_key = admin.get_api_key("openai_api_key")
        if not openai_api_key:
            st.error("Please configure your OpenAI API key in the Admin page.")
            return False
        
        # Initialize the Tiger Team RAG system
        rag_system = TigerTeamRAGSystem()
        result = rag_system.initialize(openai_api_key)
        
        if result["success"]:
            # Store in session state
            st.session_state.rag_system = rag_system
            st.session_state.system_initialized = True
            
            # Get system status for feedback
            status = rag_system.get_system_status()
            st.success(f"✅ {result['message']}")
            st.info(f"📊 System Status: {status['has_vectorstore']} vectorstore, {status['has_llm']} LLM, {status['has_embeddings']} embeddings")
            return True
        else:
            st.error(f"Failed to initialize RAG system: {result['error']}")
            return False
        
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

def get_ai_recommendations(case_description: str, product_name: str, priority: str = "Medium") -> str:
    """Get AI recommendations for a case using the RAG system"""
    try:
        if not st.session_state.system_initialized:
            return "System not initialized. Please check your API keys and try again."
        
        # Use the RAG system to get recommendations
        if hasattr(st.session_state, 'rag_system') and st.session_state.rag_system.is_initialized:
            return st.session_state.rag_system.get_recommendations(
                case_description=case_description,
                product_name=product_name,
                priority=priority
            )
        else:
            return "RAG system not available. Please initialize the system first."
        
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
                format_func=lambda x: "Select a customer..." if x is None else f"{x.company} - {x.name}",
                key="create_customer"
            )
            
            product_id = st.selectbox(
                "IBM Product",
                options=[None] + products,
                format_func=lambda x: "Select a product..." if x is None else f"{x.name} {x.version}",
                key="create_product"
            )
            
            priority = st.selectbox("Priority", ["Select priority...", "Critical", "High", "Medium", "Low"], index=0, key="create_priority")
            
        with col2:
            assigned_member_id = st.selectbox(
                "Assign to Tiger Team Member",
                options=[None] + members,
                format_func=lambda x: "Select a team member..." if x is None else f"{x.name} ({x.expertise_areas[0] if x.expertise_areas else 'General'})",
                key="create_member"
            )
            
            support_ticket = st.text_input("Support Ticket Number (PMR)", placeholder="e.g., PMR123456", key="create_ticket")
            desired_outcome = st.text_area("Desired Outcome", placeholder="Describe the desired resolution or outcome...", key="create_outcome")
        
        title = st.text_input("Case Title", placeholder="Enter a descriptive title for this case...", key="create_title")
        description = st.text_area("Case Description", height=150, placeholder="Provide a detailed description of the issue, including symptoms, error messages, and any relevant context...", key="create_description")
        
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
                    recommendations = get_ai_recommendations(description, product_id.name, priority)
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

def edit_case_form(case):
    """Edit case form"""
    st.markdown(f"### ✏️ Edit Case: {case.case_number}")
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 20px; border-left: 4px solid #6c757d; color: #212529;">
        <strong>📝 Edit Mode:</strong> You are currently editing this case. Make your changes below and click "Save Changes" to update the case.
    </div>
    """, unsafe_allow_html=True)
    
    db = SessionLocal()
    try:
        # Get related data for dropdowns
        customers = db.query(Customer).all()
        products = db.query(Product).all()
        members = db.query(TigerTeamMember).filter(TigerTeamMember.is_available == True).all()
        
        with st.form(f"edit_case_form_{case.id}"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Case information
                title = st.text_input("Case Title", value=case.title, key=f"title_{case.id}")
                description = st.text_area("Case Description", value=case.description, height=150, key=f"desc_{case.id}")
                desired_outcome = st.text_area("Desired Outcome", value=case.desired_outcome or "", height=100, key=f"outcome_{case.id}")
                
                # Status and priority
                status = st.selectbox("Status", ["Open", "Research", "Customer Call", "Resolved"], 
                                    index=["Open", "Research", "Customer Call", "Resolved"].index(case.status),
                                    key=f"status_{case.id}")
                priority = st.selectbox("Priority", ["Critical", "High", "Medium", "Low"], 
                                      index=["Critical", "High", "Medium", "Low"].index(case.priority),
                                      key=f"priority_{case.id}")
            
            with col2:
                # Customer and product selection
                customer_id = st.selectbox(
                    "Customer",
                    options=customers,
                    index=[c.id for c in customers].index(case.customer_id),
                    format_func=lambda x: f"{x.company} - {x.name}",
                    key=f"customer_{case.id}"
                )
                
                product_id = st.selectbox(
                    "IBM Product",
                    options=products,
                    index=[p.id for p in products].index(case.product_id),
                    format_func=lambda x: f"{x.name} {x.version}",
                    key=f"product_{case.id}"
                )
                
                assigned_member_id = st.selectbox(
                    "Assign to Tiger Team Member",
                    options=[None] + members,
                    index=([None] + [m.id for m in members]).index(case.assigned_member_id),
                    format_func=lambda x: "Select a team member..." if x is None else f"{x.name} ({x.expertise_areas[0] if x.expertise_areas else 'General'})",
                    key=f"member_{case.id}"
                )
                
                support_ticket = st.text_input("Support Ticket Number (PMR)", value=case.support_ticket_id or "", key=f"ticket_{case.id}")
                
                # Research notes
                research_notes = st.text_area("Research Notes", value=case.research_notes or "", height=100, key=f"notes_{case.id}")
            
            # Form submission
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.form_submit_button("💾 Save Changes", type="primary"):
                    # Validate required fields
                    if not title.strip():
                        st.error("Case title is required.")
                        return
                    if not description.strip():
                        st.error("Case description is required.")
                        return
                    
                    try:
                        # Update case
                        case.title = title.strip()
                        case.description = description.strip()
                        case.desired_outcome = desired_outcome.strip() if desired_outcome else None
                        case.status = status
                        case.priority = priority
                        case.customer_id = customer_id.id
                        case.product_id = product_id.id
                        case.assigned_member_id = assigned_member_id.id if assigned_member_id else None
                        case.support_ticket_id = support_ticket.strip() if support_ticket else None
                        case.research_notes = research_notes.strip() if research_notes else None
                        case.updated_at = datetime.now()
                        
                        db.commit()
                        st.success("✅ Case updated successfully!")
                        st.session_state.editing_case = None
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error updating case: {str(e)}")
                        db.rollback()
            
            with col2:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state.editing_case = None
                    st.rerun()
            
            with col3:
                if st.form_submit_button("👁️ Preview Changes"):
                    st.markdown("### 📋 Changes Preview")
                    st.markdown(f"**Title:** {title.strip()}")
                    st.markdown(f"**Status:** {status}")
                    st.markdown(f"**Priority:** {priority}")
                    st.markdown(f"**Description:** {description.strip()}")
                    if desired_outcome.strip():
                        st.markdown(f"**Desired Outcome:** {desired_outcome.strip()}")
                    if research_notes.strip():
                        st.markdown(f"**Research Notes:** {research_notes.strip()}")
                    st.info("Review your changes above. Click 'Save Changes' to apply them.")
            
            with col4:
                if st.form_submit_button("🔄 Generate New AI Recommendations"):
                    # Update case first
                    case.title = title.strip()
                    case.description = description.strip()
                    case.desired_outcome = desired_outcome.strip() if desired_outcome else None
                    case.status = status
                    case.priority = priority
                    case.customer_id = customer_id.id
                    case.product_id = product_id.id
                    case.assigned_member_id = assigned_member_id.id if assigned_member_id else None
                    case.support_ticket_id = support_ticket.strip() if support_ticket else None
                    case.research_notes = research_notes.strip() if research_notes else None
                    case.updated_at = datetime.now()
                    
                    # Generate new AI recommendations
                    with st.spinner("Generating new AI recommendations..."):
                        product_name = product_id.name if product_id else "General"
                        recommendations = get_ai_recommendations(description.strip(), product_name, priority)
                        case.ai_recommendations = recommendations
                    
                    db.commit()
                    st.success("✅ Case updated with new AI recommendations!")
                    st.session_state.editing_case = None
                    st.rerun()
    
    finally:
        db.close()

def display_case_details(case):
    """Display detailed view of a specific case"""
    st.markdown(f"### 🔍 Case Details: {case.case_number}")
    
    # Simple approach: use the case object directly but add error handling
    try:
        # Priority color coding
        priority_colors = {
            "Critical": "🔴",
            "High": "🟠", 
            "Medium": "🟡",
            "Low": "🟢"
        }
        priority_icon = priority_colors.get(case.priority, "⚪")
        
        # Header with case info
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{priority_icon} {case.title}**")
            st.markdown(f"*Case Number: {case.case_number}*")
        with col2:
            if st.button("← Back to Cases", key=f"back_to_cases_{case.id}"):
                st.session_state.current_case = None
                st.rerun()
        
        st.markdown("---")
        
        # Get related data
        db = SessionLocal()
        try:
            customer = db.query(Customer).filter(Customer.id == case.customer_id).first()
            product = db.query(Product).filter(Product.id == case.product_id).first()
            assigned_member = db.query(TigerTeamMember).filter(TigerTeamMember.id == case.assigned_member_id).first()
        finally:
            db.close()
        
        st.markdown("---")
        
        # Main case information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 Case Information")
            st.markdown(f"**Status:** {case.status}")
            st.markdown(f"**Priority:** {case.priority}")
            st.markdown(f"**Created:** {case.created_at.strftime('%Y-%m-%d %H:%M')}")
            if case.updated_at:
                st.markdown(f"**Last Updated:** {case.updated_at.strftime('%Y-%m-%d %H:%M')}")
            
            st.markdown("#### 👥 Customer Information")
            if customer:
                st.markdown(f"**Company:** {customer.company}")
                st.markdown(f"**Contact:** {customer.name}")
                if customer.contact_email:
                    st.markdown(f"**Email:** {customer.contact_email}")
                if customer.contact_phone:
                    st.markdown(f"**Phone:** {customer.contact_phone}")
                if customer.industry:
                    st.markdown(f"**Industry:** {customer.industry}")
                if customer.region:
                    st.markdown(f"**Region:** {customer.region}")
            else:
                st.markdown("*Customer information not available*")
        
        with col2:
            st.markdown("#### 🛠️ Technical Information")
            if product:
                st.markdown(f"**Product:** {product.name}")
                st.markdown(f"**Version:** {product.version}")
                st.markdown(f"**Category:** {product.category}")
            else:
                st.markdown("*Product information not available*")
            
            st.markdown("#### 👨‍💼 Assignment")
            if assigned_member:
                st.markdown(f"**Assigned To:** {assigned_member.name}")
                expertise = assigned_member.expertise_areas
                if expertise and isinstance(expertise, list) and len(expertise) > 0:
                    st.markdown(f"**Expertise:** {', '.join(expertise)}")
                else:
                    st.markdown("**Expertise:** General")
                st.markdown(f"**Email:** {assigned_member.email}")
            else:
                st.markdown("*No team member assigned*")
            
            if case.support_ticket_id:
                st.markdown(f"**Support Ticket:** {case.support_ticket_id}")
        
        # Case description
        st.markdown("#### 📝 Case Description")
        st.markdown(f'<div class="case-description-field">{case.description}</div>', unsafe_allow_html=True)
        
        # Desired outcome
        if case.desired_outcome:
            st.markdown("#### 🎯 Desired Outcome")
            st.markdown(f'<div class="case-description-field">{case.desired_outcome}</div>', unsafe_allow_html=True)
        
        # Research notes
        if case.research_notes:
            st.markdown("#### 📝 Research Notes")
            st.markdown(f'<div class="research-data-field">{case.research_notes}</div>', unsafe_allow_html=True)
        
        # AI Recommendations
        if case.ai_recommendations:
            st.markdown("#### 🤖 AI Research Recommendations")
            st.markdown("""
            <div class="ai-recommendations-field">
                <strong>💡 AI Analysis:</strong> These recommendations are generated by analyzing IBM documentation, 
                best practices, and similar cases to provide actionable guidance for your Tiger Team research.
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f'<div class="ai-recommendations-field">{case.ai_recommendations}</div>', unsafe_allow_html=True)
        else:
            st.markdown("#### 🤖 AI Research Recommendations")
            st.info("""
            **No AI recommendations generated yet.**
            
            Click the button below to generate comprehensive research recommendations based on:
            - IBM product documentation analysis
            - Known issues and solutions
            - Best practices and troubleshooting steps
            - Next actions for the Tiger Team
            """)
            if st.button("🔄 Generate AI Recommendations", key="generate_ai", help="Generate comprehensive AI research recommendations"):
                with st.spinner("🤖 Analyzing case and generating AI recommendations..."):
                    # Get fresh case object in current session
                    fresh_case = db.query(Case).filter(Case.id == case.id).first()
                    if fresh_case:
                        recommendations = get_ai_recommendations(fresh_case.description, product.name if product else "General", fresh_case.priority)
                        fresh_case.ai_recommendations = recommendations
                        fresh_case.updated_at = datetime.now()
                        db.commit()
                        st.success("✅ AI recommendations generated successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Case not found in database")
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📝 Edit Case", key="edit_case"):
                st.session_state.editing_case = case.id
                st.rerun()
        
        with col2:
            if st.button("📧 Contact Customer", key="contact_customer"):
                if customer and customer.contact_email:
                    st.info(f"Contact {customer.name} at {customer.contact_email}")
                elif customer:
                    st.info(f"Contact {customer.name} (email not available)")
                else:
                    st.info("Customer contact information not available")
        
        with col3:
            if st.button("📊 View Similar Cases", key="similar_cases"):
                st.info("Feature coming soon: View cases with similar issues or products")
        
        with col4:
            if st.button("🔄 Generate AI Recommendations", key="regenerate_ai", help="Generate comprehensive AI research recommendations based on IBM documentation and best practices"):
                with st.spinner("🤖 Analyzing case and generating AI recommendations..."):
                    # Get fresh case object in current session
                    fresh_case = db.query(Case).filter(Case.id == case.id).first()
                    if fresh_case:
                        recommendations = get_ai_recommendations(fresh_case.description, product.name if product else "General", fresh_case.priority)
                        fresh_case.ai_recommendations = recommendations
                        fresh_case.updated_at = datetime.now()
                        db.commit()
                        st.success("✅ AI recommendations generated successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Case not found in database")
    
    except Exception as e:
        st.error(f"Error displaying case details: {str(e)}")
        st.write("Debug info:", case.id if case else "No case object")
    
    finally:
        if 'db' in locals():
            db.close()

def display_cases():
    """Display existing cases"""
    logger.info("Starting display_cases function")
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
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Open", "Research", "Customer Call", "Resolved"],
                index=0,
                key="filter_status"
            )
        with col2:
            priority_filter = st.selectbox(
                "Filter by Priority",
                ["All", "Critical", "High", "Medium", "Low"],
                index=0,
                key="filter_priority"
            )
        
        # Apply filters
        filtered_cases = cases
        if status_filter != "All":
            filtered_cases = [c for c in filtered_cases if c.status == status_filter]
        if priority_filter != "All":
            filtered_cases = [c for c in filtered_cases if c.priority == priority_filter]
        
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
                    
                    if st.button(f"🔍 View Details", key=f"view_{case.id}", type="primary"):
                        st.session_state.current_case = case
                        st.rerun()
    finally:
        db.close()

def research_assistant():
    """AI Research Assistant using RAG system"""
    st.markdown("### 🔍 AI Research Assistant")
    
    if not st.session_state.system_initialized:
        st.warning("Please initialize the system first.")
        return
    
    # Add RAG system status display
    if hasattr(st.session_state, 'rag_system'):
        status = st.session_state.rag_system.get_system_status()
        if status['initialized']:
            st.success("✅ RAG system ready - IBM documentation loaded")
        else:
            st.warning("⚠️ RAG system not fully initialized")
    
    user_question = st.text_area(
        "Ask about IBM products, support issues, or research strategies:",
        height=100,
        placeholder="e.g., How do I troubleshoot WebSphere memory leaks? What are common Db2 performance issues?",
        key="research_question"
    )
    
    if st.button("🔍 Get AI Research", type="primary", key="research_button"):
        if user_question.strip():
            with st.spinner("🤖 Researching IBM documentation..."):
                if hasattr(st.session_state, 'rag_system') and st.session_state.rag_system.is_initialized:
                    response = st.session_state.rag_system.get_recommendations(
                        case_description=user_question,
                        product_name="General",
                        priority="Medium"
                    )
                else:
                    response = "RAG system not available. Please initialize the system first."
                
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
    logger.info("Starting main function")
    st.markdown('<h1 class="main-header">🦁 IBM Tiger Team Support</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered case management for critical IBM support issues</p>', unsafe_allow_html=True)
    
    # Sidebar for navigation
    with st.sidebar:
        st.markdown("### 📋 Quick Actions")
        
        if st.button("📊 View All Cases"):
            st.session_state.show_cases = True
            st.session_state.show_create = False
            st.session_state.show_research = False
            st.session_state.current_case = None  # Clear current case to exit details view
        
        if st.button("➕ Create New Case"):
            st.session_state.show_create = True
            st.session_state.show_cases = False
            st.session_state.show_research = False
            st.session_state.current_case = None  # Clear current case to exit details view
        
        if st.button("🔍 Research Assistant"):
            st.session_state.show_research = True
            st.session_state.show_cases = False
            st.session_state.show_create = False
            st.session_state.current_case = None  # Clear current case to exit details view
        
        if st.button("🔧 Admin"):
            st.session_state.show_admin = True
            st.session_state.show_cases = False
            st.session_state.show_create = False
            st.session_state.show_research = False
            st.session_state.current_case = None
    
    # Initialize session state for navigation
    if 'show_cases' not in st.session_state:
        st.session_state.show_cases = False
    if 'show_create' not in st.session_state:
        st.session_state.show_create = False
    if 'show_research' not in st.session_state:
        st.session_state.show_research = False
    if 'show_admin' not in st.session_state:
        st.session_state.show_admin = False
    if 'editing_case' not in st.session_state:
        st.session_state.editing_case = None
    
    # Main content area - use conditional rendering based on session state
    if st.session_state.current_case:
        # Always get fresh case data from database
        db = SessionLocal()
        try:
            fresh_case = db.query(Case).filter(Case.id == st.session_state.current_case.id).first()
            if fresh_case:
                # Check if we're in edit mode
                if st.session_state.editing_case == fresh_case.id:
                    # Show edit form with fresh data
                    edit_case_form(fresh_case)
                else:
                    # Show case details view with fresh data
                    display_case_details(fresh_case)
            else:
                st.error("Case not found in database.")
                st.session_state.current_case = None
                st.rerun()
        finally:
            db.close()
    
    elif st.session_state.show_cases:
        st.markdown("### 📊 View All Cases")
        display_cases()
        if st.button("← Back to Main Menu", key="back_to_main_from_cases"):
            st.session_state.show_cases = False
            st.session_state.show_create = False
            st.session_state.show_research = False
            st.rerun()
    
    elif st.session_state.show_create:
        create_case_form()
        if st.button("← Back to Main Menu", key="back_to_main_from_create"):
            st.session_state.show_cases = False
            st.session_state.show_create = False
            st.session_state.show_research = False
            st.rerun()
    
    elif st.session_state.show_research:
        research_assistant()
        if st.button("← Back to Main Menu", key="back_to_main_from_research"):
            st.session_state.show_cases = False
            st.session_state.show_create = False
            st.session_state.show_research = False
            st.rerun()
    
    elif st.session_state.show_admin:
        from app.admin import admin_page
        admin_page()
        if st.button("← Back to Main Menu", key="back_to_main_from_admin"):
            st.session_state.show_cases = False
            st.session_state.show_create = False
            st.session_state.show_research = False
            st.session_state.show_admin = False
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
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Create Case", "📊 View Cases", "🔍 Research Assistant", "📜 History", "🔧 Admin"])
        
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
        
        with tab5:
            from app.admin import admin_page
            admin_page()

if __name__ == "__main__":
    main()
