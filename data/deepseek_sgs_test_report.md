# SGS 3 Tonne Low Profile Trolley Jack (STJ3LP) — PDP Optimisation Report

**Subject PDP:** https://www.sgs-engineering.com/sgs-3-ton-low-profile-trolley-jack
**Style guide supplied:** None (default structure and UK English applied; deviation noted in §2)
**Research note:** The subject page's product body could not be read by the retrieval tooling (see limitations in §2). Gap decisions are built on the page's own metadata/dataLayer plus SGS manufacturer sources and SGS-supplied product copy for the same product code.

---

## 1. Issues to fix (Page Defects)

1. **Typo in the product name / metadata — "Tonnne".** The page meta description reads *"SGS 3 **Tonnne** Low Profile Trolley Jack STJ3LP"*. Fix in title, H1 (if present), meta description and description body.
2. **Model-code ambiguity across the SGS 3-tonne low-profile family.** The subject page sells **STJ3LP (80–500 mm)**, but SGS also sells **TJ3LP (98–535 mm)**, **TJ3LP2 (75–508 mm)**, **TJ3LP-JSR2/JSR3 bundles (98–535 mm / 75–508 mm)** and a **Pro 3.0T foot-pump jack (90–540 mm)** — all marketed as a "3 Tonne Low Profile Trolley Jack". The PDP must show **STJ3LP** and **80–500 mm** above the fold so shoppers do not compare the wrong specifications.
3. **Conflicting height figures inside SGS's own listings.** Several SGS bundle pages state **"Max Height 500"** in the attribute table while the description says **"maximum lift height 508mm"** (TJ3LP2). The subject product is **80–500 mm**; do not copy 508 mm or 535 mm onto this page.
4. **Conflicting saddle-diameter attributes.** SGS bundle pages show *Jacks Saddle Diameter 98.0 mm*, while STJ3LP is published as **110 mm**. Attribute tables appear to be shared/copied between models — audit the STJ3LP attribute set.
5. **Weight inconsistency across the SGS 3-tonne range** — 32 kg (STJ3LP), 35.5 kg (TJ3LP2), 44.5 kg (TJ3LP), 42.3–47.7 kg net on bundle pages. Confirm the on-page weight is the STJ3LP figure (32 kg) before publishing.
6. **No JSON-LD detected in the document `<head>`** (head was fully retrievable). Body-end schema could not be inspected — confirm a Product block exists, reuses the live `@id` (so the Feefo review block merges), and carries `mpn`, `sku`, `gtin13`, `manufacturer`.
7. **Warranty terms are not stated on the page metadata.** SGS's own owner's manuals describe the warranty as a **domestic** warranty; the listing says "2 years". State the term and any commercial-use limitation, or the page will generate avoidable warranty objections.
8. **Safety/stand guidance appears absent from the retrievable page text.** SGS's own guidance is explicit that a trolley jack is a lifting device, not a holding device. Add the axle-stand and pre-lift safety block.
9. **GTIN needs confirmation before schema use.** SGS-supplied listing code **5055462789104** passes GTIN-13 check-digit validation and the 5055462 prefix matches other SGS barcodes, but confirm it is the STJ3LP carton barcode, not a marketplace SKU.
10. **Price/availability differences across channels** (SGS £99.99 at time of capture; B&Q marketplace £116.98–£127.98 across snapshots). Audit only — excluded from copy and schema as instructed.

---

## 2. Research Summary

**Subject page (captured)**
- Title tag: *SGS 3 Tonne Low Profile Trolley Jack - SGS*; canonical self-referencing; `hreflang` en-GB / en-IE / x-default; language `en-GB`.
- dataLayer: `product_Id: 21325`, `product_code: STJ3LP`, `product_name: "SGS 3 Tonne Low Profile Trolley Jack"`, `product_category: "Car Jack & Trolley Stands"`, `product_value: 99.99 GBP` (price = audit note only).
- Meta description (raw): *"SGS 3 Tonnne Low Profile Trolley Jack **STJ3LP** … Elevate Your Lifting Capabilities with the SGS 3 Tonnne Low Profile Trolley Jack. Designed for heavy-duty applications, this trolley jack combines power, ma…"* — truncated by the CMS character limit.

**Verified product identity**
| Field | Value | Verified from |
|---|---|---|
| Product name | SGS 3 Tonne Low Profile Trolley Jack | Subject page title + dataLayer |
| Brand | SGS | Subject page; SGS documentation |
| Manufacturer | SGS Engineering (UK) Ltd, Unit 1, West Side Park, Raynesway, Derby, DE21 7AZ | SGS owner's manuals (EC Declaration of Conformity) |
| MPN / product code | **STJ3LP** | Subject page meta description + dataLayer; SGS-supplied listing |
| Retailer SKU | STJ3LP (SGS internal product ID 21325) | Subject page dataLayer |
| EAN / GTIN-13 | 5055462789104 (check digit valid; SGS 5055462 prefix) | SGS-supplied B&Q listing — **confirm** |
| Product type | Hydraulic low-profile trolley (garage/workshop) jack | Subject page + SGS |
| Colour / material | Black / steel | SGS-supplied listing |
| Warranty | 2 years | SGS-supplied listing; SGS site convention |

**Verified key specifications (STJ3LP)**
| Specification | Value | Source |
|---|---|---|
| Maximum capacity | 3 tonnes (3,000 kg) | SGS product copy; SGS Buyers Guide |
| Lifting range | **80 mm – 500 mm** | SGS Buyers Guide ("extends up to 500mm … as low as 80mm"); SGS product copy (Min 80 mm / Max 500 mm) |
| Pump | Double pump (dual piston) | SGS product copy |
| Piston rod diameter | 30 mm | SGS product copy |
| Saddle diameter | 110 mm | SGS product copy |
| Handle length / diameter | 1,150 mm / 34 mm | SGS product copy |
| Front wheels | Ø60 mm × 48 mm | SGS product copy |
| Rear wheels | Ø60 mm × 31 mm | SGS product copy |
| Wheel material | Nylon | SGS product copy |
| Net weight | 32 kg | SGS-supplied listing |
| Low-temperature oil operation | down to −20 °C (SGS specification) | SGS product copy |
| Warranty | 2 years | SGS-supplied listing |

