"""
save_practice_session.py

Run ONCE to save a session already on Practice Profile & Hours tab.
After this, all Module 2 tests start directly on the right tab.

Usage: python3 save_practice_session.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os, time
from dotenv import load_dotenv

load_dotenv()

BASE_URL   = os.getenv("BASE_URL", "https://dentalbase-dev-v2.vercel.app")
AUTH_DIR   = Path(".playwright_auth")
ADMIN_STATE     = AUTH_DIR / "admin.json"
PRACTICE_STATE  = AUTH_DIR / "practice_profile.json"

AUTH_DIR.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        base_url=BASE_URL,
        storage_state=str(ADMIN_STATE),
        viewport={"width": 1920, "height": 1080},
    )
    page = context.new_page()

    print("Going to /settings...")
    page.goto("/settings", wait_until="commit")

    print("Waiting for Practice Profile & Hours tab...")
    end = time.time() + 120
    while time.time() < end:
        tab = page.get_by_role("button", name="Practice Profile & Hours", exact=True)
        if tab.is_visible():
            tab.click()
            print("Tab clicked!")
            time.sleep(2)
            break
        time.sleep(0.5)

    # Save state AFTER clicking the tab
    context.storage_state(path=str(PRACTICE_STATE))
    print(f"✅ Practice Profile session saved to {PRACTICE_STATE}")
    browser.close()
