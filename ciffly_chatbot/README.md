# Ciffly Chatbot

Standalone AI chatbot project (separate from task_backend). Supervisor routes to three agents:

- **QnA** – general questions, how-to, product info (uses `search_ranker_tool`)
- **Lead** – sign up, demo, contact capture (uses `lead_capture_tool`)
- **Support** – issues and tickets (uses `support_ticket_tracker_tool`)

Built with **LangGraph** and **LangChain**, ready for **AWS** (Lambda, Docker, optional DynamoDB checkpoints).

---

## Quick start (local)

1. **Enter project**
   ```bash
   cd c:\ciffly_chatbot
   ```

2. **Create virtual env and install**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

3. **Configure env**
   - Copy `env.example` to `.env`
   - Set `OPENAI_API_KEY=sk-...` (or `ANTHROPIC_API_KEY`)

4. **Run a test**
   ```bash
   python run_local.py "I want to get a demo"
   ```

---

## Project layout

| File / folder       | Purpose |
|---------------------|--------|
| `agents.py`         | Support, QnA, Lead agents + supervisor router |
| `tools.py`          | Tools: support ticket, search ranker, lead capture |
| `chatbot_inference.py` | Graph build, `run_chat()`, optional DynamoDB checkpointer |
| `lambda_function.py`| AWS Lambda handler |
| `logger_utils.py`   | Logging to console + `logs/chatbot.log` |
| `Dockerfile`        | Container image for Lambda or ECS |
| `template.yaml`     | SAM template: Lambda + optional DynamoDB table |
| `env.example`       | Example env vars (copy to `.env`) |

---

## AWS deployment

```bash
sam build
sam deploy --guided
```

Set **OpenAIApiKey** when prompted. Use **UseCheckpointTable** = `true` for multi-turn state in DynamoDB.

---

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` | One required | LLM API key |
| `DYNAMODB_CHECKPOINT_TABLE` | No | Table name for checkpoints (multi-turn) |
| `LOG_LEVEL` | No | `INFO` (default) |
| `CORS_ORIGIN` | No | For Lambda response headers |
