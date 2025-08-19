#!/usr/bin/env python3
"""
Quick test script for Architecture Agent
Run this to validate the Architecture Agent is working correctly
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def test_architecture_agent():
    """Quick test of Architecture Agent"""
    print("🏗️ Testing Architecture Agent...")
    
    try:
        from app.architecture_agent import ArchitectureAgent
        
        # Get API keys
        openai_key = os.getenv("OPENAI_API_KEY")
        tavily_key = os.getenv("TAVILY_API_KEY")
        
        if not openai_key:
            print("❌ OPENAI_API_KEY not found in environment")
            print("   Set it with: export OPENAI_API_KEY='your-key-here'")
            return False
        
        print("✅ OpenAI API key found")
        
        # Initialize agent
        print("🔧 Initializing Architecture Agent...")
        agent = ArchitectureAgent(openai_key, tavily_key)
        
        # Check status
        status = agent.get_system_status()
        print(f"✅ Agent initialized: {status['initialized']}")
        print(f"   - Catalog sources: {status['catalog_sources']}")
        print(f"   - Web search: {'✅' if status['has_web_search'] else '❌'}")
        
        # Test a simple question
        print("\n🧪 Testing architecture guidance...")
        question = "What are the best practices for IBM MQ high availability?"
        
        guidance = agent.get_architecture_guidance(question)
        
        if guidance and len(guidance) > 200:
            print("✅ Architecture guidance generated successfully!")
            print(f"   Response length: {len(guidance)} characters")
            
            # Show a preview
            preview = guidance[:300] + "..." if len(guidance) > 300 else guidance
            print(f"\n📝 Preview:\n{preview}")
            
            return True
        else:
            print("❌ Architecture guidance failed or too short")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Architecture Agent: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Architecture Agent Quick Test")
    print("=" * 40)
    
    success = test_architecture_agent()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 Architecture Agent test PASSED!")
        print("   The agent is working correctly.")
    else:
        print("❌ Architecture Agent test FAILED!")
        print("   Check your API keys and configuration.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
