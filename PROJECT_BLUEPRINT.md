# Kasukabe Gap Patrol — Complete Project Blueprint

> **One-line pitch:** A Shinchan-themed research detective that helps people discover what scattered online sources leave unclear, conflicting, or out of date—and shows exactly what to verify next.

## 1. Project identity

- **Project title:** Kasukabe Gap Patrol — Digital Dark Spot Detective
- **Product type:** Evidence-first, AI-assisted research and decision-support web application
- **Hackathon problem:** Digital Dark Spot
- **Primary user:** Someone who needs to make a decision using information scattered across websites, notices, PDFs, and FAQs
- **Signature experience:** Build a research case, pin source evidence to a 3D Kasukabe investigation board, inspect missing or conflicting details, and leave with a verification mission
- **Theme requirement:** Shinchan must be unmistakable across the product. A real-time 3D Shinchan/fan-model is a required part of the experience, not an optional decoration.

The existing `index.html` is only an early static concept. Treat this blueprint as the specification for the complete project. The end product should be a functional application with persistent cases, source ingestion, analysis, evidence navigation, and a working 3D scene.

## 2. Challenge brief translated into product requirements

The organizer's problem statement describes information spread across multiple sources, where users may find summaries but still not know what is missing, which details conflict, whether a source is old, or what to verify next. Its expected workflow is to enter a topic or question, review several sources, find unanswered questions and contradictions, flag dated information, and create a prioritized checklist. The interface must distinguish what a source actually says from an AI-generated suggestion.

The product therefore needs all of these visible capabilities:

1. A user can create a research case from a question, goal, and relevant context.
2. A user can add multiple sources as URLs, pasted excerpts, or uploaded documents.
3. Each source has provenance: title, URL or upload name, publisher if known, publication date if present, retrieval date, and relevant page/section.
4. The app presents a structured snapshot of the sources, with traceable source references.
5. It identifies possible information gaps and unanswered questions.
6. It detects potential conflicts between claims about the same subject, scope, and time period.
7. It flags source age and date ambiguity without pretending age alone proves a source is wrong.
8. It creates an editable, prioritized verification plan.
9. Every important finding can be opened to inspect its supporting passages.
10. Evidence and AI suggestions are visually and semantically distinct.
11. A sample case makes the full demo flow usable even when the user has no API key or source files.

### Organizer requirements versus submission announcement

The attached problem statement names **Unista** as the submission platform and lists a final deadline of **1 November 2026 at 5:00 PM**. The separate announcement supplied by the participant says **UNSTOP only**, gives the mandatory fields as title, description, and GitHub repository link, and says deployment, demo video, and PPT are optional. Those platform instructions conflict. Follow the latest direct organizer announcement for the actual submission workflow; the implementation of this product does not depend on either platform.

## 3. Product principles

### Evidence before confidence

Every factual statement in a report should be traceable to a source passage. If a statement is an inference, mark it as an inference. If no passage supports it, do not present it as fact.

### Missing from this case does not mean nonexistent

Use language such as “not found in the reviewed sources” or “verify whether a current rule exists.” Never claim that a policy does not exist solely because the ingested sources omit it.

### The user stays in control

Let people edit suggested requirements, exclude sources, dismiss findings with a reason, edit checklist items, and rerun analysis. Do not make a decision for them.

### Sources are not interchangeable

Show dates, source type, publisher, and links. An official current notice and an undated forum comment should not appear as equally authoritative. Avoid a single unexplained “trust score.”

### Shinchan is the host of a useful tool

The character, 3D setting, humor, and colors should make the workflow memorable. The theme must never hide evidence, make the app childish to navigate, or turn serious topics into jokes.

### Progressive disclosure

Start with a clear next action. Reveal claim detail, model reasoning, and passage comparison when the user asks. Do not put every statistic and control on a single dashboard.

## 4. Target users and jobs to be done

### Primary: applicant or student

