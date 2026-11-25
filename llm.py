"""Multi-provider LLM helpers for OpenAI, Anthropic, Google Gemini, and DeepSeek."""

from __future__ import annotations

from typing import Any

# Prices are USD per 1M tokens (standard / paid tier, short-context where applicable).
# Sources:
# - OpenAI: https://developers.openai.com/api/docs/pricing
# - Anthropic: https://platform.claude.com/docs/en/models/overview
# - Google: https://aistudio.google.com/docs/pricing
# - DeepSeek: https://api-docs.deepseek.com/quick_start/pricing/
# Preferred New Optimization defaults when the matching API key is configured.
DEFAULT_PROVIDER = "Anthropic"
DEFAULT_MODEL = "claude-sonnet-5-5"

MODELS: dict[str, list[dict[str, Any]]] = {
    # Anthropic first so it is the default provider when its key is present.
    "Anthropic": [
        {
            "id": "claude-sonnet-5-5",
            "label": "Claude Sonnet 5.5",
            "input_per_mtok": 2.00,
            "output_per_mtok": 10.00,
            "notes": "Default model; base token pricing",
        },
        {
            "id": "claude-opus-5-5",
            "label": "Claude Opus 5.5",
            "input_per_mtok": 4.00,
            "output_per_mtok": 20.00,
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
    "OpenAI": [
        {
            "id": "gpt-6-astra",
            "label": "GPT-6 Astra",
            "input_per_mtok": 10.00,
            "output_per_mtok": 50.00,
            "notes": "Standard short-context (≤272K)",
        },
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
    "Google": [
        {
            "id": "gemini-4-carbon",
            "label": "Gemini 4 Carbon",
            "input_per_mtok": 2.00,
            "output_per_mtok": 10.00,
            "notes": (
                "Promo through Nov 30, 2026; then $4.00 / $20.00; "
                "output includes thinking tokens"
            ),
        },
        {
            "id": "gemini-4-argon",
            "label": "Gemini 4 Argon",
            "input_per_mtok": 2.00,
            "output_per_mtok": 10.00,
            "notes": (
                "Promo through Nov 30, 2026; then $4.00 / $20.00; "
                "output includes thinking tokens; usually fewer tokens/turn than Carbon"
            ),
        },
        {
            "id": "gemini-4-hydrogen",
            "label": "Gemini 4 Hydrogen",
            "input_per_mtok": 1.50,
            "output_per_mtok": 7.50,
            "notes": "Paid tier; output includes thinking tokens",
        },
        {
            "id": "gemini-3.8-flash",
            "label": "Gemini 3.8 Flash",
            "input_per_mtok": 0.75,
            "output_per_mtok": 3.75,
            "notes": "Promo through Dec 31, 2026; then $1.50 / $7.50",
        },
        {
            "id": "gemini-3.5-flash-lite",
            "label": "Gemini 3.5 Flash-Lite",
            "input_per_mtok": 0.30,
            "output_per_mtok": 2.50,
            "notes": "Paid tier (text/image/video/audio input)",
        },
    ],
    "DeepSeek": [
        {
            "id": "deepseek-flash",
            "label": "DeepSeek V4.1 Flash",
            "input_per_mtok": 0.30,
            "output_per_mtok": 1.20,
            "notes": (
                "DeepSeek-V4.1-Flash-1017; peak cache-miss rates "
                "(off-peak half); thinking on by default; output includes reasoning tokens"
            ),
        },
    ],
}

PRICING_SOURCES = {
    "OpenAI": "https://developers.openai.com/api/docs/pricing",
    "Anthropic": "https://platform.claude.com/docs/en/models/overview",
    "Google": "https://aistudio.google.com/docs/pricing",
    "DeepSeek": "https://api-docs.deepseek.com/quick_start/pricing/",
}

PROVIDER_KEY_MAP = {
    "OpenAI": "openai",
    "Anthropic": "anthropic",
    "Google": "google",
    "DeepSeek": "deepseek",
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
    elif provider == "DeepSeek":
        content, usage = _generate_deepseek(model, api_key, system_prompt, user_prompt, temperature)
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


def _deepseek_usage_dict(usage: Any, *, prompt_style: bool = False) -> dict[str, int]:
    """Normalize DeepSeek Responses or Chat Completions usage into shared keys."""
    if usage is None:
        return {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "cached_input_tokens": 0,
        }
    if prompt_style:
        input_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
        output_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
        details = getattr(usage, "prompt_tokens_details", None)
        cached = int(getattr(details, "cached_tokens", 0) or 0) if details is not None else 0
        if not cached:
            cached = int(getattr(usage, "prompt_cache_hit_tokens", 0) or 0)
    else:
        input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
        output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
        details = getattr(usage, "input_tokens_details", None)
        cached = int(getattr(details, "cached_tokens", 0) or 0) if details is not None else 0
        if not cached:
            cached = int(getattr(usage, "cache_read_input_tokens", 0) or 0)
    total_tokens = int(getattr(usage, "total_tokens", 0) or (input_tokens + output_tokens))
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cached_input_tokens": cached,
    }


def _deepseek_add_usage(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    return {
        "input_tokens": int(a.get("input_tokens", 0)) + int(b.get("input_tokens", 0)),
        "output_tokens": int(a.get("output_tokens", 0)) + int(b.get("output_tokens", 0)),
        "total_tokens": int(a.get("total_tokens", 0)) + int(b.get("total_tokens", 0)),
        "cached_input_tokens": int(a.get("cached_input_tokens", 0))
        + int(b.get("cached_input_tokens", 0)),
    }


DEEPSEEK_TOOL_PREAMBLE = """
## DeepSeek runtime tooling (overrides skill tool names)

In this API request you have server-side tools:
- `deepseek_read_url` — fetch URLs present in the latest user message
- `deepseek_web_search` — web search and deep thinking search

Whenever the skill mentions WebSearch, use these server tools instead. They run
on the server inside this same turn. Do not ask permission. Do not reply with
only a plan such as "I'll start researching". Call the tools now, then write the
full markdown deliverable in this same response.
""".strip()

DEEPSEEK_FORCE_NUDGE = (
    "You did not finish. Immediately use `deepseek_read_url` and/or "
    "`deepseek_web_search` now, then produce the COMPLETE markdown deliverable "
    "with all required sections (Issues to fix, Research Summary, Gap Validation "
    "Table, Excluded Content Gaps, Final WYSIWYG PDP Copy, HTML PDP Copy, "
    "JSON-LD Schema, Sources). Do not reply with a plan only."
)

DEEPSEEK_WEB_TOOLS: list[dict[str, Any]] = [
    {"type": "deepseek_web_search"},
    {"type": "deepseek_read_url"},
]


def _deepseek_report_incomplete(content: str) -> bool:
    """True when the model stopped before producing the expected PDP deliverable."""
    text = (content or "").strip()
    if len(text) < 1500:
        return True
    lower = text.lower()
    required_any = (
        ("issues to fix" in lower or "page defects" in lower),
        "research summary" in lower,
        ("wysiwyg" in lower or "final wysiwyg" in lower),
        ("html" in lower and ("pdp" in lower or "```html" in lower)),
        ("json-ld" in lower or "jsonld" in lower or '"@type"' in lower),
    )
    # Require most core sections; allow one miss if the report is otherwise long.
    if sum(1 for ok in required_any if ok) < 4:
        return True
    return False


def _deepseek_research_useful(content: str) -> bool:
    """True when a research-first turn has enough substance to expand from."""
    text = (content or "").strip()
    if len(text) < 500:
        return False
    lower = text.lower()
    return ("##" in text or "research summary" in lower or "issues to fix" in lower)


def _deepseek_looks_like_plan_stub(content: str) -> bool:
    """Detect short 'I'll start researching…' replies that skipped tool use."""
    text = (content or "").strip().lower()
    if len(text) > 400:
        return False
    markers = (
        "i'll start",
        "i will start",
        "let me start",
        "i'll begin",
        "i will begin",
        "i'll research",
        "i will research",
        "i'll read",
        "let me research",
        "let me read",
    )
    return any(m in text for m in markers)


def _deepseek_augment_system(system_prompt: str) -> str:
    return f"{DEEPSEEK_TOOL_PREAMBLE}\n\n{system_prompt.strip()}"


def _deepseek_message_to_dict(message: Any) -> dict[str, Any]:
    """Serialize an OpenAI-style assistant message, preserving server_tool_calls."""
    if hasattr(message, "model_dump"):
        try:
            dumped = message.model_dump(exclude_none=True)
            if isinstance(dumped, dict) and dumped.get("role"):
                # Keep extension fields DeepSeek needs for multi-turn URL context.
                keep = {
                    k: dumped[k]
                    for k in (
                        "role",
                        "content",
                        "reasoning_content",
                        "server_tool_calls",
                        "tool_calls",
                    )
                    if k in dumped and dumped[k] is not None
                }
                if keep.get("role") == "assistant":
                    keep.setdefault("content", dumped.get("content") or "")
                    return keep
        except Exception:
            pass

    payload: dict[str, Any] = {
        "role": "assistant",
        "content": getattr(message, "content", None) or "",
    }
    reasoning = getattr(message, "reasoning_content", None)
    if reasoning:
        payload["reasoning_content"] = reasoning
    extras = getattr(message, "model_extra", None) or {}
    server_tool_calls = getattr(message, "server_tool_calls", None)
    if server_tool_calls is None and isinstance(extras, dict):
        server_tool_calls = extras.get("server_tool_calls")
    if server_tool_calls is not None:
        payload["server_tool_calls"] = server_tool_calls
    return payload


def _deepseek_server_tool_steps(message: Any) -> int:
    extras = getattr(message, "model_extra", None) or {}
    stc = getattr(message, "server_tool_calls", None)
    if stc is None and isinstance(extras, dict):
        stc = extras.get("server_tool_calls")
    try:
        return len(stc or [])
    except Exception:
        return 0


def _generate_deepseek(
    model: str,
    api_key: str,
    system_prompt: str,
    user_prompt: str,
    _temperature: float,
) -> tuple[str, dict[str, int]]:
    """Call DeepSeek with thinking + server web tools enabled.

    Temperature is unused: thinking mode ignores sampling params.

    DeepSeek sometimes returns a plan-only stub with thinking/tools skipped.
    We use non-streaming calls, a DeepSeek tool preamble, and retry/continue
    when that happens.
    """
    from openai import OpenAI

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
        timeout=1200.0,
    )
    system = _deepseek_augment_system(system_prompt)
    task = (
        user_prompt.strip()
        + "\n\nExecute tools in this turn and produce the COMPLETE deliverable "
        "with all required markdown sections. Do not stop after announcing that "
        "you will research."
    )
    errors: list[str] = []

    # Primary path: chat completions with thinking + web tools + stub recovery.
    try:
        content, usage = _deepseek_chat_with_recovery(
            client,
            model=model,
            system_prompt=system,
            user_prompt=task,
        )
        if not _deepseek_report_incomplete(content):
            return content, usage
        errors.append(f"chat recovery incomplete ({len(content)} chars)")
    except Exception as exc:
        errors.append(f"chat recovery: {exc}")

    # Fallback: Anthropic Messages API on DeepSeek.
    try:
        content, usage = _deepseek_anthropic_messages(
            api_key=api_key,
            model=model,
            system_prompt=system,
            user_prompt=task,
        )
        if not _deepseek_report_incomplete(content):
            return content, usage
        errors.append(f"anthropic-messages incomplete ({len(content)} chars)")
    except Exception as exc:
        errors.append(f"anthropic-messages: {exc}")

    raise RuntimeError(
        "DeepSeek failed to generate a complete PDP report. " + " | ".join(errors)
    )


def _deepseek_chat_create(
    client: Any,
    *,
    model: str,
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]],
    max_tokens: int = 65536,
) -> tuple[Any, str, dict[str, int]]:
    """One non-streaming DeepSeek chat call; returns (message, content, usage)."""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        tools=tools,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}},
        stream=False,
    )
    err = getattr(response, "error", None)
    if err is not None:
        message = getattr(err, "message", None) or str(err)
        raise RuntimeError(f"DeepSeek chat error payload: {message}")

    choice = (getattr(response, "choices", None) or [None])[0]
    if choice is None:
        raise RuntimeError("DeepSeek chat returned no choices.")

    finish_reason = getattr(choice, "finish_reason", None)
    if finish_reason in {"content_filter", "aborted", "insufficient_system_resource"}:
        raise RuntimeError(f"DeepSeek chat stopped early (finish_reason={finish_reason!r}).")

    message = choice.message
    content = (getattr(message, "content", None) or "").strip()
    if not content:
        raise RuntimeError(
            f"DeepSeek chat returned empty text (finish_reason={finish_reason!r})."
        )
    usage = _deepseek_usage_dict(getattr(response, "usage", None), prompt_style=True)
    return message, content, usage


