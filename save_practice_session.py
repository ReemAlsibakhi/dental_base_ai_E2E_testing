"""
save_practice_session.py

Run ONCE to save a session on Practice Profile & Hours tab.
Handles login automatically — same as save_session.py.

Usage: python3 save_practice_session.py
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
ADMIN_STATE    = AUTH_DIR / "admin.json"
PRACTICE_STATE = AUTH_DIR / "practice_profile.json"

AUTH_DIR.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(base_url=BASE_URL)
    page = context.new_page()

    # ── Step 1: Login ──────────────────────────────────────────────
    print("Step 1: Going to /login ...")
    page.goto("/login", wait_until="commit")

    end = time.time() + 180
    while time.time() < end:
        if "/overview" in page.url:
            print("Already logged in!")
            break
        btn = page.locator("button:has-text('Get started')")
        if btn.is_visible():
            print("Clicking Get started ...")
            btn.click()
            page.locator('#username').wait_for(state="visible", timeout=20_000)
            page.locator('#username').fill(EMAIL)
            page.locator('#password').fill(PASSWORD)
            page.locator('#kc-login').click()
            print("Waiting for /overview ...")
            page.wait_for_url("**/overview**", timeout=60_000, wait_until="commit")
            break
        time.sleep(0.5)

    print(f"Logged in: {page.url}")

    # ── Step 2: Go to Settings ─────────────────────────────────────
    print("\nStep 2: Going to /settings ...")
    page.goto("/settings", wait_until="commit")

    # ── Step 3: Wait for Practice Profile tab and click it ─────────
    print("Step 3: Waiting for Practice Profile & Hours tab ...")
    end = time.time() + 120
    while time.time() < end:
        tab = page.get_by_role("button", name="Practice Profile & Hours", exact=True)
        if tab.is_visible():
            tab.click()
            print("Tab clicked!")
            time.sleep(2)
            break
        time.sleep(0.5)
    else:
        print("❌ Tab never appeared!")
        browser.close()
        exit(1)

    # ── Step 4: Save both sessions ─────────────────────────────────
    context.storage_state(path=str(ADMIN_STATE))
    context.storage_state(path=str(PRACTICE_STATE))
    print(f"\n✅ Admin session saved:    {ADMIN_STATE}")
    print(f"✅ Practice session saved: {PRACTICE_STATE}")
    print("\nNow run: pytest tests/practice_profile/ --headed -v")
    browser.close()
