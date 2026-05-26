"""Download a CNKI article through the user's authorized browser session.

This helper opens a visible Playwright browser with a persistent profile. The
user must complete any CNKI login, off-campus access, captcha, or institutional
authorization manually. The script only clicks normal visible download links and
captures the resulting file.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


def append_log(log_file: Path, message: str) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("a", encoding="utf-8") as fh:
        fh.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {message}\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="CNKI detail page URL.")
    parser.add_argument("--download-dir", required=True, help="Directory for downloaded files.")
    parser.add_argument("--profile-dir", required=True, help="Persistent Playwright profile directory.")
    parser.add_argument("--log-file", default=None, help="Optional log file path.")
    parser.add_argument(
        "--wait-seconds",
        type=int,
        default=900,
        help="How long to wait for user login or download completion.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    download_dir = Path(args.download_dir)
    profile_dir = Path(args.profile_dir)
    log_file = Path(args.log_file) if args.log_file else download_dir / "cnki_download.log"
    download_dir.mkdir(parents=True, exist_ok=True)
    profile_dir.mkdir(parents=True, exist_ok=True)
    log_file.write_text("", encoding="utf-8")

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
        page.set_default_timeout(20_000)
        append_log(log_file, f"open {args.url}")
        page.goto(args.url, wait_until="domcontentloaded", timeout=60_000)
        page.wait_for_timeout(3000)
        append_log(log_file, f"url={page.url}")
        append_log(log_file, f"title={page.title()}")

        deadline = time.time() + args.wait_seconds
        saved_files: list[Path] = []

        while time.time() < deadline and not saved_files:
            title = page.title()
            if "login" in page.url.lower() or "登录" in title:
                append_log(log_file, "waiting for user login")
                page.wait_for_timeout(3000)
                continue

            links = page.locator("a").evaluate_all(
                """els => els.map((a, i) => ({
                    i,
                    text: (a.innerText || a.textContent || '').trim(),
                    href: a.href || '',
                    cls: a.className || '',
                    id: a.id || ''
                })).filter(x => x.text || x.href)"""
            )
            append_log(log_file, f"links={json.dumps(links, ensure_ascii=False)[:3000]}")

            selectors = [
                "text=CAJ下载",
                "text=CAJ 下载",
                "a:has-text('CAJ')",
                "a:has-text('整本下载')",
                "a:has-text('全文下载')",
                "a:has-text('下载')",
            ]
            for selector in selectors:
                try:
                    locator = page.locator(selector).first
                    if locator.count() == 0:
                        continue
                    append_log(log_file, f"click {selector}")
                    with page.expect_download(timeout=30_000) as download_info:
                        locator.click(timeout=10_000)
                    download = download_info.value
                    target = download_dir / (download.suggested_filename or "cnki_download.caj")
                    download.save_as(str(target))
                    append_log(log_file, f"saved {target} size={target.stat().st_size}")
                    saved_files.append(target)
                    break
                except PlaywrightTimeoutError:
                    append_log(log_file, f"no download after {selector}")
                except Exception as exc:
                    append_log(log_file, f"selector failed {selector}: {exc}")

            if not saved_files:
                page.wait_for_timeout(3000)

        if not saved_files:
            screenshot = download_dir / "cnki_download_failed.png"
            page.screenshot(path=str(screenshot), full_page=True)
            append_log(log_file, f"no download captured; screenshot={screenshot}")

        context.close()


if __name__ == "__main__":
    main()
