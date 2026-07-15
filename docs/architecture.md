# Current System Architecture

This document describes the **current** architecture of the application.

---

## High-Level Flow

```
User
   │
   ▼
Streamlit UI
   │
   ▼
ChatService
   │
   ├──────────────► MemoryManager
   │                     │
   │                     ▼
   │              Conversation History
   │
   ▼
OllamaClient
   │
   ▼
Local LLM
   │
   ▼
Streaming Response
   │
   ▼
MemoryManager
   │
   ▼
Streamlit UI
```

---

## Components

### Streamlit UI

Responsible for:

- User interaction
- Displaying chat history
- Streaming model responses

---

### ChatService

Acts as the orchestration layer.

Responsibilities:

- Receive user messages
- Retrieve conversation history
- Send requests to the LLM
- Store AI responses

---

### MemoryManager

Responsible for:

- Managing chat sessions
- Storing conversation history
- Retrieving messages for a session

Current implementation uses in-memory Python data structures.

---

### OllamaClient

Responsible for:

- Communicating with the local Ollama server
- Streaming model responses
- Abstracting LLM interaction from business logic

---

## Current Limitations

- Memory is not persistent.
- Conversation history is lost after restart.
- No semantic retrieval.
- No long-term memory.