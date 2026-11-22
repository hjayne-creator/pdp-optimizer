"""Multi-provider LLM helpers for OpenAI, Anthropic, and Google Gemini."""

from __future__ import annotations

from typing import Any

# Prices are USD per 1M tokens (standard / paid tier, short-context where applicable).
# Sources:
# - OpenAI: https://developers.openai.com/api/docs/pricing
# - Anthropic: https://platform.claude.com/docs/en/models/overview
# - Google: https://aistudio.google.com/docs/pricing
MODELS: dict[str, list[dict[str, Any]]] = {
    "OpenAI": [
        {
            "id": "gpt-6.1-sol",
            "label": "GPT-6.1 Sol",
            "input_per_mtok": 2.00,
            "output_per_mtok": 10.00,
            "notes": "Standard short-context (≤272K)",
        },
        {
            "id": "gpt-6.1-terra",
            "label": "GPT-6.1 Terra",
            "input_per_mtok": 1.00,
            "output_per_mtok": 5.00,
            "notes": "Standard short-context (≤272K)",
        },
        {
            "id": "gpt-6-luna",
            "label": "GPT-6 Luna",
            "input_per_mtok": 0.10,
            "output_per_mtok": 0.50,
            "notes": "Standard short-context (≤272K)",
        },
        {
            "id": "gpt-6-sol",
            "label": "GPT-6 Sol",
            "input_per_mtok": 2.00,
            "output_per_mtok": 10.00,
            "notes": "Standard short-context (≤272K)",
        },
        {
            "id": "gpt-5.6-terra",
            "label": "GPT-5.6 Terra",
            "input_per_mtok": 2.00,
            "output_per_mtok": 12.00,
            "notes": "Standard short-context (≤272K)",
        },
        {
            "id": "gpt-5.6-luna",
            "label": "GPT-5.6 Luna",
            "input_per_mtok": 0.20,
            "output_per_mtok": 1.20,
            "notes": "Standard short-context (≤272K)",
        },
    ],
    "Anthropic": [
        {
            "id": "claude-opus-5-5",
            "label": "Claude Opus 5.5",
            "input_per_mtok": 4.00,
            "output_per_mtok": 20.00,
            "notes": "Base token pricing",
        },
        {
            "id": "claude-sonnet-5-5",
            "label": "Claude Sonnet 5.5",
            "input_per_mtok": 2.00,
            "output_per_mtok": 10.00,
            "notes": "Base token pricing",
        },
        {
            "id": "claude-haiku-5-5",
            "label": "Claude Haiku 5.5",
            "input_per_mtok": 0.10,
            "output_per_mtok": 0.50,
            "notes": "From $0.10 / $0.50 per MTok (tiered)",
        },
    ],
    "Google": [
        {
            "id": "gemini-3.5-flash-lite",
            "label": "Gemini 3.5 Flash-Lite",
            "input_per_mtok": 0.30,
            "output_per_mtok": 2.50,
            "notes": "Paid tier (text/image/video/audio input)",
        },
        {
            "id": "gemini-3.8-flash",
            "label": "Gemini 3.8 Flash",
            "input_per_mtok": 0.75,
            "output_per_mtok": 3.75,
            "notes": "Promo through Dec 31, 2026; then $1.50 / $7.50",
        },
        {
            "id": "gemini-4-hydrogen",
            "label": "Gemini 4 Hydrogen",
            "input_per_mtok": 1.50,
            "output_per_mtok": 7.50,
            "notes": "Paid tier; output includes thinking tokens",
        },
    ],
}

PRICING_SOURCES = {
    "OpenAI": "https://developers.openai.com/api/docs/pricing",
    "Anthropic": "https://platform.claude.com/docs/en/models/overview",
    "Google": "https://aistudio.google.com/docs/pricing",
}

PROVIDER_KEY_MAP = {
    "OpenAI": "openai",
    "Anthropic": "anthropic",
    "Google": "google",
}


def model_options(provider: str) -> list[str]:
    return [m["id"] for m in MODELS.get(provider, [])]


def model_labels(provider: str) -> dict[str, str]:
    return {m["id"]: m["label"] for m in MODELS.get(provider, [])}


def get_model(provider: str, model_id: str) -> dict[str, Any] | None:
    for model in MODELS.get(provider, []):
        if model["id"] == model_id:
            return model
    return None


def format_model_option(provider: str, model_id: str) -> str:
    model = get_model(provider, model_id)
    if not model:
        return model_id
    return (
        f"{model['label']}  ·  "
        f"${model['input_per_mtok']:.2f} in / ${model['output_per_mtok']:.2f} out per 1M tok"
    )


def pricing_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for provider, models in MODELS.items():
        for model in models:
            rows.append(
                {
                    "Provider": provider,
                    "Model": model["label"],
                    "API ID": model["id"],
                    "Input $/1M": model["input_per_mtok"],
                    "Output $/1M": model["output_per_mtok"],
                    "Notes": model.get("notes", ""),
                }
            )
    return rows


def estimate_cost(
    *,
    provider: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
) -> float | None:
    """Estimate USD cost from token counts using catalog standard/paid rates."""
    info = get_model(provider, model)
    if not info:
        return None
    return (
        (input_tokens / 1_000_000) * float(info["input_per_mtok"])
        + (output_tokens / 1_000_000) * float(info["output_per_mtok"])
    )


def format_cost(cost: float | None) -> str:
    if cost is None:
        return "n/a"
    if cost < 0.01:
        return f"${cost:.4f}"
    return f"${cost:.3f}"


