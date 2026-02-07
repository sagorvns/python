"""
AWS Lambda handler for Ciffly Chatbot.
Invoke via API Gateway (REST or WebSocket) or direct Lambda invocation.
"""
import json
import os

from logger_utils import get_logger

logger = get_logger(__name__)


def _get_body(event: dict) -> dict:
    """Parse body from API Gateway or direct invoke."""
    body = event.get("body")
    if body is None:
        return event
    if isinstance(body, str):
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {"message": body}
    return body


def _response(status_code: int, body: dict | list) -> dict:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": os.getenv("CORS_ORIGIN", "*"),
        },
        "body": json.dumps(body),
    }


def handler(event: dict, context: object) -> dict:
    """
    Lambda entry point.

    Expected input (e.g. from API Gateway body):
        { "message": "user text", "thread_id": "optional-session-id" }

    Returns:
        { "reply": "assistant message", "messages": [...] } or error.
    """
    try:
        body = _get_body(event)
        user_message = body.get("message") or body.get("query") or ""
        thread_id = body.get("thread_id")

        if not user_message.strip():
            return _response(400, {"error": "Missing 'message' or 'query'"})

        from chatbot_inference import run_chat

        messages = run_chat(user_message, thread_id=thread_id)

        # Last message is typically the assistant reply
        last = messages[-1] if messages else None
        reply = getattr(last, "content", str(last)) if last else "No response."

        return _response(200, {"reply": reply, "messages": _serialize_messages(messages)})

    except Exception as e:
        logger.exception("Lambda handler error")
        return _response(500, {"error": str(e)})


def _serialize_messages(messages: list) -> list[dict]:
    """Convert message objects to JSON-serializable dicts."""
    out = []
    for m in messages:
        role = getattr(m, "type", "unknown")
        if hasattr(m, "content"):
            out.append({"role": role, "content": m.content})
        else:
            out.append({"role": role, "content": str(m)})
    return out
