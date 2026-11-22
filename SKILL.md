---
name: pdp-optimizer
description: Research, validate, and improve an ecommerce product detail page (PDP) using the subject page, official manufacturer documentation, a customer style guide, and competitor research. Use when asked to audit, rewrite, enrich, compare, or create PDP copy, HTML, or Product JSON-LD for an ecommerce product.
connectors: ScreamingFrog
---

# Ecommerce PDP Optimizer

Optimize ecommerce product-detail-page content for accuracy, completeness, buyer confidence, and auditability. Work carefully; do not trade verification for speed.

## Required inputs

Collect these inputs before beginning. Ask for anything that is missing.

1. **Subject PDP URL** — the product page to improve.
2. **Customer style guide** — rules for the product description and page voice. It may be uploaded with the request or supplied as a local file path. Read it before researching or drafting.

Official manufacturer sources are research sources, not an input requirement. Locate and use them when available.

Before crawling, read the site blacklist from the designated local directory, when present. Do not visit, crawl, extract, or cite a blacklisted domain or any of its subdomains. The blacklist overrides every research fallback below.

## Source authority and claim rules

Apply these rules to every claim in the final output.

- The subject PDP and customer style guide govern existing page content and presentation requirements.
- Official manufacturer sources are authoritative for specifications, certifications, ratings, compliance, dimensions, limits, warranty, protection features, and safety language.
- Competitor PDPs are discovery sources only. Do not use them as authority for exact specifications unless the information is independently confirmed by an official manufacturer source.
- Verify every number, unit, and unit conversion before publishing it. If sources conflict, use official manufacturer documentation for technical specifications. If the conflict cannot be resolved, omit the value or identify it as unverifiable in the audit.
- Do not fabricate, infer, or silently reconcile conflicting facts.
- Do not use absolutes or unsupported promotional language, including “ensures,” “guarantees,” “prevents damage,” “maintenance-free,” or “worldwide deployment.”
- Do not include medical, safety, compliance, performance, or compatibility claims unless directly supported by an authoritative source.

## Research method

### 1. Extract the subject page

Use a JavaScript-capable browser or crawler when available. Many PDPs load specification tables, tabs, images, and structured data after rendering.

Preferred order:

1. Crawl with Screaming Frog using JavaScript rendering, when the Screaming Frog MCP connector is available.
2. Use an available browser to render and inspect the page.
3. Fall back to WebFetch for static pages.

Use the same preference for the subject page, manufacturer sources, and competitor PDPs. If browser rendering is unavailable and extracted content appears incomplete, disclose that limitation in the Research Summary.

#### Screaming Frog procedure

Follow these steps in order; they avoid known failure points.

1. **Crawl in list mode.** Use `sf_crawl_from_list` with one URL or with the subject page and competitor PDPs together. Poll `sf_crawl_progress` until `crawlRunning` is `false` before reading results.
2. **Save files only to existing folders.** Writes to a missing subfolder fail. Call `sf_create_directory` first (for example, `pdp/`) or write to the base directory.
3. **Extract page content.** Call `sf_url_content` with `page_content_type: MARKDOWN` and a `file_path`, then read the file with `sf_read_text_file`. Inline output is capped at 8,192 characters.
4. **Extract head elements.** `sf_url_info` returns the title, meta description, H1, meta robots, canonical, status, and indexability. Write the result to a file, then read it.
5. **Extract live JSON-LD.** Export the custom extractor with `sf_export_seo_element_urls` using `seo_element_name: Custom Extraction` and `filter_name: LDJSON`, then call `sf_task_status`. The result's sample row contains each JSON-LD block in full. The **Structured Data → JSON-LD URLs** export lists types and validation counts only; use it for errors and warnings.
6. **Do not page through raw HTML** with `sf_read_text_file`. Minified pages may place the whole body on one line, exceeding the 100 KB response limit even when only a few lines are requested.
7. **Do not retry disabled Node.js scripts.** `sf_run_node_script` works only when the SEO Spider Node.js runtime is enabled. If it reports disabled, continue with steps 3–5.
8. **Do not bypass bot protection.** If a site shows a Cloudflare challenge (HTTP 403 or “Just a moment…”), rely on the Screaming Frog crawl and record the limitation.

Catalog the following subject-page content:

- Product title/H1, brand, manufacturer, manufacturer part number, retailer SKU, and product type
- Existing description, feature bullets, specification-linked benefits, applications, and compatibility or usage guidance
- Specifications, dimensions, materials, certifications, compliance claims, warranty, and protection features
- Documents, downloads, FAQs, product-specific reviews or feedback, and visible structured-data values

Treat price, stock, lead times, shipping estimates, tariffs, promotions, and temporary availability as audit notes only—not static PDP copy.

Retain accurate, useful, product-specific subject-page content unless it is duplicated, outdated, clearly dynamic, or better placed elsewhere on the page.

### 2. Verify with official manufacturer sources

For the exact model, locate and review relevant official sources, such as:

