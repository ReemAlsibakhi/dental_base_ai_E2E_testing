"""
tests/dentivoice/test_greetings.py — Phase 2
Greeting Messages (DV·R5, R6) — inside AI Identity panel
"""
import pytest
from playwright.sync_api import expect
from pages.dentivoice_page import DentiVoicePage
from test_data.dentivoice_data import (
    GREETING_MAX_VALID, GREETING_MAX_INVALID,
)


def _open(dv):
    dv.open_edit(DentiVoicePage.CARD["ai_identity"])


def _fill_greeting(dv, locator, value):
    """Fill greeting textarea using execCommand."""
    locator.click()
    dv.page.wait_for_timeout(100)
    locator.evaluate("""el => {
        el.focus();
        el.setSelectionRange(0, el.value.length);
        document.execCommand('delete', false, null);
    }""")
    dv.page.wait_for_timeout(300)
    if value:
        locator.evaluate(f"""el => {{
            el.focus();
            document.execCommand('insertText', false, {repr(value)});
        }}""")
        dv.page.wait_for_timeout(300)


@pytest.mark.functional
def test_initial_greeting_valid_saves(dentivoice_page):
    """TC-F-DV-06: Valid initial greeting saves."""
    _open(dentivoice_page)
    _fill_greeting(dentivoice_page, dentivoice_page.first_message,
                   "Hello! How can I help you today?")
    dentivoice_page.save_and_assert_success()


@pytest.mark.functional
def test_initial_greeting_empty_accepted(dentivoice_page):
    """TC-F-DV-07: Empty initial greeting accepted (optional)."""
    _open(dentivoice_page)
    _fill_greeting(dentivoice_page, dentivoice_page.first_message, "")
    dentivoice_page.fill_ai_name("Sofia")
    dentivoice_page.save_and_assert_success()


@pytest.mark.functional
def test_after_hours_greeting_valid_saves(dentivoice_page):
    """TC-F-DV-08: Valid after-hours greeting saves."""
    _open(dentivoice_page)
    _fill_greeting(dentivoice_page, dentivoice_page.after_hours,
                   "Our office is closed. Please call back during business hours.")
    dentivoice_page.save_and_assert_success()


@pytest.mark.functional
def test_after_hours_greeting_empty_accepted(dentivoice_page):
    """TC-F-DV-09: Empty after-hours greeting accepted (optional)."""
    _open(dentivoice_page)
    _fill_greeting(dentivoice_page, dentivoice_page.after_hours, "")
    dentivoice_page.fill_ai_name("Sofia")
    dentivoice_page.save_and_assert_success()


@pytest.mark.negative
def test_initial_greeting_501_chars_rejected(dentivoice_page):
    """TC-N-DV-09: Initial greeting 501 chars → error."""
    _open(dentivoice_page)
    _fill_greeting(dentivoice_page, dentivoice_page.first_message, GREETING_MAX_INVALID)
    dentivoice_page.page.wait_for_timeout(500)
    error_count = dentivoice_page.page.locator("p.text-red-500").count()
    is_disabled = dentivoice_page.save_button.is_disabled()
    if not is_disabled and error_count == 0:
        dentivoice_page.click_save()
        dentivoice_page.page.wait_for_timeout(500)
        error_count = dentivoice_page.page.locator("p.text-red-500").count()
    assert is_disabled or error_count > 0, "501-char greeting should be rejected"
    dentivoice_page.cancel()


@pytest.mark.negative
def test_after_hours_501_chars_rejected(dentivoice_page):
    """TC-N-DV-10: After-hours greeting 501 chars → error."""
    _open(dentivoice_page)
    _fill_greeting(dentivoice_page, dentivoice_page.after_hours, GREETING_MAX_INVALID)
    dentivoice_page.page.wait_for_timeout(500)
    error_count = dentivoice_page.page.locator("p.text-red-500").count()
    is_disabled = dentivoice_page.save_button.is_disabled()
    if not is_disabled and error_count == 0:
        dentivoice_page.click_save()
        dentivoice_page.page.wait_for_timeout(500)
        error_count = dentivoice_page.page.locator("p.text-red-500").count()
    assert is_disabled or error_count > 0, "501-char after-hours should be rejected"
    dentivoice_page.cancel()


@pytest.mark.boundary
def test_initial_greeting_500_chars_accepted(dentivoice_page):
    """TC-B-DV-05: Initial greeting 500 chars (max valid)."""
    _open(dentivoice_page)
    _fill_greeting(dentivoice_page, dentivoice_page.first_message, GREETING_MAX_VALID)
    dentivoice_page.save_and_assert_success()


@pytest.mark.boundary
def test_after_hours_500_chars_accepted(dentivoice_page):
    """TC-B-DV-06: After-hours greeting 500 chars (max valid)."""
    _open(dentivoice_page)
    _fill_greeting(dentivoice_page, dentivoice_page.after_hours, GREETING_MAX_VALID)
    dentivoice_page.save_and_assert_success()


@pytest.mark.regression
def test_greetings_persist_after_reload(dentivoice_page):
    """TC-R: Greeting persists after reload."""
    _open(dentivoice_page)
    # Read current value and use a different one to guarantee dirty state
    current = dentivoice_page.first_message.input_value()
    msg = "Persist greeting A" if "Persist greeting B" not in current else "Persist greeting B"
    _fill_greeting(dentivoice_page, dentivoice_page.first_message, msg)
    dentivoice_page.save_and_assert_success()

    dentivoice_page.navigate_to_dentivoice()
    _open(dentivoice_page)
    value = dentivoice_page.first_message.input_value()
    assert msg in value
    dentivoice_page.cancel()
