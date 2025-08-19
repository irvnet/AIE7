#!/usr/bin/env python3
"""
Test scenarios for the Architecture Agent
Validates the specialized IBM architecture guidance capabilities
"""

import os
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from app.architecture_agent import ArchitectureAgent, CatalogSource

# Test scenarios for Architecture Agent
ARCHITECTURE_TEST_SCENARIOS = [
    {
        "name": "IBM MQ Integration Patterns",
        "question": "How should I design a high-availability IBM MQ messaging architecture for a financial services application?",
        "pattern_tags": ["messaging", "high-availability", "financial"],
        "expected_topics": ["MQ clustering", "HA patterns", "financial compliance"]
    },
    {
        "name": "API Connect Microservices",
        "question": "What's the best way to implement API Connect for microservices architecture with Kubernetes?",
        "pattern_tags": ["api-gateway", "microservices", "kubernetes"],
        "expected_topics": ["API Connect", "microservices", "Kubernetes deployment"]
    },
    {
        "name": "WebSphere Application Server Clustering",
        "question": "How do I set up WebSphere Application Server clustering for horizontal scaling?",
        "pattern_tags": ["application-server", "clustering", "scaling"],
        "expected_topics": ["WebSphere clustering", "horizontal scaling", "load balancing"]
    },
    {
        "name": "Db2 Performance Optimization",
        "question": "What are the best practices for optimizing Db2 performance in a z/OS environment?",
        "pattern_tags": ["database", "performance", "z-os"],
        "expected_topics": ["Db2 optimization", "z/OS", "performance tuning"]
    },
    {
        "name": "Hybrid Cloud Integration",
        "question": "How should I architect a hybrid cloud solution using IBM Cloud and on-premises systems?",
        "pattern_tags": ["hybrid-cloud", "integration", "ibm-cloud"],
        "expected_topics": ["hybrid cloud", "IBM Cloud", "integration patterns"]
    },
    {
        "name": "Security Architecture",
        "question": "What security patterns should I implement for IBM products in a regulated environment?",
        "pattern_tags": ["security", "compliance", "regulated"],
        "expected_topics": ["security patterns", "compliance", "regulatory"]
    },
    {
        "name": "Disaster Recovery Planning",
        "question": "How do I design a disaster recovery solution for IBM MQ and Db2 systems?",
        "pattern_tags": ["disaster-recovery", "mq", "db2"],
        "expected_topics": ["disaster recovery", "MQ", "Db2", "backup strategies"]
    },
    {
        "name": "Container Orchestration",
        "question": "What's the recommended approach for containerizing IBM applications with OpenShift?",
        "pattern_tags": ["containers", "openshift", "containerization"],
        "expected_topics": ["OpenShift", "containers", "IBM applications"]
    }
]

