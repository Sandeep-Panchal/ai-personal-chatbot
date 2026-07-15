# Changelog

All notable changes to this project will be documented in this file.

---

# v0.1.0 — Phase - 1 - Foundation

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