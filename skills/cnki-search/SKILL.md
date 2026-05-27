---
name: cnki-search
description: Search CNKI (中国知网) for academic papers, browse journals, extract structured metadata. Supports keyword search, advanced filters (CSSCI/北大核心), journal browsing, and batch metadata extraction.
---

# CNKI Search

Search CNKI and extract structured paper metadata using browser automation. Works with both Chrome DevTools MCP (recommended) and Playwright (fallback).

## Search modes

### 1. Quick keyword search
Search by topic keywords. Returns title, authors, source, year, volume, pages, citation/download counts.

### 2. Advanced search
Apply filters: author, journal, date range, source category (SCI/EI/CSSCI/北大核心/CSCD), fund, DOI.

### 3. Journal search
Find journals by name, ISSN, or CN; check indexing status and impact factors.

## Using Playwright script (fallback)

When Chrome DevTools MCP is not available, use the bundled script:

```python
python cnki_search.py --keyword "关键词" [--filters ...] [--save results.json]
```

Parameters:
- `--keyword` (required): Search term
- `--db-code`: Database code (CJFD=journals, CDMD=dissertations, all=default)
- `--source-category`: CSSCI, 北大核心, SCI, EI, CSCD
- `--year-from` / `--year-to`: Year range
- `--max-results`: Max papers to extract (default 20)
- `--save`: JSON output path

Output is a JSON array of papers with: title, authors, source, year, volume, issue, pages, doi, abstract, keywords, citation_count, download_count, url.

## Using Chrome DevTools MCP (recommended)

If Chrome DevTools MCP is installed and Chrome is running with `--remote-debugging-port=9222`:

1. Navigate to the CNKI search URL directly
2. Use `evaluate_script` to extract structured data from the results table
3. Parse and filter results

CNKI search URL format:
```
https://kns.cnki.net/kns8/defaultresult/index?kwd=关键词&dbCode=SCDB
```

Key JS selectors for data extraction (on search results page):
```javascript
// Extract paper rows from the result table
const rows = document.querySelectorAll('.result-table tbody tr');
// Each row contains: title link, authors, source, year, citation/download counts
```

## Search strategy for art studies

Read `references/cnki-strategy.md` for art-studies-specific keyword strategies, recommended journals (CSSCI art studies), and thesis-level search patterns.

## Output format

Save search results as JSON for downstream consumption by the download or drafting sub-skills:
```json
[
  {
    "id": 1,
    "title": "战国楚漆器纹样的审美特征研究",
    "authors": ["张三", "李四"],
    "source": "装饰",
    "year": 2023,
    "volume": "45",
    "issue": "3",
    "pages": "88-95",
    "doi": "10.xxx/xxxxx",
    "abstract": "...",
    "keywords": ["楚漆器", "纹样", "审美"],
    "citation_count": 12,
    "download_count": 345,
    "url": "https://kns.cnki.net/kcms2/article/abstract?...",
    "source_category": "CSSCI"
  }
]
```
