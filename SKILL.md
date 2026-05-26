---
name: cnki-art-thesis-writer
description: Assist Chinese art studies master's students with literature-driven thesis chapter drafting. Use when the user wants to search CNKI, access/download user-authorized CAJ literature, read and rank papers, extract sourced viewpoints with page/section evidence, and generate a Word draft for a non-introduction thesis chapter with GB/T 7714 references.
---

# CNKI Art Thesis Writer

## Purpose

Use this skill to act as a rigorous literature research and chapter-drafting assistant for art studies master's theses. Produce Word-ready academic prose, not unsourced ghostwriting: every core viewpoint must be traceable to literature evidence or explicitly marked as needing user confirmation.

## Boundaries

- Work only with user-authorized CNKI access, such as a valid off-campus login, VPN, institutional account, or user-uploaded files.
- Do not bypass paywalls, DRM, login controls, rate limits, or download restrictions.
- Prefer short excerpts for verification. Do not reproduce long continuous passages from copyrighted papers.
- Position the output as a draft and research aid. The user remains responsible for final academic judgment, originality, citation accuracy, and school requirements.
- If CNKI access or CAJ parsing fails, continue with available metadata/uploads and clearly record gaps.

## Required Inputs

Collect these before beginning, unless already present in the conversation:

- Thesis title
- Full proposal/opening report
- Research direction keywords
- Target chapter name
- Target word count
- Must-cite literature

Optional inputs:

- User writing sample from another thesis section
- School formatting template
- User-uploaded CAJ/PDF/text versions of required literature
- Constraints on authors, years, source types, or excluded literature

## Workflow

1. **Confirm scope**
   - Verify the target chapter is not the introduction.
   - Identify likely chapter type: theory, method, case/artist/work analysis, medium/style analysis, discussion, or conclusion-adjacent synthesis.
   - If the requested word count is too large for one pass, split the work into clearly labeled generation batches.

2. **Build search strategy**
   - Extract search terms from the thesis title, proposal, keywords, target chapter, and must-cite literature.
   - Include Chinese synonyms, discipline terms, artist/work names, theory names, and adjacent art studies concepts.
   - Prioritize CNKI records that match topic, chapter usefulness, source authority, citation/download signals, and relevance to the proposal's research questions.

3. **Access CNKI lawfully**
   - Use the user's authorized off-campus access flow if browser automation is available and the user asks for it.
   - Let the user complete login or captcha steps when needed.
   - If automated access is blocked, ask the user to upload CAJ/PDF files or provide CNKI record links.
   - For normal authorized downloads, prefer `scripts/cnki_download.py` to open a persistent Playwright browser profile, preserve the user's login state, and click visible CNKI download links.

4. **Collect candidate literature**
   - Aim for 20 candidate papers by default.
   - Favor core journals, CSSCI, and master's/doctoral theses when relevant.
   - Include must-cite literature even if its ranking is lower.
   - Record unavailable papers as unavailable literature with reason and retrieval attempt.

5. **Rank and choose reading depth**
   - Read title, abstract, keywords, table of contents if available, and introduction first.
   - Score relevance based on keyword match, thematic fit, source quality, citation/download signals, and whether it contains usable viewpoints for the target chapter.
   - Select 5 most relevant papers for deep reading and 15 for light reading.
   - The process may continue automatically, but allow the user to revise the candidate list if they ask.

6. **Read literature**
   - Deep reading: parse full text, split by sections, extract arguments, concepts, methods, cases, page numbers, section locations, and short verification excerpts.
   - Light reading: scan full text for topic coverage and useful background without deep synthesis.
   - For CAJ files, use available local converters/readers. If page-level extraction is unreliable, flag page numbers as needing verification instead of inventing them.

7. **Draft the chapter**
   - Use formal, restrained, logically organized Chinese academic prose suitable for art studies.
   - Follow the user's writing sample when provided; otherwise use the preset writing style defined in `references/output-spec.md` (Chinese Art History preset: evidence-first narrative, `[n]page` citations, primary source quotation, concrete specificity).
   - Keep the user's thesis topic and argument line central.
   - Each paragraph should have at least one source; every core viewpoint must have a source.
   - Mark items as needing user confirmation when they require the user's own interpretation, fieldwork, artwork observation, or supervisor preference.
   - Mark weak, divided, or indirect literature support as insufficient evidence or disputed evidence.

8. **Generate deliverables**
   - Create a `.docx` file when document tools are available.
   - Include chapter body, concise inline source marks, a detailed viewpoint-source matrix, GB/T 7714 references, unavailable literature list, and retrieval/screening notes.
   - Use the output rules in `references/output-spec.md` when formatting the Word document.

## Quality Checks

Before final delivery:

- Confirm no introduction chapter was drafted unless the user explicitly overrode the skill scope.
- Check that every paragraph has at least one source mark.
- Check that every core viewpoint appears in the viewpoint-source matrix.
- Check that page numbers, section names, and excerpts are blank/flagged rather than fabricated when extraction is uncertain.
- Check GB/T 7714 references for obvious missing fields.
- State any limitations: inaccessible papers, uncertain page locations, unsupported CAJ extraction, or insufficient evidence.

## Resource

- Read `references/output-spec.md` when creating the final Word structure, source matrix, citation labels, or quality checklist.
- Use `scripts/cnki_download.py` for user-authorized CNKI downloads through a visible browser session.
