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

## Week 5 Gemini Test Endpoint

This week adds a simple Gemini API test endpoint without adding RAG logic yet.

### What `/test-gemini` Does

The `/test-gemini` endpoint sends a hardcoded prompt to Gemini:

`Explain what a large language model is in one paragraph.`

It returns the prompt and Gemini-generated response as JSON. The endpoint does not accept user input, upload documents, chunk text, create embeddings, or retrieve context.

### Where the Gemini Call Lives

The Gemini API call lives inside the `test_gemini()` function in `rag_app.py`. That function creates a `gemini-1.5-flash` model with the `google-generativeai` SDK and calls `generate_content()`.

### What I Learned

The Gemini Python documentation shows that the backend should create a model object, call `generate_content()` with a prompt, and read the generated text from the response. Keeping this logic in the backend protects the API key and gives the server control over prompts, costs, and error handling.

### Questions and Uncertainties

- Which Gemini model should be used long term for this project?
- How should errors from Gemini be logged without exposing sensitive information?
- What limits should be added later to control usage and cost?


## Git Commands Used So Far

- git clone  
- git status  
- git add  
- git commit  
- git push