“Before I apply, help me find every requirement, deadline, document, renewal rule, and unresolved detail across the current official sources.”

### Secondary: citizen or service user

“Before I visit or submit an application, tell me which official steps and documents are clear, which sources disagree, and what to confirm with the agency.”

### Secondary: researcher or small business owner

“Before I act on a policy, market, or research claim, show me how the sources support it and where the evidence is incomplete or stale.”

### Decisions the product supports

- Applying for a scholarship, job, grant, public service, or program
- Checking eligibility and required documents
- Comparing policy pages or notices
- Preparing questions for an official office or source owner
- Reviewing whether an old article still applies to the current period

The first demo should use a scholarship decision because it makes deadlines, documents, eligibility, and renewal requirements easy to demonstrate. Keep the architecture domain-neutral so a user can also investigate public services, careers, health information, or business rules.

## 5. The end-to-end user journey

### Stage A — Enter the Kasukabe Detective HQ

The opening screen is a 3D scene: Shinchan at a colorful investigation desk in a recognizable Kasukabe neighborhood. The user sees one primary action, **Start a new case**, and one secondary action, **Try the sample case**. The 3D mascot gives a short, optional welcome and points to the next step. The page also works if WebGL is unavailable.

### Stage B — Define the case

The case wizard asks:

- **What decision are you making?** A plain-language question.
- **What topic or program is this about?** A title or organization.
- **Where does it apply?** Optional country, region, jurisdiction, or institution.
- **When do you need the answer?** Optional date or application round.
- **What details matter most?** Suggested categories such as eligibility, dates, documents, cost, renewal, process, exceptions, and contact route.

The app proposes a requirement checklist based on the question. The user can remove or add requirements before analysis. This keeps AI interpretations from silently defining the case.

### Stage C — Gather sources

The Source Locker supports:

1. **Paste a URL:** Fetch and extract readable page text on the server. Show the final URL, page title, publication date when detectable, retrieval date, and extracted text preview.
2. **Paste text:** The user enters a title, optional URL, publisher, date, and excerpt.
3. **Upload a document:** At minimum, support PDF and text files. DOCX can be a follow-on if the chosen parser is reliable.
4. **Try a sample case:** Load clearly labeled fictional sources for the scholarship demo.

Each source passes through visible states: queued, retrieving, extracting, ready, needs attention, or failed. The user can correct metadata, remove a source, and see exactly what text was extracted. Never invent a URL, publisher, date, or quotation.

### Stage D — Review the source snapshots

The Source Locker shows one source card per item. Each card has the title, publisher, URL, date, freshness label, extraction status, and a short summary of what the source explicitly covers. A click opens the source text with page or section anchors and highlights the passages used in analysis.

The user should be able to tell at a glance:

- which source contains a deadline;
- which source lists documents;
- which source covers eligibility or renewal;
- which requested topics are not mentioned in a source;
- which metadata is unknown.

### Stage E — Run the patrol

The analysis pipeline extracts candidate claims, maps them to the user's requirements, compares claims, and generates issue signals. Show a short progress sequence such as “Reading pages,” “Pinning evidence,” “Checking dates,” and “Looking for missing details.” Do not display a fake AI typing animation that implies work the application is not doing.

If no AI key is configured, the app runs its transparent local checks and labels the method as **Rule-based preview**. If an AI provider is configured, label the provider-backed run **AI-assisted review** and preserve the same evidence requirements.

### Stage F — Explore the 3D Evidence Map

The central case workspace is an interactive 3D investigation board rather than a wall of dashboard cards:

- source folders or document stacks are source nodes;
- evidence/claim cards are claim nodes;
- the user's requested requirements form the case checklist along the edge of the board;
- solid green strings mean a source passage supports a claim;
- split red strings mean two claims may conflict;
- dotted gold strings mean partial coverage or a question needing verification;
- a dark “missing clue” space means the current source set has not answered a requirement;
- a fading or calendar-stamped source signals age or an unknown publication date.

