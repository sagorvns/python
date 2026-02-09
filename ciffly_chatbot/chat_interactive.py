"""
Interactive CLI chatbot - chat in the terminal with conversation history.
Usage: python chat_interactive.py
"""
import sys
from chatbot_inference import run_chat
from logger_utils import get_logger

logger = get_logger(__name__)


def main():
    print("=" * 60)
    print("🤖 Ciffly Chatbot - Interactive Mode")
    print("=" * 60)
    print("Type your message and press Enter to chat.")
    print("Type 'quit', 'exit', or press Ctrl+C to stop.\n")
    
    thread_id = "interactive-session"
    
    try:
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Goodbye! Thanks for chatting!")
                break
            
            # Get chatbot response
            try:
                messages = run_chat(user_input, thread_id=thread_id)
                
                # Extract the last message (bot's response)
                if messages:
                    last_message = messages[-1]
                    response = getattr(last_message, 'content', str(last_message))
                    
                    # Handle list responses (from tool calls)
                    if isinstance(response, list):
                        response = '\n'.join([
                            item.get('text', str(item)) if isinstance(item, dict) else str(item)
                            for item in response
                        ])
                    
                    print(f"\n🤖 Bot: {response}\n")
                else:
                    print("\n🤖 Bot: No response received.\n")
                    
            except Exception as e:
                logger.error(f"Error processing message: {e}", exc_info=True)
                print(f"\n❌ Error: {e}\n")
                
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for chatting!")
        sys.exit(0)


if __name__ == "__main__":
    main()
