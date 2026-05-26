import os

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException


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


@app.get("/test-gemini")
def test_gemini() -> dict[str, str]:
    outline_prompt = (
        "Create a short three-bullet outline explaining what a large language "
        "model is."
    )

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        outline_response = model.generate_content(outline_prompt)

        if not outline_response.text:
            raise ValueError("Gemini returned an empty outline.")

        outline = outline_response.text.strip()
        final_prompt = (
            "Use this outline to explain what a large language model is in one "
            f"clear paragraph:\n\n{outline}"
        )
        final_response = model.generate_content(final_prompt)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Gemini request failed. Check your API key and try again.",
        ) from exc

    if not final_response.text:
        raise HTTPException(
            status_code=502,
            detail="Gemini returned an empty response.",
        )

    return {"response": final_response.text}
