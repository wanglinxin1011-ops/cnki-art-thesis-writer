---
name: cnki-researcher
description: End-to-end orchestrator for CNKI literature research and thesis chapter drafting. Runs the full pipeline: search → screen → download → read → draft → review → deliver. Supports session persistence, interrupt-resume, and quality-gated iteration.
---

# CNKI Researcher Agent

Orchestrate the full research-and-writing pipeline. This agent manages cross-cutting concerns (session, progress, retry) and delegates each phase to the appropriate sub-skill.

## Phases

```
[Phase 0] Init session → [P1] Search CNKI → [P2] Screen & rank → [P3] Download →
[P4] Read & extract → [P5] Draft chapter → [P6] Quality review →
[P7] Deliver .docx
         ↑____________ failed review _____________↓
```

### Phase 0: Init session
- Create a session directory: `sessions/{topic_slug}_{YYYYMMDD}/`
- Save user inputs (thesis title, proposal, target chapter, constraints) to `session.json`
- Track progress in `progress.json`: `{"phase": 0, "status": "in_progress", "papers": [], "notes": {}}`

### Phase 1: Search CNKI
- Read `skills/cnki-search/SKILL.md`
- Extract search terms from thesis title, proposal, keywords, target chapter
- Run searches for each term cluster (aim for 20+ candidate papers)
- Favor core journals, CSSCI, and relevant master's/doctoral theses
- Save results to `papers/candidates.json`
- Update `progress.json` phase → 1

### Phase 2: Screen & rank
- Read titles, abstracts, keywords for all candidates
- Score relevance numerically (0-10)
- Select 5 for deep reading, ~15 for light reading
- Update `progress.json` with rankings

### Phase 3: Download
- Read `skills/cnki-download/SKILL.md`
- For each paper selected for deep reading, attempt download using the Playwright script
- Record successful downloads in `papers/downloaded/` 
- Record unavailable papers with reason
- For CAJ files, note that the user may need to use CAJViewer

### Phase 4: Read & extract
- For deep-read papers: extract arguments, concepts, cases, page numbers, section locations
- For light-read papers: note topic coverage and useful background
- Build the viewpoint-source matrix incrementally in `draft/matrix.json`
- Flag uncertain page numbers

### Phase 5: Draft chapter
- Read `skills/thesis-draft/SKILL.md` and `references/output-spec.md`
- Write chapter body with citation marks
- Build viewpoint-source matrix table
- Generate GB/T 7714 references from paper metadata

### Phase 6: Quality review
Check:
1. Is this an introduction chapter? → reject
2. Does every paragraph have ≥1 source mark?
3. Are page numbers and excerpts verified (not fabricated)?
4. Are GB/T 7714 refs complete? Mark missing fields as `待补全`
5. Is the viewpoint-source matrix populated?

If review score < 70%, go back to Phase 5 with specific revision notes.
If review score < 50%, go back to Phase 1 to search for more papers.

### Phase 7: Deliver
- Create .docx with python-docx
- Include: chapter body → matrix → references → user confirmation items → unavailable list → retrieval notes
- State total papers found, deep-read, light-read, unavailable
- Warn about any uncertain page numbers or extraction limitations

## Session management

Each session directory:
```
sessions/{topic_slug}_{YYYYMMDD}/
├── session.json          # User inputs & parameters
├── progress.json         # Phase tracking {phase, status, notes}
├── papers/
│   ├── candidates.json   # All search results
│   ├── ranked.json       # Scored & ranked
│   └── downloaded/       # Downloaded paper files
└── draft/
    ├── matrix.json       # Viewpoint-source matrix
    ├── chapter.md        # Chapter draft
    └── references.json   # GB/T 7714 references
```

To resume a session: read `progress.json`, identify the last incomplete phase, and restart from there.

## Interrupt handling

If the user interrupts mid-pipeline:
1. Save current phase and all data to session directory
2. On next invocation, if a session directory exists, offer to resume
3. Resume from the saved phase
