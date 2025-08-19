import streamlit as st
import os
import json
from pathlib import Path
from typing import Dict, Optional

class AdminManager:
    """Admin interface for managing API keys and system configuration"""
    
    def __init__(self):
        self.config_file = Path("config/admin_config.json")
        self.config_file.parent.mkdir(exist_ok=True)
        self.load_config()
    
    def load_config(self) -> Dict:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                st.error(f"Error loading config: {str(e)}")
        return {}
    
    def save_config(self, config: Dict) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            st.error(f"Error saving config: {str(e)}")
            return False
    
    def get_api_key(self, key_name: str) -> Optional[str]:
        """Get API key from environment or config"""
        # First try environment variable
        env_key = os.getenv(key_name.upper())
        if env_key:
            return env_key
        
        # Then try config file
        config = self.load_config()
        return config.get(key_name, None)
    
    def set_api_key(self, key_name: str, value: str) -> bool:
        """Set API key in both environment and config"""
        try:
            # Set environment variable
            os.environ[key_name.upper()] = value
            
            # Save to config file
            config = self.load_config()
            config[key_name] = value
            return self.save_config(config)
        except Exception as e:
            st.error(f"Error setting API key: {str(e)}")
            return False

def admin_page():
    """Admin page for managing system configuration"""
    st.markdown("### 🔧 Admin Configuration")
    
    admin = AdminManager()
    
    # API Keys Section
    st.markdown("#### 🔑 API Keys Management")
    
    with st.form("api_keys_form"):
        st.markdown("**Required API Keys:**")
        
        # OpenAI API Key
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=admin.get_api_key("openai_api_key") or "",
            help="Required for LLM and embedding functionality"
        )
        
        # Tavily API Key
        tavily_key = st.text_input(
            "Tavily API Key",
            type="password",
            value=admin.get_api_key("tavily_api_key") or "",
            help="Required for web search capabilities"
        )
        
        # Optional: Add more API keys as needed
        # langsmith_key = st.text_input(
        #     "LangSmith API Key",
        #     type="password",
        #     value=admin.get_api_key("langsmith_api_key") or "",
        #     help="Optional: For tracing and evaluation"
        # )
        
        submitted = st.form_submit_button("💾 Save API Keys")
        
        if submitted:
            success_count = 0
            
            if openai_key:
                if admin.set_api_key("openai_api_key", openai_key):
                    success_count += 1
                    st.success("✅ OpenAI API key saved")
                else:
                    st.error("❌ Failed to save OpenAI API key")
            
            if tavily_key:
                if admin.set_api_key("tavily_api_key", tavily_key):
                    success_count += 1
                    st.success("✅ Tavily API key saved")
                else:
                    st.error("❌ Failed to save Tavily API key")
            
            if success_count > 0:
                st.success(f"✅ {success_count} API key(s) saved successfully!")
    
    # System Status Section
    st.markdown("---")
    st.markdown("#### 📊 System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        openai_status = "✅ Configured" if admin.get_api_key("openai_api_key") else "❌ Missing"
        st.metric("OpenAI API", openai_status)
    
    with col2:
        tavily_status = "✅ Configured" if admin.get_api_key("tavily_api_key") else "❌ Missing"
        st.metric("Tavily API", tavily_status)
    
    with col3:
        rag_status = "✅ Ready" if (admin.get_api_key("openai_api_key") and st.session_state.get("system_initialized", False)) else "❌ Not Ready"
        st.metric("RAG System", rag_status)
    
    # System Information
    st.markdown("---")
    st.markdown("#### ℹ️ System Information")
    
    # Check IBM documentation
    docs_path = Path("data/documentation")
    if docs_path.exists():
        pdf_files = list(docs_path.glob("*.pdf"))
        st.info(f"📚 IBM Documentation: {len(pdf_files)} PDF files found")
        
        if pdf_files:
            with st.expander("📋 Document List"):
                for pdf in pdf_files:
                    size_mb = pdf.stat().st_size / (1024 * 1024)
                    st.write(f"• {pdf.name} ({size_mb:.1f} MB)")
    else:
        st.warning("⚠️ IBM documentation directory not found")
    
    # Database status
    db_path = Path("tiger_team_support.db")
    if db_path.exists():
        size_mb = db_path.stat().st_size / (1024 * 1024)
        st.info(f"🗄️ Database: {size_mb:.1f} MB")
    else:
        st.warning("⚠️ Database not found")
    
    # System Initialization Section
    st.markdown("---")
    st.markdown("#### 🚀 System Initialization")
    
    # Check if system is already initialized
    if st.session_state.get("system_initialized", False):
        st.success("✅ System is initialized and ready")
    else:
        st.warning("⚠️ System needs initialization")
    
    # Initialize button
    if st.button("🚀 Initialize System", type="primary", help="Initialize the RAG system and database"):
        openai_key = admin.get_api_key("openai_api_key")
        tavily_key = admin.get_api_key("tavily_api_key")
        
        if not openai_key:
            st.error("❌ Please configure OpenAI API key first")
        elif not tavily_key:
            st.warning("⚠️ Tavily API key recommended for web search capabilities")
            with st.spinner("Initializing system with local docs only..."):
                try:
                    success = initialize_rag_system(admin)
                    if success:
                        st.success("✅ System initialized successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to initialize system")
                except Exception as e:
                    st.error(f"❌ Error initializing system: {str(e)}")
        else:
            with st.spinner("Initializing system with full capabilities..."):
                try:
                    success = initialize_rag_system(admin)
                    if success:
                        st.success("✅ System initialized successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to initialize system")
                except Exception as e:
                    st.error(f"❌ Error initializing system: {str(e)}")
    
    # Quick Actions
    st.markdown("---")
    st.markdown("#### ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧪 Test API Keys", help="Test if API keys are working"):
            test_api_keys(admin)
    
    with col2:
        if st.button("🔄 Refresh Status", help="Refresh system status"):
            st.rerun()

def initialize_rag_system(admin: AdminManager):
    """Initialize the RAG system and database"""
    try:
        # Create database tables
        from app.database import Base, engine
        Base.metadata.create_all(bind=engine)
        
        # Get API keys from admin manager
        openai_api_key = admin.get_api_key("openai_api_key")
        if not openai_api_key:
            st.error("Please configure your OpenAI API key first.")
            return False
        
        # Initialize the Tiger Team RAG system
        from app.rag_system import TigerTeamRAGSystem
        rag_system = TigerTeamRAGSystem()
        result = rag_system.initialize(openai_api_key)
        
        if result["success"]:
            # Store in session state
            st.session_state.rag_system = rag_system
            st.session_state.system_initialized = True
            return True
        else:
            st.error(f"Failed to initialize RAG system: {result['message']}")
            return False
            
    except Exception as e:
        st.error(f"Error initializing system: {str(e)}")
        return False

def test_api_keys(admin: AdminManager):
    """Test API keys functionality"""
    st.markdown("#### 🔍 API Key Testing")
    
    # Test OpenAI
    openai_key = admin.get_api_key("openai_api_key")
    if openai_key:
        try:
            from langchain_openai import OpenAIEmbeddings
            embeddings = OpenAIEmbeddings(openai_key=openai_key)
            test_embedding = embeddings.embed_query("test")
            if test_embedding:
                st.success("✅ OpenAI API key working")
            else:
                st.error("❌ OpenAI API key test failed")
        except Exception as e:
            st.error(f"❌ OpenAI API key error: {str(e)}")
    else:
        st.warning("⚠️ OpenAI API key not configured")
    
    # Test Tavily
    tavily_key = admin.get_api_key("tavily_api_key")
    if tavily_key:
        try:
            from langchain_community.tools.tavily_search import TavilySearchResults
            tavily_tool = TavilySearchResults(api_key=tavily_key)
            # Note: We don't actually call it to avoid charges, just test initialization
            st.success("✅ Tavily API key configured")
        except Exception as e:
            st.error(f"❌ Tavily API key error: {str(e)}")
    else:
        st.warning("⚠️ Tavily API key not configured")
