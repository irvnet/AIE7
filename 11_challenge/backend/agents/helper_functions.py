"""
Helper Functions for Multi-Agent System
Based on proven patterns from example code lessons 5-9
"""

import functools
from typing import Any, Callable, List, Optional, TypedDict, Union
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph


def agent_node(state, agent, name):
    """Create an agent node for LangGraph"""
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}


def create_agent(
    llm: ChatOpenAI,
    tools: list,
    system_prompt: str,
) -> AgentExecutor:
    """Create a function-calling agent and add it to the graph.
    
    Based on proven pattern from example code lesson 6.
    """
    system_prompt += ("\nWork autonomously according to your specialty, using the tools available to you."
    " Do not ask for clarification."
    " Your other team members (and other teams) will collaborate with you with their own specialties."
    " You are chosen for a reason!")
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor


def create_team_supervisor(
    llm: ChatOpenAI,
    system_prompt: str,
    team_members: List[str],
) -> Callable:
    """Create a team supervisor agent.
    
    Based on proven pattern from example code lesson 6.
    """
    system_prompt += f"\n\nYou are a supervisor tasked with managing a conversation between the following workers: {', '.join(team_members)}. Given the following user request, respond with the worker to act next. Each worker will perform a task and respond with their results and status. When each team is finished, you must respond with FINISH."
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    
    def supervisor(state):
        messages = state["messages"]
        response = llm.invoke(messages)
        return {"next": response.content}
    
    return supervisor


def enter_chain(message: str, members: List[str] = None):
    """Create entry point for a chain.
    
    Based on proven pattern from example code lesson 6.
    """
    results = {
        "messages": [HumanMessage(content=message)],
    }
    if members:
        results["team_members"] = ", ".join(members)
    return results


def get_last_message(state: dict) -> str:
    """Extract the last message from state."""
    return state["messages"][-1].content


def join_graph(response: dict):
    """Join graph response back to parent state."""
    return {"messages": [response["messages"][-1]]} 