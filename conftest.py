"""
conftest.py — Global test infrastructure.

Responsibilities:
  - Browser lifecycle (session-scoped)
  - Auth state management (admin + non-admin)
  - Shared browser contexts and raw pages
  - Screenshot on failure
  - Automated bug report generation

Module-specific fixtures live in their own conftest.py:
  tests/profile/conftest.py
  tests/practice_profile/conftest.py
  tests/scheduling_rules/conftest.py
  tests/patient_outreach/conftest.py
  tests/dentivoice/conftest.py
"""

import os
import json
import time
import pytest
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from pages.login_page import LoginPage

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

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

VIEWPORT = {"width": 1280, "height": 800}

# Collect failures for bug report
_failures: list[dict] = []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_valid_state_file(path: Path) -> bool:
    """Check if auth state file exists and contains cookies."""
    try:
        if not path.exists():
            return False
        data = json.loads(path.read_text())
        return bool(data.get("cookies"))
    except Exception:
        return False


def _is_session_still_valid(browser: Browser, state_path: Path) -> bool:
    """Verify saved session is still active against the live site."""
    try:
        context = browser.new_context(
            base_url=BASE_URL,
            storage_state=str(state_path),
            viewport=VIEWPORT,
        )
        page = context.new_page()
        page.goto("/settings", wait_until="commit", timeout=30_000)

        deadline = time.time() + 30
        while time.time() < deadline:
            if "/settings" in page.url:
                context.close()
                return True
            time.sleep(0.5)

        context.close()
        return False
    except Exception:
        return False


