from playwright.sync_api import sync_playwright
import pandas as pd
import time

INPUT_FILE = "puma_product_urls.csv"
OUTPUT_FILE = "puma_products_stage2fast2.csv"


def scrape_product_page(page, url):
    page.goto(url, wait_until="domcontentloaded", timeout=60000)

    data = {
        "url": url,
        "brand": "Puma",
        "product_name": None,
        "sale_price": None,
        "mrp": None,
    }

    try:
        data["product_name"] = page.locator('h1[data-test-id="pdp-title"]').inner_text(timeout=3000)
    except:
        pass

    try:
        data["sale_price"] = page.locator('span[data-test-id="item-sale-price-pdp"]').inner_text(timeout=2000)
    except:
        pass

    try:
        data["mrp"] = page.locator('span[data-test-id="item-price-pdp"]').inner_text(timeout=2000)
    except:
        pass

    return data


def run_stage2_fast():
    urls = pd.read_csv(INPUT_FILE)["product_url"].dropna().unique().tolist()
    print(f"Loaded {len(urls)} URLs")

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for i, url in enumerate(urls, 1):
            if i % 25 == 0:
                print(f"{i}/{len(urls)} done...")

            try:
                results.append(scrape_product_page(page, url))
            except Exception as e:
                print("Failed:", url, e)

        browser.close()

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✓ Saved {len(df)} records to {OUTPUT_FILE}")


if __name__ == "__main__":
    run_stage2_fast()
