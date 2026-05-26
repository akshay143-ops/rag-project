# RAG Project

This repository contains my Retrieval-Augmented Generation (RAG) project for the GenAI Secure Coding course.

This project will be built incrementally each week.

## Week 3 Setup

This week sets up the starter backend structure for the RAG project.

### Project Files

- `rag_app.py`: Creates the FastAPI app, loads environment variables from `.env`, reads `GEMINI_API_KEY`, configures the Gemini client, and provides starter endpoints.
- `requirements.txt`: Lists the Python dependencies needed for the project.
- `.env`: Stores local environment variables such as the Gemini API key. This file should not be committed.
- `.gitignore`: Prevents secrets, virtual environments, cache files, and OS files from being pushed to GitHub.

### Starter App Notes

Environment variables are loaded with `python-dotenv` using `load_dotenv()`.
The Gemini API key is read from `GEMINI_API_KEY`.
If the key is missing, the app fails clearly with an error message.
The Gemini client is configured, but no Gemini or RAG logic has been implemented yet.

The FastAPI app currently includes:

- `/`: Confirms the API is running.
- `/health`: Returns a simple health status.
- `/gemini-status`: Confirms the Gemini key was loaded and explains that Gemini calls are not implemented yet.

### Questions and Uncertainties

- What document types will the RAG app support first?
- Which embedding model or vector database will be used later?
- How should user questions and retrieved context be validated before sending them to Gemini?


## Git Commands Used So Far

- git clone  
- git status  
- git add  
- git commit  
- git push