def _new_context(browser: Browser, **kwargs) -> BrowserContext:
    """Create a browser context with standard defaults."""
    return browser.new_context(
        base_url=BASE_URL,
        viewport=VIEWPORT,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# Browser (session-scoped)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def browser_instance() -> Browser:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        yield browser
        browser.close()


# ---------------------------------------------------------------------------
# Auth state (session-scoped)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def admin_auth_state(browser_instance: Browser) -> Path:
    """Return valid admin auth state — reuse saved session or do fresh login."""
    AUTH_DIR.mkdir(exist_ok=True)

    if _is_valid_state_file(ADMIN_STATE) and \
       _is_session_still_valid(browser_instance, ADMIN_STATE):
        return ADMIN_STATE

    context = _new_context(browser_instance)
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
    """Return valid non-admin auth state."""
    AUTH_DIR.mkdir(exist_ok=True)
    if not NON_ADMIN_EMAIL:
        pytest.skip("NON_ADMIN_EMAIL not configured")
    if _is_valid_state_file(NON_ADMIN_STATE):
        return NON_ADMIN_STATE

    context = _new_context(browser_instance)
    page = context.new_page()
    login = LoginPage(page)
    login.goto()
    login.login(NON_ADMIN_EMAIL, NON_ADMIN_PASSWORD)
    login.wait_for_successful_login()
    context.storage_state(path=str(NON_ADMIN_STATE))
    context.close()
    return NON_ADMIN_STATE


# ---------------------------------------------------------------------------
# Browser contexts (session-scoped)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def admin_context(browser_instance: Browser, admin_auth_state: Path) -> BrowserContext:
    context = _new_context(browser_instance, storage_state=str(admin_auth_state))
    context.set_default_timeout(20_000)
    yield context
    context.close()


@pytest.fixture(scope="session")
def non_admin_context(browser_instance: Browser, non_admin_auth_state: Path) -> BrowserContext:
    context = _new_context(browser_instance, storage_state=str(non_admin_auth_state))
    context.set_default_timeout(20_000)
    yield context
    context.close()


# ---------------------------------------------------------------------------
# Raw pages (function-scoped) — for tests that need a bare Page
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
# Screenshot on failure + failure collection
# ---------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when != "call" or not rep.failed:
        return

    # Find the page from any POM or raw Page fixture
    page: Page | None = None
    for name in ("admin_page", "non_admin_page", "profile_page",
                  "practice_profile_page", "scheduling_rules_page",
                  "patient_outreach_page", "dentivoice_page"):
        val = item.funcargs.get(name)
        if val is not None:
            page = getattr(val, "page", val)
            break

    screenshot_path: str | None = None
    if page and not page.is_closed():
        Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
        safe_name = rep.nodeid.replace("/", "_").replace("::", "__")
        screenshot_path = f"reports/screenshots/{safe_name}.png"
        page.screenshot(path=screenshot_path, full_page=True)

    _failures.append({
        "test_id":    rep.nodeid,
        "module":     item.module.__name__ if hasattr(item, "module") else "",
        "error":      str(rep.longrepr).split("\n")[-1] if rep.longrepr else "",
        "full_error": str(rep.longrepr) if rep.longrepr else "",
        "screenshot": screenshot_path,
        "duration":   round(rep.duration, 2) if hasattr(rep, "duration") else 0,
    })


# ---------------------------------------------------------------------------
# Bug report (session end)
# ---------------------------------------------------------------------------

def pytest_sessionfinish(session, exitstatus):
    """Generate structured Markdown bug report if there are failures."""
    if not _failures:
        return

    Path("reports").mkdir(exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report_path = Path("reports/bug_report.md")

    by_module: dict[str, list] = {}
    for f in _failures:
        mod = f["module"].split(".")[-1].replace("_", " ").title()
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
        name = f["test_id"].split("::")[-1]
        err  = f["error"][:80] + "..." if len(f["error"]) > 80 else f["error"]
        lines.append(f"| {i} | `{name}` | {err} |")

    lines += ["", "---", "", "## Failures by Module", ""]

    for mod, failures in by_module.items():
        lines += [f"### {mod}", ""]
        for f in failures:
            name = f["test_id"].split("::")[-1]
            lines += [
                f"#### ❌ `{name}`",
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
        "3. Re-run after fixes: `pytest --headed -v`",
        "",
        f"*Auto-generated by Playwright E2E suite — {now}*",
    ]

    report_path.write_text("\n".join(lines))
    print(f"\n📋 Bug report generated: {report_path}")
    print(f"   {len(_failures)} failures documented")

# ---------------------------------------------------------------------------
# Profile fixtures
# ---------------------------------------------------------------------------

from pages.profile_page import ProfilePage


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
# Practice Profile fixtures
# ---------------------------------------------------------------------------

from pages.practice_profile_page import PracticeProfilePage


@pytest.fixture()
def practice_profile_page(admin_context: BrowserContext) -> PracticeProfilePage:
    page = admin_context.new_page()
    pp = PracticeProfilePage(page)
    pp.navigate_to_practice_profile()
    pp.open_edit_form()
    yield pp
    try:
        if not page.is_closed():
            pp.cancel()
    except Exception:
        pass
    if not page.is_closed():
        page.close()


@pytest.fixture(scope="module")
def practice_profile_form_open(admin_context: BrowserContext) -> PracticeProfilePage:
    page = admin_context.new_page()
    pp = PracticeProfilePage(page)
    pp.navigate_to_practice_profile()
    pp.open_edit_form()
    yield pp
    try:
        if not page.is_closed():
            pp.cancel()
    except Exception:
        pass
    if not page.is_closed():
        page.close()


# ---------------------------------------------------------------------------
# Scheduling Rules fixtures
# ---------------------------------------------------------------------------

from pages.scheduling_rules_page import SchedulingRulesPage


@pytest.fixture()
def scheduling_rules_page(admin_context: BrowserContext) -> SchedulingRulesPage:
    page = admin_context.new_page()
    sr = SchedulingRulesPage(page)
    sr.navigate_to_scheduling_rules()
    yield sr
    try:
        if not page.is_closed():
            sr.cancel()
    except Exception:
        pass
    if not page.is_closed():
        page.close()


# ---------------------------------------------------------------------------
# Patient Outreach fixtures
# ---------------------------------------------------------------------------

from pages.patient_outreach_page import PatientOutreachPage


@pytest.fixture()
def patient_outreach_page(admin_context: BrowserContext) -> PatientOutreachPage:
    page = admin_context.new_page()
    po = PatientOutreachPage(page)
    po.navigate_to_patient_outreach()
    yield po
    try:
        if not page.is_closed():
            po.cancel()
    except Exception:
        pass
    if not page.is_closed():
        page.close()


# ---------------------------------------------------------------------------
# DentiVoice fixtures
# ---------------------------------------------------------------------------

from pages.dentivoice_page import DentiVoicePage


@pytest.fixture()
def dentivoice_page(admin_context: BrowserContext) -> DentiVoicePage:
    page = admin_context.new_page()
    dv = DentiVoicePage(page)
    dv.navigate_to_dentivoice()
    yield dv
    try:
        if not page.is_closed():
            dv.cancel()
    except Exception:
        pass
    if not page.is_closed():
        page.close()


# ---------------------------------------------------------------------------
# Insurance & Billing fixtures
# ---------------------------------------------------------------------------

from pages.insurance_billing_page import InsuranceBillingPage


@pytest.fixture()
def insurance_billing_page(admin_context: BrowserContext) -> InsuranceBillingPage:
    page = admin_context.new_page()
    ib = InsuranceBillingPage(page)
    ib.navigate()
    yield ib
    try:
        if not page.is_closed():
            ib.cancel()
    except Exception:
        pass
    if not page.is_closed():
        page.close()
