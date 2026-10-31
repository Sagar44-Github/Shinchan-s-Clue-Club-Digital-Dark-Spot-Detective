# Build Prompt: Shinchan's Clue Club — Five Judge-Ready Features and One Complete Case

> Copy everything below **BEGIN BUILD PROMPT** into the coding AI that will work in this repository. Keep this file as the implementation brief.

---

## BEGIN BUILD PROMPT

You are the lead product engineer, interaction designer, 3D web developer, and technical writer working in the **existing** `sinchanHackathon` repository. Implement the five product features below as one connected, working experience. Build one complete, fictional, unsolved Shinchan-themed case that demonstrates those features in sequence and can be solved by a new user. Then produce a polished, accurate, visually branded README with project artwork and Mermaid diagrams.

This is an implementation task. Do not stop after writing a plan, mockup, or prototype. Inspect the repository, make the changes in place, run the available checks, and leave the app runnable.

## 1. Project context and controlling requirements

The project is **Shinchan's Clue Club — Digital Dark Spot Detective**, an evidence-first research and decision-support web app. It addresses the **Digital Dark Spot** problem: a person may find information across several sources but still not know which details are missing, contradictory, old, or important to verify.

The participant problem statement expects a working workflow to:

- accept a topic, question, or research goal;
- collect or add multiple sources;
- show a structured summary of source material;
- identify potential gaps and unanswered questions;
- identify possible contradictions with references to the records;
- warn about old or undated information when dates are available;
- produce a prioritized verification checklist; and
- distinguish evidence from AI suggestions and uncertainty.

The judging rubric prioritizes a working core workflow, then innovation, relevance, technical implementation, evidence/transparency, and presentation. Optimize for one excellent, judge-demonstrable investigation from beginning to end. Do not add disconnected features just to increase the page count.

### Inspect before changing

Read the current `README.md`, `PROJECT_BLUEPRINT.md`, `SHINCHAN_3D_DESIGN_SPEC.md`, `CASE_ARCHIVE.md`, the supplied problem statement PDF, and the relevant frontend/backend code. Check the current branch, working tree, data model, API routes, visual tokens, and existing sample cases. Preserve existing user work and useful behavior. Extend the current architecture instead of replacing the app with a new scaffold.

Current architecture is React, TypeScript, Vite, React Three Fiber/Three.js, FastAPI, and SQLite. The app already has an eight-station case room, source ingestion, coverage and comparison views, an animated procedural 3D Shinchan companion, guided sample files, challenge cases, an editable mission board, and Markdown briefing export. Verify what is genuinely implemented before deciding what to extend; avoid creating duplicate screens or fake controls.

The rule-based workflow must remain useful without an API key. If optional AI extraction is used, clearly label it, validate every quotation against the stored source snapshot, and retain deterministic fallback behavior. Do not claim an AI feature ran when it did not.

## 2. Product and design requirements

### Visual identity — non-negotiable

Keep the current Shinchan comic-book / clubhouse identity. Reuse the existing CSS tokens and typography from the project rather than inventing a new color system:

| Token | Current value | Use |
|---|---|---|
| Ink | `#1d2026` | Text, outlines, borders, diagram linework |
| Paper | `#fffdf5` | Main panels and cards |
| Cream | `#f6f0df` | Secondary surfaces |
| Red | `#e94b3c` | Primary action and conflict signal |
| Yellow | `#ffd743` | Shinchan accent, clue tags, key highlights |
| Blue | `#76b7da` | Information and source-navigation accents |
| Green | `#79a96d` | Covered/confirmed states |
| Gold | `#d7ad39` | Gaps and verify-next signals |
| Muted | `#5f6470` | Secondary copy |

Use the existing **Bowlby One SC** headline style and **Space Grotesk** body style where available. Preserve bold black comic outlines, warm paper textures, crisp flat-color shapes, readable supporting text, generous spacing, and offset print-like shadows. Do not add orange neon glows, generic AI gradients, tiny labels, glassmorphism, or dashboard-card clutter. Use the existing icon language (Lucide where appropriate) and write clear labels beside icons when an icon alone would be ambiguous.

