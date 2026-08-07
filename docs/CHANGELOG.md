# Changelog

All notable changes to this project will be documented in this file.

---

# v0.3.0 — Phase 3 - Conversation Summary

## Added

- Rolling conversation summarization
- SummaryAgent for LLM-based conversation summarization
- SummaryMemory for summary orchestration
- SummaryRepository for persistent summary storage
- Summary database schema
- Summary versioning
- Configurable summarization thresholds
- Conversation range retrieval for incremental summarization

## Architecture

- Introduced dedicated SummaryMemory component
- Introduced dedicated SummaryAgent
- Separated summarization business logic from LLM interaction
- Extended repository layer with SummaryRepository
- Added persistent conversation summaries

## Improvements

- Reduced future prompt growth through rolling summaries
- Established the foundation for context compression
- Prepared the architecture for future Context Builder and long-term memory

## Known Limitations

- Conversation summaries are generated but not yet used to build LLM prompts
- No Context Builder
- No Semantic Memory
- No Episodic Memory
- No Procedural Memory
- No Long-Term Memory Retrieval
- No Retrieval-Augmented Generation (RAG)
- No Tool Calling

---

# v0.2.0 — Phase 2 - Persistent Conversation Memory

## Added

- SQLite database integration
- Persistent chat sessions
- Persistent conversation history
- Repository pattern for database access
- Database initialization and schema management
- Conversation title generation using LLM
- Session persistence across application restarts

## Architecture

- Separation of business logic and persistence layer
- Repository layer for database operations
- Database models for sessions and messages
- SQLite-backed conversation management
- Improved project structure for future memory modules

## Improvements

- Replaced in-memory conversation storage with SQLite persistence
- Added conversation title generation for better chat organization

## Known Limitations

- No conversation summarization
- No long-term memory
- No semantic memory
- No context builder

---

# v0.1.0 — Phase 1 - Foundation

## Added

- Initial project structure
- Streamlit chat interface
- Ollama integration
- Streaming LLM responses
- SessionManager
- MemoryManager
- ChatService
- Configuration module
- Multiple chat session support
- In-memory conversation storage

## Architecture

- Layered project structure
- Separation of UI and business logic
- Dedicated memory management
- Dedicated session management
- LLM abstraction layer

## Known Limitations

- Conversations are stored only in memory
- Data is lost when the application stops
- No persistent storage
- No conversation search
- No memory summarization