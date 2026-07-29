# RAG Learning App

A Retrieval-Augmented Generation (RAG) application built with Python, ChromaDB, SentenceTransformers, and Google Gemini. You'll build this incrementally over Weeks 10–15.

## What This App Does

You can ask this app questions about Python, machine learning, databases, APIs, and AI concepts. It finds the most relevant documents from its knowledge base and sends them to Gemini as context — so the answers are grounded in real information rather than guesswork.

## System Architecture

![RAG App Architecture Diagram](docs/rag-app-architecture-diagram.svg)

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the full architecture explanation and editable Excalidraw source.

```
User Query
    │
    ▼
[security.py]      ← Validate and sanitize input (Week 12)
    │
    ▼
[workflow.py]      ← Rewrite query for better retrieval (Week 15)
    │
    ▼
[embeddings.py]    ← Convert query to a vector
    │
    ▼
[vector_store.py]  ← Find similar document vectors in ChromaDB
    │
    ▼
[filters.py]       ← Remove irrelevant results (Week 14)
    │
    ▼
[rag_pipeline.py]  ← Build prompt with retrieved context
    │
    ▼
  Gemini API       ← Generate answer
    │
    ▼
[monitoring.py]    ← Check for hallucinations (Week 13)
    │
    ▼
[app.py]           ← Display answer, sources, confidence
```

## Setup

### 1. Clone the repository
```bash
git clone <repo-url>
cd student-rag-project
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

Activate it:
- **Mac/Linux:** `source venv/bin/activate`
- **Windows:** `venv\Scripts\activate`

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your Gemini API key

Copy the example environment file:
```bash
cp .env.example .env
```

Open `.env` and replace `your-gemini-api-key-here` with your actual key.
Get a free key at: https://aistudio.google.com/apikey

### 5. Run the app
```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

---

## File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Streamlit web interface |
| `config.py` | Configuration constants |
| `embeddings.py` | Convert text to vector embeddings |
| `vector_store.py` | Store and search vectors with ChromaDB |
| `data_loader.py` | Sample tech documents |
| `rag_pipeline.py` | Central orchestration — ties everything together |
| `conversation.py` | Conversation history (Week 11) |
| `security.py` | Input validation and security (Week 12) |
| `monitoring.py` | Hallucination detection (Week 13) |
| `filters.py` | Similarity filtering and fallbacks (Week 14) |
| `workflow.py` | Query rewriting and multi-hop retrieval (Week 15) |
| `compliance.py` | Metadata tagging and sensitive data redaction (Week 18) |

---

## Compliance and Sensitive Data Handling

This project is a learning app, but it models compliance-aware patterns used in commercial AI systems. The most relevant trust principles are:

- **Security:** user input is validated before retrieval or model calls, and secrets such as `.env` are excluded from Git.
- **Confidentiality:** potentially sensitive values are tagged and redacted before they are displayed, stored in session history, or sent to the model.
- **Privacy:** personal identifiers such as emails, phone numbers, SSNs, and credit-card-like values are treated as sensitive and masked.

Sensitive data could appear in user questions, model responses, future uploaded/internal documents, retrieved context, error messages, and any debug or analytics output. The current sample documents are public learning content, but document metadata is still generated so downstream controls can use the same structure for public and sensitive sources.

The metadata tagging scheme is:

- `sensitivity`: `public`, `confidential`, or `restricted`
- `data_type`: `operational`, `email`, `phone`, `ssn`, or `credit_card`
- `source`: `user_input`, `document`, or `model_output`
- `contains_sensitive_data`: `true` or `false`

Redaction occurs in `compliance.py` and is applied at key boundaries:

- User input is redacted before display in the Streamlit chat.
- User input is redacted before query rewriting, retrieval, and model prompts.
- Source documents are tagged during ingestion and stored with ChromaDB metadata.
- Retrieved metadata is carried through the pipeline with the response.
- Model output and API error messages are redacted before being returned to the UI.
- Conversation history stores redacted user and assistant messages.

This approach is intentionally simple. It uses regex-based detection, so it will not catch every form of sensitive data and may occasionally redact harmless text. It is not a certification of compliance, but it demonstrates safe defaults that reduce exposure risk and support audit-friendly metadata.

---

## Testing and CI

This project uses `pytest` for automated tests. The tests focus on deterministic, safety-critical helpers that do not call Gemini or depend on a live vector database.

Current tests cover:

- Sensitive data redaction for email addresses and phone numbers
- Metadata tagging for restricted user input such as SSNs
- Public text detection with no sensitive data
- Prompt-injection blocking in `validate_input()`
- Empty and overly long query rejection
- Input sanitization behavior

These tests matter because redaction, metadata tagging, and input validation are safety boundaries. If those helpers break, the app could leak private data or process unsafe prompts.

Intentionally not tested in unit tests:

- Live Gemini API calls
- Streamlit UI rendering
- SentenceTransformer embedding quality
- ChromaDB retrieval ranking

Run tests locally with:

```bash
pytest
```

GitHub Actions runs the same test suite on every push and pull request using `.github/workflows/tests.yml`.

---

## Weekly Progress

Update this checklist as you complete each week's assignment.

- [ ] Week 10 — Ran the starter app and explored the codebase
- [x] Week 11 — Implemented conversation context
- [x] Week 12 — Implemented input security
- [x] Week 13 — Implemented hallucination monitoring
- [x] Week 14 — Implemented filtering and fallbacks
- [x] Week 15 — Implemented multi-step AI workflows

---

---
## Assignment: Week 10 — Run the Starter App

**Learning objective:** Understand how a basic RAG pipeline works end-to-end.

### Background

RAG (Retrieval-Augmented Generation) connects a vector database to an LLM. Instead of asking the LLM to answer from memory (which leads to hallucination), we first *retrieve* relevant documents from our knowledge base, then *augment* the LLM's prompt with those documents so it can generate a *grounded* answer.

This week, everything is already built. Your job is to run it, understand how the pieces fit together, and answer the reflection questions below.

### What to do

1. Follow the Setup instructions above and get the app running
2. Ask the app at least 3 questions — try both on-topic and off-topic questions
3. Read through these four files and make sure you understand what each one does:
   - `data_loader.py` — where does the knowledge base come from?
   - `embeddings.py` — what does `embed_text()` return, and why?
   - `vector_store.py` — what does ChromaDB store, and how does `query_similar()` work?
   - `rag_pipeline.py` — trace a question from `run_rag()` all the way to a returned answer

### Reflection questions (be ready to discuss in class)

- What would happen if you asked a question that no document in the knowledge base covers?
- Why do we store vector embeddings instead of just the original text?
- What is the difference between keyword search and semantic search?

### ✅ When done
Check off **Week 10** in the Weekly Progress section above, then delete this entire Week 10 assignment section (from `## Assignment: Week 10` down to the next `---`).

---

