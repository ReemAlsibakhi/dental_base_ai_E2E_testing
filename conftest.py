"""
conftest.py — Global pytest fixtures for the DentalBase Profile E2E suite.

Auth strategy:
  - One-time login is performed via the `admin_auth_state` session-scoped fixture.
  - Every test gets a fresh browser context seeded with that saved storage state,
    so no test ever hits the login page again (fast & isolated).
  - Non-admin tests use a separate auth state fixture.
"""

import os
import pytest
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from pages.login_page import LoginPage
from pages.profile_page import ProfilePage

load_dotenv()

BASE_URL: str = os.getenv("BASE_URL", "https://dentalbase-staging-v2.vercel.app")
ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "")
ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "")
NON_ADMIN_EMAIL: str = os.getenv("NON_ADMIN_EMAIL", "")
NON_ADMIN_PASSWORD: str = os.getenv("NON_ADMIN_PASSWORD", "")

AUTH_DIR = Path(".playwright_auth")
ADMIN_STATE = AUTH_DIR / "admin.json"
NON_ADMIN_STATE = AUTH_DIR / "non_admin.json"


# ---------------------------------------------------------------------------
# Browser — session-scoped so one browser process per test run
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=os.getenv("HEADLESS", "true").lower() == "true",
            slow_mo=int(os.getenv("SLOW_MO", "0")),
        )
        yield browser
        browser.close()


# ---------------------------------------------------------------------------
# Auth state — perform login once per session, persist storage state to disk
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def admin_auth_state(browser_instance: Browser) -> Path:
    AUTH_DIR.mkdir(exist_ok=True)
    context = browser_instance.new_context(base_url=BASE_URL)
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    login_page.wait_for_successful_login()
    context.storage_state(path=str(ADMIN_STATE))
    context.close()
    return ADMIN_STATE


@pytest.fixture(scope="session")
def non_admin_auth_state(browser_instance: Browser) -> Path:
    AUTH_DIR.mkdir(exist_ok=True)
    context = browser_instance.new_context(base_url=BASE_URL)
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(NON_ADMIN_EMAIL, NON_ADMIN_PASSWORD)
    login_page.wait_for_successful_login()
    context.storage_state(path=str(NON_ADMIN_STATE))
    context.close()
    return NON_ADMIN_STATE


# ---------------------------------------------------------------------------
# Per-test context + page — each test gets full isolation
# ---------------------------------------------------------------------------

@pytest.fixture()
def admin_context(browser_instance: Browser, admin_auth_state: Path) -> BrowserContext:
    context = browser_instance.new_context(
        base_url=BASE_URL,
        storage_state=str(admin_auth_state),
        viewport={"width": 1280, "height": 800},
        record_video_dir="reports/videos" if os.getenv("CI") else None,
    )
    context.set_default_timeout(15_000)
    yield context
    context.close()


@pytest.fixture()
def non_admin_context(browser_instance: Browser, non_admin_auth_state: Path) -> BrowserContext:
    context = browser_instance.new_context(
        base_url=BASE_URL,
        storage_state=str(non_admin_auth_state),
        viewport={"width": 1280, "height": 800},
    )
    context.set_default_timeout(15_000)
    yield context
    context.close()


@pytest.fixture()
def admin_page(admin_context: BrowserContext) -> Page:
    page = admin_context.new_page()
    page.on("console", lambda msg: None)  # silence console noise
    yield page
    # Capture screenshot on failure (pytest-playwright handles this natively,
    # but we add an explicit fallback here)
    if hasattr(page, "_impl_obj") and not page.is_closed():
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
# Screenshot on failure hook
# ---------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page: Page = item.funcargs.get("admin_page") or item.funcargs.get("non_admin_page")
        if page and not page.is_closed():
            Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
            safe_name = rep.nodeid.replace("/", "_").replace("::", "__")
            page.screenshot(path=f"reports/screenshots/{safe_name}.png", full_page=True)
