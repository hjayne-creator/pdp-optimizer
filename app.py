from io import BytesIO
from pathlib import Path

import streamlit as st

from llm import (
    MODELS,
    PRICING_SOURCES,
    PROVIDER_KEY_MAP,
    format_cost,
    format_model_option,
    generate,
    get_model,
    model_options,
    pricing_rows,
)
from storage import (
    delete_report,
    list_reports,
    load_api_keys,
    load_report,
    save_api_keys,
    save_report,
)

SKILL_PATH = Path(__file__).resolve().parent / "SKILL.md"

OUTPUT_FORMAT_INSTRUCTIONS = """
## Streamlit delivery format

Follow the skill above. Then return the report using these exact markdown headings, in order:

## 1. Issues to fix (Page Defects)
## 2. Research Summary
## 3. Gap Validation Table
## 4. Excluded Content Gaps
## 5. Final WYSIWYG PDP Copy
## 6. HTML PDP Copy
## 7. JSON-LD Schema
## 8. Sources

### How it compares (important, but not always required)

Research alternative products separately from exact-match competitor PDPs (skill section 3b).

- Include a **How it compares** section inside the Final WYSIWYG PDP Copy (and mirrored in HTML) only when research finds at least three suitable alternative products with enough verified, comparable specifications.
- Use a concise markdown/HTML table comparing the subject product with 3–5 alternatives on buyer-relevant, verified attributes only.
- If fewer than three suitable alternatives are found, omit **How it compares** entirely. Do not invent alternatives or fill empty cells.
- In the Research Summary, explicitly state either:
  - that How it compares was included (list the alternatives), or
  - that it was omitted and why (e.g. fewer than three verified alternatives).

### Customer style guide (writing phase)

When a Customer Style Guide is provided in the user message:

- Read it before drafting and treat it as authoritative for voice, tone, terminology, structure, section naming, and presentation constraints.
- Apply it throughout **Final WYSIWYG PDP Copy** and **HTML PDP Copy**.
- If the style guide conflicts with the default visible-copy structure above, follow the style guide and note the deviation in the Research Summary.
- Do not invent style rules that are not in the guide. If no style guide is provided, use clear UK/EN professional ecommerce tone.

Visible WYSIWYG copy structure (omit a section only when it does not apply; style guide may override):
1. Product identity
2. Key specifications
3. Overview
4. Features
5. Applications
6. Compatibility and selection guidance
7. How it compares (only when criteria are met)
8. Technical specifications
9. Customer questions / FAQs
10. Customer concerns / objection handling

For section 5: buyer-facing PDP copy only as clean markdown — no meta commentary, research notes, or inline citations.
For section 6: wrap the HTML in a single ```html fenced block.
For section 7: wrap the JSON-LD in a single ```json fenced block.

Tooling note: Screaming Frog / browser connectors may be unavailable in this app. Use the best research available to you and disclose material extraction or research limitations in the Research Summary.
"""


def read_style_guide(uploaded_file) -> tuple[str, str, bool]:
    """Return (content, status_note, ok) from an uploaded style guide file."""
    name = uploaded_file.name
    suffix = Path(name).suffix.lower()
    raw = uploaded_file.read()

    try:
        if suffix in {".txt", ".md"}:
            content = raw.decode("utf-8").strip()
        elif suffix == ".docx":
            from docx import Document

            doc = Document(BytesIO(raw))
            parts: list[str] = []
            for para in doc.paragraphs:
                text = para.text.strip()
                if text:
                    parts.append(text)
            for table in doc.tables:
                for row in table.rows:
                    cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if cells:
                        parts.append(" | ".join(cells))
            content = "\n".join(parts).strip()
        else:
            return (
                "Unsupported style guide format. Default to clear UK/EN professional ecommerce tone.",
                f"{name} (unsupported type)",
                False,
            )
    except Exception as exc:
        return (
            "Could not parse uploaded style guide. Default to clear UK/EN professional ecommerce tone.",
            f"{name} (parse failed: {exc})",
            False,
        )

    if not content:
        return (
            "Uploaded style guide was empty after parsing. Default to clear UK/EN professional ecommerce tone.",
            f"{name} (empty)",
            False,
        )
    return content, name, True


