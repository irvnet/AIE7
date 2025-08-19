import os
import json
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain_community.tools import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

logger = logging.getLogger(__name__)

@dataclass
class CatalogSource:
    """Represents a documentation source from the catalog"""
    product: str
    category: str
    title: str
    url: str
    format: str
    type: str
    doc_type: str
    topic: str
    pattern_tags: List[str]
    stability: str
    license_ok: bool

class ArchitectureAgent:
    """Specialized agent for IBM architecture, best practices, and integration patterns"""
    
    def __init__(self, openai_api_key: str, tavily_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key
        self.tavily_api_key = tavily_api_key
        self.is_initialized = False
        
        # Initialize components
        self.llm = None
        self.tavily_tool = None
        self.catalog_sources = []
        
        # High-quality source patterns
        self.quality_sources = {
            "ibm.com/docs": "IBM Product Documentation",
            "redbooks.ibm.com": "IBM Redbooks",
            "ibm.com/architecture": "IBM Architecture Center",
            "ibm.com/developer": "IBM Developer",
            "ibm.com/cloud": "IBM Cloud Documentation",
            "ibm.com/support": "IBM Support Knowledge Base"
        }
        
        self._initialize()
    
    def _initialize(self):
        """Initialize the architecture agent"""
        try:
            # Initialize LLM
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.1,
                openai_api_key=self.openai_api_key
            )
            
            # Initialize web search tool if API key available
            if self.tavily_api_key:
                self.tavily_tool = TavilySearchResults(
                    api_key=self.tavily_api_key,
                    max_results=5
                )
            
            # Load catalog sources
            self._load_catalog_sources()
            
            self.is_initialized = True
            logger.info("Architecture Agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Architecture Agent: {str(e)}")
            self.is_initialized = False
    
    def _load_catalog_sources(self):
        """Load and parse the sources catalog"""
        try:
            catalog_path = "data/sources.catalog.json"
            if os.path.exists(catalog_path):
                with open(catalog_path, 'r') as f:
                    catalog_data = json.load(f)
                
                self.catalog_sources = []
                for source in catalog_data:
                    if source.get("license_ok", False):  # Only use licensed sources
                        catalog_source = CatalogSource(
                            product=source.get("product", ""),
                            category=source.get("category", ""),
                            title=source.get("title", ""),
                            url=source.get("url", ""),
                            format=source.get("format", ""),
                            type=source.get("type", ""),
                            doc_type=source.get("doc_type", ""),
                            topic=source.get("topic", ""),
                            pattern_tags=source.get("pattern_tags", []),
                            stability=source.get("stability", ""),
                            license_ok=source.get("license_ok", True)
                        )
                        self.catalog_sources.append(catalog_source)
                
                logger.info(f"Loaded {len(self.catalog_sources)} catalog sources")
            else:
                logger.warning("Catalog file not found, using default sources")
                
        except Exception as e:
            logger.error(f"Error loading catalog sources: {str(e)}")
    
    def get_architecture_guidance(self, question: str, pattern_tags: Optional[List[str]] = None) -> str:
        """Get specialized architecture guidance using high-quality sources"""
        if not self.is_initialized:
            return "Architecture Agent not initialized. Please check your API keys."
        
        try:
            # Get relevant sources based on question and pattern tags
            relevant_sources = self._get_relevant_sources(question, pattern_tags)
            
            # Perform targeted web searches
            search_results = self._perform_targeted_searches(question, relevant_sources)
            
            # Generate architecture guidance
            guidance = self._generate_architecture_guidance(question, search_results, relevant_sources)
            
            return guidance
            
        except Exception as e:
            logger.error(f"Error getting architecture guidance: {str(e)}")
            return f"Error generating architecture guidance: {str(e)}"
    
    def _get_relevant_sources(self, question: str, pattern_tags: Optional[List[str]] = None) -> List[CatalogSource]:
        """Get relevant sources from catalog based on question and pattern tags"""
        relevant_sources = []
        
        # Filter by pattern tags if provided
        if pattern_tags:
            for source in self.catalog_sources:
                if any(tag in source.pattern_tags for tag in pattern_tags):
                    relevant_sources.append(source)
        
        # If no pattern-specific sources, get general architecture sources
        if not relevant_sources:
            for source in self.catalog_sources:
                if (source.doc_type in ["redbook", "product-doc"] and 
                    source.topic in ["reference", "admin-config", "performance"]):
                    relevant_sources.append(source)
        
        # Limit to top 10 most relevant
        return relevant_sources[:10]
    
    def _perform_targeted_searches(self, question: str, relevant_sources: List[CatalogSource]) -> Dict[str, List[str]]:
        """Perform targeted web searches using high-quality sources"""
        search_results = {
            "ibm_docs": [],
            "redbooks": [],
            "architecture_center": [],
            "developer": [],
            "support": []
        }
        
        if not self.tavily_tool:
            return search_results
        
        try:
            # Search IBM documentation
            ibm_query = f"site:ibm.com/docs {question}"
            ibm_results = self._safe_search(ibm_query)
            search_results["ibm_docs"] = ibm_results
            
            # Search IBM Redbooks
            redbook_query = f"site:redbooks.ibm.com {question}"
            redbook_results = self._safe_search(redbook_query)
            search_results["redbooks"] = redbook_results
            
            # Search IBM Architecture Center
            arch_query = f"site:ibm.com/architecture {question}"
            arch_results = self._safe_search(arch_query)
            search_results["architecture_center"] = arch_results
            
            # Search IBM Developer
            dev_query = f"site:ibm.com/developer {question}"
            dev_results = self._safe_search(dev_query)
            search_results["developer"] = dev_results
            
            # Search IBM Support Knowledge Base
            support_query = f"site:ibm.com/support {question}"
            support_results = self._safe_search(support_query)
            search_results["support"] = support_results
            
        except Exception as e:
            logger.error(f"Error performing targeted searches: {str(e)}")
        
        return search_results
    
    def _safe_search(self, query: str) -> List[str]:
        """Safely perform web search with error handling"""
        try:
            results = self.tavily_tool.invoke(query)
            if isinstance(results, list):
                return [str(result.get("content", result)) for result in results[:3]]
            else:
                return [str(results)]
        except Exception as e:
            logger.error(f"Search error for query '{query}': {str(e)}")
            return []
    
    def _generate_architecture_guidance(self, question: str, search_results: Dict[str, List[str]], 
                                      relevant_sources: List[CatalogSource]) -> str:
        """Generate comprehensive architecture guidance"""
        
        # Format search results
        formatted_results = self._format_search_results(search_results)
        
        # Format relevant sources
        formatted_sources = self._format_relevant_sources(relevant_sources)
        
        # Create specialized architecture prompt
        architecture_prompt = ChatPromptTemplate.from_template("""
        You are an IBM Enterprise Architecture Specialist with deep expertise in IBM product integration, 
        best practices, and enterprise architecture patterns. Provide comprehensive guidance for this 
        architecture question.

        QUESTION: {question}

        RESEARCH CONTEXT:
        {formatted_results}

        RELEVANT SOURCES:
        {formatted_sources}

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
        Use only information from the provided research context and relevant sources.
        """)
        
        # Generate response
        chain = architecture_prompt | self.llm | StrOutputParser()
        response = chain.invoke({
            "question": question,
            "formatted_results": formatted_results,
            "formatted_sources": formatted_sources
        })
        
        return response
    
    def _format_search_results(self, search_results: Dict[str, List[str]]) -> str:
        """Format search results for the prompt"""
        formatted = []
        
        if search_results["ibm_docs"]:
            formatted.append("IBM PRODUCT DOCUMENTATION:")
            formatted.extend([f"- {result}" for result in search_results["ibm_docs"]])
            formatted.append("")
        
        if search_results["redbooks"]:
            formatted.append("IBM REDBOOKS:")
            formatted.extend([f"- {result}" for result in search_results["redbooks"]])
            formatted.append("")
        
        if search_results["architecture_center"]:
            formatted.append("IBM ARCHITECTURE CENTER:")
            formatted.extend([f"- {result}" for result in search_results["architecture_center"]])
            formatted.append("")
        
        if search_results["developer"]:
            formatted.append("IBM DEVELOPER:")
            formatted.extend([f"- {result}" for result in search_results["developer"]])
            formatted.append("")
        
        if search_results["support"]:
            formatted.append("IBM SUPPORT KNOWLEDGE BASE:")
            formatted.extend([f"- {result}" for result in search_results["support"]])
            formatted.append("")
        
        return "\n".join(formatted) if formatted else "No search results available."
    
    def _format_relevant_sources(self, sources: List[CatalogSource]) -> str:
        """Format relevant sources for the prompt"""
        if not sources:
            return "No relevant sources identified."
        
        formatted = []
        for source in sources:
            formatted.append(f"- {source.title} ({source.product})")
            formatted.append(f"  Type: {source.doc_type}, Topic: {source.topic}")
            if source.pattern_tags:
                formatted.append(f"  Patterns: {', '.join(source.pattern_tags)}")
            formatted.append(f"  URL: {source.url}")
            formatted.append("")
        
        return "\n".join(formatted)
    
    def get_system_status(self) -> Dict:
        """Get the current status of the Architecture Agent"""
        return {
            "initialized": self.is_initialized,
            "has_llm": self.llm is not None,
            "has_web_search": self.tavily_tool is not None,
            "catalog_sources": len(self.catalog_sources),
            "quality_sources": len(self.quality_sources)
        }