def test_architecture_agent_initialization():
    """Test Architecture Agent initialization"""
    print("🧪 Testing Architecture Agent Initialization...")
    
    # Get API keys from environment
    openai_key = os.getenv("OPENAI_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    
    if not openai_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False
    
    try:
        # Initialize Architecture Agent
        agent = ArchitectureAgent(openai_key, tavily_key)
        
        # Check initialization status
        status = agent.get_system_status()
        print(f"✅ Architecture Agent initialized: {status['initialized']}")
        print(f"   - LLM available: {status['has_llm']}")
        print(f"   - Web search available: {status['has_web_search']}")
        print(f"   - Catalog sources: {status['catalog_sources']}")
        print(f"   - Quality sources: {status['quality_sources']}")
        
        return status['initialized']
        
    except Exception as e:
        print(f"❌ Error initializing Architecture Agent: {str(e)}")
        return False

def test_catalog_loading():
    """Test catalog source loading"""
    print("\n📚 Testing Catalog Source Loading...")
    
    try:
        # Test catalog loading directly
        catalog_path = Path("data/sources.catalog.json")
        if not catalog_path.exists():
            print("❌ Catalog file not found")
            return False
        
        with open(catalog_path, 'r') as f:
            catalog_data = json.load(f)
        
        print(f"✅ Catalog loaded: {len(catalog_data)} sources")
        
        # Check for high-quality sources
        licensed_sources = [s for s in catalog_data if s.get("license_ok", False)]
        print(f"   - Licensed sources: {len(licensed_sources)}")
        
        # Check source types
        redbooks = [s for s in licensed_sources if s.get("doc_type") == "redbook"]
        product_docs = [s for s in licensed_sources if s.get("doc_type") == "product-doc"]
        
        print(f"   - Redbooks: {len(redbooks)}")
        print(f"   - Product docs: {len(product_docs)}")
        
        return len(licensed_sources) > 0
        
    except Exception as e:
        print(f"❌ Error loading catalog: {str(e)}")
        return False

def test_architecture_guidance(agent, scenario):
    """Test architecture guidance for a specific scenario"""
    print(f"\n🏗️ Testing: {scenario['name']}")
    print(f"   Question: {scenario['question']}")
    
    try:
        # Get architecture guidance
        guidance = agent.get_architecture_guidance(
            scenario['question'], 
            scenario.get('pattern_tags')
        )
        
        # Check response quality
        if guidance and len(guidance) > 100:
            print(f"✅ Response received ({len(guidance)} characters)")
            
            # Check for expected topics
            guidance_lower = guidance.lower()
            found_topics = []
            for topic in scenario['expected_topics']:
                if topic.lower() in guidance_lower:
                    found_topics.append(topic)
            
            print(f"   - Found {len(found_topics)}/{len(scenario['expected_topics'])} expected topics")
            if found_topics:
                print(f"   - Topics: {', '.join(found_topics)}")
            
            return len(found_topics) > 0
        else:
            print("❌ Response too short or empty")
            return False
            
    except Exception as e:
        print(f"❌ Error getting guidance: {str(e)}")
        return False

def run_architecture_agent_tests():
    """Run comprehensive Architecture Agent tests"""
    print("🚀 Running Architecture Agent Test Suite")
    print("=" * 50)
    
    # Test 1: Initialization
    init_success = test_architecture_agent_initialization()
    if not init_success:
        print("❌ Initialization failed - stopping tests")
        return False
    
    # Test 2: Catalog loading
    catalog_success = test_catalog_loading()
    if not catalog_success:
        print("❌ Catalog loading failed - stopping tests")
        return False
    
    # Test 3: Architecture guidance scenarios
    print("\n🏗️ Testing Architecture Guidance Scenarios...")
    
    # Initialize agent for testing
    openai_key = os.getenv("OPENAI_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    agent = ArchitectureAgent(openai_key, tavily_key)
    
    scenario_results = []
    for scenario in ARCHITECTURE_TEST_SCENARIOS:
        result = test_architecture_guidance(agent, scenario)
        scenario_results.append(result)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(scenario_results)
    total = len(scenario_results)
    
    print(f"✅ Passed: {passed}/{total} scenarios")
    print(f"❌ Failed: {total - passed}/{total} scenarios")
    
    if passed == total:
        print("🎉 All tests passed!")
    elif passed >= total * 0.7:
        print("⚠️ Most tests passed - some issues to investigate")
    else:
        print("❌ Many tests failed - needs investigation")
    
    return passed >= total * 0.7

def test_quick_scenarios():
    """Quick test of key scenarios without full validation"""
    print("⚡ Quick Architecture Agent Test")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("❌ OPENAI_API_KEY not found")
        return False
    
    try:
        agent = ArchitectureAgent(openai_key)
        
        # Test a simple scenario
        question = "What are the best practices for IBM MQ clustering?"
        guidance = agent.get_architecture_guidance(question)
        
        if guidance and len(guidance) > 200:
            print("✅ Quick test passed - Architecture Agent is working")
            return True
        else:
            print("❌ Quick test failed - response too short")
            return False
            
    except Exception as e:
        print(f"❌ Quick test error: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Architecture Agent")
    parser.add_argument("--quick", action="store_true", help="Run quick test only")
    
    args = parser.parse_args()
    
    if args.quick:
        success = test_quick_scenarios()
    else:
        success = run_architecture_agent_tests()
    
    sys.exit(0 if success else 1)
