# 🧪 Ciffly Chatbot - Testing Guide

This guide shows you **3 different ways** to test your chatbot!

---

## 📋 **Quick Overview**

| Method | Best For | Difficulty |
|--------|----------|------------|
| **1. Command Line** | Quick one-off tests | ⭐ Easy |
| **2. Interactive CLI** | Terminal-based conversations | ⭐ Easy |
| **3. REST API (curl)** | API testing, automation | ⭐⭐ Medium |
| **4. Web UI** | Visual testing, demos | ⭐ Easy |

---

## 1️⃣ **Command Line (One-off Messages)**

### Usage:
```powershell
.venv\Scripts\python.exe run_local.py "Your message here"
```

### Examples:
```powershell
# Test Lead Agent
.venv\Scripts\python.exe run_local.py "I want to schedule a demo"

# Test QnA Agent
.venv\Scripts\python.exe run_local.py "What features do you offer?"

# Test Support Agent
.venv\Scripts\python.exe run_local.py "I'm having login issues"
```

**Pros:** ✅ Quick and simple  
**Cons:** ❌ No conversation history

---

## 2️⃣ **Interactive CLI (Terminal Chat)**

### Usage:
```powershell
.venv\Scripts\python.exe chat_interactive.py
```

### Features:
- ✅ Continuous conversation
- ✅ Maintains conversation history
- ✅ Type 'quit' or 'exit' to stop
- ✅ Press Ctrl+C to exit

### Example Session:
```
🤖 Ciffly Chatbot - Interactive Mode
============================================================
Type your message and press Enter to chat.
Type 'quit', 'exit', or press Ctrl+C to stop.

You: I want a demo
🤖 Bot: Great! I can help you with that. I'll just need a few details...

You: My name is John Doe
🤖 Bot: Thanks John! What's your email address?

You: quit
👋 Goodbye! Thanks for chatting!
```

**Pros:** ✅ Natural conversation flow, maintains context  
**Cons:** ❌ Terminal-only interface

---

## 3️⃣ **REST API (curl / Postman)**

### Step 1: Start the API Server
```powershell
.venv\Scripts\python.exe api_server.py
```

The server will start at: `http://localhost:5000`

### Step 2: Test with curl

#### Health Check:
```powershell
curl http://localhost:5000/health
```

#### Send a Message:
```powershell
curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d "{\"message\": \"I want a demo\"}"
```

#### With Thread ID (for conversation history):
```powershell
curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d "{\"message\": \"My name is John\", \"thread_id\": \"session-123\"}"
```

### API Response Format:
```json
{
  "response": "Great! I can help you with that...",
  "thread_id": "session-123",
  "status": "success"
}
```

### Test with Postman:
1. Open Postman
2. Create new POST request to `http://localhost:5000/chat`
3. Set Headers: `Content-Type: application/json`
4. Body (raw JSON):
   ```json
   {
     "message": "I want a demo",
     "thread_id": "my-session"
   }
   ```
5. Click Send

**Pros:** ✅ Perfect for integration testing, automation  
**Cons:** ❌ Requires API server running

---

## 4️⃣ **Web UI (Browser Interface)** ⭐ RECOMMENDED

### Step 1: Start the API Server
```powershell
.venv\Scripts\python.exe api_server.py
```

### Step 2: Open the Web UI
Open `chat_ui.html` in your browser:
- **Option A:** Double-click the file
- **Option B:** Right-click → Open with → Chrome/Edge/Firefox
- **Option C:** Drag and drop into browser

### Features:
- ✅ Beautiful gradient design
- ✅ Real-time chat interface
- ✅ Typing indicators
- ✅ Smooth animations
- ✅ Conversation history
- ✅ Error handling
- ✅ Mobile responsive

### Screenshot:
```
┌─────────────────────────────────────┐
│   🤖 Ciffly Chatbot                 │
│   Ask me anything! I can help...    │
├─────────────────────────────────────┤
│                                     │
│  👋 Hello! I'm your Ciffly...       │
│                                     │
│              I want a demo     [You]│
│                                     │
│  Great! I can help you...      [Bot]│
│                                     │
├─────────────────────────────────────┤
│ [Type your message here...] [Send] │
└─────────────────────────────────────┘
```

**Pros:** ✅ Best user experience, visual, easy to demo  
**Cons:** ❌ Requires API server running

---

## 🎯 **Recommended Testing Flow**

### For Development:
1. Use **Interactive CLI** for quick testing
2. Use **Command Line** for specific test cases

### For Demos:
1. Start **API Server**
2. Open **Web UI** in browser
3. Show off the beautiful interface!

### For Integration:
1. Start **API Server**
2. Test with **curl** or **Postman**
3. Integrate with your frontend/backend

---

## 🐛 **Troubleshooting**

### Issue: "Connection refused" in Web UI
**Solution:** Make sure the API server is running:
```powershell
.venv\Scripts\python.exe api_server.py
```

### Issue: "CORS error" in browser
**Solution:** The API server has CORS enabled. Make sure you're accessing the HTML file via `file://` protocol or use a local web server.

### Issue: "Module not found"
**Solution:** Make sure you're using the virtual environment:
```powershell
.venv\Scripts\python.exe <script_name>.py
```

---

## 📊 **Test Scenarios**

### Test All Three Agents:

#### Lead Capture Agent:
```
"I want to schedule a demo"
"I'd like to sign up"
"Can I get more information?"
```

#### QnA Agent:
```
"What features do you offer?"
"How does this work?"
"Tell me about your product"
```

#### Support Agent:
```
"I'm having login issues"
"I need help with my account"
"Something is broken"
```

---

## 🚀 **Next Steps**

1. **Try all 4 methods** to see which you prefer
2. **Test all three agents** (Lead, QnA, Support)
3. **Customize the UI** (edit `chat_ui.html`)
4. **Integrate with your app** using the REST API

---

**Happy Testing! 🎉**
