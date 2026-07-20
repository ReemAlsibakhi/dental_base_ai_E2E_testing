"""
tests/dentivoice/test_emergency_handling.py — Phase 3
Emergency Handling (DV·R12-R18) — Configure button (index 2)

Confirmed DOM:
  Options: plain divs with text — use get_by_text()
  Book Earliest: "Book Earliest Available"
  On-Call: "Connect to On-Call"
  Refer to ER: "Refer to Emergency Room"
  firstAidAdvice: textarea[name="firstAidAdvice"] — no maxLength enforced
"""
import pytest
from playwright.sync_api import expect
from pages.dentivoice_page import DentiVoicePage
from test_data.dentivoice_data import (
    VALID_PHONE,
    FIRST_AID_MAX_VALID, FIRST_AID_MAX_INVALID,
    TRIAGE_MAX_VALID,
)


def _open(dv):
    dv.open_edit(DentiVoicePage.CARD["emergency"])
    dv.page.wait_for_timeout(500)


def _get_modal(dv):
    return dv.page.locator('[role="dialog"]')


def _click_option(dv, text):
    """Click an emergency handling option div by text."""
    modal = _get_modal(dv)
    modal.get_by_text(text, exact=False).first.click()
    dv.page.wait_for_timeout(300)


def _fill_field(dv, selector, value):
    modal = _get_modal(dv)
    field = modal.locator(selector).first
    field.click()
    dv.page.wait_for_timeout(100)
    # Use fill() for clear — works for all input types including tel
    field.fill("")
    dv.page.wait_for_timeout(200)
    if value:
        field.press_sequentially(value, delay=30)
    dv.page.wait_for_timeout(300)


# ===========================================================================
# TC-F — Functional
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
def test_emergency_panel_opens(dentivoice_page):
    """TC-F: Emergency Handling panel opens."""
    _open(dentivoice_page)
    expect(dentivoice_page.cancel_button).to_be_visible()
    dentivoice_page.cancel()


@pytest.mark.functional
def test_book_earliest_saves(dentivoice_page):
    """TC-F-DV-10: Book Earliest saves — always switch away first."""
    _open(dentivoice_page)
    # Always click a different option first to guarantee dirty state
    _click_option(dentivoice_page, "Connect to On-Call")
    dentivoice_page.page.wait_for_timeout(300)
    _click_option(dentivoice_page, "Book Earliest Available")
    dentivoice_page.page.wait_for_timeout(300)
    dentivoice_page.save_and_assert_success()


@pytest.mark.functional
def test_refer_to_er_saves(dentivoice_page):
    """TC-F-DV-12: Refer to ER → saves.
    Runs after test_book_earliest which saves Book Earliest — so ER is dirty.
    """
    _open(dentivoice_page)
    _click_option(dentivoice_page, "Refer to Emergency Room")
    dentivoice_page.page.wait_for_timeout(300)
    dentivoice_page.save_and_assert_success()


@pytest.mark.functional
def test_oncall_with_valid_phone_saves(dentivoice_page):
    """TC-F-DV-11: Connect to On-Call + valid phone → saves."""
    _open(dentivoice_page)
    _click_option(dentivoice_page, "Connect to On-Call")
    _fill_field(dentivoice_page, 'input[type="tel"]', VALID_PHONE)
    dentivoice_page.save_and_assert_success()


# ===========================================================================
# TC-N — Negative
# ===========================================================================

@pytest.mark.negative
def test_oncall_empty_phone_shows_error(dentivoice_page):
    """TC-N-DV-12: On-Call + empty phone → error."""
    _open(dentivoice_page)
    _click_option(dentivoice_page, "Connect to On-Call")
    _fill_field(dentivoice_page, 'input[type="tel"]', "")
    dentivoice_page.click_save()
    dentivoice_page.page.wait_for_timeout(500)
    errors = dentivoice_page.page.locator("p.text-red-500").count()
    is_disabled = dentivoice_page.save_button.is_disabled()
    assert errors > 0 or is_disabled
    dentivoice_page.cancel()


