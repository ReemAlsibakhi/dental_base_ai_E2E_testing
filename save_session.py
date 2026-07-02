"""
Run this ONCE to save your login session.
After this, tests will never hit the login page again.

Usage: python3 save_session.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os, time
from dotenv import load_dotenv

load_dotenv()

BASE_URL  = os.getenv("BASE_URL", "https://dentalbase-dev-v2.vercel.app")
EMAIL     = os.getenv("ADMIN_EMAIL", "")
PASSWORD  = os.getenv("ADMIN_PASSWORD", "")
AUTH_DIR  = Path(".playwright_auth")
AUTH_FILE = AUTH_DIR / "admin.json"

AUTH_DIR.mkdir(exist_ok=True)

print("Opening browser — please wait for the spinner...")
print(f"Email: {EMAIL}")
print(f"Password: {'*' * len(PASSWORD)}\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(base_url=BASE_URL)
    page = context.new_page()

    page.goto("/login", wait_until="commit")
    print("Waiting for 'Get started' button (spinner may take 1-2 min)...")

    logged_in = False
    end = time.time() + 180

    while time.time() < end:
        # Already on overview
        if "/overview" in page.url:
            print("Already logged in!")
            logged_in = True
            break

        # Get started button appeared
        try:
            btn = page.locator("button:has-text('Get started')").first
            if btn.is_visible(timeout=500):
                print("'Get started' found — clicking...")
                btn.click()
                page.locator('#username').wait_for(state="visible", timeout=20_000)
                print(f"Filling credentials: {EMAIL}")
                page.locator('#username').fill(EMAIL)
                page.locator('#password').fill(PASSWORD)
                page.locator('#kc-login').click()
                print("Credentials submitted — waiting for /overview...")
                page.wait_for_url("**/overview**", timeout=60_000, wait_until="commit")
                print(f"Landed on: {page.url}")
                logged_in = True
                break
        except Exception as e:
            pass

        time.sleep(0.5)

    if not logged_in:
        print("❌ Login failed — session NOT saved")
        browser.close()
        exit(1)

    # Verify we are actually on /overview before saving
    if "/overview" not in page.url:
        print(f"❌ Expected /overview but got: {page.url} — session NOT saved")
        browser.close()
        exit(1)

    context.storage_state(path=str(AUTH_FILE))
    print(f"\n✅ Session saved to {AUTH_FILE}")
    print(f"   URL at save time: {page.url}")
    print("\nNow run: pytest tests/practice_profile/test_smoke_practice_profile.py --headed -v")
    browser.close()