def load_system_prompt() -> str:
    """Load SKILL.md as the authoritative system prompt, plus delivery format."""
    skill_text = ""
    if SKILL_PATH.exists():
        raw = SKILL_PATH.read_text(encoding="utf-8")
        if raw.startswith("---"):
            parts = raw.split("---", 2)
            skill_text = parts[2].strip() if len(parts) >= 3 else raw.strip()
        else:
            skill_text = raw.strip()
    else:
        skill_text = (
            "You are an expert Ecommerce PDP Optimizer. Research, validate, and improve "
            "ecommerce PDP copy with strict source-authority rules. Never fabricate specs."
        )
    return f"{skill_text}\n\n{OUTPUT_FORMAT_INSTRUCTIONS.strip()}"


def extract_section(text: str, *aliases: str) -> str:
    """Pull a named section from the model report using heading aliases."""
    import re

    if not text:
        return ""

    alias_pattern = "|".join(re.escape(a) for a in aliases)
    start = re.search(
        rf"(?im)^(?:#{{1,3}}\s*|\*\*)?(?:\d+[.)]\s*)?(?:{alias_pattern})\b.*$",
        text,
    )
    if not start:
        return ""

    rest = text[start.end() :]
    end = re.search(
        rf"(?im)^(?:#{{1,3}}\s*|\*\*)?(?:\d+[.)]\s*)?(?:"
        r"Issues to fix|Page Defects|Research Summary|Gap Validation|"
        r"Excluded Content Gaps|Final WYSIWYG|WYSIWYG PDP Copy|"
        r"HTML PDP Copy|JSON-LD Schema|Sources"
        r")\b",
        rest,
    )
    body = rest[: end.start()] if end else rest
    return body.strip()


def strip_code_fence(text: str) -> str:
    """Remove surrounding markdown code fences if present."""
    import re

    if not text:
        return ""
    fenced = re.search(r"```(?:\w+)?\s*\n([\s\S]*?)\n```", text.strip())
    return fenced.group(1).strip() if fenced else text.strip()


def render_run_cost(usage: dict) -> None:
    """Show estimated cost and token usage for a completed run."""
    if not usage:
        return
    cost = usage.get("cost_usd")
    cols = st.columns(4)
    cols[0].metric("Est. cost", format_cost(cost))
    cols[1].metric("Input tokens", f"{int(usage.get('input_tokens') or 0):,}")
    cols[2].metric("Output tokens", f"{int(usage.get('output_tokens') or 0):,}")
    cols[3].metric("Total tokens", f"{int(usage.get('total_tokens') or 0):,}")
    note = usage.get("pricing_note") or ""
    cached = int(usage.get("cached_input_tokens") or 0)
    extras = []
    if cached:
        extras.append(f"Cached input tokens: {cached:,}")
    if note:
        extras.append(note)
    if extras:
        st.caption(" · ".join(extras))


