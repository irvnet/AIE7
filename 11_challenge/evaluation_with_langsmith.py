#!/usr/bin/env python3
"""
Enhanced Evaluation with LangSmith Integration
Provides better visibility and faster execution for performance comparison
"""

import os
import sys
from pathlib import Path
import time
from typing import Dict, Any

# Add backend to path
sys.path.append(str(Path(__file__).parent / "backend"))

def setup_langsmith():
    """Setup LangSmith for tracing"""
    try:
        import langsmith
        # Set up LangSmith (optional - will work without it)
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_PROJECT"] = "student-loan-assistant-evaluation"
        print("✅ LangSmith tracing enabled")
        return True
    except ImportError:
        print("⚠️  LangSmith not available - continuing without tracing")
        return False

def run_quick_evaluation():
    """Run a quick evaluation to test the comparison"""
    print("🚀 Quick Performance Comparison")
    print("=" * 50)
    
    # Get API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        try:
            openai_key = input("Please enter your OpenAI API key: ").strip()
            if not openai_key:
                print("OpenAI API key is required")
                return
            os.environ["OPENAI_API_KEY"] = openai_key
        except KeyboardInterrupt:
            print("\nEvaluation cancelled")
            return
    
    # Setup LangSmith
    setup_langsmith()
    
    try:
        from evaluation import EnhancedRAGASEvaluator
        
        # Test with just 2 questions for quick comparison
        print("\n🔧 Testing Advanced Retrieval...")
        evaluator_advanced = EnhancedRAGASEvaluator(
            openai_api_key=openai_key,
            use_advanced_retrieval=True
        )
        
        # Setup multi-agent system
        print("Setting up advanced retrieval multi-agent system...")
        evaluator_advanced.setup_multi_agent_system(openai_key)
        
        # Test single question
        test_question = "What is the maximum loan amount for dependent undergraduate students?"
        print(f"Question: {test_question}")
        
        start_time = time.time()
        response_advanced = evaluator_advanced.multi_agent_system.process_query(test_question)
        advanced_time = time.time() - start_time
        
        print(f"Advanced Response: {response_advanced[:200]}...")
        print(f"Advanced Time: {advanced_time:.2f}s")
        
        print("\n🔧 Testing Baseline Retrieval...")
        evaluator_baseline = EnhancedRAGASEvaluator(
            openai_api_key=openai_key,
            use_advanced_retrieval=False
        )
        
        # Setup multi-agent system
        print("Setting up baseline retrieval multi-agent system...")
        evaluator_baseline.setup_multi_agent_system(openai_key)
        
        start_time = time.time()
        response_baseline = evaluator_baseline.multi_agent_system.process_query(test_question)
        baseline_time = time.time() - start_time
        
        print(f"Baseline Response: {response_baseline[:200]}...")
        print(f"Baseline Time: {baseline_time:.2f}s")
        
        # Quick comparison
        print("\n" + "="*50)
        print("QUICK COMPARISON RESULTS")
        print("="*50)
        print(f"Advanced Retrieval Time: {advanced_time:.2f}s")
        print(f"Baseline Retrieval Time: {baseline_time:.2f}s")
        print(f"Time Difference: {baseline_time - advanced_time:.2f}s")
        print(f"Speed Improvement: {((baseline_time - advanced_time) / baseline_time * 100):.1f}%")
        
        # Response quality comparison (simple length comparison)
        print(f"\nAdvanced Response Length: {len(response_advanced)} chars")
        print(f"Baseline Response Length: {len(response_baseline)} chars")
        
        return {
            "advanced": {
                "response": response_advanced,
                "time": advanced_time,
                "length": len(response_advanced)
            },
            "baseline": {
                "response": response_baseline,
                "time": baseline_time,
                "length": len(response_baseline)
            }
        }
        
    except Exception as e:
        print(f"❌ Error during evaluation: {e}")
        import traceback
        traceback.print_exc()
        return None