Selecting a node opens a readable 2D evidence inspector beside the 3D scene. The user can orbit, zoom, filter by requirement, and use a list view. All interactions have keyboard and non-3D alternatives.

### Stage G — Resolve the dark spots

The app separates findings into four issue families:

1. **Coverage gap:** A requested requirement has no evidence in the reviewed sources.
2. **Unanswered question:** Sources mention the subject but leave a specific decision-relevant detail unclear.
3. **Potential conflict:** Two passages appear incompatible on the same requirement, scope, and time period.
4. **Freshness warning:** A source may describe an earlier round, has no visible date, or was retrieved long ago.

Each finding shows: what triggered it, which requirement it relates to, the source passages inspected, what the app can and cannot conclude, and the next verification action. Conflicts must be called **potential** until scope and date are compared.

### Stage H — Make a verification mission

The Verification Mission converts findings into concrete tasks, for example:

- Open the current official scholarship notice and confirm the active deadline.
- Ask the program office whether a reference letter is mandatory for this round.
- Locate an official renewal policy and record its GPA/credit conditions.
- Replace an older round notice with a current source.

Every task includes priority, reason, linked evidence, a suggested source or question, status, and optional notes. Users can reorder tasks, mark them done, edit them, or dismiss them. Do not imply the app has contacted an office or verified a fact when it has not.

### Stage I — Create a decision-ready briefing

The final report contains:

1. The original question and context
2. A short structured source summary
3. What is supported by the sources
4. Potential conflicts, with both passages side by side
5. Missing or unanswered details, labeled as signals
6. Source age and unknown-date warnings
7. The prioritized verification mission
8. Source bibliography with URLs, publisher, dates, and page/section
9. Analysis method and limitations

Export to Markdown first. PDF export is a later milestone. Copy and print views should preserve citations and labels.

## 6. Information architecture and screens

### 6.1 Welcome / Detective HQ

- 3D Shinchan/Kasukabe hero scene
- Start case and sample case calls to action
- Short “how the patrol works” sequence
- Small case history area once the user has saved cases

### 6.2 Case Wizard

- One question per step with a visible progress path
- Requirement categories presented as editable tags
- Source-adding methods visible before analysis
- Save-and-return behavior

### 6.3 Case Room

- Header: case name, current analysis run, source count, save status
- Stage navigation: **Question → Sources → Evidence Map → Dark Spots → Mission → Briefing**
- 3D map/list toggle
- Right-side evidence inspector on node selection
- No generic KPI dashboard as the central screen

### 6.4 Source Locker

- Upload/paste/URL controls
- Queue and extraction state
- Source list with type, publisher, date, freshness, and status
- Text preview with exact passage highlights
- Replace, remove, edit metadata, and retry actions

### 6.5 Claim Workshop

- Requirement rows with source passages as columns
- Claims grouped by requirement and source
- Side-by-side comparison for candidate conflicts
- User controls: agree, same scope, different period, dismiss, or needs human check
- Show extracted claims separately from source text

### 6.6 Dark Spot Explorer

- 3D evidence map, with a 2D list alternative
- Filters: gap, unanswered, conflict, date warning, unresolved
- Requirement coverage ribbon: covered, partial, conflict, missing, unknown
- Selecting a signal opens evidence and next-step details

### 6.7 Verification Mission

- Prioritized editable task list or mission route
- Status: open, in progress, verified, dismissed
- Add notes and attach a new source to resolve a task
- Re-run analysis after source changes and show what changed

### 6.8 Briefing / Export

- Human-readable report with linked citations
- Clear distinction between source statements, derived comparisons, and suggestions
- Export Markdown and print-friendly HTML
- Report version tied to the analysis run and source snapshots

### 6.9 Settings / Trust Center

