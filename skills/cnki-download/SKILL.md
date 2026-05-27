---
name: cnki-download
description: Download papers from CNKI as CAJ or PDF files using Playwright browser automation. Accepts a CNKI paper URL or paper metadata, opens a visible browser, clicks download links, and saves the file.
---

# CNKI Download

Download papers from CNKI using the bundled Playwright script. Works with a persistent browser profile to preserve login state.

## Usage

```python
python scripts/cnki_download.py --url "CNKI_PAPER_URL" --download-dir "./papers" --profile-dir "./wecom_session"
```

Parameters:
- `--url`: CNKI paper detail page URL (required)
- `--download-dir`: Where to save downloaded files (required)
- `--profile-dir`: Playwright profile directory with saved login (required)
- `--wait-seconds`: Max time to wait for download (default 900)
- `--log-file`: Optional log file path

For batch download from search results JSON:
```python
python cnki_download.py --batch results.json --download-dir "./papers" --profile-dir "./wecom_session"
```

## File types

The script tries download selectors in order:
1. CAJ download (primary for CNKI)
2. PDF download (when available)
3. Full-text download (generic fallback)

After download, the script verifies the file is non-empty and saves it with its suggested filename.

## Tips

- First run will prompt for CNKI login — complete it in the visible browser window
- Subsequent runs reuse the saved session in `--profile-dir`
- If download links are not visible, the user may need to click through first
