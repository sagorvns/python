"""
Ciffly Chatbot agents: Support, QnA, Lead capture, and Supervisor router.
"""
from typing import Literal, TypedDict

from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langgraph.prebuilt import create_react_agent
from logger_utils import get_logger

from tools import (
    lead_capture_tool,
    search_ranker_tool,
    support_ticket_tracker_tool,
)

logger = get_logger(__name__)


# --- State ---
class State(TypedDict):
    """Chat state: list of messages."""
    messages: list[BaseMessage]


# --- Support Agent ---
SUPPORT_PROMPT = """You are a support agent. Your job is to acknowledge user issues and create a support ticket.

- Collect: name, email, phone, and a clear description of the issue.
- Do not re-ask for information the user has already provided.
- Always call support_ticket_tracker_tool with whatever details you have (use placeholders only if truly missing).
- Reply in this format: <response><sep><follow_up_question or empty>
- Keep responses concise and professional."""


def build_support_agent(llm: BaseChatModel):
    return create_react_agent(
        llm,
        tools=[support_ticket_tracker_tool],
        prompt=ChatPromptTemplate.from_messages([
            ("system", SUPPORT_PROMPT),
            ("placeholder", "{messages}"),
        ]),
    )


# --- QnA Agent ---
QNA_PROMPT = """You are a QnA agent. Use the search_ranker_tool to find up to top 10 relevant snippets for the user's query.

- Provide concise, factual answers based only on the search results.
- If results are insufficient, say so and suggest rephrasing or contacting support.
- Do not invent information."""


def build_qna_agent(llm: BaseChatModel):
    return create_react_agent(
        llm,
        tools=[search_ranker_tool],
        prompt=ChatPromptTemplate.from_messages([
            ("system", QNA_PROMPT),
            ("placeholder", "{messages}"),
        ]),
    )


# --- Lead Agent ---
def make_lead_prompt(suffix: str = "") -> str:
    return f"""You are a lead capture agent. Your goal is to collect and save lead details.

Lead capture requirements:
- Collect: name, valid email, valid phone number.
- If something is missing, ask once politely.
- Ask for preferred contact method (email or phone).

Validation:
- Email: must have local part, '@', and domain.
- Phone: 7–14 digits, numbers only. Politely re-prompt if invalid.

Response rules:
- First response: acknowledge without asking a question.
- Second response: one short follow-up question if needed.
- Do not re-ask for already collected details.
- Do not confirm appointments; only capture lead info.

Output format: Generated reply <sep> Follow-up question (or empty)
Keep reply under 250 characters.
{suffix}"""


def build_lead_agent(llm: BaseChatModel):
    return create_react_agent(
        llm,
        tools=[lead_capture_tool],
        prompt=ChatPromptTemplate.from_messages([
            ("system", make_lead_prompt()),
            ("placeholder", "{messages}"),
        ]),
    )


# --- Supervisor (Router) ---
SUPERVISOR_SYSTEM = """You are a supervisor. Route the user's request to the right agent.

- qna_agent: general questions, how-to, product info (intent: info).
- lead: user wants to sign up, get a demo, or leave contact details (intent: lead).
- support_agent: user has a problem, bug, or needs help with an issue (intent: support).

Reply with the next agent and intent only."""


def get_supervisor_chain(llm: BaseChatModel):
    from pydantic import BaseModel, Field

    class RouterModel(BaseModel):
        next: Literal["qna_agent", "lead", "support_agent"] = Field(description="Next agent to invoke")
        intent: str = Field(description="Brief intent label")

    structured_llm = llm.with_structured_output(RouterModel)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SUPERVISOR_SYSTEM),
        ("human", "{input}"),
    ])
    return prompt | structured_llm
