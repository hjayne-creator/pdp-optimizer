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


def _anthropic_text_blocks(content: Any) -> list[str]:
    parts: list[str] = []
    for block in content or []:
        text = getattr(block, "text", None)
        if text:
            parts.append(text)
    return parts


def _generate_anthropic(
    model: str,
    api_key: str,
    system_prompt: str,
    user_prompt: str,
    _temperature: float,
) -> tuple[str, dict[str, int]]:
    """Call Anthropic Messages API. Sampling params are intentionally unused:
    SDK 1+/API 2026-10-21 removed temperature/top_p/top_k from create().

    Web search runs in a server-side loop that can return stop_reason=pause_turn
    before the final report is written; continue those turns until completion.
    """
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)
    tools: list[dict[str, Any]] | None = [
        {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 12,
        }
    ]
    messages: list[dict[str, Any]] = [{"role": "user", "content": user_prompt}]
    text_parts: list[str] = []
    input_tokens = 0
    output_tokens = 0
    cached = 0
    max_rounds = 10
    used_tools = True

    for round_idx in range(max_rounds):
        kwargs: dict[str, Any] = {
            "model": model,
            "max_tokens": 16384,
            "system": system_prompt,
            "messages": messages,
        }
        if tools is not None:
            kwargs["tools"] = tools

        try:
            response = client.messages.create(**kwargs)
        except Exception:
            if tools is None or round_idx > 0:
                raise
            # First-call tool setup can fail on some accounts/SDK combos.
            tools = None
            used_tools = False
            response = client.messages.create(
                model=model,
                max_tokens=16384,
                system=system_prompt,
                messages=messages,
            )

        usage = getattr(response, "usage", None)
        if usage is not None:
            input_tokens += int(getattr(usage, "input_tokens", 0) or 0)
            output_tokens += int(getattr(usage, "output_tokens", 0) or 0)
            cached += int(getattr(usage, "cache_read_input_tokens", 0) or 0)

        text_parts.extend(_anthropic_text_blocks(response.content))
        stop_reason = getattr(response, "stop_reason", None)

        if stop_reason == "pause_turn" and used_tools:
            # Server-tool loop paused; send assistant content back unchanged.
            messages.append({"role": "assistant", "content": response.content})
            continue

        if stop_reason == "max_tokens":
            messages.append({"role": "assistant", "content": response.content})
            messages.append(
                {
                    "role": "user",
                    "content": (
                        "Continue exactly where you left off. "
                        "Finish the full deliverable with all required sections."
                    ),
                }
            )
            continue

        break
    else:
        raise RuntimeError(
            "Anthropic hit the continuation limit before finishing the report. "
            "Try again, or temporarily reduce web-search scope."
        )

    content = "\n".join(text_parts).strip()
    if not content:
        raise RuntimeError("Anthropic returned an empty response.")
    if len(content) < 500 and "##" not in content:
        raise RuntimeError(
            "Anthropic stopped before producing a full report "
            f"(stop_reason={getattr(response, 'stop_reason', None)!r}, "
            f"{len(content)} chars). Try running again."
        )

    return content, {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "cached_input_tokens": cached,
    }


def _extract_gemini_text(response: Any) -> str:
    """Pull visible text parts from a Gemini response, skipping thought-only parts."""
    texts: list[str] = []
    for candidate in getattr(response, "candidates", None) or []:
        content = getattr(candidate, "content", None)
        for part in getattr(content, "parts", None) or []:
            if getattr(part, "thought", False):
                continue
            text = getattr(part, "text", None)
            if text:
                texts.append(text)
    if texts:
        return "\n".join(texts).strip()
    try:
        return (getattr(response, "text", None) or "").strip()
    except Exception:
        return ""


def _gemini_empty_detail(response: Any) -> str:
    """Build a short diagnostic when Gemini returns no visible text."""
    details: list[str] = []
    prompt_feedback = getattr(response, "prompt_feedback", None)
    if prompt_feedback is not None:
        block = getattr(prompt_feedback, "block_reason", None)
        if block:
            details.append(f"prompt_block={block}")
    candidates = getattr(response, "candidates", None) or []
    if not candidates:
        details.append("no candidates")
    for idx, candidate in enumerate(candidates):
        finish = getattr(candidate, "finish_reason", None)
        if finish:
            details.append(f"candidate[{idx}].finish_reason={finish}")
        finish_message = getattr(candidate, "finish_message", None)
        if finish_message:
            details.append(f"candidate[{idx}].finish_message={finish_message}")
        grounding = getattr(candidate, "grounding_metadata", None)
        if grounding is not None:
            queries = getattr(grounding, "web_search_queries", None) or []
            chunks = getattr(grounding, "grounding_chunks", None) or []
            if queries:
                details.append(f"search_queries={len(queries)}")
            details.append(f"grounding_chunks={len(chunks)}")
    meta = getattr(response, "usage_metadata", None)
    if meta is not None:
        details.append(
            "tokens="
            f"prompt:{getattr(meta, 'prompt_token_count', 0) or 0}/"
            f"candidates:{getattr(meta, 'candidates_token_count', 0) or 0}/"
            f"thoughts:{getattr(meta, 'thoughts_token_count', 0) or 0}"
        )
    return "; ".join(details) if details else "no additional diagnostics"


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

    def _call(*, use_search: bool) -> Any:
        config_kwargs: dict[str, Any] = {
            "system_instruction": system_prompt,
            "temperature": temperature,
        }
        if use_search:
            config_kwargs["tools"] = [types.Tool(google_search=types.GoogleSearch())]
        return client.models.generate_content(
            model=model,
            contents=user_prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )

    response = None
    content = ""
    # Search grounding can "succeed" with finish_reason=STOP and empty text.
    # Retry without tools when that happens (common on hosted Streamlit).
    try:
        response = _call(use_search=True)
        content = _extract_gemini_text(response)
    except Exception:
        response = None
        content = ""

    if not content:
        response = _call(use_search=False)
        content = _extract_gemini_text(response)

    if not content:
        raise RuntimeError(
            "Gemini returned an empty response. "
            f"Diagnostics: {_gemini_empty_detail(response)}"
        )

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
