import json

import ollama


MODEL_NAME = "gemma3:1b"


class AIEngineError(Exception):
    """Raised when AI processing fails."""


def generate_response(
    prompt: str,
    response_format: dict | str | None = None,
) -> str:
    """Generate a response using the local Ollama model."""

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    try:
        options = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are EduGram, an educational AI assistant. "
                        "Follow the user's instructions carefully. "
                        "Use accurate, student-friendly language."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        }

        if response_format is not None:
            options["format"] = response_format

        response = ollama.chat(**options)
        content = response["message"]["content"]

        if not isinstance(content, str) or not content.strip():
            raise AIEngineError("The AI returned an empty response.")

        return content.strip()

    except AIEngineError:
        raise
    except Exception as exc:
        raise AIEngineError(
            "Could not generate an AI response. "
            "Check that Ollama is running and the model is available."
        ) from exc