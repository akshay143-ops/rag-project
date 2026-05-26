import os

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")

genai.configure(api_key=gemini_api_key)

app = FastAPI(title="RAG Project")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "RAG Project API is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/gemini-status")
def gemini_status() -> dict[str, str]:
    return {
        "status": "configured",
        "message": "Gemini API key loaded. Gemini calls are not implemented yet.",
    }