- AI provider status and model name if used
- Data retention controls and delete-case action
- Rules for source-age warnings
- Reduced motion and 3D performance controls
- Privacy explanation for pasted/uploaded content

## 7. Analysis design: how the app reaches a finding

### 7.1 Convert the user's question into requirements

Create a requirement set from the user's language. Example categories for a scholarship case:

- current deadline and time zone;
- eligibility and exclusions;
- required documents;
- submission channel and application link;
- award amount and duration;
- renewal/retention conditions;
- contact or appeal route.

The model may suggest requirements, but the UI must show them for user approval. Each requirement has a stable ID, plain-language description, importance, and type.

### 7.2 Extract evidence-backed claims

The extractor returns structured items, never just free-form prose:

- claim text;
- source ID and source snapshot ID;
- exact quotation;
- character offsets or page/section locator;
- extracted date/time/value and units when present;
- related requirement ID;
- claim polarity and scope;
- extraction method and model metadata;
- status: candidate, accepted, corrected, or dismissed.

Validate every quotation against the stored text. If a quote cannot be found exactly, reject or mark that claim as unsupported. Never silently repair an AI-generated quotation.

### 7.3 Summarize each source

Summaries should be concise and fact-bound. Every sentence should link to one or more passages. Present a source snapshot as “This page says…” and not as an endorsement that it is current or correct.

### 7.4 Detect coverage gaps

Compare requested requirements with mapped evidence:

- **Covered:** at least one clear, relevant passage found.
- **Partial:** related information exists but a decision-critical sub-detail is missing.
- **Conflicting:** incompatible candidate claims exist.
- **Not found:** no relevant passage found in the ingested set.
- **Unknown:** extraction failed, source was inaccessible, or evidence quality is too low.

“Not found” is an observation about the case's source set, not a claim about the world.

### 7.5 Compare claims for potential conflicts

Only compare claims when they refer to the same entity, requirement, geographic/institutional scope, and relevant period. Normalize dates, currency, units, and common document names before comparison. Classify outcomes as:

- compatible;
- one source adds detail;
- potentially conflicting;
- different scope or application round;
- cannot determine.

Example: “one reference letter” and a list omitting reference letters are not automatically a proven contradiction. Report a **document-list mismatch to verify** unless both sources explicitly claim their list is complete for the same round.

### 7.6 Evaluate freshness

Keep separate fields for publication date, last-updated date, access/retrieval date, and event/application dates. A recent crawl date does not make old content current. Rules should be domain-configurable and explain the trigger. Suggested labels:

- recent date visible;
- older than the case's chosen freshness window;
- publication date not found;
- page may cover an earlier round;
- dates disagree.

Do not mark a source false just because it is old. Tell the user which current source would resolve the warning.

### 7.7 Prioritize verification tasks

Use a transparent priority recipe, not a mysterious score. A task rises in priority when the detail is time-sensitive, high consequence, unsupported, disputed, or sourced only from older/undated material. Show the reasons as labels such as **Deadline-sensitive**, **Sources disagree**, or **Official confirmation needed**. Let users reorder tasks.

## 8. AI and trust model

### AI may assist with

- turning a question into candidate requirements;
- extracting candidate claims and exact passages;
- mapping a passage to one or more requirements;
- proposing a concise source summary;
- identifying candidate comparisons for a human to inspect;
- drafting verification questions and checklist wording.

### Deterministic code should own

- source IDs and provenance;
- exact quotation validation;
- persistence and revision history;
- date arithmetic and age labels;
- source-to-claim links;
- export citation formatting;
- checklist state;
- schema validation and analysis-run reproducibility.

### Required labels

- **Source statement:** A direct claim from a passage, with citation.
- **AI-extracted claim:** Candidate claim awaiting user inspection.
- **Potential gap signal:** A requirement was not covered by the current source set.
- **Potential conflict:** Passages may disagree; scope and date still require review.
- **Verified by user:** The user recorded that they checked an authoritative source.