def render_report_tabs(full_output: str, key_prefix: str = "live") -> None:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📄 Full Report",
        "📝 WYSIWYG Copy",
        "💻 HTML Code",
        "⚡ JSON-LD Schema",
        "🔍 Research & Gaps",
    ])

    wysiwyg_copy = extract_section(
        full_output,
        "Final WYSIWYG PDP Copy",
        "WYSIWYG PDP Copy",
        "Final WYSIWYG",
    )
    html_copy = strip_code_fence(
        extract_section(full_output, "HTML PDP Copy", "HTML Copy")
    )
    jsonld_copy = strip_code_fence(
        extract_section(full_output, "JSON-LD Schema", "JSON-LD", "JSON LD Schema")
    )
    research_copy = "\n\n".join(
        part for part in [
            extract_section(full_output, "Issues to fix (Page Defects)", "Issues to fix", "Page Defects"),
            extract_section(full_output, "Research Summary"),
            extract_section(full_output, "Gap Validation Table", "Gap Validation"),
            extract_section(full_output, "Excluded Content Gaps"),
            extract_section(full_output, "Sources"),
        ] if part
    )

    with tab1:
        st.markdown(full_output)
        st.download_button(
            label="Download Full Report (.md)",
            data=full_output,
            file_name="pdp_optimization_report.md",
            mime="text/markdown",
            key=f"{key_prefix}_dl_full",
        )

    with tab2:
        st.info("Copy-ready WYSIWYG text for your ecommerce platform CMS.")
        display_wysiwyg = wysiwyg_copy or full_output
        if not wysiwyg_copy:
            st.caption("Section heading not found — showing full report rendered as formatted copy.")
        st.markdown(display_wysiwyg)
        st.download_button(
            label="Download WYSIWYG Copy (.md)",
            data=display_wysiwyg,
            file_name="pdp_wysiwyg_copy.md",
            mime="text/markdown",
            key=f"{key_prefix}_dl_wysiwyg",
        )
        with st.expander("Plain text (for CMS paste)"):
            st.text_area(
                "WYSIWYG source",
                value=display_wysiwyg,
                height=300,
                label_visibility="collapsed",
                key=f"{key_prefix}_wysiwyg_src",
            )

    with tab3:
        st.info("Semantic clean HTML structure.")
        if html_copy:
            st.code(html_copy, language="html")
            st.download_button(
                label="Download HTML",
                data=html_copy,
                file_name="pdp_copy.html",
                mime="text/html",
                key=f"{key_prefix}_dl_html",
            )
        else:
            st.warning("Could not locate the HTML PDP Copy section. Check the Full Report tab.")

    with tab4:
        st.info("Valid schema.org Product JSON-LD block.")
        if jsonld_copy:
            st.code(jsonld_copy, language="json")
            st.download_button(
                label="Download JSON-LD",
                data=jsonld_copy,
                file_name="pdp_schema.json",
                mime="application/json",
                key=f"{key_prefix}_dl_jsonld",
            )
        else:
            st.warning("Could not locate the JSON-LD Schema section. Check the Full Report tab.")

    with tab5:
        st.markdown("### Audit, Defect & Gap Validation Breakdown")
        if research_copy:
            st.markdown(research_copy)
        else:
            st.warning("Could not locate research sections. Check the Full Report tab.")


def page_api_keys() -> None:
    st.header("API Keys")
    st.caption("Keys are saved locally in `data/api_keys.json` (gitignored). They stay on this machine between runs.")

    saved = load_api_keys()
    with st.form("api_keys_form"):
        openai_key = st.text_input(
            "OpenAI API Key",
            value=saved.get("openai", ""),
            type="password",
            help="Used for GPT models.",
        )
        anthropic_key = st.text_input(
            "Anthropic API Key",
            value=saved.get("anthropic", ""),
            type="password",
            help="Used for Claude models.",
        )
        google_key = st.text_input(
            "Google AI API Key",
            value=saved.get("google", ""),
            type="password",
            help="Used for Gemini models (Google AI Studio).",
        )
        submitted = st.form_submit_button("Save keys", type="primary")

    if submitted:
        save_api_keys({
            "openai": openai_key,
            "anthropic": anthropic_key,
            "google": google_key,
        })
        st.success("API keys saved.")

    status = load_api_keys()
    cols = st.columns(3)
    for col, (label, field) in zip(cols, [
        ("OpenAI", "openai"),
        ("Anthropic", "anthropic"),
        ("Google", "google"),
    ]):
        with col:
            if status.get(field):
                st.success(f"{label}: saved")
            else:
                st.warning(f"{label}: missing")


