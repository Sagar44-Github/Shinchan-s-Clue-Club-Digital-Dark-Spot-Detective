# Shinchan 3D Art Direction and UI/UX Specification

## 1. Non-negotiable visual brief

The product must read as a Shinchan project within the first few seconds. Shinchan is the host and detective guide; Kasukabe is the setting; the humor is playful and brief; and a rendered 3D Shinchan character appears in the normal product path. Red shirt, yellow shorts, expressive eyebrows, round face, cheeky stance, and recognizable Shinchan proportions make the theme clear. A small emoji, a color palette alone, or a 2D logo does not satisfy the requirement.

Use official/approved art assets if the participant has them. Otherwise create an original stylized 3D fan-model for the hackathon prototype and label the project as a fan-themed hackathon demo. Do not present unofficial artwork as an official asset. Add Shiro, Action Kamen, or the Kasukabe Defense Force only as secondary references that support the mission context.

## 2. Creative direction

### Mood

“A kid's detective clubhouse that contains a surprisingly serious evidence lab.” The space should feel warm, energetic, mischievous, and handmade: a low desk, colored pencils, sticky notes, toy magnifier, folders, school notebook texture, neighborhood map, and red string connecting clues. The evidence itself remains calm, legible, and professional.

### Visual hierarchy

1. **Case question** — the user's decision is always visible.
2. **Source evidence** — clean text panels with direct quotes and provenance.
3. **Finding type** — missing, conflict, outdated, or unanswered.
4. **Next action** — the verification task.
5. **3D character and props** — guide the user's attention without blocking content.

### Avoid

- A generic purple-gradient AI dashboard
- A static cartoon wallpaper behind ordinary dashboard cards
- 3D content that cannot be clicked or that carries the only copy of important information
- Excessive motion, camera spins, confetti, or comic effects over source text
- Cluttered kanji, unlicensed logo reproductions, or fake “official” seals
- Using Shinchan's comic voice for sensitive or high-stakes advice

## 3. Color and material system

Use the palette as a starting point, then validate contrast in the actual UI.

| Token | Suggested value | Use |
|---|---|---|
| Shinchan red | `#E94B35` | Primary action, shirt, selected clue |
| Shorts yellow | `#FFD447` | Secondary highlight, clue pin, attention |
| Ink black | `#282421` | Main text, outlines, 3D line work |
| Paper cream | `#FFF9EC` | Main page and notebook panels |
| Kasukabe sky | `#75BCE7` | Navigation, geography, calm context |
| Evidence green | `#477A5D` | Supported passage / verified task |
| Conflict coral | `#C9473A` | Potential disagreement |
| Gap gold | `#B98418` | Missing/unclear information |
| Freshness blue | `#4C7492` | Date and source-age status |

Materials should mix matte toy-like 3D forms with paper, pencil, and wood textures. Keep material contrast restrained so text remains the sharpest element. Avoid metallic sci-fi surfaces; this is a neighborhood detective desk, not a futuristic AI cockpit.

## 4. Typography, shapes, and iconography

- Use a friendly rounded sans-serif for headings and body. Choose an installed or bundled font with a dependable system fallback.
- Use a compact monospaced face only for source IDs, dates, and small metadata labels.
- Give cards soft, slightly irregular corners; keep all text containers aligned to a consistent grid.
- Use simple evidence icons: page, magnifier, calendar, question mark, crossed statements, and checkmark.
- Do not rely on color alone. Pair each status color with a label and icon.
- Keep body text comfortable to read; source quotations should be larger than secondary metadata.

## 5. Required 3D art assets

### A. Shinchan detective model — required

- Original rigged 3D model in a polished TV-cartoon/clay style, clearly recognizable as Shinchan
- Signature red top and yellow shorts, expressive eyebrows and face
- At least these animation states: idle/breathing, blink, point to clue, celebrate a verified task, puzzled reaction for an unresolved question
- No animation should be required to understand any text or finding

### B. Kasukabe Detective HQ environment — required

- Desk, paper folders, clue cards, magnifier, pencil, small neighborhood map, and a window/sign suggesting Kasukabe
- A main camera angle that leaves a clean space for UI panels
- A light rig with warm daylight and soft contact shadows
- A small set of animated details (paper flutter, light idle movement) that pause for reduced-motion mode

### C. Evidence map objects — required

- Source folders for source nodes
- Quote cards for claim/evidence nodes
- Red thread or ribbon for potential conflict
- Dotted yellow thread for partial coverage or a verification question
- Green pin/thread for an evidence-backed requirement
- A visibly empty clue space for a coverage gap
- Calendar stamp/fading paper treatment for source-age warnings

### D. Optional secondary characters and props

- Shiro as a quiet companion in the HQ or onboarding scene
- Action Kamen as a small “mission” graphic or loading accent
- Kasukabe Defense Force badges on case milestones
- Use them sparingly so Shinchan and the evidence stay central

## 6. Scene and interaction design

### 6.1 Welcome scene: “Detective HQ”

Camera: waist-high, three-quarter view over the desk. Shinchan stands or sits next to a case board and looks toward the primary action. The desk contains one sample case folder and one blank folder. The background can show a stylized Kasukabe street through a window.

Actions:

- **Start a case:** Shinchan gestures toward the case wizard.
- **Try the sample case:** He opens the scholarship folder and the app loads the synthetic demo sources.
- **How it works:** A three-step caption animates from question → evidence → verification mission.

