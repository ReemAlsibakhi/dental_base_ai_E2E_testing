"""
tests/dentivoice/test_daily_email.py — Phase 3
Daily Email Report (DV·R9) — Terminology panel, toggle nth(0)
"""
import pytest
from playwright.sync_api import expect
from pages.dentivoice_page import DentiVoicePage
from test_data.dentivoice_data import DV_ERR, VALID_EMAIL


def _open(dv):
    dv.open_edit(DentiVoicePage.CARD["terminology"])
    dv.page.wait_for_timeout(500)


def _get_modal(dv):
    return dv.page.locator('[role="dialog"]')


def _fill_email(dv, value):
    """Fill email input — use fill() which works for type=email."""
    modal = _get_modal(dv)
    field = modal.locator('input[type="email"], input[placeholder*="email" i]').first
    field.click()
    dv.page.wait_for_timeout(100)
    # fill() clears and sets value, works for input[type=email]
    field.fill(value if value else "temp@temp.com")
    dv.page.wait_for_timeout(200)
    if not value:
        # For empty: clear after fill
        field.fill("")
    dv.page.wait_for_timeout(300)


# ===========================================================================
# TC-F — Functional
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
def test_terminology_panel_opens(dentivoice_page):
    """TC-SM: Terminology panel opens."""
    _open(dentivoice_page)
    expect(dentivoice_page.cancel_button).to_be_visible()
    dentivoice_page.cancel()


@pytest.mark.functional
def test_daily_email_toggle_on_with_valid_email(dentivoice_page):
    """TC-F-DV-17: Toggle Daily Email ON + valid email → saves."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    toggle = modal.locator('button[role="switch"]').nth(0)
    if toggle.get_attribute("aria-checked") == "false":
        toggle.click()
        dentivoice_page.page.wait_for_timeout(500)
    email_field = modal.locator('input[type="email"], input[placeholder*="email" i]')
    if email_field.count() > 0:
        _fill_email(dentivoice_page, VALID_EMAIL)
    dentivoice_page.save_and_assert_success()


@pytest.mark.functional
def test_daily_email_toggle_off_saves(dentivoice_page):
    """TC-F-DV-18: Toggle Daily Email OFF → saves."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    toggle = modal.locator('button[role="switch"]').nth(0)
    # Ensure OFF — if already OFF, turn ON first to create dirty state
    if toggle.get_attribute("aria-checked") == "false":
        toggle.click()
        dentivoice_page.page.wait_for_timeout(500)
    toggle.click()
    dentivoice_page.page.wait_for_timeout(500)
    assert toggle.get_attribute("aria-checked") == "false"
    dentivoice_page.save_and_assert_success()


# ===========================================================================
# TC-N — Negative
# ===========================================================================

@pytest.mark.negative
def test_daily_email_on_empty_email_shows_error(dentivoice_page):
    """TC-N-DV-23: Daily Email ON + empty email → error."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    toggle = modal.locator('button[role="switch"]').nth(0)
    if toggle.get_attribute("aria-checked") == "false":
        toggle.click()
        dentivoice_page.page.wait_for_timeout(500)
    email_field = modal.locator('input[type="email"], input[placeholder*="email" i]')
    if email_field.count() > 0:
        _fill_email(dentivoice_page, "")
        dentivoice_page.click_save()
        dentivoice_page.page.wait_for_timeout(500)
        errors = dentivoice_page.page.locator("p.text-red-500").count()
        is_disabled = dentivoice_page.save_button.is_disabled()
        assert errors > 0 or is_disabled, "Empty email should show error"
    dentivoice_page.cancel()


@pytest.mark.negative
def test_daily_email_on_invalid_email_shows_error(dentivoice_page):
    """TC-N-DV-24: Daily Email ON + invalid email → error."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    toggle = modal.locator('button[role="switch"]').nth(0)
    if toggle.get_attribute("aria-checked") == "false":
        toggle.click()
        dentivoice_page.page.wait_for_timeout(500)
    email_field = modal.locator('input[type="email"], input[placeholder*="email" i]')
    if email_field.count() > 0:
        _fill_email(dentivoice_page, "not-an-email")
        dentivoice_page.click_save()
        dentivoice_page.page.wait_for_timeout(500)
        errors = dentivoice_page.page.locator("p.text-red-500").count()
        assert errors > 0, "Invalid email should show error"
    dentivoice_page.cancel()
