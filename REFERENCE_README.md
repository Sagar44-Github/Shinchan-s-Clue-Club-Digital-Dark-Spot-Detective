# Kasukabe Gap Patrol

**Find what the search missed before it becomes an “oh no!”**

## Handoff package

- [Complete project blueprint](PROJECT_BLUEPRINT.md)
- [Shinchan 3D art direction and UI/UX specification](SHINCHAN_3D_DESIGN_SPEC.md)
- [Copy-paste master build prompt for another coding AI](MASTER_BUILD_PROMPT.md)

The 3D Shinchan experience is a required part of the full project specification. The current `index.html` is an early static concept and does not yet implement the full architecture or 3D scene described in the blueprint.

Kasukabe Gap Patrol is a Shinchan-inspired, evidence-first information gap detector. A user asks a decision question, adds excerpts from multiple sources, and gets a structured review of likely omissions, conflicting requirements, and older material, with each signal tied back to the exact source notes and a prioritized verification checklist.

## Why this fits Digital Dark Spot

Search and summary tools usually show what they found. This prototype focuses on what the reviewed information may still leave unanswered. Its sample scholarship case demonstrates a mismatch in document lists, an unconfirmed current deadline, a missing renewal policy, and an older round notice. The report distinguishes a **source excerpt** from a **gap signal**: not finding a detail in this source set does not mean that detail does not exist.

## Run it

Open `index.html` in a modern browser. No installation or API key is required. The demo works locally, and users can add their own source title, publication date, and copied excerpt. Use the “Run the gap patrol” button to refresh the findings. Evidence can be expanded, checklist items can be tracked, and the report can be copied.

## Demo data and analysis

The preloaded scholarship sources are fictional sample material created to demonstrate the workflow. They are not real scholarship rules or real official sources. The current prototype uses transparent browser-side checks for document-list differences, missing deadline or renewal mentions, and source age. It does not claim to verify facts against the live web. All findings need confirmation against the current official source.

## Next build steps

1. Add URL import with safe page fetching and visible extraction provenance.
2. Add optional AI-assisted question-to-requirement mapping, with each generated suggestion labeled and linked to its supporting passages.
3. Add source snapshots, date-aware change tracking, and side-by-side passage comparison.
4. Add exportable case reports and accessibility/language support.

## Hackathon submission copy

**Project title:** Kasukabe Gap Patrol — Digital Dark Spot Detective

**Project description:** Kasukabe Gap Patrol is a Shinchan-inspired web app that helps people find decision-critical details missing from scattered online information. Users enter a research question and compare excerpts from multiple sources. The app flags possible omissions, conflicting requirements, and older material; shows the exact evidence behind each signal; and creates a prioritized checklist of what to verify next. A clear evidence-versus-suggestion interface helps users see what sources actually say and what still needs checking. The demo includes a fictional scholarship case and supports adding source excerpts. The prototype uses transparent local checks and labels its sample data and uncertainty rather than presenting suggestions as facts. Future scope includes URL import, optional AI-assisted requirement mapping, and change tracking.

**GitHub repository link:** Add the public repository URL after publishing this folder.

**Deployment link:** Optional; deploy this folder as a static site.

**Demo video / PPT:** Optional.