def page_new_run() -> None:
    st.header("New Optimization")

    keys = load_api_keys()
    providers = list(MODELS.keys())
    available = [p for p in providers if keys.get(PROVIDER_KEY_MAP[p])]
    if not available:
        st.warning("No API keys saved yet. Add at least one under **API Keys**.")
        return

    col_a, col_b = st.columns(2)
    with col_a:
        provider = st.selectbox(
            "Provider",
            options=available,
            help="Only providers with a saved API key are listed.",
        )
    with col_b:
        options = model_options(provider)
        model = st.selectbox(
            "Model",
            options=options,
            format_func=lambda m: format_model_option(provider, m),
        )

    selected = get_model(provider, model)
    if selected:
        st.caption(
            f"Pricing (standard/paid): **${selected['input_per_mtok']:.2f}** input · "
            f"**${selected['output_per_mtok']:.2f}** output per 1M tokens"
            + (f" — {selected['notes']}" if selected.get("notes") else "")
            + f" · [source]({PRICING_SOURCES.get(provider, '#')})"
        )

    subject_url = st.text_input(
        "Subject PDP URL",
        placeholder="https://www.example.com/product-page",
        help="The product page you want to audit and optimize.",
    )
    style_guide_file = st.file_uploader(
        "Customer Style Guide (Optional)",
        type=["txt", "md", "docx"],
        help="Upload the brand voice rules or style guide document.",
    )
    run_button = st.button("🚀 Optimize PDP", type="primary")

    if run_button:
        if not subject_url:
            st.error("Please provide a valid Subject PDP URL.")
            return

        style_guide_ok = False
        if style_guide_file is not None:
            style_guide_content, style_guide_note, style_guide_ok = read_style_guide(style_guide_file)
            if style_guide_ok:
                st.caption(f"Style guide loaded: `{style_guide_note}` ({len(style_guide_content):,} characters).")
            else:
                st.warning(f"Style guide not applied: {style_guide_note}")
        else:
            style_guide_content = (
                "No custom style guide uploaded. Default to clear UK/EN professional ecommerce tone."
            )
            style_guide_note = "None"

        style_guide_writing_rule = (
            "Apply the Customer Style Guide / Brand Rules below as the authority for voice, tone, "
            "terminology, structure, and presentation when writing Final WYSIWYG PDP Copy and HTML PDP Copy. "
            "If the guide conflicts with the default section list, follow the guide and note the deviation "
            "in the Research Summary."
            if style_guide_ok
            else "No usable style guide was provided; use clear UK/EN professional ecommerce tone."
        )

        user_prompt = f"""
Please optimize the following Subject PDP URL using the Ecommerce PDP Optimizer skill rules.

Subject PDP URL: {subject_url}

Customer Style Guide / Brand Rules:
{style_guide_content}

Style guide writing instruction:
{style_guide_writing_rule}

Required work:
1. Research and verify the subject product (manufacturer sources preferred; disclose limits).
2. Review exact-match competitor PDPs when available.
3. Separately research alternative products for a possible **How it compares** table. Include that table in the Final WYSIWYG PDP Copy and HTML only if at least three suitable alternatives have verified, comparable specs; otherwise omit it and say why in the Research Summary.
4. Produce the full deliverable set (Issues, Research Summary, Gap Validation Table, Excluded Content Gaps, WYSIWYG copy, HTML, JSON-LD, Sources).
5. During the PDP writing phase (sections 5 and 6), actively apply the Customer Style Guide rules above.

Buyer-focused, neutral, no unsupported marketing claims. Prefer metric units where applicable unless the style guide says otherwise.
"""
        api_key = keys.get(PROVIDER_KEY_MAP[provider], "")
        model_label = selected["label"] if selected else model
        with st.spinner(f"Running {model_label}… analyzing page and generating assets…"):
            try:
                result = generate(
                    provider=provider,
                    model=model,
                    api_key=api_key,
                    system_prompt=load_system_prompt(),
                    user_prompt=user_prompt,
                )
                result_text = result["content"]
                usage = {
                    "input_tokens": result["input_tokens"],
                    "output_tokens": result["output_tokens"],
                    "total_tokens": result["total_tokens"],
                    "cached_input_tokens": result.get("cached_input_tokens", 0),
                    "cost_usd": result.get("cost_usd"),
                    "pricing_note": result.get("pricing_note", ""),
                }
                report = save_report(
                    subject_url=subject_url,
                    provider=provider,
                    model=model,
                    result_text=result_text,
                    style_guide_note=style_guide_note,
                    usage=usage,
                )
                st.session_state["active_report_id"] = report["id"]
                st.session_state["result_text"] = result_text
                st.session_state["result_meta"] = {
                    "subject_url": subject_url,
                    "provider": provider,
                    "model": model,
                    "model_label": model_label,
                    "usage": usage,
                }
                st.success(
                    f"Optimization complete — saved as report `{report['id']}` · "
                    f"est. cost **{format_cost(usage.get('cost_usd'))}**"
                )
            except Exception as e:
                st.error(f"An error occurred during generation: {e}")
                return

    if "result_text" in st.session_state:
        st.divider()
        meta = st.session_state.get("result_meta", {})
        if meta:
            st.caption(
                f"{meta.get('provider', '')} · {meta.get('model', '')} · {meta.get('subject_url', '')}"
            )
        usage = meta.get("usage") or {}
        if usage:
            render_run_cost(usage)
        st.subheader("Optimization Report & Assets")
        render_report_tabs(st.session_state["result_text"], key_prefix="live")
    else:
        st.info("Enter a Subject PDP URL, choose a model, then click **Optimize PDP**.")


