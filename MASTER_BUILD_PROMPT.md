# Master Build Prompt — Kasukabe Gap Patrol

Copy this prompt and provide it together with `PROJECT_BLUEPRINT.md` and `SHINCHAN_3D_DESIGN_SPEC.md` to the coding AI that will implement the application.

---

## Prompt

You are the lead product designer and full-stack engineer responsible for building **Kasukabe Gap Patrol — Digital Dark Spot Detective**. Read both companion specifications completely before coding:

1. `PROJECT_BLUEPRINT.md`
2. `SHINCHAN_3D_DESIGN_SPEC.md`

The existing static `index.html` is an early concept only. Inspect the repository, preserve useful material, and replace or restructure it as needed. Do not stop after writing a plan, a screenshot, or a static mockup. Implement a working end-to-end application.

## Product outcome

Build an evidence-first research application where a person enters a decision question, adds multiple source URLs/excerpts/documents, reviews source snapshots, finds possible information gaps, unanswered questions, conflicts, and old/undated material, and leaves with an editable prioritized verification mission and a cited briefing.

The application must feel unmistakably Shinchan-themed and must contain visible **real 3D art** in the normal user flow. Use a rendered Shinchan/fan-model in a Kasukabe detective HQ and a clickable Evidence Map. Do not use a static hero image, emoji, or 2D-only illustration as the replacement for the 3D requirement. Use actual 3D geometry, lighting, camera, and interaction. If a full asset is unavailable, create an original low-poly 3D model from meshes and provide simple idle/point/blink animation. Keep an accessible 2D list fallback, but the 3D version must work by default.

## Required build behavior

### 1. Start screen and case creation

- Create an inviting 3D Detective HQ with a clear **Start a case** button and **Try the sample case** option.
- Let a user enter a research question, topic, jurisdiction/context, decision date, and relevant information categories.
- Generate candidate requirements from the question only as suggestions; allow the user to edit/confirm them before analysis.
- Provide save/resume behavior for a case.

### 2. Source intake and provenance

- Support pasted excerpts with title, optional URL, publisher, and date.
- Support URL import and PDF/text upload if feasible in this build. Make extraction status visible.
- Keep the source title, final URL, publication/update date if present, retrieval time, source text, and page/section locator.
- Show the extracted text to the user and allow metadata correction.
- Clearly distinguish user-provided text, fetched pages, and synthetic demo sources.
- Never invent source text, publication dates, publisher names, or URL references.

### 3. Analysis and evidence

- Produce source snapshots and requirement coverage states: covered, partial, potential conflict, not found in reviewed sources, or unknown.
- Detect candidate document-list mismatches, missing coverage, date gaps, and older-source warnings in the sample workflow.
- Compare claims only when subject, scope, and time period are relevant. Call uncertain differences **potential conflicts**.
- Every factual finding and summary statement must link to an exact source passage and source metadata.
- Validate extracted quotations against the stored source text. Reject unsupported quotations.
- Distinguish source statements, AI-extracted claims, rule-based signals, and user-verified outcomes in the UI.
- A gap means “not found in this source set”; never turn it into “the information does not exist.”
- If no AI key is configured, run a functional deterministic preview and label it honestly. Never fake AI output.
- If AI is integrated, call it on the server using an adapter and environment variable; never expose secrets in browser JavaScript.

### 4. 3D Evidence Map

- Use a shallow tabletop scene in the Kasukabe Detective HQ.
- Represent source documents as folders, exact passages as quote cards, requirements as labeled pins, and relationships as colored/patterned threads.
- Selecting a 3D item must open the matching readable HTML inspector with the quote, URL, date, and section/page.
- Show a red split thread for a potential conflict, a dotted yellow thread for partial/unanswered information, green for source-supported evidence, and a visibly empty clue space for “not found.”
- Provide orbit/zoom/reset controls and a synchronized accessible 2D list view.
- Respect reduced motion, lazily load models, and show a useful fallback if WebGL is unavailable.
- Do not put critical information only in the canvas.

