#!/usr/bin/env python3
"""
Test script for enhanced evaluation endpoint
"""

import requests
import json
import os

def test_enhanced_evaluation():
    """Test the enhanced evaluation endpoint"""
    
    # Get API key from environment or prompt
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        openai_key = input("Please enter your OpenAI API key: ").strip()
    
    # Test quick evaluation
    print("🧪 Testing Quick Evaluation...")
    response = requests.post("http://localhost:8000/evaluate", json={
        "openai_api_key": openai_key,
        "evaluation_type": "quick"
    })
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print("✅ Quick evaluation successful!")
            print(f"Evaluation type: {result.get('evaluation_type')}")
            
            # Display results
            if "results" in result and result["results"]:
                results = result["results"]
                if "advanced" in results and "baseline" in results:
                    print("\n📊 Quick Evaluation Results:")
                    print(f"Advanced Time: {results['advanced']['time']:.2f}s")
                    print(f"Baseline Time: {results['baseline']['time']:.2f}s")
                    print(f"Speed Improvement: {((results['baseline']['time'] - results['advanced']['time']) / results['baseline']['time'] * 100):.1f}%")
                else:
                    print("❌ Unexpected results format")
            else:
                print("❌ No results returned")
        else:
            print(f"❌ Evaluation failed: {result.get('error')}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        print(response.text)
    
    print("\n" + "="*50)
    
    # Test with LangSmith (optional)
    langsmith_key = input("Enter LangSmith API key (optional, press Enter to skip): ").strip()
    if langsmith_key:
        print("🧪 Testing Quick Evaluation with LangSmith...")
        response = requests.post("http://localhost:8000/evaluate", json={
            "openai_api_key": openai_key,
            "evaluation_type": "quick",
            "langsmith_api_key": langsmith_key
        })
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ Quick evaluation with LangSmith successful!")
            else:
                print(f"❌ Evaluation failed: {result.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")

if __name__ == "__main__":
    test_enhanced_evaluation() 