Keep the character in a bounded stage panel. Do not make users orbit the camera just to find the start button.

### 6.2 Case wizard: “Write the mission”

Use a notebook-like stepper with one focus per step. Shinchan reacts subtly to progress. The visual shows a folder filling with labeled tabs: **Question**, **Requirements**, **Sources**. Use a normal form for input; do not place editable text in the 3D world.

### 6.3 Source Locker: “Pin the pages”

Sources appear as stacked 3D folders on the left of the evidence desk and as accessible HTML cards in the document list. Selecting a folder highlights its node in the map and opens the source's text/metadata inspector. Dragging a file onto the locker can be a progressive enhancement; a normal upload button is always available.

### 6.4 Evidence Map: “Connect the clues”

Use a shallow tabletop scene, not a free-flying universe. Pin source folders around the perimeter, claims in the center, and requirements along the bottom rail. Use short strings between objects, with the colors and patterns in the status table below. Click or keyboard-select a node to synchronize the inspector. Provide zoom-to-fit, reset-camera, and 2D list controls.

### 6.5 Claim Workshop: “Compare the pages”

When a potential conflict is selected, bring two paper cards side by side in the 3D scene and highlight the exact conflicting phrase on each. The same comparison must also be available in a 2D HTML panel with complete text, dates, and source links.

### 6.6 Verification Mission: “What should I check next?”

Checklist items appear as a short route/map of tasks. Completing a task adds a Kasukabe Defense Force-style stamp or Shinchan thumbs-up, with a restrained animation. The task remains editable; the animation is feedback, not a substitute for status text.

## 7. Evidence visual grammar

| Meaning | Visual | Accessible text label |
|---|---|---|
| Direct source passage | Solid green line + page pin | “Source passage supports this” |
| Candidate disagreement | Red split line + two passage cards | “Potential conflict — review both sources” |
| Partial/unclear coverage | Dotted yellow line + question marker | “Needs clarification” |
| Not found in current case | Open/empty clue slot + gold outline | “Not found in reviewed sources” |
| Older or undated source | Blue calendar stamp / faded paper | “Date warning — verify current version” |
| User verified | Green check + stamped card | “Verified by user” |

No 3D effect should state or imply a finding is more certain than the underlying evidence supports.

## 8. Motion, sound, and reduced-motion behavior

- Shinchan's idle loop: subtle breathing and occasional blink; no constant jumping.
- Pointer response: at most a small head/eye look toward a selected clue.
- Finding selection: a string brightens and the linked passage opens; no camera fly-through unless the user asks.
- Verified task: short stamp/pose, under one second.
- Loading: show real pipeline progress; use a small magnifier animation only as decoration.
- Sound is off by default. If used, provide a visible mute toggle and never use sound to convey status.
- `prefers-reduced-motion` disables idle animation, camera easing, and celebratory motion. The scene remains static and usable.

## 9. Accessibility and fallback specification

- The canvas has an accessible name and concise description.
- Every source, claim, connection, and task can be selected from a keyboard-accessible HTML list.
- Node selection moves focus to or announces the corresponding evidence inspector.
- Status changes are announced with an `aria-live` region.
- Focus rings, text contrast, labels, and icons are visible without the canvas.
- A **Switch to list view** control is always visible.
- If WebGL fails, show the same relationships in a 2D graph/list using SVG or HTML; do not show a blank rectangle.
- On low-power mobile devices, disable expensive shadows and reduce model detail while preserving the mascot and scene silhouette.

## 10. Technical art and performance targets

- Implement the scene with Three.js using React Three Fiber if the app uses React. Confirm major-version compatibility before selecting packages.
- Deliver model assets in compressed GLB/glTF where practical; include source files or a short asset provenance note.
- Target a small first-load experience: lazy-load 3D assets, cap texture sizes, compress geometry/textures, and avoid loading every character animation on the first screen.
- Use one primary 3D scene with reusable objects for source/claim nodes rather than separate expensive scenes per screen.
- Avoid continuous rendering while idle; pause animation when the page is hidden.
- Set a project budget for total initial 3D downloads and monitor mobile performance.
- Keep all source text and UI labels in normal HTML for crisp text and screen-reader support.

## 11. Asset-production fallback ladder

If the implementation AI cannot find or produce a full rigged model, proceed in this order while preserving the requirement that genuine 3D art is visible:

1. Build a simple custom low-poly/fan-model with head, hair, body, shirt, and shorts as separate meshes.
2. Add a small set of procedural animations (blink, point, idle) through transforms.
3. Create the desk, folders, magnifier, string, and room from reusable meshes.
4. Replace placeholder geometry with refined GLB models when available.

The first version can use a simple 3D model, but it must still be rendered in WebGL with depth, lighting, and interaction. A 2D face or flat SVG alone is not an acceptable substitute.

## 12. Final visual review checklist

- Shinchan is recognizable without reading the product name.
- At least one real 3D Shinchan character model is visible in the standard first-run flow.
- Users can click a 3D source or claim and see the matching HTML evidence.
- The red conflict thread opens both passages; the empty clue space explains the gap.
- The interface still communicates all evidence in 2D/list mode.
- The 3D scene never covers controls, quotes, dates, or navigation.
- Reduced motion and WebGL failure are handled.
- Colors, labels, and patterns make all statuses understandable without color vision.
- No unofficial art is presented as an official Shinchan asset.