def _deepseek_extract_subject_url(user_prompt: str) -> str:
    """Best-effort Subject PDP URL extraction for a focused first turn."""
    import re

    match = re.search(
        r"Subject PDP URL:\s*(\S+)",
        user_prompt or "",
        flags=re.IGNORECASE,
    )
    if match:
        return match.group(1).strip().rstrip(")>\"'")
    match = re.search(r"https?://\S+", user_prompt or "")
    return match.group(0).rstrip(")>\"'") if match else ""


def _deepseek_call_until_tools_or_report(
    client: Any,
    *,
    model: str,
    system_prompt: str,
    user_prompt: str,
    usage_total: dict[str, int],
) -> tuple[str, Any, dict[str, int]]:
    """Send a prompt; if DeepSeek returns a plan stub, force-continue once."""
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    message, content, usage = _deepseek_chat_create(
        client,
        model=model,
        messages=messages,
        tools=DEEPSEEK_WEB_TOOLS,
    )
    usage_total = _deepseek_add_usage(usage_total, usage)

    if not _deepseek_report_incomplete(content):
        return content, message, usage_total

    if _deepseek_server_tool_steps(message) == 0 and (
        _deepseek_looks_like_plan_stub(content) or len(content) < 500
    ):
        messages.append(_deepseek_message_to_dict(message))
        messages.append({"role": "user", "content": DEEPSEEK_FORCE_NUDGE})
        message2, content2, usage2 = _deepseek_chat_create(
            client,
            model=model,
            messages=messages,
            tools=DEEPSEEK_WEB_TOOLS,
        )
        usage_total = _deepseek_add_usage(usage_total, usage2)
        return content2, message2, usage_total

    return content, message, usage_total


