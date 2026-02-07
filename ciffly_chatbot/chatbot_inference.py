"""
Ciffly Chatbot graph: supervisor routes to Support, QnA, or Lead agent.
"""
import os
from typing import Literal, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

from agents import (
    build_lead_agent,
    build_qna_agent,
    build_support_agent,
    get_supervisor_chain,
)
from logger_utils import get_logger

load_dotenv()
logger = get_logger(__name__)


def _get_llm():
    """Create LLM from env (OPENAI_API_KEY or ANTHROPIC_API_KEY)."""
    if os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.2,
        )
    try:
        from langchain_anthropic import ChatAnthropic
        if os.getenv("ANTHROPIC_API_KEY"):
            return ChatAnthropic(
                model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
                temperature=0.2,
            )
    except ImportError:
        pass
    raise RuntimeError("Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env")


def _get_checkpointer():
    """Optional DynamoDB checkpointer for persistence (e.g. multi-turn)."""
    table_name = os.getenv("DYNAMODB_CHECKPOINT_TABLE")
    if not table_name:
        return None
    try:
        from langgraph.checkpoint.dynamodb import DynamoDBSaver
        return DynamoDBSaver.from_conn_str(table_name)
    except ImportError:
        try:
            from langgraph_dynamodb_checkpoint import DynamoDBSaver
            return DynamoDBSaver(table_name=table_name)
        except ImportError:
            logger.warning("DynamoDB checkpointer not installed; run: pip install langgraph-dynamodb-checkpoint")
            return None
    except Exception as e:
        logger.warning("DynamoDB checkpointer disabled: %s", e)
        return None


# Graph state: messages + routing key from supervisor
class GraphState(TypedDict):
    messages: list[BaseMessage]
    next: str | None


def _supervisor_node(state: GraphState) -> dict:
    last = state["messages"][-1] if state["messages"] else None
    if not last or not getattr(last, "content", None):
        return {"next": "qna_agent"}
    llm = _get_llm()
    chain = get_supervisor_chain(llm)
    out = chain.invoke({"input": last.content})
    return {"next": out.next}


def _support_node(state: GraphState) -> dict:
    llm = _get_llm()
    agent = build_support_agent(llm)
    result = agent.invoke(state)
    return {"messages": result["messages"]}


def _qna_node(state: GraphState) -> dict:
    llm = _get_llm()
    agent = build_qna_agent(llm)
    result = agent.invoke(state)
    return {"messages": result["messages"]}


def _lead_node(state: GraphState) -> dict:
    llm = _get_llm()
    agent = build_lead_agent(llm)
    result = agent.invoke(state)
    return {"messages": result["messages"]}


def _route_after_supervisor(state: GraphState) -> Literal["support_agent", "qna_agent", "lead"]:
    n = state.get("next") or "qna_agent"
    if n == "support_agent":
        return "support_agent"
    if n == "lead":
        return "lead"
    return "qna_agent"


def build_graph():
    """Build the supervisor -> support/qna/lead graph."""
    graph = StateGraph(GraphState)

    graph.add_node("supervisor", _supervisor_node)
    graph.add_node("support_agent", _support_node)
    graph.add_node("qna_agent", _qna_node)
    graph.add_node("lead", _lead_node)

    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges("supervisor", _route_after_supervisor)
    graph.add_edge("support_agent", END)
    graph.add_edge("qna_agent", END)
    graph.add_edge("lead", END)

    checkpointer = _get_checkpointer()
    return graph.compile(checkpointer=checkpointer)


# Lazy singleton for Lambda
_graph = None


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


def run_chat(user_message: str, thread_id: str | None = None) -> list[BaseMessage]:
    """Run one user turn and return updated messages."""
    messages = [HumanMessage(content=user_message)]
    config = {"configurable": {"thread_id": thread_id or "default"}}
    result = get_graph().invoke({"messages": messages}, config=config)
    return result.get("messages", [])