- Official product page, datasheet, specification sheet, manual, or installation guide
- Safety documentation and compliance certificates
- Dimensional drawings and product-family documentation, only when clearly applicable to the exact model

Use these sources to verify technical details, resolve conflicts, and test competitor claims. Manufacturer sources do not count as competitor sources.

A manufacturer-branded document, such as a data sheet or brochure carrying the manufacturer's name, address, and exact product code, still counts as a manufacturer source when hosted on a reseller's domain. Name the host in Sources.

Confirm the exact model before trusting any source. Manufacturers often reuse model names across generations or trims, such as “Tech” and “Tech Pro.” Match on the manufacturer product code, not the name alone, and list excluded near-match models in the Research Summary.

### 3. Find valid competitor PDPs

Search using the brand/manufacturer name plus the exact manufacturer part number or model number. Review organic results only; exclude sponsored placements and shopping ads. Apply the local site blacklist before opening any result.

These competitor PDPs are for the same subject product. Aim to review 3–6 valid exact-match PDPs. If fewer than three exist after a reasonable search, stop and report the number found. Do not review more than six unless the user specifically requests broader research.

A valid competitor PDP must:

- Represent the exact same product, manufacturer part number, model number, or SKU equivalent.
- Contain product-specific content.
- Be a product detail page rather than a category, search, blog, landing, or marketplace-search page.

Exclude alternate models and variants, used products, thin pages, and generic how-to or deployment content. The local site blacklist always takes precedence.

### 3a. Category research when no direct competitors exist

If the product is brand-only, has no exact manufacturer part number, or no valid exact-match competitor PDP can be found, conduct category research using non-blacklisted, reputable sources. Look for buyer-relevant category information such as common applications, selection factors, terminology, installation considerations, frequent questions, and recurring objections.

Category research is contextual only. Do not treat it as product evidence and do not use it to create or imply product-specific specifications, compatibility, certifications, safety, performance, warranty, included components, or claims. Incorporate category insights only as neutral, clearly general buyer guidance that does not overstate applicability to the subject product. Identify category sources separately in the Research Summary and Sources, and report the number of valid exact-match PDPs found.

### 3b. Research alternative products for “How it compares”

Research alternative products separately from exact-match competitor PDPs. An alternative must be a current, distinct product that serves the same core buyer need or application as the subject product.

Use official manufacturer product pages, datasheets, or manuals as the authority for comparison facts. A stockist page may help discover an alternative or locate a missing document, but must not be the sole source for a comparison value.

Only create a comparison table when research identifies at least three suitable alternatives with enough verified, comparable information. If fewer than three suitable alternatives are found, omit **How it compares** entirely.

For each eligible alternative, record:

- Brand, product name, and manufacturer part number or model
- Buyer-relevant attributes that can be compared fairly with the subject product
- Important configuration or scope differences that affect the comparison

Do not compare price, stock, lead time, promotions, customer ratings, or subjective claims such as “best,” “better,” or “premium.” Do not imply that the subject product is superior unless that conclusion follows directly and neutrally from the displayed specifications.

### 4. Extract competitor content

For each valid competitor PDP, record:

- Product title, brand, manufacturer part number, and retailer SKU
- Product description, feature bullets, benefits tied to features or specifications, applications, compatibility, and included components
- Specifications, materials, dimensions, FAQs, recurring product-specific concerns, certifications, standards, warranty, documents, downloads, and schema fields
- Content prioritization: what is above the fold; what appears in bullets, tables, FAQs, downloads, and structured data

### 5. Validate content gaps

Compare the subject page with official manufacturer sources and competitor PDPs.

Treat an item as an eligible content gap only when it is missing from the subject page, materially helps a buyer evaluate the product, and is either:

- Verified by official manufacturer documentation, or
- Present on at least two independent valid competitor PDPs.

Do not use a claim found on only one competitor PDP unless an official manufacturer source verifies it.

Classify each candidate as one of:

`Product Identifier` · `Technical Specification` · `Feature` · `Benefit` · `Application` · `Compatibility Guidance` · `Installation/Use Guidance` · `Safety/Compliance Note` · `Material/Construction Detail` · `Dimension/Fit Detail` · `FAQ` · `Customer Concern/Objection` · `Warranty/Support Detail` · `Schema Attribute` · `Excluded Claim`

Prepare a gap-validation table for all content missing from the subject page. Include the content element, evidence, inclusion decision, and rationale.

## Create the improved PDP

Write an accurate, neutral, professional PDP that preserves useful subject-page content and adds only validated information. Prioritize additions by buyer-decision importance, subject-page emphasis, manufacturer emphasis, competitor frequency, and search intent.

### Copy retention

- Prefer retaining accurate, useful subject-page copy over rewriting it.
- **Retain** useful overview prose and feature bullets from the subject catalog when they are product-specific and verified.
- **Light-edit only** where needed: spelling, units, EN/UK English, product-led voice, and removal of fluff or unsupported claims.
- **Expand** only for validated gaps and clearer feature-to-benefit wording; do not wholesale-rewrite good copy.

