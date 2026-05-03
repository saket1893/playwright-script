from playwright.sync_api import sync_playwright
from config import config
from Data.locators import (
    MARKET_DATA_MENU,
    EQUITY_SME_MARKET_LINK,
    DOWNLOAD_CSV_BUTTON,
    DOWNLOAD_CSV_BUTTON_ALT_1,
    DOWNLOAD_CSV_BUTTON_ALT_2,
    DOWNLOAD_CSV_BUTTON_ALT_3,
    DOWNLOAD_CSV_BUTTON_ALT_4,
    DOWNLOAD_CSV_BUTTON_ALT_5,
    CSV_DOWNLOAD_PATH,
)


def test_open_page():
    with sync_playwright() as p:
        print("\n" + "=" * 60)
        print("TEST STARTED: Market Data Download Flow")
        print("=" * 60)

        print("\n[STEP 1] Launching browser...")
        browser = p.chromium.launch(headless=False, slow_mo=100, args=["--start-maximized"])
        context = browser.new_context(viewport=None)
        page = context.new_page()
        print("✓ Browser launched successfully and maximized")

        print("\n[STEP 2] Navigating to base URL...")
        page.goto(config.base_url, timeout=120000)
        print(f"✓ Navigated to {config.base_url}")

        print("\n[STEP 3] Waiting for page to fully load...")
        page.wait_for_load_state("networkidle")
        print("✓ Page fully loaded (networkidle)")

        title = page.title()
        print(f"✓ Page title: {title}")
        assert title is not None

        print("\n[STEP 4] Waiting for Market Data menu to be visible...")
        page.locator(MARKET_DATA_MENU).wait_for(timeout=10000)
        print(f"✓ Market Data menu is visible - Locator: {MARKET_DATA_MENU}")

        print("\n[STEP 5] Clicking on Market Data menu...")
        menu_element = page.locator(MARKET_DATA_MENU)
        menu_element.click()
        print("✓ Market Data menu clicked")

        print("\n[STEP 6] Waiting for dropdown menu to load...")
        page.wait_for_timeout(500)  # Wait for dropdown animation
        print("✓ Dropdown menu loaded")

        print("\n[STEP 7] Waiting for Equity & SME Market link to be visible...")
        page.locator(EQUITY_SME_MARKET_LINK).wait_for(timeout=10000)
        print(f"✓ Equity & SME Market link is visible - Locator: {EQUITY_SME_MARKET_LINK}")

        print("\n[STEP 8] Clicking on Equity & SME Market link...")
        equity_link = page.locator(EQUITY_SME_MARKET_LINK)
        equity_link.click()
        print("✓ Equity & SME Market link clicked")

        print("\n[STEP 9] Waiting for Equity market data table to load...")
        page.wait_for_load_state("networkidle")
        print("✓ Table loaded (networkidle)")

        print("\n[STEP 10] Waiting for CSV download button to be visible...")
        print(f"   - Primary locator: {DOWNLOAD_CSV_BUTTON}")
        print(f"   - Alt locator 1: {DOWNLOAD_CSV_BUTTON_ALT_1}")
        print(f"   - Alt locator 2: {DOWNLOAD_CSV_BUTTON_ALT_2}")
        print(f"   - Alt locator 3: {DOWNLOAD_CSV_BUTTON_ALT_3}")
        print(f"   - Alt locator 4: {DOWNLOAD_CSV_BUTTON_ALT_4}")
        print(f"   - Alt locator 5: {DOWNLOAD_CSV_BUTTON_ALT_5}")

        download_button = None
        button_locator = None
        locator_attempts = [
            (DOWNLOAD_CSV_BUTTON, "Primary - a#dnldEquityStock"),
            (DOWNLOAD_CSV_BUTTON_ALT_1, "Alt 1 - Full path to anchor"),
            (DOWNLOAD_CSV_BUTTON_ALT_2, "Alt 2 - Alternative path"),
            (DOWNLOAD_CSV_BUTTON_ALT_3, "Alt 3 - Generic downloads link"),
            (DOWNLOAD_CSV_BUTTON_ALT_4, "Alt 4 - Image inside anchor"),
            (DOWNLOAD_CSV_BUTTON_ALT_5, "Alt 5 - Span text"),
        ]

        for locator, label in locator_attempts:
            try:
                test_btn = page.locator(locator)
                test_btn.wait_for(timeout=5000)
                if test_btn.is_visible():
                    download_button = test_btn
                    button_locator = locator
                    print(f"✓ Found button with {label}: {locator}")
                    break
            except Exception as e:
                print(f"   - {label} failed: {str(e)}")
                continue

        if not download_button:
            print("✗ Download button not found with any locator!")
            print("\n[DEBUG] Taking screenshot to inspect page...")
            page.screenshot(path="screenshot_button_not_found.png")
            print("   - Screenshot saved to screenshot_button_not_found.png")
            raise AssertionError("Could not find CSV download button")

        print(f"✓ CSV download button found - Locator: {button_locator}")

        print("\n[STEP 11] Scrolling button into view...")
        download_button.scroll_into_view_if_needed()
        print("✓ Download button scrolled into view")

        print("\n[STEP 11.5] Checking button state...")
        is_enabled = download_button.is_enabled()
        is_visible = download_button.is_visible()
        print(f"   - Button enabled: {is_enabled}")
        print(f"   - Button visible: {is_visible}")

        print("\n[STEP 12] Taking screenshot before clicking...")
        page.screenshot(path="screenshot_before_download.png")
        print("   - Screenshot saved to screenshot_before_download.png")

        print("\n[STEP 13] Inspecting download button element...")
        # Get the href attribute to understand the click behavior
        href_attr = download_button.get_attribute('href')
        onclick_attr = download_button.get_attribute('onclick')
        data_attr = download_button.get_attribute('data-action')
        data_download = download_button.get_attribute('download')
        print(f"   - href: {href_attr}")
        print(f"   - onclick: {onclick_attr}")
        print(f"   - data-action: {data_attr}")
        print(f"   - download: {data_download}")

        print("\n[STEP 14] Attempting multiple click strategies...")
        download_triggered = False
        
        with page.expect_download(timeout=30000) as download_info:
            # Strategy 1: Hover and Click
            print("   [Strategy 1] Hover + Click...")
            try:
                download_button.hover()
                page.wait_for_timeout(300)
                download_button.click(force=True, timeout=5000)
                print("   ✓ Strategy 1: Hover + Click succeeded")
                download_triggered = True
            except Exception as e:
                print(f"   ✗ Strategy 1 failed: {e}")

            # Strategy 2: Double Click
            if not download_triggered:
                print("   [Strategy 2] Double Click...")
                try:
                    download_button.dblclick(force=True, timeout=5000)
                    print("   ✓ Strategy 2: Double Click succeeded")
                    download_triggered = True
                except Exception as e:
                    print(f"   ✗ Strategy 2 failed: {e}")

            # Strategy 3: Direct JavaScript click
            if not download_triggered:
                print("   [Strategy 3] Direct JavaScript click...")
                try:
                    page.evaluate('(selector) => document.querySelector(selector).click()', 'a#dnldEquityStock')
                    print("   ✓ Strategy 3: JavaScript click succeeded")
                    download_triggered = True
                except Exception as e:
                    print(f"   ✗ Strategy 3 failed: {e}")

            # Strategy 4: Click via parent anchor
            if not download_triggered:
                print("   [Strategy 4] Click parent anchor...")
                try:
                    parent = page.locator('a#dnldEquityStock')
                    parent.click(button='left', force=True, timeout=5000)
                    print("   ✓ Strategy 4: Parent anchor click succeeded")
                    download_triggered = True
                except Exception as e:
                    print(f"   ✗ Strategy 4 failed: {e}")

            # Strategy 5: Try clicking the image
            if not download_triggered:
                print("   [Strategy 5] Click image inside anchor...")
                try:
                    img = page.locator('a#dnldEquityStock img')
                    img.click(force=True, timeout=5000)
                    print("   ✓ Strategy 5: Image click succeeded")
                    download_triggered = True
                except Exception as e:
                    print(f"   ✗ Strategy 5 failed: {e}")

        if not download_triggered:
            print("✗ All click strategies failed!")
            raise AssertionError("Could not trigger download with any click method")

        print("\n[STEP 15] Download listener waiting for file...")
        download = download_info.value
        print(f"   ✓ Download started")
        print(f"   - Suggested filename: {download.suggested_filename}")

        print(f"\n[STEP 16] Saving CSV file to: {CSV_DOWNLOAD_PATH}")
        download.save_as(str(CSV_DOWNLOAD_PATH))
        print(f"✓ CSV file saved successfully at {CSV_DOWNLOAD_PATH}")

        print("\n[STEP 17] Verifying downloaded file exists...")
        if CSV_DOWNLOAD_PATH.exists():
            file_size = CSV_DOWNLOAD_PATH.stat().st_size
            print(f"✓ CSV file verified - Size: {file_size} bytes")
        else:
            print("✗ CSV file not found!")
            print(f"   - Expected path: {CSV_DOWNLOAD_PATH}")
            raise AssertionError(f"Downloaded file not found at {CSV_DOWNLOAD_PATH}")

        print("\n[STEP 18] Keeping browser open for inspection (2 minutes)...")
        page.wait_for_timeout(120000)  # 2 minutes

        print("\n" + "=" * 60)
        print("TEST COMPLETED SUCCESSFULLY")
        print("=" * 60 + "\n")