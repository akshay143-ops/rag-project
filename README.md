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

## Week 6 Multi-Step Gemini Flow

This week updates `/test-gemini` so it uses a simple multi-step AI flow instead of a single prompt.

### Flow Description

Step 1 asks Gemini to create a short three-bullet outline explaining what a large language model is. The app stores that outline as an intermediate value inside `test_gemini()`.

Step 2 builds a second prompt using the outline from Step 1. Gemini then expands the outline into one clear paragraph, and the endpoint returns only this final response to the client.

### Why the Steps Are Separated

The outline step gives the model a simple planning task before writing the final answer. The expansion step depends on that outline, which makes the final response easier to control and shows how later AI calls can reuse earlier outputs.

### Challenges and Open Questions

- The endpoint still requires a real Gemini API key in `.env`; the placeholder value will cause the Gemini request to fail safely.
- Later versions may need logging for intermediate outputs, but logs should avoid secrets and sensitive data.
- It is still unclear how much intermediate reasoning should be returned to users in future RAG endpoints.


## Git Commands Used So Far

- git clone  
- git status  
- git add  
- git commit  
- git push
