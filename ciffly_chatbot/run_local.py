"""
Run the chatbot locally (CLI). Usage:
  python run_local.py "Your message here"
  echo "Your message" | python run_local.py
"""
import sys
from chatbot_inference import run_chat


def main():
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = sys.stdin.read().strip()
    if not message:
        print("Usage: python run_local.py <message>", file=sys.stderr)
        sys.exit(1)
    messages = run_chat(message)
    last = messages[-1] if messages else None
    reply = getattr(last, "content", str(last)) if last else "No response."
    print(reply)


if __name__ == "__main__":
    main()
