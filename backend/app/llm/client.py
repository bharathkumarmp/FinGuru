import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FINGURU_LLM_MODEL = os.getenv(
    "FINGURU_LLM_MODEL",
    "gpt-5.6-luna",
)


def get_openai_client() -> OpenAI:
    """
    Create the OpenAI client.

    The API key is loaded from the environment.
    """

    if not OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured. "
            "Add it to the FinGuru .env file."
        )

    return OpenAI(
        api_key=OPENAI_API_KEY
    )


def generate_llm_response(
    prompt: str,
    model: Optional[str] = None,
) -> str:
    """
    Send a prompt to the LLM and return the generated response.
    """

    client = get_openai_client()

    selected_model = model or FINGURU_LLM_MODEL

    response = client.responses.create(
        model=selected_model,
        input=prompt,
    )

    return response.output_text.strip()