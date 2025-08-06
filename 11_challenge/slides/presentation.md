---
marp: true
theme: default
paginate: true
backgroundColor: #fff
color: #333
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    padding: 40px;
    font-size: 1.0em; /* Increased by ~2pt from 0.9375em */
  }
  h1 {
    color: #2563eb;
    font-size: 2.5em; /* Increased by ~2pt from 2.3em */
    margin-bottom: 20px;
  }
  h2 {
    color: #1e40af;
    font-size: 1.8em; /* Increased by ~2pt from 1.6em */
    margin-bottom: 15px;
  }
  .highlight {
    background-color: #dbeafe;
    padding: 10px;
    border-radius: 5px;
    border-left: 4px solid #2563eb;
  }
  .decision {
    background-color: #fef3c7;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #f59e0b;
    margin: 15px 0;
  }
  .outcome {
    background-color: #dcfce7;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #16a34a;
    margin: 15px 0;
  }
  .problem {
    background-color: #fee2e2;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #dc2626;
    margin: 15px 0;
  }
---

# Student Loan Assistant
## Multi-Agent RAG System

---

# 🎯 The Problem We Solved

<div class="problem">

**Imagine: its almost time for shool... and:**

- You're a student working out funding to get to your first semester at the school you've been accepted to
- You're in the school loan department managing a sea of incoming students that have questions
- You're a parent just trying to survive one of the most important turning points in your childs life... 

All the hours of researching seem wasted since everyting has changed with a new incoming administration making big changes... How can you possibly find the information you need with the deadlines for the school year approaching so quickly??!

</div>

<div class="highlight">

**Welcome to the Solution!:** Build an AI system that provides accurate, current student loan assistance by intelligently combining multiple information sources and expert agents.

</div>

---

# 🏗️ Multi-Agent Architecture

<div class="decision">

** Multi-Agent vs Single Agent

- Single agents struggle with complex, multi-step tasks
- Student loan questions require: research → analysis → document creation
- We needed specialized expertise for different types of questions

</div>

<div class="outcome">

**Our Solution:** Two specialized teams
- **Research Team:** Finds and validates current information
- **Document Team:** Creates personalized guidance documents

**Outcome:** Each agent focuses on what they do best, leading to higher quality results.

</div>

---

## Multi-Agent System Architecture

![image](diagram.png)


**Key Features:**
- **Hierarchical Structure:** Meta supervisor orchestrates specialized teams
- **Specialized Agents:** Each agent has a specific expertise area
- **Multiple Data Sources:** Documents, APIs, and external resources
- **Flexible Response:** Direct answers or detailed documents

---

# 🔍 Information Strategy: Current vs Outdated

<div class="problem">

**An issue we discovered:**
- Government documents contain static, often outdated information
- School loan Interest rates regularly 
- Students, parents and educators need current, actionable information in a timely fashion

</div>

<div class="decision">

**Decision:** Implement intelligent information validation
- **Reject anything older than 12 months** for time-sensitive queries
- **Use specific years** (2024, 2025) instead of vague "current" terms
- **5-attempt retry system** to ensure we get current data without getting stuck

</div>


---

# ⚡ Performance Optimization: Speed Matters

<div class="decision">

**Key Decision:** Which retrieval method to use for document search

**The Challenge:** We had 6 different search methods, each with trade-offs:
- Multi-Query: 12x slower but comprehensive
- Contextual Compression: 69x slower but precise
- BM25: 60% slower but keyword-focused

</div>

<div class="outcome">

**Our Analysis:** Tested all methods on 10 diverse questions
- **Ensemble Retrieval won:** 17% faster than baseline
- **Combines semantic + keyword search** with 70/30 weighting
- **100% success rate** across all test cases

**Why This Mattered:** This was a key lesson learned since the system was slow and keyword search alone was very insufficient. Semantic search yielded better, but not necessary accurate results though doing semantic search first, then keyword search worked well. It also provided faster results as the system was initially slow.

</div>

---

# 📊 Quality Assurance: Measure What Matters

<div class="decision">

**Key Decision:** How to measure success beyond just "does it work?"

**Our Approach:** Comprehensive evaluation framework
- **RAGAS metrics:** Faithfulness, relevance, precision, recall
- **Agent-specific metrics:** Tool usage, goal achievement, coordination
- **Real-world testing:** 10 complex scenarios covering all loan types

</div>

<div class="outcome">

**Critical Finding:** Our system achieved perfect faithfulness and relevance scores, but we discovered UI issues that were masking the underlying quality.

**Why Important:** Without proper evaluation, we wouldn't know if our optimizations were actually improving the system.

</div>

---

# 🚀 Advanced Capabilities: Beyond Simple Q&A

<div class="decision">

**Key Decision:** How to handle complex, multi-step requests

**The Challenge:** Students don't just want answers—they want action plans
- "How do I apply for income-based repayment?"
- "What documents do I need for loan forgiveness?"

</div>

<div class="outcome">

**Our Solution:** Intelligent document creation system
- **Automatic outline generation** for complex topics
- **Step-by-step guidance** with specific requirements
- **Personalized recommendations** based on individual situations

**Why This Mattered:** It transforms our system from an information source into a true assistant that helps students take action.

</div>

---

# 🎯 The Result: Real Impact

<div class="outcome">

**A system that:**
- Provides **current, accurate information** (not outdated rates)
- **Understands context** and creates personalized guidance
- **Responds in under 0.2 seconds** for fast user experience
- **Achieves perfect accuracy** on complex loan questions

</div>

<div class="highlight">

**The Key Insight:** Every technical decision was driven by user needs. We didn't just build a system that works—we built one that solves real problems for real students.

**The Impact:** Students can now get accurate, current loan assistance in seconds, not hours of research across multiple government websites.

</div>

---

# 💡 Key Decision Themes

## 1. **User-Centric Design**
Every decision prioritized student needs

## 2. **Performance Matters**
Speed and accuracy are equally important

## 3. **Validation is Critical**
Measure what matters, not just what's easy

## 4. **Simplicity Wins**
Complex solutions often perform worse than optimized simple ones

## 5. **Current Information is Non-Negotiable**
Outdated data is worse than no data

---

# Thank You!

<div class="highlight">

*"We didn't just build another chatbot. We built an intelligent assistant that understands the difference between 2023 and 2025 interest rates—and why that matters to a student's financial future."*

</div>

## Questions? 
