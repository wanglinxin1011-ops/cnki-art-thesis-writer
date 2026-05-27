"""Download CNKI articles via Playwright with a persistent browser profile.

Supports single URL download and batch download from JSON search results.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


def log(msg: str, log_file: Path | None = None) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} {msg}"
    print(line, flush=True)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a", encoding="utf-8") as f:
            f.write(line + "\n")


DOWNLOAD_SELECTORS = [
    "text=CAJ下载",
    "text=CAJ 下载",
    "a:has-text('CAJ')",
    "text=PDF下载",
    "text=PDF 下载",
    "a:has-text('PDF')",
    "a:has-text('整本下载')",
    "a:has-text('全文下载')",
    "a:has-text('下载')",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download CNKI papers.")
    parser.add_argument("--url", default=None, help="CNKI paper detail page URL")
    parser.add_argument("--batch", default=None, help="JSON file with paper list (each with 'url' field)")
    parser.add_argument("--download-dir", required=True, help="Directory for downloaded files")
    parser.add_argument("--profile-dir", required=True, help="Persistent Playwright profile directory")
    parser.add_argument("--log-file", default=None, help="Optional log file path")
    parser.add_argument("--wait-seconds", type=int, default=900, help="Max wait time for downloads")
    return parser.parse_args()


def download_paper(page, url: str, download_dir: Path, log_file: Path | None) -> Path | None:
    log(f"Navigate: {url}", log_file)
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3000)

    # Wait for login if needed
    deadline = time.time() + 120
    while time.time() < deadline:
        if "login" in page.url.lower() or "登录" in page.title():
            log("Waiting for user login...", log_file)
            page.wait_for_timeout(3000)
        else:
            break

    for selector in DOWNLOAD_SELECTORS:
        try:
            locator = page.locator(selector).first
            if locator.count() == 0:
                continue
            log(f"Click: {selector}", log_file)
            with page.expect_download(timeout=30000) as download_info:
                locator.click(timeout=10000)
            download = download_info.value
            target = download_dir / (download.suggested_filename or "cnki_download.caj")
            download.save_as(str(target))
            size = target.stat().st_size
            log(f"Saved: {target.name} ({size} bytes)", log_file)
            if size > 0:
                return target
        except PlaywrightTimeoutError:
            log(f"Timeout: {selector}", log_file)
        except Exception as e:
            log(f"Error: {selector}: {e}", log_file)
    return None


def main() -> None:
    args = parse_args()
    download_dir = Path(args.download_dir)
    profile_dir = Path(args.profile_dir)
    log_file = Path(args.log_file) if args.log_file else download_dir / "cnki_download.log"
    download_dir.mkdir(parents=True, exist_ok=True)
    profile_dir.mkdir(parents=True, exist_ok=True)

    papers = []
    if args.url:
        papers.append({"url": args.url})
    if args.batch:
        batch_data = json.loads(Path(args.batch).read_text(encoding="utf-8"))
        if isinstance(batch_data, list):
            papers.extend(batch_data)
        else:
            papers.append(batch_data)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=False,
            accept_downloads=True,
            downloads_path=str(download_dir),
            viewport={"width": 1366, "height": 900},
            locale="zh-CN",
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.set_default_timeout(20000)

        for i, paper in enumerate(papers):
            url = paper.get("url", paper.get("link", ""))
            if not url:
                log(f"Paper {i}: no URL, skip", log_file)
                continue
            log(f"Paper {i + 1}/{len(papers)}: {paper.get('title', url)}", log_file)
            result = download_paper(page, url, download_dir, log_file)
            if result:
                log(f"OK: {result.name}", log_file)
            else:
                log(f"FAIL: no download captured", log_file)
                screenshot = download_dir / f"fail_{i}.png"
                page.screenshot(path=str(screenshot), full_page=True)
                log(f"Screenshot: {screenshot}", log_file)

        context.close()
    log("Done", log_file)


if __name__ == "__main__":
    main()