Never display an AI output as an official fact. If no model is configured, do not fake an AI response. Run the rule-based preview and label it.

## 9. Data model

Use relational records with stable IDs and preserve immutable source snapshots for each analysis run.

### `ResearchCase`

`id`, `title`, `question`, `context`, `jurisdiction`, `decision_date`, `created_at`, `updated_at`, `status`, `owner_id` (optional).

### `Requirement`

`id`, `case_id`, `category`, `text`, `importance`, `origin` (`user` or `AI suggestion`), `accepted_at`, `sort_order`.

### `SourceDocument`

`id`, `case_id`, `source_type`, `title`, `url`, `publisher`, `publication_date`, `updated_date`, `retrieved_at`, `content_hash`, `extraction_status`, `visibility`, `created_at`.

### `SourceSnapshot`

`id`, `source_id`, `raw_text_location` or `raw_text`, `normalized_text`, `snapshot_at`, `content_hash`, `extractor_name`, `extractor_version`, `metadata_json`.

### `EvidencePassage`

`id`, `snapshot_id`, `quote`, `start_offset`, `end_offset`, `page_number`, `section_heading`, `locator_url`.

### `Claim`

`id`, `analysis_run_id`, `requirement_id`, `passage_id`, `claim_text`, `claim_type`, `polarity`, `scope`, `effective_date`, `confidence_band`, `review_status`, `model_metadata`.

### `Finding`

`id`, `analysis_run_id`, `requirement_id`, `finding_type`, `title`, `explanation`, `priority_reasons`, `status`, `created_at`.

### `FindingEvidence`

`finding_id`, `passage_id`, `relationship` (`supports`, `differs`, `qualifies`, `checked_but_not_found`).

### `VerificationTask`

`id`, `case_id`, `finding_id`, `action_text`, `priority`, `status`, `suggested_authority`, `user_notes`, `sort_order`, `completed_at`.

### `AnalysisRun`

`id`, `case_id`, `started_at`, `completed_at`, `status`, `method`, `model_name`, `prompt_version`, `rule_version`, `source_snapshot_ids`, `error_summary`.

Never overwrite old source text when a page changes. A new fetch creates a new snapshot, enabling comparison over time.

## 10. Technical architecture

### Recommended first implementation

- **Frontend:** React + TypeScript, organized as a multi-step application rather than one dashboard page.
- **3D:** Three.js through React Three Fiber, with accessible HTML controls layered around the canvas. Keep the React and React Three Fiber major versions compatible; check their official compatibility guidance when choosing versions.
- **Backend:** Python FastAPI service for ingestion, extraction orchestration, and case APIs.
- **Database:** SQLite for a local hackathon/demo instance; use migrations and keep the data-access layer portable to PostgreSQL if the project grows.
- **Analysis:** A provider adapter for an optional server-side LLM, strict structured outputs, plus a deterministic local rule engine for no-key demos.
- **Document extraction:** Server-side text extraction for PDFs and HTML. Store extracted text and provenance; retain uploaded originals only as long as necessary.
- **Run locally:** One documented command or a small `docker compose` setup that starts the web app and API.

