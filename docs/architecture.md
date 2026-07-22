# Current System Architecture

This document describes the **current** architecture of the application.

---

# High-Level Flow

```text
User
   │
   ▼
Streamlit UI
   │
   ▼
ChatService
   │
   ▼
MemoryManager
   │
   ├─────────────────────────────┐
   ▼                             ▼
SessionRepository         MessageRepository
   │                             │
   └──────────────┬──────────────┘
                  ▼
               SQLite
                  │
                  ▼
            Conversation Data
                  │
                  ▼
             MemoryManager
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
          MessageRepository
                  │
                  ▼
                SQLite
                  │
                  ▼
            Streamlit UI
```

---

# Components

## Streamlit UI

Responsible for:

* User interaction
* Managing chat sessions
* Displaying conversation history
* Streaming AI responses

---

## ChatService

Acts as the orchestration layer of the application.

Responsibilities:

* Receive user messages
* Coordinate conversation flow
* Retrieve conversation history
* Format messages for the LLM
* Stream responses from the LLM
* Generate conversation titles
* Delegate persistence to the MemoryManager

---

## MemoryManager

Acts as the application's memory abstraction layer.

Responsibilities:

* Create and manage chat sessions
* Store user and assistant messages
* Retrieve conversation history
* Update conversation metadata
* Coordinate communication with the repository layer

The MemoryManager contains business logic and is independent of the underlying database implementation.

---

## Repository Layer

Responsible for all database operations.

### SessionRepository

Responsibilities:

* Create sessions
* Retrieve sessions
* Update session information

### MessageRepository

Responsibilities:

* Store messages
* Retrieve conversation history
* Retrieve messages for a specific session

Repositories isolate database access from the business logic.

---

## SQLite Database

Responsible for persistent storage.

Current schema:

### Sessions

* Session ID
* Conversation title
* Created timestamp
* Updated timestamp

### Messages

* Message ID
* Session ID
* Role (User / Assistant / System)
* Message content
* Created timestamp

Conversation history is now preserved across application restarts.

---

## OllamaClient

Responsible for:

* Communicating with the local Ollama server
* Streaming model responses
* Abstracting LLM interaction from business logic

---

# Current Architecture

```
User
   │
   ▼
Streamlit UI
   │
   ▼
ChatService
   │
   ▼
MemoryManager
   │
   ▼
Repositories
   │
   ▼
SQLite
   │
   ▼
OllamaClient
   │
   ▼
Local LLM
```

---

# Current Limitations

The application currently sends the **entire conversation history** to the LLM for every request.

As conversations grow:

* Token usage increases.
* Response latency increases.
* Context windows become limited.

The current implementation does not yet support:

* Conversation summarization
* Context compression
* Episodic memory
* Semantic memory
* Procedural memory
* Long-term memory
* Semantic retrieval
* Vector database integration

These capabilities are planned for **Phase 3 — Memory Management**.