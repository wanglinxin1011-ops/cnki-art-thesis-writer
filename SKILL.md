---
name: cnki-art-thesis-writer
description: Orchestrate CNKI literature research, paper search/download, and thesis chapter drafting for Chinese art studies master's students. Use when the user wants to search CNKI, find/download papers, extract viewpoints with page evidence, write thesis chapters, or generate a Word draft with GB/T 7714 references.
---

# CNKI Art Thesis Writer — Orchestrator

This is the entry point for a multi-phase research-and-writing workflow. Route to sub-skills based on what phase the user is in:

| Phase | Sub-skill | When to use |
|-------|-----------|-------------|
| 1. Search CNKI | `skills/cnki-search/` | User wants to find papers, browse journals, or build a candidate list |
| 2. Download papers | `skills/cnki-download/` | User wants to download PDF/CAJ files from CNKI |
| 3. Draft chapter | `skills/thesis-draft/` | User has literature and wants to write a thesis chapter |

For end-to-end automation, read and invoke the agent at `agents/cnki-researcher.md` which orchestrates all phases with session persistence and interrupt-resume.

## Prerequisites

- Node.js >= 18 (for Chrome DevTools MCP — primary automation path)
- Python 3.8+ with `pip install playwright` (fallback for downloads)
- Playwright browsers: `python -m playwright install chromium`
- Chrome/Chromium browser
- Valid CNKI institutional or off-campus login

## Boundaries

- Work only with user-authorized CNKI access. Do not bypass paywalls, DRM, or rate limits.
- Prefer short excerpts. Do not reproduce long continuous passages from copyrighted papers.
- The output is a draft and research aid. The user is responsible for final academic judgment.
- If automation fails, continue with available metadata or user-uploaded files and clearly record gaps.

## Quick Reference

When the user makes a request, identify which phase they're in, read that sub-skill's SKILL.md, and follow its instructions. For full workflow automation (search → screen → download → analyze → draft → deliver), use the orchestrator agent.