The copy should help buyers answer:

- Is this the exact product I need?
- Will it work in my application?
- Is it compatible with my setup?
- Can I trust this source?
- Should I buy it now?

Do not mention competitors, research, content gaps, sources, or verification logic inside the final PDP copy. The **How it compares** table may identify researched alternative products, but must remain factual and neutral.

When a claim is risky, remove or soften only the unsupported portion. Preserve useful buyer guidance by replacing it with verified facts or safe selection guidance where possible. Avoid duplication, vague superlatives, marketing fluff, and overconfident installation, application, or reliability language.

### Required visible-copy structure

Use the following sections by default. Omit a section only when it does not genuinely apply; do not invent content to fill it. Do not add visible section headings beyond those listed below. If the customer style guide explicitly changes the structure—for example, by weaving applications into another section or forbidding comparison tables for resold products—follow the style guide and note the deviation in the report.

1. Product identity
2. Key specifications
3. Overview
4. Features
5. Applications
6. Compatibility and selection guidance
7. How it compares (only when the criteria below are met)
8. Technical specifications
9. Customer questions / FAQs
10. Customer concerns / objection handling

Use bullets where useful, except in **Overview**, which must be prose. Present **Technical specifications** as a two-column table: `Specification | Value + Unit`.

### How it compares

Include this section only when at least three suitable alternative products have verified, comparable specifications.

Use a concise table comparing the subject product with three to five alternatives. Compare only attributes that are material to the purchase decision and available for each product, such as dimensions, capacity, material, electrical rating, mounting method, compatibility, warranty, or included components.

- Identify configuration differences plainly; do not normalize or infer missing values.
- Leave out a field rather than using an unsupported, estimated, or non-comparable value.
- Use neutral, factual wording. This is a selection aid, not a promotional comparison.
- Do not include inline citations in the visible PDP copy. List the official supporting sources in the final **Sources** section.
- Omit the entire section when fewer than three alternatives meet the research and verification requirements.

Before finalizing, check for unsupported specifications or standards, unverified claims, unsafe setup advice, conflicting conversions, exaggerated application claims, and repetitive content.

## Create Product JSON-LD

Generate JSON-LD separately from the visible PDP copy. Include, when supported:

- Core fields: `name`, `brand`, `manufacturer`, `mpn`, `sku`, `model`, `description`, `category`, `url`, and subject-page `image`
- `additionalProperty` for accurate, useful product attributes, such as size, dimensions, weight, material, color, capacity, voltage, current, power, compatibility, mounting style, connector type, certifications, standards, and warranty

Audit the live JSON-LD captured in step 1 before writing the new block:

- Reuse the existing Product `@id` exactly, including case and relative or absolute form, so platform, review-provider (for example, Feefo), and new blocks merge into one product.
- Flag mismatches between schema and visible content, especially availability versus the visible stock message (for example, `InStock` against “Pre-order”), product name, description, and model.
- Flag duplicate `aggregateRating` blocks, empty fields (`priceValidUntil`, `shippingDetails`, `color`), relative URLs, and missing `mpn`, `gtin`, `manufacturer`, or `model`.
- Check that a GTIN/EAN belongs to the manufacturer, such as by confirming that its prefix matches the brand's other barcodes, before placing it in `gtin13`.

Include `offers` only if price and availability are dynamically maintained. Include `aggregateRating` or `review` only when supported by visible review data. Never generate fake ratings, reviews, images, availability, or unsupported values. Do not add price, stock, lead time, tariff status, or availability to visible copy or schema unless the user specifically asks.

## Deliverables

Open the report with a short **Issues to fix** list of page defects found during research—for example, conflicting warranty information, incorrect weights, the wrong model in metadata, schema mismatches, or suspect barcodes—that need action regardless of the new copy.

Then return the following, in order:

1. **Research Summary** — subject page, manufacturer sources reviewed, competitor PDPs reviewed, category sources reviewed (if used), the number of valid exact-match competitor PDPs found, and any material research limitations.
2. **Gap Validation Table** — every content element missing from the subject page, where it was verified, whether it was included, and why.
3. **Excluded Content Gaps** — discovered but unused content, with reasons.
4. **Final WYSIWYG PDP Copy** — clean, copy-ready content without HTML.
5. **HTML PDP Copy** — clean semantic HTML that mirrors the visible copy.
6. **JSON-LD Schema** — separate Product schema block.
7. **Sources** — every source URL with a brief description of its use. Do not put inline citations inside the final PDP copy.

When the customer has a project folder with earlier reports, match its file naming and layout—for example, `<model>-pdp-report.md` for deliverables 1–4 and 7, and `<model>-pdp-copy.html` for deliverables 5–6. Save the files to that folder.

## Final quality gate

- Do not fabricate or infer unsupported specifications.
- Do not use a competitor claim unless it is manufacturer-verified or corroborated by two independent competitor PDPs.
- Preserve important accurate subject-page content.
- Prefer clarity to cleverness and buyer confidence to marketing language.