def _deepseek_chat_with_recovery(
    client: Any,
    *,
    model: str,
    system_prompt: str,
    user_prompt: str,
) -> tuple[str, dict[str, int]]:
    """Research-first chat with stub continuation; then expand to full report."""
    usage_total = {
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "cached_input_tokens": 0,
    }
    subject_url = _deepseek_extract_subject_url(user_prompt)
    url_line = subject_url or "the Subject PDP URL in the task"

    # DeepSeek often ignores huge one-shot "write everything" prompts and returns
    # a plan stub. A focused research-first turn + force-continue is reliable.
    # Keep this first-turn prompt short. Long one-shot task dumps often make
    # DeepSeek return a plan stub with thinking/tools skipped.
    research_prompt = (
        f"Subject PDP URL: {url_line}\n\n"
        "Use `deepseek_read_url` and `deepseek_web_search` NOW (do not announce a plan).\n"
        "Follow the system skill rules for source authority and verification.\n"
        "Return at least:\n"
        "## 1. Issues to fix (Page Defects)\n"
        "## 2. Research Summary\n\n"
        "Research Summary must include verified product identity, key specs, "
        "competitor notes when found, and source URLs."
    )
    _ = user_prompt  # retained for signature compatibility / future turn context

    last_content = ""
    for _attempt in range(2):
        content, message, usage_total = _deepseek_call_until_tools_or_report(
            client,
            model=model,
            system_prompt=system_prompt,
            user_prompt=research_prompt,
            usage_total=usage_total,
        )
        last_content = content
        if not _deepseek_report_incomplete(content):
            # Already a full report (force-continue sometimes writes everything).
            return content, usage_total

        # If we have real research text, ask for the remaining deliverable sections.
        if _deepseek_research_useful(content):
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": research_prompt},
                _deepseek_message_to_dict(message),
                {
                    "role": "user",
                    "content": (
                        "Using the research already gathered (including any page/search "
                        "results in context), produce the COMPLETE deliverable with ALL "
                        "sections now:\n"
                        "## 1. Issues to fix (Page Defects)\n"
                        "## 2. Research Summary\n"
                        "## 3. Gap Validation Table\n"
                        "## 4. Excluded Content Gaps\n"
                        "## 5. Final WYSIWYG PDP Copy\n"
                        "## 6. HTML PDP Copy\n"
                        "## 7. JSON-LD Schema\n"
                        "## 8. Sources\n"
                        "You may use tools again if needed. Do not reply with a plan only."
                    ),
                },
            ]
            # Replies that already used web tools must be passed back unchanged.
            _msg2, content2, usage2 = _deepseek_chat_create(
                client,
                model=model,
                messages=messages,
                tools=DEEPSEEK_WEB_TOOLS,
            )
            usage_total = _deepseek_add_usage(usage_total, usage2)
            last_content = content2
            if not _deepseek_report_incomplete(content2):
                return content2, usage_total

    return last_content, usage_total


def _deepseek_anthropic_messages(
    *,
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
) -> tuple[str, dict[str, int]]:
    """DeepSeek Anthropic-compatible Messages API with thinking + web tools."""
    import anthropic

    client = anthropic.Anthropic(
        api_key=api_key,
        base_url="https://api.deepseek.com/anthropic",
        timeout=1200.0,
    )
    response = client.messages.create(
        model=model,
        max_tokens=65536,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
        extra_body={
            "thinking": {"type": "enabled"},
            "tools": [
                {"type": "deepseek_web_search", "name": "deepseek_web_search"},
                {"type": "deepseek_read_url", "name": "deepseek_read_url"},
            ],
        },
    )
    parts: list[str] = []
    for block in getattr(response, "content", None) or []:
        # Skip thinking/tool blocks; keep visible text only.
        if getattr(block, "type", None) == "text" and getattr(block, "text", None):
            parts.append(block.text)
    content = "\n".join(parts).strip()
    if not content:
        raise RuntimeError(
            "DeepSeek Anthropic Messages API returned no text "
            f"(stop_reason={getattr(response, 'stop_reason', None)!r})."
        )
    return content, _deepseek_usage_dict(getattr(response, "usage", None))
