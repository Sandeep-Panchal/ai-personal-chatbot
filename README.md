# AI Personal ChatBot

A **ChatGPT-like AI Personal Assistant** built from scratch as a long-term learning project.

The objective of this project is not simply to build another chatbot, but to understand the engineering principles behind modern AI assistants. The project is developed incrementally, with each phase introducing new concepts in software architecture, memory management, and AI system design.

---

# Learning Objectives

This project focuses on learning and implementing:

* Software Architecture
* AI System Design
* Conversation Management
* Memory Management
* Database Design
* Context Engineering
* Retrieval-Augmented Generation (RAG)
* Long-Term Memory
* Agentic Workflows
* Scalable AI Application Design

The emphasis is on understanding **why** a design exists before implementing **how** it works.

---

# End Goal

Build a personal AI assistant capable of:

* Managing multiple chat conversations
* Remembering information across sessions
* Maintaining long-term memory
* Retrieving relevant context automatically
* Answering questions from uploaded documents
* Supporting agentic workflows
* Following production-quality software engineering practices

---

# Current Features

* Interactive chat interface using Streamlit
* Local LLM integration with Ollama
* Streaming AI responses
* Multiple chat sessions
* Session isolation
* In-memory conversation history
* Modular and layered project architecture

---

# Technology Stack

| Category       | Technology |
| -------------- | ---------- |
| Language       | Python     |
| User Interface | Streamlit  |
| LLM Runtime    | Ollama     |

---

# Repository Structure

```text
AI-Personal-ChatBot/
│
├── app/                # Application source code
├── docs/               # Project documentation
├── pyproject.toml      # Project configuration and dependencies
├── uv.lock             # Locked dependency versions
└── README.md
```

---

# Prerequisites

Before running the project, ensure the following are installed:

* Python 3.12 or later
* uv
* Ollama
* A supported Ollama model (configured in the application)

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd AI-Personal-ChatBot
```
Set up the project environment and install dependencies:

```bash
uv sync
```
---

# Running the Application

Ensure that:

- Ollama is installed and running.
- The configured model has been downloaded.

Start the application:

From the project root directory, run:

```bash
uv run python -m streamlit run app/ui/streamlit_app.py
```

Open the URL displayed by Streamlit in your browser.

---

# Project Status

**Current Phase**

✅ **Phase 1 — Foundation**

This phase establishes the foundational architecture, including conversation flow, session management, and in-memory conversation history.

---

# Documentation

| Document               | Purpose                            |
| ---------------------- | ---------------------------------- |
| `README.md`            | Project overview and setup guide   |
| `docs/CHANGELOG.md`    | Release history                    |
| `docs/roadmap.md`      | Current development roadmap        |
| `docs/architecture.md` | Current system architecture        |
| `docs/phases/`         | Documentation for completed phases |

---

# Development Philosophy

This project follows a few guiding principles:

* Learn by building
* Simplicity before complexity
* Incremental development
* Clear separation of concerns
* Modular architecture
* Document important design decisions
* Complete one phase before starting the next

Each phase represents a stable milestone before moving on to additional functionality.

---

# Contributing

This repository is currently maintained as a personal learning project. Contributions are not planned at this stage.

---

# License

License information will be added in a future release.