def page_pricing() -> None:
    st.header("Model Pricing")
    st.caption(
        "USD per 1M tokens for models available in this app. "
        "OpenAI figures use Standard short-context rates; Google figures use paid-tier rates."
    )
    st.dataframe(pricing_rows(), use_container_width=True, hide_index=True)

    st.subheader("Official sources")
    for provider, url in PRICING_SOURCES.items():
        st.markdown(f"- [{provider} pricing]({url})")

    st.info(
        "Batch, Flex, Fast, Ultrafast, long-context, and cache rates may differ. "
        "Check the linked docs before estimating production spend."
    )


def page_saved_reports() -> None:
    st.header("Saved Reports")
    reports = list_reports()
    if not reports:
        st.info("No saved reports yet. Run an optimization to create one.")
        return

    labels = {
        r["id"]: (
            f"{r['created_at'][:19].replace('T', ' ')} UTC · {r['model']} · "
            f"{format_cost(r.get('cost_usd'))} · {r['subject_url']}"
        )
        for r in reports
    }
    selected_id = st.selectbox(
        "Select a report",
        options=[r["id"] for r in reports],
        format_func=lambda rid: labels.get(rid, rid),
        index=0,
    )

    if st.button("Delete selected report"):
        delete_report(selected_id)
        if st.session_state.get("active_report_id") == selected_id:
            st.session_state.pop("result_text", None)
            st.session_state.pop("result_meta", None)
            st.session_state.pop("active_report_id", None)
        st.success("Report deleted.")
        st.rerun()

    report = load_report(selected_id)
    if not report:
        st.error("Could not load that report.")
        return

    st.divider()
    st.markdown(f"**URL:** {report.get('subject_url', '')}")
    st.caption(
        f"{report.get('provider', '')} · {report.get('model', '')} · "
        f"created {report.get('created_at', '')} · style guide: {report.get('style_guide_note') or 'None'}"
    )
    render_run_cost(report.get("usage") or {})
    render_report_tabs(report.get("result_text", ""), key_prefix=f"saved_{selected_id}")


# --- App shell ---
st.set_page_config(
    page_title="Ecommerce PDP Optimizer",
    page_icon="🛒",
    layout="wide",
)

st.title("🛒 Ecommerce Product Detail Page (PDP) Optimizer")
st.markdown(
    "Research, validate, and optimize ecommerce PDP copy, HTML, and structured JSON-LD schema "
    "based on strict source authority rules and customer style guides."
)

with st.sidebar:
    st.header("Navigation")
    nav = st.radio(
        "Go to",
        options=["New Optimization", "Saved Reports", "Model Pricing", "API Keys"],
        label_visibility="collapsed",
    )
    st.divider()
    keys = load_api_keys()
    configured = sum(1 for v in keys.values() if v)
    st.caption(f"API keys configured: {configured}/3")
    st.caption(f"Saved reports: {len(list_reports())}")
    st.caption(f"Models available: {sum(len(v) for v in MODELS.values())}")

if nav == "API Keys":
    page_api_keys()
elif nav == "Saved Reports":
    page_saved_reports()
elif nav == "Model Pricing":
    page_pricing()
else:
    page_new_run()
