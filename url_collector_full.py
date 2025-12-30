from playwright.sync_api import sync_playwright
import pandas as pd
import time

URL = "https://in.puma.com/in/en/womens/womens-shoes"
TARGET = 732


def scroll_and_collect(page, delay=5, scroll_px=1000, max_rounds=200):
    collected = set()

    for i in range(max_rounds):
        # collect visible URLs
        links = page.locator('li[data-test-id="product-list-item"] a[data-test-id="product-list-item-link"]')
        for j in range(links.count()):
            href = links.nth(j).get_attribute("href")
            if href:
                full_url = "https://in.puma.com" + href if href.startswith("/") else href
                collected.add(full_url)

        print(f"Round {i+1}: collected {len(collected)} unique URLs")

        # stop if target reached
        if len(collected) >= TARGET:
            print("Target reached!")
            break

        # scroll
        page.mouse.wheel(0, scroll_px)
        time.sleep(delay)

    return collected


def collect_product_urls():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=150)
        page = browser.new_page()

        page.goto(URL, timeout=60000)
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)

        try:
            page.click("button:has-text('Accept')", timeout=2000)
        except:
            pass

        time.sleep(3)

        urls = scroll_and_collect(page)

        browser.close()

    return urls


if __name__ == "__main__":
    print("Starting URL collection...\n")

    urls = collect_product_urls()

    df = pd.DataFrame({"product_url": list(urls)})
    df.to_csv("puma_product_urls1.csv", index=False)

    print(f"\n✓ Saved {len(df)} unique product URLs.")
