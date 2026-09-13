import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# FINGURU ENVIRONMENT
# ============================================================

# client.py
#   ↓
# app/llm/
#   ↓
# app/
#   ↓
# backend/
#
# Therefore parents[2] = backend/

BASE_DIR = Path(__file__).resolve().parents[2]

ENV_FILE = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_FILE,
    override=False,
)


# ============================================================
# CONFIGURATION
# ============================================================

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

FINGURU_LLM_MODEL = os.getenv(
    "FINGURU_LLM_MODEL",
    "gpt-5.6-luna",
)


# ============================================================
# DEBUG-SAFE CONFIGURATION CHECK
# ============================================================

def is_llm_configured() -> bool:
    """
    Return True when an OpenAI API key is available.

    Never expose the complete API key.
    """

    return bool(
        OPENAI_API_KEY
        and OPENAI_API_KEY.strip()
    )


# ============================================================
# OPENAI CLIENT
# ============================================================

def get_openai_client() -> OpenAI:
    """
    Create and return the OpenAI client.

    The API key is loaded from:
        backend/.env
    """

    if not is_llm_configured():
        raise RuntimeError(
            "OPENAI_API_KEY is not configured. "
            "Add it to the FinGuru backend/.env file."
        )

    return OpenAI(
        api_key=OPENAI_API_KEY.strip()
    )


# ============================================================
# LLM GENERATION
# ============================================================

def generate_llm_response(
    prompt: str,
    model: Optional[str] = None,
) -> str:
    """
    Send a prompt to the OpenAI Responses API
    and return the generated text.
    """

    if not prompt or not prompt.strip():
        raise ValueError(
            "LLM prompt cannot be empty."
        )

    client = get_openai_client()

    selected_model = (
        model or FINGURU_LLM_MODEL
    )

    try:

        response = client.responses.create(
            model=selected_model,
            input=prompt,
        )

    except Exception as exc:

        raise RuntimeError(
            f"OpenAI LLM generation failed: {exc}"
        ) from exc

    answer = getattr(
        response,
        "output_text",
        None,
    )

    if not answer:
        raise RuntimeError(
            "OpenAI returned an empty response."
        )

    return answer.strip()