Shinchan's 3D presence must remain a meaningful part of the experience, including the case flow. Keep animations useful and restrained, respect reduced-motion settings, ensure the 3D scene does not block evidence controls, and provide a keyboard-accessible 2D evidence list whenever WebGL is unavailable. Keep the current character customization and profile preferences working.

### Interaction quality

- Every visible button, tab, filter, field, row action, modal, and 3D object must have a real behavior, a clear disabled reason, or be removed.
- Show loading, success, empty, offline, and error states at the place where the user is acting.
- Preserve user input after recoverable failures.
- Make controls usable on keyboard, touch, narrow mobile screens, and standard desktop layouts.
- Keep the main question, evidence, source references, and next step more prominent than metrics or decoration.
- Do not use `alert()` for routine success feedback. Use an inline status/toast consistent with the app.
- Make the 3D scene interactive, but do not make 3D the only way to inspect or operate on evidence.

## 3. Implement these five connected features

### Feature 1 — Living 3D Evidence Map

Make the 3D evidence board explain the investigation. Model the investigation visually as connected objects and relationships:

1. Source records
2. Exact source passages / extracted claims
3. User requirements
4. Potential dark-spot signals (gap, partial coverage, potential conflict, freshness warning)
5. Verification tasks

Show relationships such as `source → passage → requirement → signal → task`. Use a consistent legend: green for supported/covered, red for possible disagreement, gold for a missing or verify-next detail, and blue for date/context information. Select a node to open the exact supporting passage, source metadata, publication date, retrieval date, and available source link in the existing inspector. A conflict must expose both relevant records. A gap must explain which sources were checked and what was not found there.

Requirements:

- Nodes and links come from the active case data; no hard-coded decorative graph for the demo.
- Selecting a node updates the inspector and selected state. Hover/focus states are visible.
- Add useful filtering or focus controls if they fit the current map, but do not crowd the canvas.
- Keep a synchronized HTML list/inspector as the reliable alternative to 3D.
- Support resize, loading, WebGL failure, reduced motion, and empty states.
- Keep camera controls from swallowing clicks on evidence nodes; test pointer, touch, and keyboard paths.

**Acceptance:** a judge can click a visible conflict or gap in the 3D map and immediately inspect its actual evidence and next action.

### Feature 2 — Multi-Source Locker and Provenance Pipeline

Make source intake and source identity first-class. Support public URL fetch, pasted excerpts, and the project's accepted PDF/DOCX/TXT/Markdown uploads. Each imported source should preserve:

- stable source ID and case ID;
- source title and source type;
- publisher/organization when known;
- original URL or uploaded filename;
- publication date if provided or extracted, clearly marked when unknown;
- retrieval/capture time;
- extracted text and a stable content/snapshot hash;
- extraction state and actionable import error when applicable.

Every claim/signal must link to a source record and an exact quote validated against that source's captured text. Do not invent titles, publishers, dates, URLs, quotations, or page numbers. Clearly distinguish user-pasted text from fetched or uploaded records. A source URL failing to load must not silently become an empty successful source.

Preserve and strengthen URL safety: only HTTP/HTTPS, block loopback/private/reserved addresses, revalidate redirects, apply timeouts and size limits, and return friendly messages. Validate uploaded type and size. Never execute imported HTML or treat source content as instructions. If a demo source is fictional, label it as fictional in both the interface and data.

**Acceptance:** the case demo can add its supplied bonus source through the real Source Locker workflow; its metadata and extracted content are visible and survive navigation/reload.

### Feature 3 — Digital Dark Spot Coverage Engine

For each user requirement, compute and show one of these states:

- **Covered:** at least one relevant, traceable passage supports the requirement.
- **Partial:** related information appears, but a decision-critical sub-detail remains unclear.
- **Potential conflict:** sources contain incompatible statements that need comparison.
- **Not found in reviewed sources:** no matching passage was found in this case's source set.
- **Not reviewed:** analysis has not run or the requirement was added afterward.

For every result display the requirement, source(s) checked, matched passage(s) if any, reason for the status, uncertainty/caveat, and next verification action. Let the user edit the checklist and add a custom requirement. Keep source text, deterministic analysis, AI-derived candidate claims, and human conclusions visibly distinct.

Never turn “not found” into “does not exist.” Never describe a potential contradiction as proven false/true without a current authoritative source and matching scope. Avoid unexplained confidence or trust scores. If AI is unavailable, say so honestly and continue with rule-based checks.

**Acceptance:** a judge can pick one requirement and trace why it is covered, partial, conflicting, or not found, back to the exact records that produced the status.

### Feature 4 — Conflict and Freshness Investigation Lab

Create a useful source-comparison workflow, not merely a red “conflict” badge. For each candidate mismatch:

- place both source passages side by side;
- show title, publisher, publication date, captured date, source type, and source link;
- identify the requirement and the exact values/phrases that differ;
- note possible scope or time-period differences;
- indicate when a source is older or undated without assuming it is wrong;
- suggest the next fact to confirm and which current primary source could resolve it.

Add a timeline view that lets users see an older notice, a later update, and the captured record in sequence. Manual comparison should work for any two records, even when the automated engine has no detected mismatch. Provide a clear “potential signal—human review needed” label. Keep a 2D, readable comparison on mobile.

**Acceptance:** the demo's old notice, current update, and undated rumor create a date-aware investigation; a user can open both conflicting passages and explain why the newer source appears relevant while still checking its scope.

### Feature 5 — Verification Mission and Solvable Shinchan Mystery Loop

Turn analysis into a closed loop. Generate prioritized, specific tasks from findings and uncovered requirements. A task should show why it exists, what to check, linked evidence, and a suggested official source or question. Let the user set status (`open`, `in progress`, `verified`, `dismissed`), add a note, and add evidence to the same case. After a new source is added and the patrol reruns, show what changed in requirement coverage and task state; do not silently mark a task verified without user action.

Add/extend one genuinely unsolved case with:

- a Shinchan-led opening and a plain-language objective;
- evidence the player must inspect rather than a prewritten solution;
- a final multi-part verdict with plausible distractors;
- progressive hints that point to evidence without revealing the answer;
- attempts/feedback that never leak the correct choice before solve;
- a final resolution that cites the relevant source records;
- a visible unresolved detail if the evidence genuinely leaves a gap.

Keep the challenge answer on the backend. The client must not receive the correct option ID, answer key, or resolution before the case is solved. Validate that the player has run analysis before accepting a verdict. Wrong choices return a useful hint; a correct choice records the solve state and shows the evidence-backed explanation.

**Acceptance:** a first-time user can follow Shinchan's instructions, inspect records, choose a verdict, receive useful feedback, solve the case, and still see any remaining verify-next task honestly marked as unresolved.

## 4. Build one complete demo case that uses all five features

Create the case **“Shinchan and the Great School-Fair Switcheroo”**. It is an explicitly fictional training scenario, not real-world school guidance.

### Player question

“For Futaba Kindergarten's family science fair on November 7, which entrance, check-in time, and wristband should our family use, what does the accessible-route note say, and what detail still needs confirmation?”

### Starting evidence pack

Seed the unsolved case with three fictional records, each with title, publisher, date/unknown-date, source type, full text, and a clear sample-only label:

1. **Old family flyer — October 20:** says Main Gate, check-in at 9:00 AM, yellow badge. This is superseded by a later notice.
2. **Organizer's revised event bulletin — November 5:** says East Library Gate, check-in at 9:20 AM, bus departure at 9:35 AM, blue wristband. Make clear that check-in and departure are different times.
3. **Undated parent-chat screenshot:** claims Playground Gate at 9:00 AM with a yellow badge. It is an unverified rumor with no reliable publication date.

