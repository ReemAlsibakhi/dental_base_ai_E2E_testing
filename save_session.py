"""
Run this ONCE to save your login session.
After this, tests will never hit the login page again.

Usage: python3 save_session.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
import time

load_dotenv()

BASE_URL  = os.getenv("BASE_URL", "https://dentalbase-dev-v2.vercel.app")
EMAIL     = os.getenv("ADMIN_EMAIL", "")
PASSWORD  = os.getenv("ADMIN_PASSWORD", "")
AUTH_DIR  = Path(".playwright_auth")
AUTH_FILE = AUTH_DIR / "admin.json"

AUTH_DIR.mkdir(exist_ok=True)

print("Opening browser — please wait for the spinner...")
print("This may take up to 2 minutes on the dev environment.\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headed so you can see it
    context = browser.new_context(base_url=BASE_URL)
    page = context.new_page()

    page.goto("/login", wait_until="commit")
    print("Waiting for 'Get started' button (spinner may take 1-2 min)...")

    # Wait up to 3 minutes
    end = time.time() + 180
    while time.time() < end:
        if "/overview" in page.url:
            print("Already logged in!")
            break
        if page.locator("button:has-text('Get started')").is_visible():
            print("'Get started' found — clicking...")
            page.locator("button:has-text('Get started')").click()
            page.locator('#username').wait_for(state="visible", timeout=20_000)
            page.locator('#username').fill(EMAIL)
            page.locator('#password').fill(PASSWORD)
            page.locator('#kc-login').click()
            print("Credentials submitted — waiting for /overview...")
            page.wait_for_url("**/overview**", timeout=60_000, wait_until="commit")
            break
        time.sleep(0.5)

    context.storage_state(path=str(AUTH_FILE))
    print(f"\n✅ Session saved to {AUTH_FILE}")
    print("Now run: pytest tests/profile/test_smoke.py --headed -v")
    browser.close()
