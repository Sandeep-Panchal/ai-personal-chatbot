# Phase 3 — Conversation Summary

## Objective

The objective of this phase is to introduce intelligent memory management to overcome the limitations of sending the entire conversation history to the LLM for every request.

This phase implements **rolling conversation summarization**, allowing the application to compress older conversation while preserving the most recent messages for contextual continuity.

This lays the foundation for future long-term memory capabilities such as semantic memory, episodic memory, and context-aware retrieval.

---

# Goals

- Reduce prompt size as conversations grow
- Preserve important historical context
- Maintain recent conversational context
- Introduce rolling conversation summaries
- Separate memory orchestration from LLM summarization
- Build the foundation for long-term memory

---

# Features Implemented

## Conversation Summary

Implemented a rolling conversation summarization strategy.

The system periodically summarizes older conversation while preserving the most recent messages.

Example:

```text
Conversation

1 ... 8      → Summary Version 1

9 ... 16     → Summary Version 2
              (Summary 1 + Messages 9-16)

17 ... 24    → Summary Version 3
              (Summary 2 + Messages 17-24)
```

Only the latest summary is required for future summarization.

---

## Configurable Summary Strategy

The summarization behavior is configurable.

Current configuration:

- Step Threshold = 10 messages
- Keep Last Messages = 2 messages

During development, smaller thresholds are used to simplify testing.

In production this can be increased to larger values (for example 100/20).

---

## Rolling Summary Versioning

Each generated summary stores:

- Summary version
- Conversation summary
- Covers until message number
- Creation timestamp

Each new summary is generated using:

- Previous summary
- Newly completed conversation segment

This avoids repeatedly summarizing the entire conversation.

---

## SummaryAgent

Introduced a dedicated SummaryAgent responsible only for LLM-based summarization.

Responsibilities:

- Format conversation history
- Construct summarization prompts
- Invoke the LLM
- Return an updated conversation summary

The SummaryAgent contains no database logic.

---

## SummaryMemory

Introduced a dedicated SummaryMemory component.

Responsibilities:

- Determine when summarization should occur
- Retrieve the latest summary
- Retrieve conversation segments
- Coordinate summary generation
- Persist updated summaries

SummaryMemory contains business logic while delegating LLM interaction to the SummaryAgent.

---

## Summary Repository

Added a dedicated repository for conversation summaries.

Responsibilities:

- Store summaries
- Retrieve the latest summary

Database operations remain isolated from business logic.

---

## Database

Introduced a new Summary table.

### Summary

Fields:

- Summary ID
- Session ID
- Summary Version
- Conversation Summary
- Covers Until Message Number
- Created Timestamp

This table stores rolling summaries independently of conversation messages.

---

# Architecture

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

# Summary Generation Workflow

```text
Assistant Response Stored
           │
           ▼
Count Conversation Messages
           │
           ▼
Threshold Reached?
      │          │
     No         Yes
      │          │
      │          ▼
      │    Retrieve Latest Summary
      │          │
      │          ▼
      │    Retrieve Next Conversation Segment
      │          │
      │          ▼
      │      SummaryAgent
      │          │
      │          ▼
      │    Generate New Summary
      │          │
      │          ▼
      │      Store Summary
      │
      ▼
Continue Chat
```

---

# Key Design Decisions

## Rolling Summarization

Instead of repeatedly summarizing the entire conversation, each new summary is generated from:

- Previous summary
- Newly completed conversation segment

This keeps prompt size small while preserving important context.

---

## Dedicated SummaryAgent

Prompt engineering and LLM interaction are isolated inside the SummaryAgent.

Business logic remains inside SummaryMemory.

This separation improves maintainability and keeps responsibilities well defined.

---

## Dedicated SummaryMemory

Summary orchestration is separated from session and message management.

This allows future memory components to be added independently without affecting existing functionality.

---

## Repository Pattern

Summary persistence follows the same repository-based architecture introduced in Phase 2.

Repositories remain responsible only for database access.

---

# What Was Learned

During this phase, the following concepts were explored:

- Conversation summarization
- Rolling summaries
- Context compression
- Prompt engineering for summarization
- Memory orchestration
- Separation of business logic and LLM logic
- Incremental memory management
- Summary versioning

---

# Current Limitations

Although conversation summarization has been implemented, the memory subsystem is still under development.

The application does not yet support:

- Context builder
- Semantic memory
- Episodic memory
- Procedural memory
- Long-term memory retrieval
- Memory ranking
- Retrieval-Augmented Generation (RAG)
- Vector database integration

Currently, summaries are generated and stored, but they are **not yet incorporated into the prompt construction process**. The next milestone will focus on building context using the latest summary together with the most recent conversation messages.