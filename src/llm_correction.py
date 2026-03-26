import os
from dataclasses import dataclass
from typing import Protocol, Dict, Any, Optional


class LLMClient(Protocol):
    def correct(self, text: str) -> str:
        ...


@dataclass
class DummyLLMClient:
    """
    Simple placeholder that just returns the input.
    Replace with real OpenAI/Anthropic/Mistral clients.
    """
    name: str = "dummy"

    def correct(self, text: str) -> str:
        # You can add simple heuristics here if you want.
        return text


def get_llm_client(provider: str = "dummy") -> LLMClient:
    provider = provider.lower()
    if provider == "dummy":
        return DummyLLMClient()

    # Example stubs for future expansion
    if provider == "openai":
        raise NotImplementedError("OpenAI client not wired yet.")
    if provider == "anthropic":
        raise NotImplementedError("Anthropic client not wired yet.")
    if provider == "mistral":
        raise NotImplementedError("Mistral client not wired yet.")

    raise ValueError(f"Unknown provider: {provider}")


def build_prompt(raw_name: str) -> str:
    return (
        "You are an expert in chemical nomenclature. "
        "Given a possibly noisy OCR string, return a single corrected IUPAC-like name.\n\n"
        f"Input: {raw_name}\n"
        "Output (just the corrected name, no explanation):"
    )


def correct_text(
    raw_text: str,
    provider: str = "dummy",
    extra_config: Optional[Dict[str, Any]] = None,
) -> str:
    """
    High-level correction entrypoint.
    """
    client = get_llm_client(provider)
    prompt = build_prompt(raw_text)

    # For real LLMs, you'd send `prompt` and parse the response.
    # Here we just call the dummy client.
    corrected = client.correct(prompt)

    # In a real implementation, you'd strip the prompt and keep only the model's answer.
    return corrected
