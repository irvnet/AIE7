#!/usr/bin/env python3
"""
Debug script to test evaluation functions directly
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / "backend"))

def test_evaluation_directly():
    """Test evaluation functions directly"""
    
    # Get API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        openai_key = input("Please enter your OpenAI API key: ").strip()
    
    print("🔧 Testing evaluation functions directly...")
    
    try:
        from evaluation_with_langsmith import run_quick_evaluation
        
        print("Calling run_quick_evaluation...")
        results = run_quick_evaluation(openai_key)
        
        print(f"Results type: {type(results)}")
        print(f"Results: {results}")
        
        if results:
            print("✅ Evaluation successful!")
            return True
        else:
            print("❌ Evaluation returned None")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_evaluation_directly() 