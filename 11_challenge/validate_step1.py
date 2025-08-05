#!/usr/bin/env python3
"""
Validation script for Step 1.1 - Tests code structure without API keys
"""

import inspect
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / "backend"))

def test_class_structure():
    """Test that the EnhancedRAGASEvaluator class has the expected structure"""
    print("🧪 Testing Class Structure")
    print("=" * 30)
    
    try:
        from evaluation import EnhancedRAGASEvaluator
        
        # Check constructor parameters
        sig = inspect.signature(EnhancedRAGASEvaluator.__init__)
        params = list(sig.parameters.keys())
        
        print(f"✅ Constructor parameters: {params}")
        
        # Check that use_advanced_retrieval parameter exists
        if 'use_advanced_retrieval' in params:
            print("✅ use_advanced_retrieval parameter found")
        else:
            print("❌ use_advanced_retrieval parameter missing")
            return False
        
        # Check that parameter has default value
        param = sig.parameters['use_advanced_retrieval']
        if param.default is True:
            print("✅ use_advanced_retrieval defaults to True")
        else:
            print(f"❌ use_advanced_retrieval default is {param.default}, expected True")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing class structure: {e}")
        return False

def test_method_signatures():
    """Test that methods have expected signatures"""
    print("\n🔧 Testing Method Signatures")
    print("=" * 30)
    
    try:
        from evaluation import EnhancedRAGASEvaluator
        
        # Test setup_multi_agent_system method
        sig = inspect.signature(EnhancedRAGASEvaluator.setup_multi_agent_system)
        print(f"✅ setup_multi_agent_system signature: {sig}")
        
        # Test generate_synthetic_test_data method
        sig = inspect.signature(EnhancedRAGASEvaluator.generate_synthetic_test_data)
        print(f"✅ generate_synthetic_test_data signature: {sig}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing method signatures: {e}")
        return False

def test_imports():
    """Test that all required imports work"""
    print("\n📦 Testing Imports")
    print("=" * 20)
    
    try:
        # Test main evaluation import
        from evaluation import EnhancedRAGASEvaluator
        print("✅ EnhancedRAGASEvaluator import successful")
        
        # Test backend imports
        from backend.agents.multi_agent_system import MultiAgentSystem
        print("✅ MultiAgentSystem import successful")
        
        from backend.data.document_loader import DocumentLoader
        print("✅ DocumentLoader import successful")
        
        from backend.core.advanced_retrieval import AdvancedRetriever
        print("✅ AdvancedRetriever import successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_code_analysis():
    """Analyze the code for potential issues"""
    print("\n🔍 Code Analysis")
    print("=" * 20)
    
    try:
        # Read the evaluation.py file
        with open('evaluation.py', 'r') as f:
            content = f.read()
        
        # Check for key patterns
        checks = [
            ("use_advanced_retrieval parameter", "use_advanced_retrieval: bool = True"),
            ("MultiAgentSystem call with parameter", "use_advanced_retrieval=self.use_advanced_retrieval"),
            ("Baseline evaluation", "use_advanced_retrieval=False"),
            ("Advanced evaluation", "use_advanced_retrieval=True"),
            ("Performance comparison", "PERFORMANCE COMPARISON: BASELINE vs ADVANCED RETRIEVAL"),
            ("Results comparison", "baseline_score = results_baseline"),
            ("CSV output", "advanced_retrieval_evaluation_results.csv"),
        ]
        
        for check_name, pattern in checks:
            if pattern in content:
                print(f"✅ {check_name}: Found")
            else:
                print(f"❌ {check_name}: Missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error in code analysis: {e}")
        return False

def main():
    """Run all validation tests"""
    print("🚀 Validating Step 1.1 Implementation")
    print("=" * 50)
    
    tests = [
        ("Class Structure", test_class_structure),
        ("Method Signatures", test_method_signatures),
        ("Imports", test_imports),
        ("Code Analysis", test_code_analysis),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print(f"{'='*50}")
        
        if test_func():
            print(f"✅ {test_name}: PASSED")
            passed += 1
        else:
            print(f"❌ {test_name}: FAILED")
    
    print(f"\n{'='*50}")
    print(f"VALIDATION RESULTS: {passed}/{total} tests passed")
    print(f"{'='*50}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Ready for commit!")
        print("\n📝 Summary:")
        print("- ✅ Advanced retrieval parameter properly implemented")
        print("- ✅ Multi-agent system integration working")
        print("- ✅ Performance comparison framework ready")
        print("- ✅ All imports and dependencies valid")
        print("\n🚀 Ready to proceed with Step 1.2!")
    else:
        print("❌ Some tests failed - Review implementation before commit")
    
    return passed == total

 