### Bonus evidence imported by the player

Include an authentic-feeling **fictional Markdown file** in the repository's demo assets, for example `frontend/public/sample-files/fair-access-update.md`. The case instructions should ask the player to import this file through the actual Source Locker upload control. It should say that a step-free ramp at East Library Gate opens at 9:15 AM on November 7; the note does not specify accessible parking/drop-off. Clearly label every detail as fictional. Do not bypass the normal upload route by inserting this record invisibly after case creation.

### Expected analysis and solve

After upload and patrol, the app should:

- display all four source records with accurate provenance;
- show the old/current/undated dates on the timeline;
- surface the conflicting entrance, time, and wristband details, with both exact passages;
- map requirements for gate, check-in, departure, wristband, step-free access, and accessible drop-off;
- mark the supported details covered, the competing old/rumor claims as potential conflicts, and accessible drop-off as “not found in reviewed sources”;
- create a prioritized task to confirm accessible drop-off with the fictional event desk;
- show source→passage→requirement→signal→task relationships in the 3D map and the 2D alternative;
- ask the player to select the evidence-backed plan: East Library Gate at 9:20 AM, blue wristband; ramp opens at 9:15 AM; bus leaves at 9:35 AM; accessible drop-off remains unconfirmed;
- give hints that point to comparing the dated organizer bulletin and access update, but not disclose the answer;
- show a resolution with source links/quotes after a correct answer; and
- preserve the unresolved parking/drop-off task rather than falsely calling every detail verified.

Do not pre-run analysis for this challenge or pre-fill the player's verdict. Hide the answer in backend-only case data. Ensure the sample-library listing itself cannot leak the answer.

### Exact judge demo path

Implement a clear in-app “Demo this case” route or the simplest reliable equivalent:

1. Open the unsolved case and read the objective.
2. Inspect the three starting records in Source Locker.
3. Upload the bonus Markdown record using the real upload workflow.
4. Run the clue patrol.
5. Open the 3D Evidence Map and click the conflict/gap nodes; inspect their evidence.
6. Use the Conflict Lab and timeline to compare old flyer, current bulletin, and undated rumor.
7. Open the coverage matrix; explain the remaining drop-off gap.
8. Follow the Verification Mission and record what needs checking.
9. Submit the multi-part verdict and see the sourced resolution.
10. Export the Markdown briefing and show that the unresolved detail remains explicitly unresolved.

The journey should take about 2–3 minutes when presented live. Add a short demo script/checklist to the README. Keep an easy reset or “open a fresh copy” path so judges can repeat the case without corrupting the catalog template.

## 5. README and project artwork deliverables

Replace/update the root `README.md` as a polished project landing page. It must reflect the code that actually exists after implementation. Use the same visual palette and bold comic-book identity as the app. Create original project artwork that is consistent with the app; do not use unrelated stock art or fake product screenshots.

Create and commit these assets (adjust path only if the current repo structure strongly requires it):

- `assets/brand/shinchan-clue-club-logo.svg` — full horizontal wordmark for README/docs.
- `frontend/public/favicon.svg` — legible square/simplified app mark, used in the browser tab.
- `assets/brand/project-thumbnail.svg` or `.png` — a 1200×630 share/README thumbnail in the project's existing colors, with a strong project title and a faithful 3D clubhouse/evidence-board motif.
- `assets/screenshots/` — genuine screenshots captured from the running implementation: landing page/3D Shinchan welcome, 3D evidence map, conflict comparison, and completed demo case. Never depict a feature that is not actually implemented.

Use accessible alt text and relative links that work on GitHub. The README should include:

