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
SessionMemory
   │
   ▼
SessionRepository
   │
   ▼
SQLite
   │
   ▲
MessageMemory
   │
   ▼
MessageRepository
   │
   ▼
SQLite
   │
   ▼
Conversation History
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
MessageMemory
   │
   ▼
MessageRepository
   │
   ▼
SQLite
   │
   ▼
SummaryMemory
   │
   ▼
SummaryAgent
   │
   ▼
OllamaClient
   │
   ▼
Local LLM
   │
   ▼
SummaryRepository
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

- User interaction
- Managing chat sessions
- Displaying conversation history
- Streaming AI responses

---

## ChatService

Acts as the orchestration layer of the application.

Responsibilities:

- Receive user messages
- Coordinate conversation flow
- Store user messages
- Retrieve conversation history
- Format messages for the LLM
- Stream AI responses
- Store assistant responses
- Trigger conversation summarization
- Generate conversation titles

The ChatService contains no database logic.

---

# Memory Layer

The memory layer manages all conversation-related data.

It is divided into specialized components.

---

## SessionMemory

Responsibilities:

- Create chat sessions
- Retrieve sessions
- Update session metadata
- Update conversation titles

---

## MessageMemory

Responsibilities:

- Store user messages
- Store assistant messages
- Retrieve complete conversation history
- Retrieve message ranges for summarization
- Retrieve recent conversation messages

---

## SummaryMemory

Responsibilities:

- Determine when conversation summarization should occur
- Retrieve the latest conversation summary
- Retrieve conversation segments
- Coordinate summary generation
- Persist updated summaries

SummaryMemory contains business logic but no prompt engineering.

---

## SummaryAgent

Responsible for:

- Formatting conversation history
- Building summarization prompts
- Calling the LLM
- Returning an updated conversation summary

The SummaryAgent is responsible only for LLM interaction and contains no database logic.

---

# Repository Layer

Repositories isolate database access from business logic.

## SessionRepository

Responsibilities:

- Create sessions
- Retrieve sessions
- Update session information

---

## MessageRepository

Responsibilities:

- Store messages
- Retrieve conversation history
- Retrieve recent messages
- Retrieve message ranges
- Count conversation messages

---

## SummaryRepository

Responsibilities:

- Store conversation summaries
- Retrieve the latest conversation summary

---

# SQLite Database

Responsible for persistent storage.

Current schema consists of three tables.

## Sessions

- Session ID
- Conversation title
- Created timestamp
- Updated timestamp

---

## Messages

- Message ID
- Session ID
- Role (User / Assistant / System)
- Message content
- Created timestamp

---

## Summary

- Summary ID
- Session ID
- Summary Version
- Conversation summary
- Covers until message number
- Created timestamp

Conversation history and conversation summaries are preserved across application restarts.

---

## OllamaClient

Responsible for:

- Communicating with the local Ollama server
- Streaming model responses
- Generating conversation summaries
- Abstracting LLM interaction from the application

---

# Current Architecture

```text
                 User
                   │
                   ▼
             Streamlit UI
                   │
                   ▼
              ChatService
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
 SessionMemory          MessageMemory
        │                     │
        ▼                     ▼
SessionRepository     MessageRepository
        │                     │
        └──────────┬──────────┘
                   ▼
                SQLite
                   │
                   ▼
            Conversation History
                   │
                   ▼
              OllamaClient
                   │
                   ▼
               Local LLM
                   │
                   ▼
           Assistant Response
                   │
                   ▼
             SummaryMemory
                   │
                   ▼
             SummaryAgent
                   │
                   ▼
              OllamaClient
                   │
                   ▼
               Local LLM
                   │
                   ▼
           SummaryRepository
                   │
                   ▼
                SQLite
```

---

# Current Limitations

The application now supports **rolling conversation summarization** to reduce prompt growth.

The memory system is still under development.

The current implementation does not yet support:

- Context builder
- Semantic memory
- Episodic memory
- Procedural memory
- Long-term memory retrieval
- Memory ranking
- Retrieval-Augmented Generation (RAG)
- Vector database integration
- Agentic workflows

These capabilities are planned for the subsequent phases.