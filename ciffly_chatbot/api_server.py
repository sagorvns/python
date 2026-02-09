"""
Flask REST API for Ciffly Chatbot.
Usage: python api_server.py
Then test with: curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d "{\"message\": \"Hello\"}"
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot_inference import run_chat
from logger_utils import get_logger
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access
logger = get_logger(__name__)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "ciffly-chatbot"}), 200


@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint.
    Request body: {"message": "user message", "thread_id": "optional-thread-id"}
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' in request body"}), 400
        
        user_message = data['message']
        thread_id = data.get('thread_id', str(uuid.uuid4()))
        
        # Get chatbot response
        messages = run_chat(user_message, thread_id=thread_id)
        
        # Extract response
        if messages:
            last_message = messages[-1]
            response_content = getattr(last_message, 'content', str(last_message))
            
            # Handle list responses
            if isinstance(response_content, list):
                response_text = '\n'.join([
                    item.get('text', str(item)) if isinstance(item, dict) else str(item)
                    for item in response_content
                ])
            else:
                response_text = response_content
            
            return jsonify({
                "response": response_text,
                "thread_id": thread_id,
                "status": "success"
            }), 200
        else:
            return jsonify({
                "error": "No response from chatbot",
                "thread_id": thread_id,
                "status": "error"
            }), 500
            
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500


@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API documentation."""
    return jsonify({
        "service": "Ciffly Chatbot API",
        "version": "1.0",
        "endpoints": {
            "GET /health": "Health check",
            "POST /chat": "Send a message to the chatbot",
            "GET /": "This documentation"
        },
        "example_curl": "curl -X POST http://localhost:5000/chat -H 'Content-Type: application/json' -d '{\"message\": \"I want a demo\"}'"
    }), 200


if __name__ == '__main__':
    print("=" * 60)
    print("Ciffly Chatbot API Server")
    print("=" * 60)
    print("Server running at: http://localhost:5000")
    print("\nEndpoints:")
    print("  GET  /health  - Health check")
    print("  POST /chat    - Send message")
    print("\nExample curl command:")
    print('  curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d "{\\"message\\": \\"Hello\\"}"')
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