def run_full_evaluation_with_progress():
    """Run full evaluation with progress tracking"""
    print("🚀 Full Performance Evaluation with Progress Tracking")
    print("=" * 60)
    
    # Get API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        try:
            openai_key = input("Please enter your OpenAI API key: ").strip()
            if not openai_key:
                print("OpenAI API key is required")
                return
            os.environ["OPENAI_API_KEY"] = openai_key
        except KeyboardInterrupt:
            print("\nEvaluation cancelled")
            return
    
    # Setup LangSmith
    setup_langsmith()
    
    try:
        from evaluation import EnhancedRAGASEvaluator
        
        print("\n📊 Running Advanced Retrieval Evaluation...")
        evaluator_advanced = EnhancedRAGASEvaluator(
            openai_api_key=openai_key,
            use_advanced_retrieval=True
        )
        
        # Run evaluation with progress
        results_advanced = evaluator_advanced.run_evaluation()
        
        print("\n📊 Running Baseline Retrieval Evaluation...")
        evaluator_baseline = EnhancedRAGASEvaluator(
            openai_api_key=openai_key,
            use_advanced_retrieval=False
        )
        
        # Run evaluation with progress
        results_baseline = evaluator_baseline.run_evaluation()
        
        # Print comparison
        print("\n" + "="*80)
        print("PERFORMANCE COMPARISON RESULTS")
        print("="*80)
        
        print("\nStandard RAGAS Metrics Comparison:")
        print(f"{'Metric':<25} {'Baseline':<12} {'Advanced':<12} {'Improvement':<12}")
        print("-" * 65)
        
        standard_metrics = ["faithfulness", "relevance", "context_precision", "context_recall"]
        for metric in standard_metrics:
            baseline_score = results_baseline["aggregate_metrics"].get(metric, 0.0)
            advanced_score = results_advanced["aggregate_metrics"].get(metric, 0.0)
            improvement = advanced_score - baseline_score
            improvement_str = f"+{improvement:.3f}" if improvement > 0 else f"{improvement:.3f}"
            print(f"{metric.capitalize():<25} {baseline_score:<12.3f} {advanced_score:<12.3f} {improvement_str:<12}")
        
        print("\nAgent-Specific Metrics Comparison:")
        print(f"{'Metric':<25} {'Baseline':<12} {'Advanced':<12} {'Improvement':<12}")
        print("-" * 65)
        
        agent_metrics = ["tool_call_accuracy", "agent_goal_accuracy", "multi_agent_coordination"]
        for metric in agent_metrics:
            baseline_score = results_baseline["aggregate_metrics"].get(metric, 0.0)
            advanced_score = results_advanced["aggregate_metrics"].get(metric, 0.0)
            improvement = advanced_score - baseline_score
            improvement_str = f"+{improvement:.3f}" if improvement > 0 else f"{improvement:.3f}"
            print(f"{metric.capitalize():<25} {baseline_score:<12.3f} {advanced_score:<12.3f} {improvement_str:<12}")
        
        # Overall comparison
        baseline_overall = results_baseline["aggregate_metrics"].get("overall_score", 0.0)
        advanced_overall = results_advanced["aggregate_metrics"].get("overall_score", 0.0)
        overall_improvement = advanced_overall - baseline_overall
        
        print(f"\nOverall Score Comparison:")
        print(f"Baseline: {baseline_overall:.3f}")
        print(f"Advanced: {advanced_overall:.3f}")
        print(f"Improvement: {overall_improvement:+.3f}")
        
        return {
            "baseline": results_baseline,
            "advanced": results_advanced,
            "comparison": {
                "overall_improvement": overall_improvement
            }
        }
        
    except Exception as e:
        print(f"❌ Error during evaluation: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main function with options"""
    print("🎯 Performance Evaluation Options")
    print("=" * 40)
    print("1. Quick Test (1 question, fast)")
    print("2. Full Evaluation (10 questions, detailed)")
    print("3. Exit")
    
    try:
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            results = run_quick_evaluation()
            if results:
                print("\n✅ Quick evaluation completed!")
        elif choice == "2":
            results = run_full_evaluation_with_progress()
            if results:
                print("\n✅ Full evaluation completed!")
        elif choice == "3":
            print("Exiting...")
            return
        else:
            print("Invalid choice. Exiting...")
            return
            
    except KeyboardInterrupt:
        print("\nEvaluation cancelled")
        return

if __name__ == "__main__":
    main() 