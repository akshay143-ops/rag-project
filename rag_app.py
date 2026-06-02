import os

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")

genai.configure(api_key=gemini_api_key)

app = FastAPI(title="RAG Project")


class QueryRequest(BaseModel):
    question: str


def validate_user_input(text: str) -> None:
    if text is None or text.strip() == "":
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if len(text) < 5:
        raise HTTPException(status_code=400, detail="Question is too short")

    if len(text) > 500:
        raise HTTPException(status_code=400, detail="Question is too long")


def validate_model_output(text: str) -> None:
    if text is None or text.strip() == "":
        raise HTTPException(status_code=500, detail="AI returned an empty response")

    if len(text) < 10:
        raise HTTPException(status_code=500, detail="AI response is too short")


def review_model_output(original_answer: str) -> str:
    review_prompt = f"""
You are reviewing an AI-generated response.

Your job:
- If the response is unclear, incomplete, or poorly written, improve it.
- If the response is already good, return it unchanged.

AI response to review:
{original_answer}
"""

    review_model = genai.GenerativeModel("gemini-pro")
    review_response = review_model.generate_content(review_prompt)

    return review_response.text


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


@app.post("/query")
def query_ai(request: QueryRequest) -> dict[str, str]:
    validate_user_input(request.question)

    try:
        primary_model = genai.GenerativeModel("gemini-pro")
        primary_response = primary_model.generate_content(request.question)
        raw_answer = primary_response.text

        validate_model_output(raw_answer)

        reviewed_answer = review_model_output(raw_answer)
        validate_model_output(reviewed_answer)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="AI request failed. Check your API key and try again.",
        ) from exc

    return {"question": request.question, "answer": reviewed_answer}