Official implementation references: [React documentation](https://react.dev/learn), [React Three Fiber introduction](https://r3f.docs.pmnd.rs/getting-started/introduction), [FastAPI documentation](https://fastapi.tiangolo.com/), [SQLite documentation](https://www.sqlite.org/docs.html). Confirm current versions and compatibility before installing dependencies.

### Component boundaries

```text
Browser application
  ├─ Case wizard and navigation
  ├─ Source Locker and text inspector
  ├─ 3D Evidence Map + 2D list fallback
  ├─ Claim Workshop and comparison matrix
  ├─ Verification Mission
  └─ Briefing/export view
             │ JSON API
             ▼
API service
  ├─ Case and source endpoints
  ├─ Safe URL fetch and document extraction
  ├─ Source snapshot/provenance store
  ├─ Requirement and claim schemas
  ├─ Rule-based comparison/freshness engine
  ├─ Optional LLM provider adapter
  └─ Report exporter
             │
             ├─ SQLite database
             ├─ Local object/file storage for uploaded originals
             └─ Optional model provider (server-side key only)
```

### Suggested API surface

- `POST /api/cases` — create case
- `GET /api/cases/{case_id}` — retrieve case and progress
- `PATCH /api/cases/{case_id}` — update question/context
- `POST /api/cases/{case_id}/requirements` — add or edit requirements
- `POST /api/cases/{case_id}/sources/text` — add pasted text
- `POST /api/cases/{case_id}/sources/url` — fetch and ingest a URL
- `POST /api/cases/{case_id}/sources/upload` — upload supported file
- `GET /api/sources/{source_id}` — metadata and extracted text
- `POST /api/cases/{case_id}/analysis-runs` — start a run
- `GET /api/analysis-runs/{run_id}` — status and result
- `PATCH /api/verification-tasks/{task_id}` — update task status/notes
- `GET /api/cases/{case_id}/report.md` — export a cited Markdown briefing

Return clear errors for inaccessible pages, unsupported files, extraction failures, missing model configuration, and rate limits. A failed fetch must never silently become an empty “no information” result.

## 11. 3D scene integration and performance

The 3D stage is part of the primary experience: the landing HQ and the evidence-map workspace. It must use a real WebGL scene with geometry, lighting, camera controls, and at least one animated Shinchan character model. A static poster, emoji, CSS-only face, or screenshot does not satisfy the 3D requirement.

The 3D map can be stylized rather than photorealistic. Use a small Kasukabe-inspired detective room: warm wood desk, folders, source cards, red string, a magnifying glass, a Shiro accent, and a Shinchan character who reacts to the selected case. Connect 3D objects to actual case data. For example, selecting a folder opens that source; selecting the red-string conflict opens the two cited passages.

Performance and fallback requirements:

- Lazy-load the 3D bundle and models after the app shell is visible.
- Compress models and textures; set practical file budgets and avoid huge texture atlases.
- Cap device pixel ratio and avoid continuous rendering when the scene is idle.
- Support keyboard-triggered node selection and a synchronized list view.
- Respect `prefers-reduced-motion`; pause idle animation and offer a static scene.
- Detect WebGL failure and show the same source/claim graph as an accessible 2D view.
- Never hide critical evidence, labels, or decisions inside the 3D canvas.

## 12. Safety, privacy, and source handling

- Never place AI provider keys in browser code.
- For URL ingestion, defend against server-side request forgery: block private IP ranges, loopback, local hostnames, cloud metadata addresses, and unsafe redirect chains; limit content size and timeouts.
- Sanitize extracted HTML and render source text as text, not executable markup.
- Limit file types, size, and parsing time. Reject unsupported or encrypted files with a clear message.
- Keep external-site retrieval user-triggered. Respect access controls and applicable site terms; do not bypass authentication or paywalls.
- Explain whether source text is stored and for how long. Provide delete-case and delete-source actions.
- Distinguish source publisher from the person who pasted the text. Mark user-provided material as user-provided until verified.
- For high-impact topics, show a visible “verify with the official source” reminder and avoid giving a final eligibility or legal determination.

## 13. Accessibility and UX quality bar

- Use semantic headings, labels, form validation, focus management, and keyboard navigation.
- Every 3D action has a button/list equivalent.
- Provide visible focus states, sufficient contrast, reduced motion, and screen-reader status updates for ingestion/analysis progress.
- Use plain language: “not found in these sources” rather than “the rule does not exist.”
- Keep one primary action per step. Warn before deleting a case or source.
- Empty, loading, partial, failed, and successful states are designed—not left blank.
- Make mobile layouts usable; fall back to the 2D evidence list on small/low-power devices.

## 14. Delivery phases

### Phase 1 — Credible vertical slice

- Case wizard and one scholarship sample case
- Paste-text source intake with title, URL, and publication date
- Source Locker and source snapshot preview
- Requirement checklist
- Deterministic document-list mismatch, missing-coverage, and date warnings
- Exact passage linking
- Verification Mission with editable tasks
- 3D HQ scene and interactive 3D Evidence Map with 2D fallback
- Markdown briefing export

### Phase 2 — Real ingestion and AI assistance

- Safe URL fetch and PDF upload/extraction
- Optional server-side LLM adapter for claim extraction and summaries
- Quote-span validation and analysis provenance
- User review/correction of extracted claims
- Better conflict matching with date/scope normalization

### Phase 3 — Research continuity

- Versioned source snapshots and change tracking
- Re-run comparison showing what changed
- More research domains and requirement templates
- Sharing/export, localization, and deployment hardening

If the deadline is short, complete Phase 1 end to end. A working source-to-evidence-to-verification journey is more valuable than unfinished pieces from every phase.

## 15. Demo case and judging story

### Clearly synthetic scholarship sample

Use two fictional sample source cards, both marked **SAMPLE — NOT REAL RULES**:

- **Round notice, dated 1 February 2025:** Lists proof of enrollment and household income; says the old round closes on 15 March.
- **Scholarship FAQ, dated 10 January 2026:** Lists proof of enrollment, income documentation, and one reference letter; gives no current deadline in the sample text.

Expected demo signals:

- **Potential document-list mismatch:** The FAQ lists a reference letter that the round notice does not list. Ask whether the lists cover the same round and whether each is complete.
- **Current deadline not established:** The only explicit deadline appears in the older round notice.
- **Renewal requirement not found:** Neither excerpt covers renewal.
- **Freshness warning:** The round notice is from an earlier year.
- **Mission:** Locate the current official notice, confirm whether the letter is required, and find the renewal policy.

Do not present the fictional scholarship or its dates as real-world guidance. For a final live demo, add at least one real, publicly accessible source set if time allows, preserve URLs and retrieval dates, and still label all inferences.

### Suggested 3-minute demo script

1. Start at the 3D Detective HQ; introduce the case question.
2. Open the sample scholarship case and show the editable requirements.
3. Add/open the two source cards and point out dates and source text.
4. Run the patrol; follow the 3D evidence strings from source to claim.
5. Open the document mismatch and show both passages side by side.
6. Show the old deadline and explain why it cannot establish the current round's deadline.
7. Open the renewal gap, emphasizing that “not found” is a signal, not proof of absence.
8. Mark one verification task in progress and export the cited briefing.

## 16. Acceptance criteria

The handoff implementation is complete when:

- A user can create a case and edit the suggested requirement list.
- At least two sources can be added and have visible metadata/provenance.
- The user can inspect extracted text and the exact passages supporting a claim.
- The report separates source statements, derived comparisons, and suggestions.
- Missing information is labeled as missing from the reviewed source set.
- Candidate conflicts show both passages and their dates/scope.
- A date warning explains why a source may be old and what to verify.
- The verification plan is editable and its status persists.
- A cited Markdown report can be exported.
- The 3D Shinchan scene is rendered in the normal flow and has working interactions; a 2D/accessibility fallback exists.
- The fictional sample is visibly labeled as fictional.
- Missing AI configuration results in a clearly labeled rule-based demo, not fake AI claims.
- The project can be started from documented instructions and does not require secrets to view the sample case.

## 17. Reference links

- React: https://react.dev/learn
- React Three Fiber: https://r3f.docs.pmnd.rs/getting-started/introduction
- FastAPI: https://fastapi.tiangolo.com/
- SQLite: https://www.sqlite.org/docs.html

Confirm current library versions and compatibility in their official documentation when implementation begins.
