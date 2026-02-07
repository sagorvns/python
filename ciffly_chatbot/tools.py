"""Tools used by Ciffly Chatbot agents."""
from typing import Annotated

from langchain_core.tools import tool
from logger_utils import get_logger

logger = get_logger(__name__)


@tool
def support_ticket_tracker_tool(
    name: Annotated[str, "Contact name"],
    email: Annotated[str, "Contact email"],
    phone: Annotated[str, "Contact phone"],
    issue_description: Annotated[str, "Description of the support issue"],
) -> str:
    """Create or update a support ticket with the given contact and issue details."""
    # In production: persist to DB (e.g. DynamoDB) or call support API
    logger.info("Support ticket: name=%s email=%s phone=%s issue=%s", name, email, phone, issue_description)
    return f"Support ticket created for {name} ({email}). We will get back to you soon."


@tool
def search_ranker_tool(
    query: Annotated[str, "Search query to find relevant snippets"],
) -> str:
    """Search and return top relevant snippets for the user's query (e.g. docs/FAQ)."""
    # In production: call your search/vector store API
    logger.info("Search ranker query: %s", query)
    return f"[Placeholder] Top snippets for: {query}. Configure your search backend in tools.search_ranker_tool."


@tool
def lead_capture_tool(
    name: Annotated[str, "Lead name"],
    email: Annotated[str, "Valid email address"],
    phone: Annotated[str, "Valid phone number"],
    preferred_contact: Annotated[str, "Preferred contact method: email or phone"],
) -> str:
    """Capture and save lead details (name, email, phone, preferred contact)."""
    # In production: save to CRM or DynamoDB
    logger.info("Lead captured: name=%s email=%s phone=%s contact=%s", name, email, phone, preferred_contact)
    return f"Thank you, {name}. We will contact you via {preferred_contact}."
