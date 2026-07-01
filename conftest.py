"""
conftest.py — Global pytest fixtures + automatic bug report generation.

After each test run, if there are failures, a structured bug report
is generated in reports/bug_report.md automatically.
"""

import os
import json
import pytest
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from pages.login_page import LoginPage
from pages.profile_page import ProfilePage

load_dotenv()

BASE_URL           = os.getenv("BASE_URL", "https://dentalbase-dev-v2.vercel.app")
ADMIN_EMAIL        = os.getenv("ADMIN_EMAIL", "")
ADMIN_PASSWORD     = os.getenv("ADMIN_PASSWORD", "")
NON_ADMIN_EMAIL    = os.getenv("NON_ADMIN_EMAIL", "")
NON_ADMIN_PASSWORD = os.getenv("NON_ADMIN_PASSWORD", "")
HEADLESS           = os.getenv("HEADLESS", "true").lower() == "true"
SLOW_MO            = int(os.getenv("SLOW_MO", "0"))

AUTH_DIR        = Path(".playwright_auth")
ADMIN_STATE     = AUTH_DIR / "admin.json"
NON_ADMIN_STATE = AUTH_DIR / "non_admin.json"

# Collect failures for bug report
_failures = []


def _is_valid_state_file(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        data = json.loads(path.read_text())
        return bool(data.get("cookies"))
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Browser
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        yield browser
        browser.close()


# ---------------------------------------------------------------------------
# Auth state
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def admin_auth_state(browser_instance: Browser) -> Path:
    AUTH_DIR.mkdir(exist_ok=True)
    if _is_valid_state_file(ADMIN_STATE):
        return ADMIN_STATE
    context = browser_instance.new_context(
        base_url=BASE_URL, viewport={"width": 1280, "height": 800}
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
    if _is_valid_state_file(NON_ADMIN_STATE):
        return NON_ADMIN_STATE
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
# Context — session scoped (one context for all tests)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def admin_context(browser_instance: Browser, admin_auth_state: Path) -> BrowserContext:
    context = browser_instance.new_context(
        base_url=BASE_URL,
        storage_state=str(admin_auth_state),
        viewport={"width": 1920, "height": 1080},
    )
    context.set_default_timeout(20_000)
    yield context
    context.close()


@pytest.fixture(scope="session")
def non_admin_context(browser_instance: Browser, non_admin_auth_state: Path) -> BrowserContext:
    context = browser_instance.new_context(
        base_url=BASE_URL,
        storage_state=str(non_admin_auth_state),
        viewport={"width": 1280, "height": 800},
    )
    context.set_default_timeout(20_000)
    yield context
    context.close()


# ---------------------------------------------------------------------------
# Page — function scoped (new tab per test)
# ---------------------------------------------------------------------------

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
# Page object fixtures
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


@pytest.fixture(scope="module")
def profile_page_modal_open(admin_context: BrowserContext) -> ProfilePage:
    """Edit Profile modal open for entire module."""
    page = admin_context.new_page()
    pp = ProfilePage(page)
    pp.navigate_to_profile()
    pp.open_edit_modal()
    yield pp
    try:
        if pp.edit_modal.is_visible():
            pp.close_panel_button.click()
    except Exception:
        pass
    if not page.is_closed():
        page.close()


@pytest.fixture(scope="module")
def add_user_panel_open(admin_context: BrowserContext) -> ProfilePage:
    """Add User panel open for entire module."""
    page = admin_context.new_page()
    pp = ProfilePage(page)
    pp.navigate_to_profile()
    pp.open_add_user_form()
    yield pp
    try:
        if pp.add_user_modal.is_visible():
            pp.add_user_cancel_button.click()
    except Exception:
        pass
    if not page.is_closed():
        page.close()


# ---------------------------------------------------------------------------
# Screenshot on failure + collect failures for bug report
# ---------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # Screenshot
        page: Page = item.funcargs.get("admin_page") or item.funcargs.get("non_admin_page")
        screenshot_path = None
        if page and not page.is_closed():
            Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
            safe = rep.nodeid.replace("/", "_").replace("::", "__")
            screenshot_path = f"reports/screenshots/{safe}.png"
            page.screenshot(path=screenshot_path, full_page=True)

        # Collect failure for bug report
        _failures.append({
            "test_id":     rep.nodeid,
            "module":      item.module.__name__ if hasattr(item, "module") else "",
            "error":       str(rep.longrepr).split("\n")[-1] if rep.longrepr else "",
            "full_error":  str(rep.longrepr) if rep.longrepr else "",
            "screenshot":  screenshot_path,
            "duration":    round(rep.duration, 2) if hasattr(rep, "duration") else 0,
        })


# ---------------------------------------------------------------------------
# Auto-generate bug report after session ends
# ---------------------------------------------------------------------------

def pytest_sessionfinish(session, exitstatus):
    """Generate structured bug report if there are failures."""
    if not _failures:
        return

    Path("reports").mkdir(exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report_path = Path("reports/bug_report.md")

    # Group failures by module
    by_module = {}
    for f in _failures:
        mod = f["module"].replace("tests.profile.", "").replace("_", " ").title()
        by_module.setdefault(mod, []).append(f)

    lines = [
        "# Automated Bug Report",
        f"**Generated:** {now}",
        f"**Environment:** {BASE_URL}",
        f"**Total Failures:** {len(_failures)}",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| # | Test | Error |",
        "|---|------|-------|",
    ]

    for i, f in enumerate(_failures, 1):
        test_name = f["test_id"].split("::")[-1]
        error_short = f["error"][:80] + "..." if len(f["error"]) > 80 else f["error"]
        lines.append(f"| {i} | `{test_name}` | {error_short} |")

    lines += ["", "---", "", "## Failures by Module", ""]

    for mod, failures in by_module.items():
        lines += [f"### {mod}", ""]
        for f in failures:
            test_name = f["test_id"].split("::")[-1]
            lines += [
                f"#### ❌ `{test_name}`",
                "",
                f"**Test ID:** `{f['test_id']}`",
                f"**Duration:** {f['duration']}s",
                "",
                "**Error:**",
                "```",
                f["error"],
                "```",
            ]
            if f["screenshot"]:
                lines.append(f"**Screenshot:** `{f['screenshot']}`")
            lines.append("")

    lines += [
        "---",
        "",
        "## Next Steps",
        "",
        "1. Share this report with the dev team",
        "2. Create tickets for each failure",
        "3. Re-run tests after fixes: `pytest --headed -v`",
        "",
        f"*Report auto-generated by Playwright E2E suite — {now}*",
    ]

    report_path.write_text("\n".join(lines))
    print(f"\n📋 Bug report generated: {report_path}")
    print(f"   {len(_failures)} failures documented")


# ---------------------------------------------------------------------------
# Practice Profile fixtures
# ---------------------------------------------------------------------------

from pages.practice_profile_page import PracticeProfilePage


@pytest.fixture()
def practice_profile_page(admin_page: Page) -> PracticeProfilePage:
    """Navigate to Practice Profile tab and open Edit form."""
    pp = PracticeProfilePage(admin_page)
    pp.navigate_to_practice_profile()
    pp.open_edit_form()
    return pp


@pytest.fixture(scope="module")
def practice_profile_form_open(admin_context: BrowserContext) -> PracticeProfilePage:
    """Practice Profile edit form open for entire module — no re-navigation per test."""
    page = admin_context.new_page()
    pp = PracticeProfilePage(page)
    pp.navigate_to_practice_profile()
    pp.open_edit_form()
    yield pp
    try:
        pp.cancel()
    except Exception:
        pass
    if not page.is_closed():
        page.close()
