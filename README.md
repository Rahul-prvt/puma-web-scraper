# Puma Product Scraper

## Overview

This project scrapes product data from the Puma India website in two stages:

1. Collect all product URLs from a category listing page.
2. Visit each product page and extract structured product information.

The scraper uses Playwright for browser automation and Pandas for data processing.

---

## Scraping Approach

### Stage 1 — Product URL Collection

Script: `url_collector_full.py`

Purpose: Extract all individual product page URLs from the listing page.

Process:
- Launch Chromium using Playwright.
- Load the category page.
- Accept cookies if prompted.
- Scroll down repeatedly to trigger lazy loading.
- After each scroll, extract product links 

- Store URLs in a set to ensure uniqueness.
- Stop when the target count or maximum scroll limit is reached.
- Save the URLs into a CSV file.

Output: `puma_product_urls1.csv`

---

### Stage 2 — Product Data Extraction

Script: `scraper.py`

Purpose: Visit each collected URL and extract product details.

Extracted Fields:
- Product name
- Sale price
- MRP
- Brand (Puma)
- URL

Process:
- Load URLs from the CSV file.
- Visit each URL sequentially using one browser session.
- Extract elements using stable selectors:
- Title: `h1[data-test-id="pdp-title"]`
- Sale price: `span[data-test-id="item-sale-price-pdp"]`
- MRP: `span[data-test-id="item-price-pdp"]`
- Use try/except blocks to handle missing elements gracefully.
- Save results to a CSV file.

Output: `puma_products_stage2fast2.csv`

---

## Challenges Faced

| Challenge | Description |
|----------|-------------|
Dynamic content | Products load only when scrolling |
Cookie banner | Blocks interaction with the page |
Inconsistent pages | Some products lack sale price or expected structure |
Slow loading | Some pages timeout |
Duplicates | Same product loaded multiple times |

---

## How Challenges Were Handled

| Issue | Solution |
|------|----------|
Lazy loading | Simulated scrolling using mouse wheel |
Cookie popup | Click "Accept" button if present |
Missing elements | Wrapped extraction in try/except |
Timeouts | Skip failed URLs and continue |
Duplicates | Use a set to store URLs |

---

## Limitations

- No CAPTCHA or bot detection handling.
- Scraping is sequential, not parallel.
- HTML selectors are hardcoded and may break if the site changes.
- Only one category is scraped by default.
- No retry mechanism for failed pages.

---

## Summary

This scraper is designed for controlled and explainable data collection rather than large-scale crawling. It demonstrates dynamic page handling, defensive scraping, and a clean two-stage scraping pipeline.


Process:
- Launch Chromium using Playwright.
- Load the category page.
- Accept cookies if prompted.
- Scroll down repeatedly to trigger lazy loading.
- After each scroll, extract product links using:
