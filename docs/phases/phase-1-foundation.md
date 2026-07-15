# Phase 1 — Foundation

**Version:** v0.1.0

---

# Objective

Build the minimum working AI chatbot capable of handling multiple chat sessions using in-memory storage.

The goal of this phase is to establish a clean and extensible architecture rather than implement advanced AI capabilities.

---

# Features

- Streamlit chat interface
- Ollama integration
- Streaming responses
- Multiple chat sessions
- Session isolation
- In-memory conversation history
- Modular project structure

---

# Architecture

```
Streamlit UI
      │
      ▼
ChatService
      │
 ┌────┴────┐
 ▼         ▼
Memory   OllamaClient
Manager
```

---

# Design Decisions

## Why use a dictionary for memory?

- Simple implementation
- Easy to debug
- Fast iteration
- Can be replaced later without affecting business logic

---

## Why separate MemoryManager?

To isolate storage logic from application logic.

This allows future storage implementations without modifying ChatService.

---

## Why create ChatService?

To centralize conversation orchestration and keep the UI independent of business logic.

---

## Why separate SessionManager?

Managing session lifecycle is a different responsibility from managing conversation history.

Separating these concerns keeps the codebase modular.

---

# Lessons Learned

- Layered architecture
- Separation of concerns
- Session management
- Generator-based streaming
- Maintaining conversation context
- Modular project organization

---

# Current Limitations

- No persistent storage
- Memory is lost after restart
- No conversation search
- No summarization
- No long-term memory

---

# Completion Summary

Phase 1 establishes the architectural foundation for future enhancements while intentionally keeping the implementation simple.