### 5. Verification Mission and briefing

- Convert each relevant issue into an editable task with priority reason, evidence links, suggested official source/question, status, and user notes.
- Allow reorder, completion, dismissal with a reason, and adding a source to resolve a task.
- Re-running analysis after a source change should create a new run and show what changed.
- Export a cited Markdown briefing containing the question, source snapshot, supported details, gaps, potential conflicts, freshness warnings, verification plan, citations, and limitations.

## Architecture direction

Use a clean, maintainable architecture. Preferred direction:

- React + TypeScript for the multi-step frontend.
- Three.js through React Three Fiber for the interactive 3D stage; select compatible dependency versions and verify compatibility in official documentation.
- FastAPI service for source ingestion, extraction, analysis orchestration, and APIs.
- SQLite for a self-contained demo, with migrations and a data-access layer that can later move to PostgreSQL.
- An optional server-side LLM adapter plus deterministic local checks so the demo runs without secrets.
- A documented local startup path; provide sample data that works offline.

You may choose an equally suitable stack if the existing repository requires it, but explain the tradeoff in the README. Do not add many dependencies without a clear purpose. Create an explicit data model for cases, requirements, source documents, source snapshots, evidence passages, claims, findings, verification tasks, and analysis runs.

## Design direction

Follow `SHINCHAN_3D_DESIGN_SPEC.md` closely:

- Signature colors: Shinchan red, shorts yellow, warm paper cream, Kasukabe sky blue, ink black.
- Use a warm detective clubhouse, school-notebook/folder props, Kasukabe setting, red evidence strings, and an expressive 3D Shinchan character.
- Make the product a case-building journey, not a generic analytics dashboard.
- Keep text and citations in normal accessible HTML; use 3D as an interactive map and guide.
- Keep humor in short labels and mascot reactions. Never joke about the user's high-stakes decision.
- Provide focus states, keyboard access, semantic structure, reduced motion, contrast, loading/empty/error states, and mobile layout.

## Demo scenario

Include two synthetic sample scholarship sources clearly labeled **SAMPLE — NOT REAL RULES**:

1. An older round notice listing proof of enrollment and household income and an old March 15 closing date.
2. A newer FAQ listing those documents plus one reference letter but no current application deadline.

The app should surface a potential document-list mismatch, an unconfirmed current deadline, a renewal detail not found in the sample sources, and a freshness warning on the older notice. Explain that the source set is fictional. Provide the verification mission: find the current official notice, confirm the required documents for the same round, and find the official renewal policy.

## Security and reliability requirements

- Treat imported web pages and uploaded files as untrusted content.
- For URL fetches, prevent SSRF; block localhost/private/cloud-metadata ranges, unsafe redirects, oversized responses, and long-running requests.
- Sanitize HTML and never render source markup as executable code.
- Handle extraction failures explicitly; do not translate failure into “no information found.”
- Keep API keys server-side; document required environment variables without committing secrets.
- Provide delete source/delete case behavior and clearly explain whether source text is stored.
- Preserve source snapshots for each analysis run; do not silently overwrite evidence.

## Quality bar and handoff

Before declaring the build complete:

- Run the application using the documented local command.
- Verify the sample-case flow from start to exported briefing.
- Verify source adding, exact evidence navigation, conflict comparison, checklist persistence, and the 3D scene.
- Verify keyboard/list operation and the no-WebGL/reduced-motion fallback.
- Add automated checks for core analysis rules, quote validation, API schemas, and source-date behavior.
- Fix errors found during verification; do not leave buttons as decorative placeholders.

Deliver:

1. Complete source code and any 3D assets or procedural model code
2. `README.md` with setup, demo flow, environment variables, and limitations
3. A `.env.example` without real secrets
4. Sample data clearly marked synthetic
5. A short architecture note and known limitations
6. A working 3D-first experience plus accessible 2D fallback

Make reasonable decisions without stopping for routine preferences. If a required external service is unavailable, complete the no-key/local path and clearly label the limitation rather than blocking the project.

---

## End of prompt