def generate(
    *,
    provider: str,
    model: str,
    api_key: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.2,
) -> dict[str, Any]:
    """Generate text and return content plus usage/cost metadata."""
    if not api_key:
        raise ValueError(f"No API key saved for {provider}. Add one under API Keys.")

    if provider == "OpenAI":
        content, usage = _generate_openai(model, api_key, system_prompt, user_prompt, temperature)
    elif provider == "Anthropic":
        content, usage = _generate_anthropic(model, api_key, system_prompt, user_prompt, temperature)
    elif provider == "Google":
        content, usage = _generate_google(model, api_key, system_prompt, user_prompt, temperature)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    input_tokens = int(usage.get("input_tokens") or 0)
    output_tokens = int(usage.get("output_tokens") or 0)
    cost = estimate_cost(
        provider=provider,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
    )
    return {
        "content": content,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": int(usage.get("total_tokens") or (input_tokens + output_tokens)),
        "cached_input_tokens": int(usage.get("cached_input_tokens") or 0),
        "cost_usd": cost,
        "pricing_note": "Estimated from standard/paid catalog rates; excludes cache discounts and long-context surcharges.",
    }


def _openai_supports_temperature(model: str) -> bool:
    """Newer GPT-5+/GPT-6 and o-series models only accept the default temperature."""
    blocked_prefixes = ("o1", "o3", "o4", "gpt-5", "gpt-6")
    return not model.startswith(blocked_prefixes)


def _generate_openai(
    model: str,
    api_key: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
) -> tuple[str, dict[str, int]]:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    # Prefer Responses API with web_search so the model can research live pages.
    try:
        response = client.responses.create(
            model=model,
            instructions=system_prompt,
            input=user_prompt,
            tools=[{"type": "web_search"}],
            include=["web_search_call.action.sources"],
        )
        content = (getattr(response, "output_text", None) or "").strip()
        if not content:
            raise RuntimeError("OpenAI Responses API returned an empty response.")

        usage = getattr(response, "usage", None)
        input_tokens = int(getattr(usage, "input_tokens", 0) or 0) if usage else 0
        output_tokens = int(getattr(usage, "output_tokens", 0) or 0) if usage else 0
        total_tokens = int(getattr(usage, "total_tokens", 0) or (input_tokens + output_tokens)) if usage else 0
        cached = 0
        details = getattr(usage, "input_tokens_details", None) if usage else None
        if details is not None:
            cached = int(getattr(details, "cached_tokens", 0) or 0)
        return content, {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "cached_input_tokens": cached,
        }
    except Exception:
        # Fall back to chat completions if Responses/web_search is unavailable.
        pass

    kwargs: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    if _openai_supports_temperature(model):
        kwargs["temperature"] = temperature

    response = client.chat.completions.create(**kwargs)
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("OpenAI returned an empty response.")

    usage = response.usage
    input_tokens = int(getattr(usage, "prompt_tokens", 0) or 0) if usage else 0
    output_tokens = int(getattr(usage, "completion_tokens", 0) or 0) if usage else 0
    total_tokens = int(getattr(usage, "total_tokens", 0) or (input_tokens + output_tokens)) if usage else 0
    cached = 0
    details = getattr(usage, "prompt_tokens_details", None) if usage else None
    if details is not None:
        cached = int(getattr(details, "cached_tokens", 0) or 0)
    return content, {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cached_input_tokens": cached,
    }


def _generate_anthropic(
    model: str,
    api_key: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
) -> tuple[str, dict[str, int]]:
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)
    kwargs: dict[str, Any] = {
        "model": model,
        "max_tokens": 8192,
        "temperature": temperature,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
        "tools": [
            {
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 12,
            }
        ],
    }
    try:
        response = client.messages.create(**kwargs)
    except Exception:
        kwargs.pop("tools", None)
        response = client.messages.create(**kwargs)

    parts = []
    for block in response.content:
        text = getattr(block, "text", None)
        if text:
            parts.append(text)
    content = "\n".join(parts).strip()
    if not content:
        raise RuntimeError("Anthropic returned an empty response.")

    usage = response.usage
    input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
    output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
    cached = int(getattr(usage, "cache_read_input_tokens", 0) or 0)
    return content, {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "cached_input_tokens": cached,
    }


def _generate_google(
    model: str,
    api_key: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
) -> tuple[str, dict[str, int]]:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    config_kwargs: dict[str, Any] = {
        "system_instruction": system_prompt,
        "temperature": temperature,
        "tools": [types.Tool(google_search=types.GoogleSearch())],
    }
    try:
        response = client.models.generate_content(
            model=model,
            contents=user_prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )
    except Exception:
        config_kwargs.pop("tools", None)
        response = client.models.generate_content(
            model=model,
            contents=user_prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )

    content = (response.text or "").strip()
    if not content:
        raise RuntimeError("Gemini returned an empty response.")

    meta = getattr(response, "usage_metadata", None)
    input_tokens = int(getattr(meta, "prompt_token_count", 0) or 0) if meta else 0
    # candidates + thoughts count as billable output for Gemini paid pricing notes
    output_tokens = int(getattr(meta, "candidates_token_count", 0) or 0) if meta else 0
    thoughts = int(getattr(meta, "thoughts_token_count", 0) or 0) if meta else 0
    output_tokens += thoughts
    total_tokens = int(getattr(meta, "total_token_count", 0) or (input_tokens + output_tokens)) if meta else 0
    cached = int(getattr(meta, "cached_content_token_count", 0) or 0) if meta else 0
    return content, {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cached_input_tokens": cached,
    }