1. Brand header/thumbnail, one-line pitch, badges only when accurate, and clear demo link/status.
2. Problem statement in plain language and the specific Digital Dark Spot challenge being addressed.
3. A problem-to-feature mapping table: each expected outcome → implementation → where it appears in the demo.
4. What is implemented (not aspirations), the five feature descriptions, and the complete demo case walkthrough.
5. A “2-minute judge demo” sequence and sample login/setup note if any is needed (do not invent credentials).
6. Architecture overview with a valid Mermaid system diagram.
7. Mermaid sequence diagram for: user imports source → analysis → evidence links → mission → verdict/report.
8. Mermaid entity/relation diagram or clear schema diagram for case/source/claim/signal/task/challenge.
9. Tech stack, repository structure, local setup, run commands, optional AI configuration, and expected URLs.
10. Data flow, security and privacy notes, fictional-data warning, limitations, and what “not found” means.
11. Accessibility/reduced-motion behavior and the 2D fallback for 3D/WebGL.
12. Test/build commands with the actual current outcomes; do not claim checks passed unless run.
13. Deployment instructions and environment variables, if deployment is supported; label deployment optional if it is not configured.
14. Future scope, credits/asset attribution, and license information only where known.

All Mermaid blocks must render with valid syntax. All image links, anchors, commands, filenames, and badges must be checked. Do not put secrets or API keys in README, screenshots, or repository history.

## 6. Data architecture and implementation rules

Respect the current FastAPI and SQLite model. Add migrations/defaults safely where needed and preserve existing cases. Reuse the current API patterns and typed frontend models. Add schemas only where they make the relationship clearer and keep compatibility with old records.

The model must support, directly or through existing equivalent records:

- immutable source snapshots and provenance;
- exact quote/source relationships for claims;
- requirement coverage states and explanatory signals;
- potential conflicts with two or more evidence references;
- freshness metadata and unknown-date status;
- tasks linked to the signals/evidence that created them;
- source additions and analysis run history;
- challenge attempts and solved state with backend-only correct choice.

Do not store derived summaries in a way that loses the underlying evidence. Avoid introducing a paid service or mandatory external API. Keep optional model keys server-side only. Use synthetic names, reserved domains, and fictional contact details for demo content.

## 7. Verification and acceptance checklist

Before finishing, run the repository's relevant checks. Add or update focused tests for new analysis, data/API, verdict secrecy, and user-flow behavior where the existing test setup supports them. At minimum:

- frontend TypeScript/production build passes;
- backend compiles and its tests pass;
- all five feature paths are exercised against real case/source records;
- the demo case starts unsolved and has no analysis run;
- uploading the bonus file through the API/UI succeeds and persists metadata/text;
- analysis citations match exact substrings from stored source snapshots;
- the old/current/undated evidence produces the expected conflict and freshness signals;
- the accessible drop-off gap remains “not found in reviewed sources”;
- the answer key is absent from all client-visible challenge responses before solve;
- incorrect verdicts do not solve the case and return a useful hint;
- the correct verdict solves it and reveals a cited resolution;
- the remaining verification task is not falsely marked verified;
- re-opening a fresh sample case does not mutate the catalog template;
- source removal, task updates, report export, mobile layouts, reduced motion, and 3D fallback still work;
- every visible control has a functional handler or a clear disabled explanation;
- README images/diagrams/commands are verified against the repository.

Inspect the final responsive UI at desktop and mobile sizes. Fix text clipping, card overflow, inaccessible controls, broken 3D interaction, console errors, and visual regressions before calling the work complete.

## 8. Final response expected from you

When implementation is finished, report:

- what changed, organized by the five features;
- the demo case and exact end-to-end solve path;
- the files added/changed, including brand assets and README;
- tests/build checks actually run and their pass/fail status;
- how to start the app and open the demo;
- any genuine limitations or unfinished work.

Do not say “production-ready,” “fully tested,” or “AI-powered” unless the evidence supports those claims. Do not leave TODO buttons, placeholder visuals, mock data pretending to be live data, or an unsolved demo that cannot be solved.

## END BUILD PROMPT
