"""
conftest.py — Global pytest fixtures for the DentalBase Profile E2E suite.

Auth flow:
  1. Navigate to /login — app may redirect immediately to /overview if session exists
  2. If on /login → click "Get started" → Keycloak → fill credentials
  3. Storage state saved; every test reuses it — no re-login per test.
"""

import os
import pytest
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from pages.login_page import LoginPage
from pages.profile_page import ProfilePage

load_dotenv()

BASE_URL          = os.getenv("BASE_URL", "https://dentalbase-dev-v2.vercel.app")
ADMIN_EMAIL       = os.getenv("ADMIN_EMAIL", "")
ADMIN_PASSWORD    = os.getenv("ADMIN_PASSWORD", "")
NON_ADMIN_EMAIL   = os.getenv("NON_ADMIN_EMAIL", "")
NON_ADMIN_PASSWORD = os.getenv("NON_ADMIN_PASSWORD", "")
HEADLESS          = os.getenv("HEADLESS", "true").lower() == "true"
SLOW_MO           = int(os.getenv("SLOW_MO", "0"))

AUTH_DIR        = Path(".playwright_auth")
ADMIN_STATE     = AUTH_DIR / "admin.json"
NON_ADMIN_STATE = AUTH_DIR / "non_admin.json"


# ---------------------------------------------------------------------------
# Browser — one process per session
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO,
            args=["--no-sandbox"],
        )
        yield browser
        browser.close()


# ---------------------------------------------------------------------------
# Auth state — login once, persist to disk
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def admin_auth_state(browser_instance: Browser) -> Path:
    AUTH_DIR.mkdir(exist_ok=True)
    context = browser_instance.new_context(
        base_url=BASE_URL,
        viewport={"width": 1280, "height": 800},
    )
    page = context.new_page()

    login = LoginPage(page)
    login.goto()
    login.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    login.wait_for_successful_login()

    context.storage_state(path=str(ADMIN_STATE))
    context.close()
    return ADMIN_STATE


@pytest.fixture(scope="session")
def non_admin_auth_state(browser_instance: Browser) -> Path:
    AUTH_DIR.mkdir(exist_ok=True)
    if not NON_ADMIN_EMAIL:
        pytest.skip("NON_ADMIN_EMAIL not configured")
    context = browser_instance.new_context(base_url=BASE_URL)
    page = context.new_page()
    login = LoginPage(page)
    login.goto()
    login.login(NON_ADMIN_EMAIL, NON_ADMIN_PASSWORD)
    login.wait_for_successful_login()
    context.storage_state(path=str(NON_ADMIN_STATE))
    context.close()
    return NON_ADMIN_STATE


# ---------------------------------------------------------------------------
# Per-test context + page — fresh context, reused auth cookies
# ---------------------------------------------------------------------------

@pytest.fixture()
def admin_context(browser_instance: Browser, admin_auth_state: Path) -> BrowserContext:
    context = browser_instance.new_context(
        base_url=BASE_URL,
        storage_state=str(admin_auth_state),
        viewport={"width": 1280, "height": 800},
    )
    context.set_default_timeout(20_000)
    yield context
    context.close()


@pytest.fixture()
def non_admin_context(browser_instance: Browser, non_admin_auth_state: Path) -> BrowserContext:
    context = browser_instance.new_context(
        base_url=BASE_URL,
        storage_state=str(non_admin_auth_state),
        viewport={"width": 1280, "height": 800},
    )
    context.set_default_timeout(20_000)
    yield context
    context.close()


@pytest.fixture()
def admin_page(admin_context: BrowserContext) -> Page:
    page = admin_context.new_page()
    yield page
    if not page.is_closed():
        page.close()


@pytest.fixture()
def non_admin_page(non_admin_context: BrowserContext) -> Page:
    page = non_admin_context.new_page()
    yield page
    if not page.is_closed():
        page.close()


# ---------------------------------------------------------------------------
# Page-object fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def profile_page(admin_page: Page) -> ProfilePage:
    pp = ProfilePage(admin_page)
    pp.navigate_to_profile()
    return pp


@pytest.fixture()
def profile_page_non_admin(non_admin_page: Page) -> ProfilePage:
    pp = ProfilePage(non_admin_page)
    pp.navigate_to_profile()
    return pp


# ---------------------------------------------------------------------------
# Screenshot on failure
# ---------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page: Page = item.funcargs.get("admin_page") or item.funcargs.get("non_admin_page")
        if page and not page.is_closed():
            Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
            safe = rep.nodeid.replace("/", "_").replace("::", "__")
            page.screenshot(path=f"reports/screenshots/{safe}.png", full_page=True)