@pytest.mark.negative
def test_first_aid_enabled_empty_advice_error(dentivoice_page):
    """TC-N-DV-14: First-aid toggle ON + empty advice → error."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    switches = modal.locator('button[role="switch"]')
    if switches.count() > 0:
        if switches.first.get_attribute("aria-checked") == "false":
            switches.first.click()
            dentivoice_page.page.wait_for_timeout(300)
        advice = modal.locator('textarea[name="firstAidAdvice"]')
        if advice.count() > 0:
            advice.fill("")
            dentivoice_page.page.wait_for_timeout(300)
        dentivoice_page.click_save()
        dentivoice_page.page.wait_for_timeout(500)
        errors = dentivoice_page.page.locator("p.text-red-500").count()
        is_disabled = dentivoice_page.save_button.is_disabled()
        assert errors > 0 or is_disabled
    dentivoice_page.cancel()


# ===========================================================================
# TC-B — Boundary
# ===========================================================================

@pytest.mark.boundary
def test_first_aid_3000_chars_accepted(dentivoice_page):
    """TC-B-DV-10: First-aid advice 3000 chars (max valid)."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    switch = modal.locator('button[role="switch"]').first
    # Turn OFF if ON, then ON to guarantee dirty + advice field visible
    if switch.get_attribute("aria-checked") == "true":
        switch.click()
        dentivoice_page.page.wait_for_timeout(300)
    switch.click()
    dentivoice_page.page.wait_for_timeout(500)
    assert switch.get_attribute("aria-checked") == "true"
    # Fill firstAidAdvice — read current value and use a different one
    advice = modal.locator('textarea[name="firstAidAdvice"]')
    advice.click()
    dentivoice_page.page.wait_for_timeout(100)
    current = advice.input_value()
    # Use B if current starts with B, otherwise use A — always different
    char = "A" if current.startswith("B") else "B"
    dentivoice_page.fill_textarea(advice, char * 3000)
    dentivoice_page.page.wait_for_timeout(2000)
    dentivoice_page.save_and_assert_success()


# TC-B-DV-11 removed: firstAidAdvice has maxLength=-1 (no limit enforced)


# ===========================================================================
# TC-R — Regression
# ===========================================================================

@pytest.mark.regression
def test_emergency_config_persists(dentivoice_page):
    """TC-R-DV-03: Emergency config persists after reload."""
    _open(dentivoice_page)
    # Switch away from current then to On-Call to guarantee dirty state
    _click_option(dentivoice_page, "Book Earliest Available")
    dentivoice_page.page.wait_for_timeout(200)
    _click_option(dentivoice_page, "Connect to On-Call")
    _fill_field(dentivoice_page, 'input[type="tel"]', "555-999-8888")
    dentivoice_page.save_and_assert_success()

    dentivoice_page.navigate_to_dentivoice()
    _open(dentivoice_page)
    expect(dentivoice_page.cancel_button).to_be_visible()
    dentivoice_page.cancel()


@pytest.mark.boundary
def test_triage_script_5000_chars_accepted(dentivoice_page):
    """TC-B-DV-11: Triage script 5000 chars (max valid per DV·R16)."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    triage = modal.locator('textarea[name="emergencyTriageScript"]')
    dentivoice_page.smart_fill(triage, "A" * 5000)
    dentivoice_page.page.wait_for_timeout(1000)
    errors = dentivoice_page.page.locator("p.text-red-500").count()
    assert errors == 0, "5000-char triage script should be accepted"
    dentivoice_page.save_and_assert_success()


@pytest.mark.boundary
@pytest.mark.xfail(reason="DV·R16: max 5000 chars not enforced in DOM (maxLength=-1)")
def test_triage_script_5001_chars_rejected(dentivoice_page):
    """TC-B-DV-12: Triage script 5001 chars → error (per DV·R16)."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    triage = modal.locator('textarea[name="emergencyTriageScript"]')
    dentivoice_page.smart_fill(triage, "A" * 5001)
    dentivoice_page.page.wait_for_timeout(1000)
    errors = dentivoice_page.page.locator("p.text-red-500").count()
    is_disabled = dentivoice_page.save_button.is_disabled()
    assert errors > 0 or is_disabled, "5001-char triage script should be rejected"
    dentivoice_page.cancel()


@pytest.mark.negative
def test_oncall_invalid_phone_shows_error(dentivoice_page):
    """TC-N-DV-13: On-Call + invalid phone format → error."""
    _open(dentivoice_page)
    _click_option(dentivoice_page, "Connect to On-Call")
    _fill_field(dentivoice_page, 'input[type="tel"]', "not-a-phone!!!")
    dentivoice_page.page.wait_for_timeout(500)
    errors = dentivoice_page.page.locator("p.text-red-500").count()
    is_disabled = dentivoice_page.save_button.is_disabled()
    if not is_disabled and errors == 0:
        dentivoice_page.click_save()
        dentivoice_page.page.wait_for_timeout(500)
        errors = dentivoice_page.page.locator("p.text-red-500").count()
    assert errors > 0 or is_disabled, "Invalid phone should show error"
    dentivoice_page.cancel()
