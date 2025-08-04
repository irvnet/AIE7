#!/usr/bin/env python3
"""
Test script for Step 1.1: Advanced Retrieval Support in Evaluation Framework
Validates that the evaluation can switch between baseline and advanced retrieval modes
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / "backend"))

def test_evaluation_initialization():
    """Test that both baseline and advanced evaluators can be initialized"""
    print("🧪 Testing Evaluation Framework Initialization")
    print("=" * 50)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in environment")
        print("💡 Set your API key and run again")
        return False
    
    try:
        from evaluation import EnhancedRAGASEvaluator
        
        # Test advanced retrieval evaluator
        print("🔧 Testing Advanced Retrieval Evaluator...")
        evaluator_advanced = EnhancedRAGASEvaluator(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            use_advanced_retrieval=True
        )
        print("✅ Advanced retrieval evaluator initialized successfully")
        print(f"   use_advanced_retrieval: {evaluator_advanced.use_advanced_retrieval}")
        
        # Test baseline retrieval evaluator
        print("🔧 Testing Baseline Retrieval Evaluator...")
        evaluator_baseline = EnhancedRAGASEvaluator(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            use_advanced_retrieval=False
        )
        print("✅ Baseline retrieval evaluator initialized successfully")
        print(f"   use_advanced_retrieval: {evaluator_baseline.use_advanced_retrieval}")
        
        # Test default behavior (should be advanced)
        print("🔧 Testing Default Evaluator...")
        evaluator_default = EnhancedRAGASEvaluator(
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        print("✅ Default evaluator initialized successfully")
        print(f"   use_advanced_retrieval: {evaluator_default.use_advanced_retrieval}")
        
        print("\n🎉 All evaluator initializations successful!")
        return True
        
    except Exception as e:
        print(f"❌ Error during evaluation initialization: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multi_agent_system_setup():
    """Test that multi-agent system can be set up with both modes"""
    print("\n🔧 Testing Multi-Agent System Setup")
    print("=" * 40)
    
    try:
        from evaluation import EnhancedRAGASEvaluator
        
        # Test advanced retrieval setup
        print("🔧 Setting up advanced retrieval multi-agent system...")
        evaluator_advanced = EnhancedRAGASEvaluator(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            use_advanced_retrieval=True
        )
        evaluator_advanced.setup_multi_agent_system(os.getenv("OPENAI_API_KEY"))
        print("✅ Advanced retrieval multi-agent system setup successful")
        
        # Test baseline retrieval setup
        print("🔧 Setting up baseline retrieval multi-agent system...")
        evaluator_baseline = EnhancedRAGASEvaluator(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            use_advanced_retrieval=False
        )
        evaluator_baseline.setup_multi_agent_system(os.getenv("OPENAI_API_KEY"))
        print("✅ Baseline retrieval multi-agent system setup successful")
        
        print("\n🎉 All multi-agent system setups successful!")
        return True
        
    except Exception as e:
        print(f"❌ Error during multi-agent system setup: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_synthetic_data_generation():
    """Test that synthetic test data can be generated"""
    print("\n📄 Testing Synthetic Data Generation")
    print("=" * 35)
    
    try:
        from evaluation import EnhancedRAGASEvaluator
        
        evaluator = EnhancedRAGASEvaluator(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            use_advanced_retrieval=True
        )
        
        test_cases = evaluator.generate_synthetic_test_data()
        print(f"✅ Generated {len(test_cases)} test cases")
        
        # Show sample test case
        if test_cases:
            sample = test_cases[0]
            print(f"   Sample question: {sample.question[:50]}...")
            print(f"   Category: {sample.category}")
            print(f"   Expected tools: {sample.expected_tools}")
        
        print("\n🎉 Synthetic data generation successful!")
        return True
        
    except Exception as e:
        print(f"❌ Error during synthetic data generation: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests for Step 1.1"""
    print("🚀 Testing Step 1.1: Advanced Retrieval Support in Evaluation Framework")
    print("=" * 80)
    
    # Test 1: Evaluation initialization
    if not test_evaluation_initialization():
        return
    
    # Test 2: Multi-agent system setup
    if not test_multi_agent_system_setup():
        return
    
    # Test 3: Synthetic data generation
    if not test_synthetic_data_generation():
        return
    
    print("\n" + "="*80)
    print("✅ STEP 1.1 VALIDATION COMPLETE")
    print("="*80)
    print("\n📝 Summary:")
    print("- ✅ Evaluation framework supports both baseline and advanced retrieval")
    print("- ✅ Multi-agent system can be initialized in both modes")
    print("- ✅ Synthetic test data generation works")
    print("- ✅ Ready for Step 1.2: Performance comparison")
    
    print("\n🎯 Next Steps:")
    print("1. Run full evaluation with both modes")
    print("2. Compare performance metrics")
    print("3. Document improvements")

if __name__ == "__main__":
    main() 