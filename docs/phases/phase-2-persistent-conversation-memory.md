# Phase 2 — Persistent Conversation Memory

## Objective

The objective of Phase 2 was to replace the temporary in-memory conversation storage introduced in Phase 1 with a persistent storage layer using SQLite.

This phase focuses on learning how modern applications persist conversations while maintaining a clean and scalable software architecture.

---

# Goals

* Persist chat sessions across application restarts
* Persist conversation history
* Separate business logic from persistence logic
* Introduce a relational database
* Learn repository-based architecture
* Prepare the project for future memory management features

---

# Features Implemented

## Database

* SQLite integration
* Database connection manager
* Database initialization
* Automatic schema creation

### Tables

#### Sessions

Stores information about each conversation.

Fields:

* Session ID
* Conversation title
* Created timestamp
* Updated timestamp

#### Messages

Stores every message exchanged during a conversation.

Fields:

* Message ID
* Session ID
* Role
* Message
* Created timestamp

---

## Repository Layer

Introduced a dedicated repository layer responsible for all database operations.

### SessionRepository

Responsibilities:

* Create sessions
* Retrieve sessions
* Update conversation titles
* Update timestamps

### MessageRepository

Responsibilities:

* Store messages
* Retrieve conversation history
* Retrieve messages for a session

The repository layer isolates SQLite from the rest of the application.

---

## Domain Models

Introduced dataclasses representing application entities.

### ChatSession

Represents a conversation session.

### ChatMessage

Represents an individual message exchanged between the user and the assistant.

Repositories return domain objects instead of raw database tuples.

---

## MemoryManager

Refactored to become the application's memory abstraction layer.

Responsibilities include:

* Creating sessions
* Managing conversation history
* Storing messages
* Retrieving messages
* Coordinating with repositories

The MemoryManager no longer owns data storage directly.

---

## ChatService

Updated to support persistent conversations.

Responsibilities:

* Receive user input
* Retrieve conversation history
* Format messages for the LLM
* Stream responses
* Store assistant responses
* Generate conversation titles

---

## Streamlit UI

Updated to support persistent conversations.

Features include:

* Display existing conversations
* Switch between conversations
* Create new conversations
* Load historical messages from SQLite

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

# Key Design Decisions

## Repository Pattern

Database operations are isolated inside repositories.

This keeps business logic independent of the persistence layer and makes future database migrations easier.

---

## Normalized Database Design

Conversation data is divided into two tables:

* Sessions
* Messages

Each message is stored as a separate row linked to its parent session.

---

## Domain Models

Repositories return dataclass objects instead of database tuples.

This improves readability, type safety, and separates database representation from application logic.

---

## SQLite

SQLite was selected because it provides:

* Relational database concepts
* SQL fundamentals
* Zero configuration
* Local development simplicity

The focus of this phase is learning persistence and architecture rather than distributed databases.

---

# What Was Learned

During this phase, the following concepts were explored:

* Relational database design
* Primary and foreign keys
* Database normalization
* Repository Pattern
* Layered architecture
* Connection management
* Dataclasses as domain models
* Separation of concerns
* Persistent conversation management

---

# Current Limitations

Although conversations are now persistent, the assistant still sends the **entire conversation history** to the LLM for every request.

As conversations grow:

* Token usage increases
* Response latency increases
* Context windows become limited

The application currently does not support:

* Conversation summarization
* Context compression
* Long-term memory
* Semantic memory
* Episodic memory
* Procedural memory
* Memory retrieval
* Vector databases

---

# Next Phase

## Phase 3 — Memory Management

The next phase introduces intelligent memory management.

Planned features include:

* Conversation summarization
* Context compression
* Long-term memory
* Episodic memory
* Semantic memory
* Procedural memory
* Context builder
* Intelligent prompt construction

This phase transforms the application from a persistent chatbot into a true AI personal assistant capable of managing information efficiently across long conversations.