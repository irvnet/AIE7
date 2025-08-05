#!/usr/bin/env python3
"""
API Key Manager for Student Loan Assistant
Centralized management of API keys with validation and error handling
"""

import os
from typing import Dict, Optional, List
from dataclasses import dataclass

@dataclass
class APIKeys:
    """Container for all API keys"""
    openai_api_key: str
    tavily_api_key: Optional[str] = None
    langsmith_api_key: Optional[str] = None

class APIKeyManager:
    """Manages API keys with validation and collection"""
    
    def __init__(self):
        self.required_keys = ["openai_api_key"]
        self.optional_keys = ["tavily_api_key", "langsmith_api_key"]
        self.collected_keys = {}
    
    def validate_openai_key(self, key: str) -> bool:
        """Validate OpenAI API key format"""
        if not key or not key.strip():
            return False
        # Basic format validation (starts with sk-)
        return key.strip().startswith("sk-")
    
    def validate_tavily_key(self, key: str) -> bool:
        """Validate Tavily API key format"""
        if not key or not key.strip():
            return True  # Optional key
        # Basic format validation
        return len(key.strip()) > 10
    
    def validate_langsmith_key(self, key: str) -> bool:
        """Validate LangSmith API key format"""
        if not key or not key.strip():
            return True  # Optional key
        # Basic format validation (starts with lsv2_)
        return key.strip().startswith("lsv2_")
    
    def collect_api_keys(self, interactive: bool = True) -> APIKeys:
        """Collect all required API keys"""
        keys = {}
        
        # Collect OpenAI API key (required)
        openai_key = self._get_openai_key(interactive)
        if not openai_key:
            raise ValueError("OpenAI API key is required but not provided")
        keys["openai_api_key"] = openai_key
        
        # Collect Tavily API key (optional)
        if interactive:
            tavily_key = self._get_tavily_key(interactive)
            if tavily_key:
                keys["tavily_api_key"] = tavily_key
        
        # Collect LangSmith API key (optional)
        if interactive:
            langsmith_key = self._get_langsmith_key(interactive)
            if langsmith_key:
                keys["langsmith_api_key"] = langsmith_key
        
        # Set environment variables
        self._set_environment_variables(keys)
        
        return APIKeys(**keys)
    
    def _get_openai_key(self, interactive: bool) -> Optional[str]:
        """Get OpenAI API key from environment or user input"""
        # Try environment variable first
        key = os.getenv("OPENAI_API_KEY")
        if key and self.validate_openai_key(key):
            print("✅ Using OpenAI API key from environment")
            return key
        
        if not interactive:
            return None
        
        # Prompt user
        while True:
            try:
                key = input("🔑 Please enter your OpenAI API key (required): ").strip()
                if not key:
                    print("❌ OpenAI API key is required")
                    continue
                
                if self.validate_openai_key(key):
                    print("✅ OpenAI API key validated")
                    return key
                else:
                    print("❌ Invalid OpenAI API key format (should start with 'sk-')")
            except KeyboardInterrupt:
                print("\n❌ API key collection cancelled")
                return None
    
    def _get_tavily_key(self, interactive: bool) -> Optional[str]:
        """Get Tavily API key from environment or user input"""
        # Try environment variable first
        key = os.getenv("TAVILY_API_KEY")
        if key and self.validate_tavily_key(key):
            print("✅ Using Tavily API key from environment")
            return key
        
        if not interactive:
            return None
        
        # Prompt user
        try:
            key = input("🔍 Enter Tavily API key (optional, press Enter to skip): ").strip()
            if not key:
                print("⚠️  Skipping Tavily API key (search functionality will be limited)")
                return None
            
            if self.validate_tavily_key(key):
                print("✅ Tavily API key validated")
                return key
            else:
                print("❌ Invalid Tavily API key format")
                return None
        except KeyboardInterrupt:
            print("\n⚠️  Skipping Tavily API key")
            return None
    
    def _get_langsmith_key(self, interactive: bool) -> Optional[str]:
        """Get LangSmith API key from environment or user input"""
        # Try environment variable first
        key = os.getenv("LANGCHAIN_API_KEY")
        if key and self.validate_langsmith_key(key):
            print("✅ Using LangSmith API key from environment")
            return key
        
        if not interactive:
            return None
        
        # Prompt user
        try:
            key = input("📊 Enter LangSmith API key (optional, press Enter to skip): ").strip()
            if not key:
                print("⚠️  Skipping LangSmith API key (tracing will be local only)")
                return None
            
            if self.validate_langsmith_key(key):
                print("✅ LangSmith API key validated")
                return key
            else:
                print("❌ Invalid LangSmith API key format (should start with 'lsv2_')")
                return None
        except KeyboardInterrupt:
            print("\n⚠️  Skipping LangSmith API key")
            return None
    
    def _set_environment_variables(self, keys: Dict[str, str]):
        """Set environment variables for all collected keys"""
        for key_name, key_value in keys.items():
            env_var_name = key_name.upper()
            os.environ[env_var_name] = key_value
        
        # Set LangSmith environment variables if provided
        if keys.get("langsmith_api_key"):
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_PROJECT"] = "student-loan-assistant-evaluation"
    
    def validate_all_keys(self, keys: APIKeys) -> List[str]:
        """Validate all provided keys and return list of errors"""
        errors = []
        
        if not keys.openai_api_key or not self.validate_openai_key(keys.openai_api_key):
            errors.append("Invalid or missing OpenAI API key")
        
        if keys.tavily_api_key and not self.validate_tavily_key(keys.tavily_api_key):
            errors.append("Invalid Tavily API key format")
        
        if keys.langsmith_api_key and not self.validate_langsmith_key(keys.langsmith_api_key):
            errors.append("Invalid LangSmith API key format")
        
        return errors

# Global instance
api_key_manager = APIKeyManager()

def get_api_keys(interactive: bool = True) -> APIKeys:
    """Get API keys with validation"""
    return api_key_manager.collect_api_keys(interactive)

def validate_api_keys(keys: APIKeys) -> List[str]:
    """Validate API keys and return list of errors"""
    return api_key_manager.validate_all_keys(keys) 