**Near-match models identified and excluded from specification use**
- **TJ3LP** — 98–535 mm, 44.5 kg, base 700 × 340 mm, saddle Ø105 mm, handle 1,290 mm (SGS TJ3LP owner's manual). Excluded: different lifting range and weight.
- **TJ3LP2** — 75–508 mm, 35.5 kg (SGS TJ3LP2 owner's manual). Excluded: different lifting range.
- **TJ3PRO** — 140–525 mm (SGS product page). Excluded.
- **SGS Pro 3.0T with foot pump** — 90–540 mm, twin pump, foot pedal (SGS product page). Excluded.
- **TJ3LP-JSR2 / TJ3LP-JSR3 bundles** — jack plus axle stands; jack specs belong to TJ3LP/TJ3LP2. Excluded.
- **Amazon listing "SGS Engineering 3 Ton Low Profile Garage Trolley Jack"** — minimum height **98 mm**, i.e. TJ3LP-family, not STJ3LP. Excluded.
- **caraccessoryshop.co.uk "SGS Trolley Jack TJ3LP"** — 98–535 mm. Excluded.

**Competitor PDPs reviewed (exact match)**
- **Valid exact-match PDPs found: 1** — B&Q/DIY.com marketplace listing *"SGS 3 Ton Low Profile Trolley Jack Dual Pump 80-500mm Range Quieter Nylon Wheels"*, product code 5055462789104, "Sold & shipped by SGS Engineering". It carries SGS's own product copy and full technical specification, but it is **SGS-operated**, so it is not independent corroboration.
- eBay listing by SGS Engineering UK Ltd (#186757604266) exists for the same 80–500 mm jack but could not be retrieved (fetch error).
- **No independent third-party exact-match PDP was found** for STJ3LP. Because fewer than three valid exact-match competitor PDPs exist, competitor-content corroboration was not used; every included claim is manufacturer-verified.

**Category / contextual sources reviewed (not product evidence)**
- SGS *Trolley Jack Buyers Guide* — capacity headroom guidance (20–30%), height-calculation method, "lifting device, not holding device" safety position, 80–500 mm statement for the 3 Tonne LP jack.
- SGS *How to Lift Your Vehicle With a Trolley Jack and Axle Stands* — pre-lift checks, wheel chocks, vehicle fall-arrest, jacking-point identification.
- SGS *How to Service a Trolley Jack: Oil Top-Up & Air Purge Guide* — ISO VG 32/46 hydraulic oil, 15-pump air-purge method, troubleshooting symptoms.

**Alternatives researched for "How it compares" (official manufacturer sources)**
- **Sealey 3100TB** — 3 tonne, min saddle 95 mm, max 500 mm, Ø110 mm saddle, 700 mm length, max chassis height 180 mm, 40.5 kg, polyurethane wheels, foot pedal, 3-year guarantee (years 2–3 by registration).
- **SIP 03633** — 3 ton, 85–500 mm, net 34.45 kg / gross 36.15 kg, 500 × 345 × 700 mm, dual piston Quick-Lift, safety bypass, extra-large saddle, 2-year warranty.
- **Draper Expert 24271** — 3 tonne, 83–500 mm, saddle Ø98 mm, handle 1,150 mm, chassis 670 mm, 34 kg, nylon wheels, EN1494, 12-month warranty.
- **Draper Expert 01106** — 3 tonne, 95–500 mm, saddle Ø110 mm, handle 1,100 mm, chassis 720 mm, 40.5 kg, nylon wheels, foot pedal, EN1494, 12-month warranty.

**Material research limitations**
- The subject PDP body (description, specification table, FAQs, documents, structured data) **could not be retrieved**: direct fetches, the Irish domain, the Wayback snapshot and a raw HTML source fetch all returned only delivery/returns boilerplate or a truncated header. Consequently, "missing from the subject page" in §3 means *not observable*, and the on-page presence of some items must be checked before publishing.
- The customer style guide was **not supplied** (no path or upload), so the default section structure and UK English were used. No deviations were required, but voice rules may need re-application.
- No local site blacklist file was available in this environment; research was conducted without one. No blacklisted domain was knowingly consulted, and marketplaces were used only where SGS itself was the seller.
- Reviews/rating data for this exact PDP could not be read, so no `aggregateRating` or `review` is generated.

---

## 3. Gap Validation Table

| # | Content element | Classification | Evidence (manufacturer-verified) | Decision | Rationale |
|---|---|---|---|---|---|
| 1 | MPN **STJ3LP** shown with product name | Product Identifier | Subject page meta + dataLayer | Include | Prevents confusion with TJ3LP / TJ3LP2 / TJ3PRO |
| 2 | Lifting range **80–500 mm** | Technical Specification | SGS Buyers Guide; SGS STJ3LP product copy | Include | Core fit decision; currently only implicit in page metadata |
| 3 | Capacity **3 t (3,000 kg)** with kg conversion | Technical Specification | SGS product copy; SGS Buyers Guide | Include | Units conflict is a common buyer question |
| 4 | Net weight **32 kg** | Technical Specification | SGS-supplied STJ3LP listing | Include | Handling objection; not in page metadata |
| 5 | Saddle diameter **110 mm** | Dimension/Fit Detail | SGS STJ3LP product copy | Include | Contact area / jacking-point fit |
| 6 | Handle length **1,150 mm**, grip Ø34 mm | Technical Specification | SGS STJ3LP product copy | Include | Reach and leverage |
| 7 | Front/rear wheel sizes + **nylon** material | Material/Construction Detail | SGS STJ3LP product copy | Include | Explains noise/floor-marking benefit |
| 8 | **Double pump** (dual piston) | Feature | SGS STJ3LP product copy | Include | Primary differentiator vs single-pump jacks |
| 9 | Piston rod Ø **30 mm** | Technical Specification | SGS STJ3LP product copy | Include | Comparable spec across range |
| 10 | Low-profile design intent | Feature | SGS product copy; Buyers Guide | Include | Core purchase driver |
| 11 | Oil rated to **−20 °C** (SGS specification) | Feature | SGS STJ3LP product copy (single manufacturer source) | Include, attributed | Manufacturer-stated only; avoid presenting as third-party tested |
| 12 | **2-year warranty** | Warranty/Support Detail | SGS-supplied listing; SGS site convention | Include | Buying-confidence gap |
| 13 | Colour black / steel construction | Material/Construction Detail | SGS-supplied listing | Include | Identity confirmation |
| 14 | **EAN 5055462789104** | Schema Attribute | SGS-supplied listing; valid check digit; SGS prefix | Include in schema only, flagged | Supports product matching; needs confirmation |
| 15 | Applications: cars, SUVs/4x4s, vans, light commercial | Application | SGS product copy ("cars, trucks, SUVs"); SGS bundle copy ("cars, vans, 4x4s") | Include, narrowed | "Trucks/industrial machinery" overstates a 3 t jack |
| 16 | Capacity headroom rule (**20–30%**) and 3 t suitability band | Compatibility Guidance | SGS Buyers Guide | Include | Answers "is 3 tonnes enough?" |
| 17 | Height calculation method (clearance + jacking point + stand height) | Compatibility Guidance | SGS Buyers Guide | Include | Highest-value selection aid |
| 18 | "Lifting device, not a holding device" + axle stands required | Safety/Compliance Note | SGS Buyers Guide | Include | Safety language already in manufacturer's voice |
| 19 | Pre-lift checks (level ground, jacking points, chocks, fall arrest) | Installation/Use Guidance | SGS axle-stand guide | Include | Recurring buyer question; manufacturer-sourced |
| 20 | Oil top-up (**ISO VG 32/46**) and 15-pump air purge | Installation/Use Guidance | SGS service guide | Include | Addresses "spongy handle / won't reach height" objections |
| 21 | Not suitable for <80 mm clearance or >500 mm lift requirement | Compatibility Guidance | Derived directly from verified 80–500 mm range | Include | Prevents mis-purchase |
| 22 | FAQs on fit, capacity, stands, maintenance | FAQ | Verified items 2–6, 16–20 | Include | Consolidates decision content |
| 23 | Comparison with three alternative 3 t low-profile jacks | Comparison | Sealey 3100TB; SIP 03633; Draper 24271/01106 official pages | Include | Three verified alternatives available |

---

## 4. Excluded Content Gaps

| Content element | Source seen | Reason for exclusion |
|---|---|---|
| "Minimum height 75 mm / maximum 508 mm" | SGS TJ3LP2 bundles | Wrong model — STJ3LP is 80–500 mm |
| "98 mm – 535 mm lifting range", 44.5 kg, Ø105 mm saddle, 1,290 mm handle | SGS TJ3LP manual and bundles | Wrong model (TJ3LP) |
| "90–540 mm, foot pedal, twin pump" | SGS Pro 3.0T foot-pump jack | Different product |
| "TUV/GS" and "CE" conformance statements | SGS axle-stand bundle copy | Statement attaches to the axle stands in that bundle; not verified for STJ3LP |
| **EN1494** compliance | Competitor pages (Draper, SIP) | Not stated by SGS for STJ3LP — cannot be claimed |
| "Protect workshop floors from damage" (nylon wheels) | SGS product copy | Absolute claim; softened to "helps reduce noise and marking" |
| "Support industrial equipment and machinery", "lift trucks" | SGS product copy | Exaggerated application claim for a 3 t trolley jack |
| Rubber saddle pad included | SGS TJ3LP/bundle copy | Not listed in STJ3LP's published specification — needs SGS confirmation |
| "Six pumps to full height" | Draper (competitor) | Competitor-only, model-specific |
| Customer review themes (castor failure, jack pad detaching, oil seepage) | Forums / aggregated reviews | Not manufacturer-verified and not tied to STJ3LP; not used as claims. Addressed only as neutral maintenance guidance |
| Price, stock, lead time, promotions, finance offers, "SGS Protect" add-on pricing | Subject page | Dynamic/commercial data — audit notes only |
| Ratings/`aggregateRating` | Feefo integration implied | Review data for this exact PDP not retrievable — no rating generated |

---

## 5. Final WYSIWYG PDP Copy

### Product identity
**SGS 3 Tonne Low Profile Trolley Jack**
Brand: SGS · Manufacturer: SGS Engineering (UK) Ltd · Product code: STJ3LP · EAN: 5055462789104 · Type: Hydraulic low-profile trolley jack · Colour: Black · Material: Steel · Warranty: 2 years

### Key specifications
- Maximum capacity: 3 tonnes (3,000 kg)
- Lifting range: 80 mm to 500 mm
- Pump: double pump (dual piston)
- Saddle diameter: 110 mm
- Handle length: 1,150 mm
- Net weight: 32 kg
- Wheels: nylon — front 60 mm × 48 mm, rear 60 mm × 31 mm

### Overview
The SGS 3 Tonne Low Profile Trolley Jack (STJ3LP) is a hydraulic garage jack rated to 3 tonnes (3,000 kg), with a lifting range of 80 mm to 500 mm. The low-profile chassis is designed to reach jacking points on vehicles with limited ground clearance, and the double pump is intended to raise the saddle quickly with less pumping effort. Nylon wheels are specified to reduce noise in use and to help avoid marking workshop floors. The jack has a 110 mm saddle, a 1,150 mm handle and a net weight of 32 kg, and is covered by a 2-year warranty. It is intended for lifting cars, SUVs, 4x4s, vans and light commercial vehicles during maintenance and repair. Like any trolley jack, it is a lifting device rather than a holding device: once the vehicle is raised, it must be supported on axle stands before anyone works underneath it.

### Features
- **3-tonne (3,000 kg) capacity** — suits larger cars, SUVs, 4x4s and light commercial vehicles within the rated load.
- **80 mm minimum height** — for jacking points on vehicles with reduced ground clearance.
- **500 mm maximum height** — allows the vehicle to be raised far enough to place axle stands.
- **Double pump (dual piston)** — raises the saddle quickly with reduced pumping effort.
- **110 mm saddle** — presents a broad contact face at the jacking point.
- **Nylon wheels (60 mm front and rear)** — quieter running and less likely to mark workshop floors than steel wheels.
- **1,150 mm handle with 34 mm grip** — leverage for pumping and for positioning the jack.
- **Steel construction, black finish** — for garage and workshop use.
- **2-year warranty**.

### Applications
- Wheel removal and tyre changes.
- Brake, suspension and exhaust work where the vehicle must be raised and supported.
- Routine servicing and inspection in home garages and workshops.
- Lifting cars, SUVs, 4x4s, vans and light commercial vehicles that fall within the 3-tonne rating and the 80–500 mm height range.

### Compatibility and selection guidance
- **Check clearance first.** The jack's lowest position is 80 mm. Measure the lowest point you need the jack to pass under; if your vehicle sits lower than that, this jack is not suitable.
- **Check lift height.** Add the height of your vehicle's jacking point to the minimum height of your axle stands. The total must be **below 500 mm**, or the jack will not raise the vehicle far enough to seat the stands.
- **Check capacity.** SGS advises choosing a jack rated 20–30% above the weight of the vehicle. A 3-tonne jack corresponds to SGS's guidance band for larger cars, SUVs and 4x4s; vehicles above 3 tonnes require a higher-rated jack.
- **Use on a firm, level surface only** — concrete or a solid garage floor. Do not use on gravel, slopes or uneven ground.
- **Always support the vehicle on axle stands** before working underneath it, and chock the wheels that remain on the ground.
- **Not suitable for** vehicles needing more than 500 mm of lift at the jacking point, or less than 80 mm of clearance.

### How it compares
Specifications below are as published by each manufacturer. Configuration differences are shown rather than normalised; where a manufacturer does not publish a value it is marked "not published".

| Product | Capacity | Lifting range | Saddle diameter | Handle length | Net weight | Wheels | Warranty | Published standard |
|---|---|---|---|---|---|---|---|---|
| **SGS 3 Tonne Low Profile Trolley Jack (STJ3LP)** | 3 t (3,000 kg) | 80–500 mm | 110 mm | 1,150 mm | 32 kg | Nylon | 2 years | Not published |
| **Sealey 3100TB Low Profile Professional Trolley Jack with Rocket Lift, 3 Tonne** | 3 t | 95–500 mm | 110 mm | Not published | 40.5 kg | Polyurethane | 3 years (years 2–3 by registration) | Not published |
| **SIP 03633 3 TON Low-Profile Trolley Jack** | 3 t | 85–500 mm | "Extra-large" (diameter not published) | Not published | 34.45 kg | Wheels and castors (material not published) | 2 years | Not published |
| **Draper Expert 24271 Low Profile Garage Trolley Jack, 3 Tonne** | 3 t | 83–500 mm | 98 mm | 1,150 mm | 34 kg | Nylon | 12 months | EN1494 |
| **Draper Expert 01106 Professional Low Profile Garage Trolley Jack, 3 Tonne** | 3 t (3,000 kg) | 95–500 mm | 110 mm | 1,100 mm | 40.5 kg | Nylon | 12 months | EN1494 |

Configuration differences that affect selection: the Sealey and Draper 01106 models add a foot pedal; the SIP and Sealey units use lift-assist pump systems (Quick-Lift / Rocket Lift); the Draper 01106 and Sealey units weigh around 40.5 kg against 32 kg for STJ3LP; the two Draper models are the only ones in this group that publish an EN1494 reference.

### Technical specifications

| Specification | Value + unit |
|---|---|
| Maximum capacity | 3 tonnes (3,000 kg) |
| Lifting range | 80 mm – 500 mm |
| Pump type | Double pump (dual piston) |
| Piston rod diameter | 30 mm |
| Saddle diameter | 110 mm |
| Handle length | 1,150 mm |
| Handle diameter | 34 mm |
| Front wheel diameter × width | 60 mm × 48 mm |
| Rear wheel diameter × width | 60 mm × 31 mm |
| Wheel material | Nylon |
| Construction | Steel |
| Colour | Black |
| Net weight | 32 kg |
| Hydraulic oil low-temperature operation | Down to −20 °C (SGS specification) |
| Warranty | 2 years |
| Product code | STJ3LP |
| EAN | 5055462789104 |

### Customer questions / FAQs
**Will this jack fit under a lowered car?**
The jack's lowest position is 80 mm. Measure the lowest part of the vehicle you need to pass under, and compare it with 80 mm before buying.

**Is a 3-tonne jack enough for my vehicle?**
3 tonnes is 3,000 kg. SGS recommends a jack rated 20–30% above the vehicle's weight, and places 3-tonne jacks in the band for larger cars, SUVs and 4x4s. Vehicles over 3 tonnes need a higher rating.

**How high will it lift?**
To 500 mm. That figure has to cover the height of the jacking point plus the minimum height of your axle stands.

**Can I get under the car with the jack alone?**
No. A trolley jack is a lifting device, not a holding device. Once the vehicle is raised, lower it onto axle stands before working underneath.

**How quickly does it reach full height?**
The double pump raises the saddle with reduced pumping effort. SGS does not publish a pump-stroke count for this model.

**What hydraulic oil does it use?**
SGS specifies ISO VG 32 or ISO VG 46 hydraulic jack oil. Never use engine oil or brake fluid.

**The handle feels spongy and it won't reach full height — what should I do?**
This usually indicates low oil or trapped air. Top the reservoir up to just below the filler hole, then open the release valve and pump the handle about 15 times to purge air, and retest.

**Can I use it on a gravel drive?**
No. Use it on a firm, level surface such as concrete or a solid garage floor.

**What is the warranty?**
2 years. SGS owner's manuals describe the warranty on its 3-tonne low-profile jacks as a domestic warranty provided directly by SGS Engineering — confirm commercial-use cover with SGS before buying for a business.

### Customer concerns / objection handling
- **"It's heavy."** Net weight is 32 kg. Position it on its wheels and roll it rather than carrying it, and keep it on the same level as the vehicle.
- **"Will it be stable once lifted?"** Stability depends on using a firm, level surface, locating the saddle fully on a manufacturer-designated jacking point, and seating the raised vehicle on axle stands. SGS advises against working under a load held only by a jack.
- **"Do I need to buy axle stands as well?"** Yes. SGS's own guidance is that the jack lifts, the stands hold; wheels that stay on the ground should be chocked.
- **"Will the wheels damage my floor?"** The jack runs on nylon wheels, which SGS specifies to reduce noise and to help avoid marking workshop floors. Nylon is not damage-proof on every surface — check the floor you intend to use.
- **"It won't lift to full height anymore."** Check oil level and purge trapped air before assuming a fault; SGS publishes a step-by-step top-up and bleed procedure.
- **"Can I use it every day in a workshop?"** It is a 3-tonne steel jack with a 2-year warranty. If the jack will be in daily commercial use, confirm the warranty terms with SGS and compare against models that publish a commercial warranty.

---

## 6. HTML PDP Copy

```html
<section class="pdp" aria-labelledby="product-title">
  <h1 id="product-title">SGS 3 Tonne Low Profile Trolley Jack</h1>

  <section class="pdp-identity" aria-labelledby="identity-heading">
    <h2 id="identity-heading">Product identity</h2>
    <ul>
      <li><strong>Brand:</strong> SGS</li>
      <li><strong>Manufacturer:</strong> SGS Engineering (UK) Ltd</li>
      <li><strong>Product code:</strong> STJ3LP</li>
      <li><strong>EAN:</strong> 5055462789104</li>
      <li><strong>Type:</strong> Hydraulic low-profile trolley jack</li>
      <li><strong>Colour:</strong> Black</li>
      <li><strong>Material:</strong> Steel</li>
      <li><strong>Warranty:</strong> 2 years</li>
    </ul>
  </section>

  <section class="pdp-key-specs" aria-labelledby="key-specs-heading">
    <h2 id="key-specs-heading">Key specifications</h2>
    <ul>
      <li>Maximum capacity: 3 tonnes (3,000 kg)</li>
      <li>Lifting range: 80 mm to 500 mm</li>
      <li>Pump: double pump (dual piston)</li>
      <li>Saddle diameter: 110 mm</li>
      <li>Handle length: 1,150 mm</li>
      <li>Net weight: 32 kg</li>
      <li>Wheels: nylon &mdash; front 60 mm &times; 48 mm, rear 60 mm &times; 31 mm</li>
    </ul>
  </section>

  <section class="pdp-overview" aria-labelledby="overview-heading">
    <h2 id="overview-heading">Overview</h2>
    <p>The SGS 3 Tonne Low Profile Trolley Jack (STJ3LP) is a hydraulic garage jack rated to 3 tonnes (3,000 kg), with a lifting range of 80&nbsp;mm to 500&nbsp;mm. The low-profile chassis is designed to reach jacking points on vehicles with limited ground clearance, and the double pump is intended to raise the saddle quickly with less pumping effort. Nylon wheels are specified to reduce noise in use and to help avoid marking workshop floors. The jack has a 110&nbsp;mm saddle, a 1,150&nbsp;mm handle and a net weight of 32&nbsp;kg, and is covered by a 2-year warranty. It is intended for lifting cars, SUVs, 4x4s, vans and light commercial vehicles during maintenance and repair. Like any trolley jack, it is a lifting device rather than a holding device: once the vehicle is raised, it must be supported on axle stands before anyone works underneath it.</p>
  </section>

  <section class="pdp-features" aria-labelledby="features-heading">
    <h2 id="features-heading">Features</h2>
    <ul>
      <li><strong>3-tonne (3,000&nbsp;kg) capacity</strong> &mdash; suits larger cars, SUVs, 4x4s and light commercial vehicles within the rated load.</li>
      <li><strong>80&nbsp;mm minimum height</strong> &mdash; for jacking points on vehicles with reduced ground clearance.</li>
      <li><strong>500&nbsp;mm maximum height</strong> &mdash; allows the vehicle to be raised far enough to place axle stands.</li>
      <li><strong>Double pump (dual piston)</strong> &mdash; raises the saddle quickly with reduced pumping effort.</li>
      <li><strong>110&nbsp;mm saddle</strong> &mdash; presents a broad contact face at the jacking point.</li>
      <li><strong>Nylon wheels (60&nbsp;mm front and rear)</strong> &mdash; quieter running and less likely to mark workshop floors than steel wheels.</li>
      <li><strong>1,150&nbsp;mm handle with 34&nbsp;mm grip</strong> &mdash; leverage for pumping and for positioning the jack.</li>
      <li><strong>Steel construction, black finish</strong> &mdash; for garage and workshop use.</li>
      <li><strong>2-year warranty.</strong></li>
    </ul>
  </section>

  <section class="pdp-applications" aria-labelledby="applications-heading">
    <h2 id="applications-heading">Applications</h2>
    <ul>
      <li>Wheel removal and tyre changes.</li>
      <li>Brake, suspension and exhaust work where the vehicle must be raised and supported.</li>
      <li>Routine servicing and inspection in home garages and workshops.</li>
      <li>Lifting cars, SUVs, 4x4s, vans and light commercial vehicles that fall within the 3-tonne rating and the 80&ndash;500&nbsp;mm height range.</li>
    </ul>
  </section>

  <section class="pdp-compatibility" aria-labelledby="compatibility-heading">
    <h2 id="compatibility-heading">Compatibility and selection guidance</h2>
    <ul>
      <li><strong>Check clearance first.</strong> The jack's lowest position is 80&nbsp;mm. Measure the lowest point you need the jack to pass under; if your vehicle sits lower than that, this jack is not suitable.</li>
      <li><strong>Check lift height.</strong> Add the height of your vehicle's jacking point to the minimum height of your axle stands. The total must be <strong>below 500&nbsp;mm</strong>, or the jack will not raise the vehicle far enough to seat the stands.</li>
      <li><strong>Check capacity.</strong> SGS advises choosing a jack rated 20&ndash;30% above the weight of the vehicle. A 3-tonne jack corresponds to SGS's guidance band for larger cars, SUVs and 4x4s; vehicles above 3 tonnes require a higher-rated jack.</li>
      <li><strong>Use on a firm, level surface only</strong> &mdash; concrete or a solid garage floor. Do not use on gravel, slopes or uneven ground.</li>
      <li><strong>Always support the vehicle on axle stands</strong> before working underneath it, and chock the wheels that remain on the ground.</li>
      <li><strong>Not suitable for</strong> vehicles needing more than 500&nbsp;mm of lift at the jacking point, or less than 80&nbsp;mm of clearance.</li>
    </ul>
  </section>

  <section class="pdp-comparison" aria-labelledby="comparison-heading">
    <h2 id="comparison-heading">How it compares</h2>
    <p>Specifications below are as published by each manufacturer. Configuration differences are shown rather than normalised; where a manufacturer does not publish a value it is marked &ldquo;not published&rdquo;.</p>
    <table>
      <caption>3-tonne low-profile trolley jacks &mdash; published specifications</caption>
      <thead>
        <tr>
          <th scope="col">Product</th>
          <th scope="col">Capacity</th>
          <th scope="col">Lifting range</th>
          <th scope="col">Saddle diameter</th>
          <th scope="col">Handle length</th>
          <th scope="col">Net weight</th>
          <th scope="col">Wheels</th>
          <th scope="col">Warranty</th>
          <th scope="col">Published standard</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">SGS 3 Tonne Low Profile Trolley Jack (STJ3LP)</th>
          <td>3&nbsp;t (3,000&nbsp;kg)</td>
          <td>80&ndash;500&nbsp;mm</td>
          <td>110&nbsp;mm</td>
          <td>1,150&nbsp;mm</td>
          <td>32&nbsp;kg</td>
          <td>Nylon</td>
          <td>2 years</td>
          <td>Not published</td>
        </tr>
        <tr>
          <th scope="row">Sealey 3100TB Low Profile Professional Trolley Jack with Rocket Lift, 3 Tonne</th>
          <td>3&nbsp;t</td>
          <td>95&ndash;500&nbsp;mm</td>
          <td>110&nbsp;mm</td>
          <td>Not published</td>
          <td>40.5&nbsp;kg</td>
          <td>Polyurethane</td>
          <td>3 years (years 2&ndash;3 by registration)</td>
          <td>Not published</td>
        </tr>
        <tr>
          <th scope="row">SIP 03633 3 TON Low-Profile Trolley Jack</th>
          <td>3&nbsp;t</td>
          <td>85&ndash;500&nbsp;mm</td>
          <td>&ldquo;Extra-large&rdquo; (diameter not published)</td>
          <td>Not published</td>
          <td>34.45&nbsp;kg</td>
          <td>Wheels and castors (material not published)</td>
          <td>2 years</td>
          <td>Not published</td>
        </tr>
        <tr>
          <th scope="row">Draper Expert 24271 Low Profile Garage Trolley Jack, 3 Tonne</th>
          <td>3&nbsp;t</td>
          <td>83&ndash;500&nbsp;mm</td>
          <td>98&nbsp;mm</td>
          <td>1,150&nbsp;mm</td>
          <td>34&nbsp;kg</td>
          <td>Nylon</td>
          <td>12 months</td>
          <td>EN1494</td>
        </tr>
        <tr>
          <th scope="row">Draper Expert 01106 Professional Low Profile Garage Trolley Jack, 3 Tonne</th>
          <td>3&nbsp;t (3,000&nbsp;kg)</td>
          <td>95&ndash;500&nbsp;mm</td>
          <td>110&nbsp;mm</td>
          <td>1,100&nbsp;mm</td>
          <td>40.5&nbsp;kg</td>
          <td>Nylon</td>
          <td>12 months</td>
          <td>EN1494</td>
        </tr>
      </tbody>
    </table>
    <p>Configuration differences that affect selection: the Sealey and Draper 01106 models add a foot pedal; the SIP and Sealey units use lift-assist pump systems (Quick-Lift / Rocket Lift); the Draper 01106 and Sealey units weigh around 40.5&nbsp;kg against 32&nbsp;kg for STJ3LP; the two Draper models are the only ones in this group that publish an EN1494 reference.</p>
  </section>

  <section class="pdp-specifications" aria-labelledby="specifications-heading">
    <h2 id="specifications-heading">Technical specifications</h2>
    <table>
      <caption>STJ3LP technical specifications</caption>
      <thead>
        <tr>
          <th scope="col">Specification</th>
          <th scope="col">Value + unit</th>
        </tr>
      </thead>
      <tbody>
        <tr><th scope="row">Maximum capacity</th><td>3 tonnes (3,000&nbsp;kg)</td></tr>
        <tr><th scope="row">Lifting range</th><td>80&nbsp;mm &ndash; 500&nbsp;mm</td></tr>
        <tr><th scope="row">Pump type</th><td>Double pump (dual piston)</td></tr>
        <tr><th scope="row">Piston rod diameter</th><td>30&nbsp;mm</td></tr>
        <tr><th scope="row">Saddle diameter</th><td>110&nbsp;mm</td></tr>
        <tr><th scope="row">Handle length</th><td>1,150&nbsp;mm</td></tr>
        <tr><th scope="row">Handle diameter</th><td>34&nbsp;mm</td></tr>
        <tr><th scope="row">Front wheel diameter &times; width</th><td>60&nbsp;mm &times; 48&nbsp;mm</td></tr>
        <tr><th scope="row">Rear wheel diameter &times; width</th><td>60&nbsp;mm &times; 31&nbsp;mm</td></tr>
        <tr><th scope="row">Wheel material</th><td>Nylon</td></tr>
        <tr><th scope="row">Construction</th><td>Steel</td></tr>
        <tr><th scope="row">Colour</th><td>Black</td></tr>
        <tr><th scope="row">Net weight</th><td>32&nbsp;kg</td></tr>
        <tr><th scope="row">Hydraulic oil low-temperature operation</th><td>Down to &minus;20&nbsp;&deg;C (SGS specification)</td></tr>
        <tr><th scope="row">Warranty</th><td>2 years</td></tr>
        <tr><th scope="row">Product code</th><td>STJ3LP</td></tr>
        <tr><th scope="row">EAN</th><td>5055462789104</td></tr>
      </tbody>
    </table>
  </section>

  <section class="pdp-faqs" aria-labelledby="faqs-heading">
    <h2 id="faqs-heading">Customer questions / FAQs</h2>

    <h3>Will this jack fit under a lowered car?</h3>
    <p>The jack's lowest position is 80&nbsp;mm. Measure the lowest part of the vehicle you need to pass under, and compare it with 80&nbsp;mm before buying.</p>

    <h3>Is a 3-tonne jack enough for my vehicle?</h3>
    <p>3 tonnes is 3,000&nbsp;kg. SGS recommends a jack rated 20&ndash;30% above the vehicle's weight, and places 3-tonne jacks in the band for larger cars, SUVs and 4x4s. Vehicles over 3 tonnes need a higher rating.</p>

    <h3>How high will it lift?</h3>
    <p>To 500&nbsp;mm. That figure has to cover the height of the jacking point plus the minimum height of your axle stands.</p>

    <h3>Can I get under the car with the jack alone?</h3>
    <p>No. A trolley jack is a lifting device, not a holding device. Once the vehicle is raised, lower it onto axle stands before working underneath.</p>

    <h3>How quickly does it reach full height?</h3>
    <p>The double pump raises the saddle with reduced pumping effort. SGS does not publish a pump-stroke count for this model.</p>

    <h3>What hydraulic oil does it use?</h3>
    <p>SGS specifies ISO VG&nbsp;32 or ISO VG&nbsp;46 hydraulic jack oil. Never use engine oil or brake fluid.</p>

    <h3>The handle feels spongy and it won't reach full height &mdash; what should I do?</h3>
    <p>This usually indicates low oil or trapped air. Top the reservoir up to just below the filler hole, then open the release valve and pump the handle about 15 times to purge air, and retest.</p>

    <h3>Can I use it on a gravel drive?</h3>
    <p>No. Use it on a firm, level surface such as concrete or a solid garage floor.</p>

    <h3>What is the warranty?</h3>
    <p>2 years. SGS owner's manuals describe the warranty on its 3-tonne low-profile jacks as a domestic warranty provided directly by SGS Engineering &mdash; confirm commercial-use cover with SGS before buying for a business.</p>
  </section>

  <section class="pdp-concerns" aria-labelledby="concerns-heading">
    <h2 id="concerns-heading">Customer concerns / objection handling</h2>
    <ul>
      <li><strong>&ldquo;It's heavy.&rdquo;</strong> Net weight is 32&nbsp;kg. Position it on its wheels and roll it rather than carrying it, and keep it on the same level as the vehicle.</li>
      <li><strong>&ldquo;Will it be stable once lifted?&rdquo;</strong> Stability depends on using a firm, level surface, locating the saddle fully on a manufacturer-designated jacking point, and seating the raised vehicle on axle stands. SGS advises against working under a load held only by a jack.</li>
      <li><strong>&ldquo;Do I need to buy axle stands as well?&rdquo;</strong> Yes. SGS's own guidance is that the jack lifts, the stands hold; wheels that stay on the ground should be chocked.</li>
      <li><strong>&ldquo;Will the wheels damage my floor?&rdquo;</strong> The jack runs on nylon wheels, which SGS specifies to reduce noise and to help avoid marking workshop floors. Nylon is not damage-proof on every surface &mdash; check the floor you intend to use.</li>
      <li><strong>&ldquo;It won't lift to full height anymore.&rdquo;</strong> Check oil level and purge trapped air before assuming a fault; SGS publishes a step-by-step top-up and bleed procedure.</li>
      <li><strong>&ldquo;Can I use it every day in a workshop?&rdquo;</strong> It is a 3-tonne steel jack with a 2-year warranty. If the jack will be in daily commercial use, confirm the warranty terms with SGS and compare against models that publish a commercial warranty.</li>
    </ul>
  </section>
</section>
```

---

## 7. JSON-LD Schema

> **Before publishing:** replace `@id` with the **exact** live Product `@id` on the page (case and relative/absolute form must match) so this block merges with the existing product node and the Feefo review widget. Confirm `image` URLs from the live PDP, confirm the GTIN is the STJ3LP carton barcode, and do not add `offers` unless price and availability are dynamically maintained. No `aggregateRating` or `review` is included because review data for this exact PDP could not be verified.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "@id": "https://www.sgs-engineering.com/sgs-3-ton-low-profile-trolley-jack#product",
  "name": "SGS 3 Tonne Low Profile Trolley Jack",
  "brand": {
    "@type": "Brand",
    "name": "SGS"
  },
  "manufacturer": {
    "@type": "Organization",
    "name": "SGS Engineering (UK) Ltd",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Unit 1, West Side Park, Raynesway",
      "addressLocality": "Derby",
      "postalCode": "DE21 7AZ",
      "addressCountry": "GB"
    }
  },
  "mpn": "STJ3LP",
  "sku": "STJ3LP",
  "model": "STJ3LP",
  "gtin13": "5055462789104",
  "description": "Hydraulic low-profile trolley jack rated to 3 tonnes (3,000 kg) with a lifting range of 80 mm to 500 mm. Double pump (dual piston), 110 mm saddle, 1,150 mm handle and nylon wheels. Intended for lifting cars, SUVs, 4x4s, vans and light commercial vehicles within the rated capacity; the raised vehicle must be supported on axle stands before working underneath.",
  "category": "Car Jack & Trolley Stands",
  "url": "https://www.sgs-engineering.com/sgs-3-ton-low-profile-trolley-jack",
  "image": [
    "https://www.sgs-engineering.com/content/images/product/sgs-3-ton-low-profile-trolley-jack.jpg"
  ],
  "additionalProperty": [
    {
      "@type": "PropertyValue",
      "name": "Maximum lifting capacity",
      "value": "3 tonnes (3,000 kg)"
    },
    {
      "@type": "PropertyValue",
      "name": "Lifting range",
      "value": "80 mm to 500 mm"
    },
    {
      "@type": "PropertyValue",
      "name": "Pump type",
      "value": "Double pump (dual piston)"
    },
    {
      "@type": "PropertyValue",
      "name": "Piston rod diameter",
      "value": "30 mm"
    },
    {
      "@type": "PropertyValue",
      "name": "Saddle diameter",
      "value": "110 mm"
    },
    {
      "@type": "PropertyValue",
      "name": "Handle length",
      "value": "1150 mm"
    },
    {
      "@type": "PropertyValue",
      "name": "Front wheel dimensions",
      "value": "60 mm diameter x 48 mm width"
    },
    {
      "@type": "PropertyValue",
      "name": "Rear wheel dimensions",
      "value": "60 mm diameter x 31 mm width"
    },
    {
      "@type": "PropertyValue",
      "name": "Wheel material",
      "value": "Nylon"
    },
    {
      "@type": "PropertyValue",
      "name": "Material",
      "value": "Steel"
    },
    {
      "@type": "PropertyValue",
      "name": "Colour",
      "value": "Black"
    },
    {
      "@type": "PropertyValue",
      "name": "Net weight",
      "value": "32 kg"
    },
    {
      "@type": "PropertyValue",
      "name": "Warranty",
      "value": "2 years"
    },
    {
      "@type": "PropertyValue",
      "name": "Product code",
      "value": "STJ3LP"
    }
  ]
}
```

*Schema audit flags:* no JSON-LD was present in `<head>`; body-end schema unverified. Ensure there is only **one** Product node, one `aggregateRating`, no empty `priceValidUntil` / `shippingDetails` / `color` properties, absolute image URLs, and that any `availability` value matches the visible stock message (e.g. `InStock` must not sit against a "pre-order" banner).

---

## 8. Sources

**Subject PDP**
1. https://www.sgs-engineering.com/sgs-3-ton-low-profile-trolley-jack — subject page: title, meta description, canonical/hreflang, dataLayer product code STJ3LP, product name, category, price (audit only). Body content not retrievable.
2. http://web.archive.org/web/20250913014939/https://www.sgs-engineering.com/sgs-3-ton-low-profile-trolley-jack — archived snapshot used to confirm the same retrieval limitation and that the URL/product identity is stable.

**Manufacturer sources (SGS)**
3. https://www.sgs-engineering.com/help-advice/trolley-jack-buyers-guide — "3 Tonne LP Trolley Jack extends up to 500mm … as low as 80mm"; capacity headroom 20–30%; height calculation method; "lifting device, not a holding device".
4. https://www.sgs-engineering.com/help-advice/how-to-use-axle-stands — pre-lift checks, jacking points, wheel chocks, fall-arrest, axle-stand requirement.
5. https://www.sgs-engineering.com/help-advice/how-to-bleed-or-air-purge-a-trolley-jack — ISO VG 32/46 oil specification, oil level, 15-pump air purge, spongy-handle diagnosis.
6. https://www.diy.com/departments/sgs-3-ton-low-profile-trolley-jack-dual-pump-80-500mm-range-quieter-nylon-wheels/5055462789104_BQ.prd — SGS-supplied product copy for **STJ3LP** ("Sold & shipped by SGS Engineering"): full description, 80/500 mm, 110 mm saddle, 1,150 mm handle, 34 mm grip, 30 mm piston rod, wheel dimensions, nylon wheels, −20 °C oil, 32 kg, product code/EAN, 2-year guarantee.
7. https://www.sgs-engineering.com/sgs-3-tonne-low-profile-trolley-jack-3-tonne-axle-stands — SGS TJ3LP2 bundle page, used only to document the 500 mm vs 508 mm and 98 mm saddle attribute conflicts (near-match model, excluded from spec use).
8. https://www.sgs-engineering.com/tj3lp-low-profile-garage-trolley-jack — SGS TJ3LP page (98–535 mm), used to document model-family ambiguity (excluded from spec use).
9. https://www.sgs-engineering.com/sgs-pro-3.0t-low-profile-trolley-jack-with-foot-pump — SGS Pro 3.0T foot-pump jack (90–540 mm), used to document model-family ambiguity (excluded).
10. https://www.manualslib.com/manual/3106902/Sgs-Tj3lp.html?page=2 — SGS TJ3LP owner's manual: 98 mm closed / 535 mm extended, 44.5 kg, saddle Ø105 mm, handle 1,290 mm, safety wording (near-match, excluded from spec use).
11. https://www.manualslib.com/manual/3731620/Sgs-Tj3lp2.html — SGS TJ3LP2 owner's manual: 75 mm / 508 mm, 35.5 kg, 24-month domestic warranty, CE mark and EC Declaration of Conformity, SGS Engineering (UK) Ltd Derby address (near-match, excluded from spec use).

**Competitor PDPs (exact match)**
12. https://www.diy.com/departments/sgs-3-ton-low-profile-trolley-jack-dual-pump-80-500mm-range-quieter-nylon-wheels/5055462789104_BQ.prd — the only valid exact-match PDP found (B&Q marketplace, SGS as seller). Used as corroboration of STJ3LP data; not independent.

**Alternatives (official manufacturer sources, for "How it compares")**
13. https://www.sealey.co.uk/product/5637781550/low-profile-professional-trolley-jack-with-rocket-lift-3-tonne — Sealey 3100TB: 95–500 mm, Ø110 mm saddle, 700 mm length, 180 mm chassis height, 40.5 kg, polyurethane wheels, foot pedal, 3-year guarantee terms.
14. https://www.sip-group.com/product/sip-3-ton--low-profile-trolley-jack/03633 — SIP 03633: 85–500 mm, 34.45 kg net / 36.15 kg gross, product dimensions, dual piston Quick-Lift, safety bypass, extra-large saddle, 2-year warranty.
15. https://www.drapertools.com/product/24271/draper-expert-professional-low-profile-garage-trolley-jack-3-tonne/ — Draper Expert 24271: 83–500 mm, Ø98 mm saddle, 1,150 mm handle, 670 mm chassis, 34 kg, nylon wheels, EN1494, 12-month warranty.
16. https://www.drapertools.com/product/01106/draper-expert-professional-low-profile-garage-trolley-jack-3-tonne-blue/ — Draper Expert 01106: 95–500 mm, Ø110 mm saddle, 1,100 mm handle, 720 mm chassis, 40.5 kg, nylon wheels, foot pedal, EN1494, 12-month warranty.

**Category/context sources (not used as product evidence)**
17. https://www.sgs-engineering.com/help-advice/how-to-use-axle-stands — also used for category-level lifting practice (vehicle data plate, wheel chocks, stand selection).
18. https://www.sgs-engineering.com/help-advice/trolley-jack-buyers-guide — also used for category-level selection factors (materials, professional vs home use, bundles).