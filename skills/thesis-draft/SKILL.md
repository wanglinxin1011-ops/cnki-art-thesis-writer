---
name: thesis-draft
description: Draft a non-introduction thesis chapter for Chinese art studies master's thesis, driven by sourced literature. Extracts viewpoints with page/section evidence, generates a Word document with GB/T 7714 references, viewpoint-source matrix, and quality review. Use when the user has literature and wants to write a thesis chapter body.
---

# Thesis Chapter Drafting

Produce rigorous, sourced Chinese academic prose for a thesis chapter. Every core viewpoint must be traceable to literature evidence or explicitly flagged for user confirmation.

## Required inputs

- Thesis title + full proposal
- Target chapter name
- Target word count
- Literature papers (from search/download phases, or user-uploaded CAJ/PDF)
- Must-cite literature if any

Optional:
- User writing sample from another thesis section
- School formatting template
- Constraints on authors, years, source types

## Workflow

### 1. Confirm scope
- Target chapter must NOT be the introduction
- Identify chapter type: theory, method, case/artist/work analysis, medium/style, discussion, synthesis
- If word count is too large for one pass, split into labeled batches

### 2. Read and rank literature
- Read title, abstract, keywords, TOC, introduction first
- Score relevance: keyword match, thematic fit, source quality, citation/download signals
- Select 5 for deep reading (full text, section-by-section extraction) and ~15 for light reading
- For CAJ files: use available converters. Flag uncertain page numbers rather than inventing them.

### 3. Extract viewpoints
For each paper (especially deep-read ones):
- Arguments, concepts, methods, cases, artist works
- Page numbers, section/chapter locations
- Short verification excerpts
- Organize into the viewpoint-source matrix format

### 4. Draft the chapter
- Formal Chinese academic prose suitable for art studies
- Evidence-first narrative: open with facts (dates, artifacts, quantities), then interpret
- Every paragraph must have at least one source
- Use `[n]page` citation format — not inline parenthetical refs
- Mark items needing user confirmation: `待用户确认`, `证据不足`, `存在争议`, `页码需核查`
- Follow the writing sample when provided; otherwise use the preset style in `references/output-spec.md`

### 5. Generate reading list
Search for remaining papers that are relevant and accessible. Record unavailable papers with reason.

### 6. Quality review
Before delivery:
- Check every paragraph has at least one source mark
- Check every core viewpoint appears in the viewpoint-source matrix
- Check page numbers and excerpts are verified, not fabricated
- Check GB/T 7714 references for missing fields
- State limitations: inaccessible papers, uncertain page locations, inadequate evidence

### 7. Deliver
Create a .docx with:
1. Chapter title and body
2. Viewpoint-source matrix (table)
3. GB/T 7714 references
4. Issues requiring user confirmation
5. Unavailable literature list
6. Retrieval and screening notes

## Citation format

Use the preset art-history writing style defined in `references/output-spec.md`:
- `[n]page` — e.g., `……制作精美的饮食器具——漆杯的景象：[3]228`
- Multiple sources: `[2]45-48; [4]15-20`
- Primary source: quote original in indented block, then interpret with `此处提到的`

## Viewpoint-source matrix

| 观点 | 来源文献 | 页码 | 文献章节/位置 | 原文摘录 | 使用方式 | 可靠性/备注 |
|---|---|---|---|---|---|---|

Usage types: 直接引用, 转述, 综合归纳, 灵感启发

If exact page/excerpt is uncertain: write `需用户核查` with explanation.
