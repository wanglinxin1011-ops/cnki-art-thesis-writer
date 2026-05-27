"""CNKI paper search via Playwright browser automation.

Extracts structured metadata from CNKI search result pages.
Usage:
    python cnki_search.py --keyword "战国漆器" --max-results 20 --save results.json
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from urllib.parse import urlencode

from playwright.sync_api import sync_playwright


DB_CODES = {
    "all": "SCDB",
    "journals": "CJFD",
    "dissertations": "CDMD",
    "conferences": "CPFD",
    "newspapers": "CCND",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search CNKI and extract paper metadata.")
    parser.add_argument("--keyword", required=True, help="Search keyword")
    parser.add_argument("--db-code", default="all", choices=list(DB_CODES.keys()), help="Database to search")
    parser.add_argument("--source-category", default=None, help="CSSCI, 北大核心, SCI, EI, CSCD")
    parser.add_argument("--year-from", type=int, default=None, help="Start year")
    parser.add_argument("--year-to", type=int, default=None, help="End year")
    parser.add_argument("--max-results", type=int, default=20, help="Max papers to extract")
    parser.add_argument("--save", default=None, help="Output JSON file path")
    parser.add_argument("--profile-dir", default=None, help="Playwright profile directory for logged-in session")
    parser.add_argument("--headless", action="store_true", help="Run headless")
    return parser.parse_args()


def build_search_url(keyword: str, db_code: str, source_category: str | None, year_from: int | None, year_to: int | None) -> str:
    params = {"kwd": keyword, "dbCode": DB_CODES.get(db_code, "SCDB")}
    filters = []
    if source_category:
        filters.append(f'source_category:{source_category}')
    if year_from:
        filters.append(f'year:{year_from}-{year_to or ""}')
    if filters:
        params["f"] = ";".join(filters)
    return f"https://kns.cnki.net/kns8/defaultresult/index?{urlencode(params)}"


def extract_papers_from_page(page, max_results: int) -> list[dict]:
    """Extract paper metadata from the current CNKI search results page using page.evaluate."""
    papers = page.evaluate("""(maxResults) => {
        const rows = document.querySelectorAll('.result-table tbody tr, .list_table tbody tr');
        const results = [];
        for (const row of rows) {
            if (results.length >= maxResults) break;
            const titleLink = row.querySelector('.fz14 a, .name a, a[target="_blank"]');
            if (!titleLink) continue;
            const title = (titleLink.textContent || '').trim();
            const url = titleLink.href || '';
            
            const cells = row.querySelectorAll('td');
            const textCells = Array.from(cells).map(c => (c.textContent || '').trim());
            
            results.push({
                title: title.replace(/\\[.*?\\]/g, '').trim(),
                authors: (textCells[1] || '').split(/[;,]/).map(s => s.trim()).filter(Boolean),
                source: textCells[2] || '',
                year: textCells[3] || '',
                volume: textCells[4] || '',
                citation_count: parseInt(textCells[5]) || 0,
                download_count: parseInt(textCells[6]) || 0,
                url: url,
            });
        }
        return results;
    }""", max_results)
    return papers


def main() -> None:
    args = parse_args()
    url = build_search_url(args.keyword, args.db_code, args.source_category, args.year_from, args.year_to)
    
    with sync_playwright() as p:
        browser_args = {}
        if args.profile_dir:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=args.profile_dir,
                headless=args.headless,
                viewport={"width": 1366, "height": 900},
            )
            page = browser.pages[0] if browser.pages else browser.new_page()
            browser_obj = browser
        else:
            browser_obj = p.chromium.launch(headless=args.headless)
            page = browser_obj.new_page()
        
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)
            
            # Handle login if needed
            if "login" in page.url.lower():
                print("Login required. User must complete login manually.", flush=True)
                page.wait_for_timeout(60000)
            
            all_papers = []
            page_num = 0
            
            while len(all_papers) < args.max_results:
                page.wait_for_timeout(2000)
                papers = extract_papers_from_page(page, args.max_results - len(all_papers))
                all_papers.extend(papers)
                
                if len(all_papers) >= args.max_results:
                    break
                
                # Try to go to next page
                next_btn = page.locator('a.next, .page-next, a:has-text("下一页")').first
                if next_btn.count() == 0:
                    break
                disabled = next_btn.get_attribute("disabled") or next_btn.get_attribute("aria-disabled")
                if disabled:
                    break
                next_btn.click()
                page_num += 1
                page.wait_for_timeout(3000)
            
            print(f"Extracted {len(all_papers)} papers", flush=True)
            
            if args.save:
                output_path = Path(args.save)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(json.dumps(all_papers, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"Saved to {output_path}", flush=True)
            else:
                print(json.dumps(all_papers, ensure_ascii=False, indent=2), flush=True)
                
        finally:
            browser_obj.close()


if __name__ == "__main__":
    main()
