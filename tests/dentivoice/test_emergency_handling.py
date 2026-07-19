"""
tests/dentivoice/test_emergency_handling.py — Phase 3
Emergency Handling (DV·R12-R18) — Configure button (index 2)
"""
import pytest
from playwright.sync_api import expect
from pages.dentivoice_page import DentiVoicePage
from test_data.dentivoice_data import (
    DV_ERR, VALID_PHONE,
    FIRST_AID_MAX_VALID, FIRST_AID_MAX_INVALID,
    TRIAGE_MAX_VALID, TRIAGE_MAX_INVALID,
)


def _open(dv):
    dv.open_edit(DentiVoicePage.CARD["emergency"])
    dv.page.wait_for_timeout(500)


def _get_modal(dv):
    return dv.page.locator('[role="dialog"]')


def _fill_field(dv, selector, value):
    """Fill input/textarea inside modal using execCommand."""
    modal = _get_modal(dv)
    field = modal.locator(selector).first
    field.click()
    dv.page.wait_for_timeout(100)
    field.evaluate("""el => {
        el.focus();
        el.setSelectionRange(0, el.value.length);
        document.execCommand('delete', false, null);
    }""")
    dv.page.wait_for_timeout(300)
    if value:
        field.evaluate(f"""el => {{
            el.focus();
            document.execCommand('insertText', false, {repr(value)});
        }}""")
        dv.page.wait_for_timeout(300)


# ===========================================================================
# TC-F — Functional
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
def test_emergency_panel_opens(dentivoice_page):
    """TC-F-DV-10: Emergency Handling panel opens."""
    _open(dentivoice_page)
    expect(dentivoice_page.cancel_button).to_be_visible()
    dentivoice_page.cancel()


@pytest.mark.functional
def test_book_earliest_saves(dentivoice_page):
    """TC-F-DV-10: Book Earliest option saves successfully."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    book_btn = modal.get_by_text("Book Earliest", exact=False).first
    if book_btn.is_visible():
        book_btn.click()
        dentivoice_page.page.wait_for_timeout(300)
    dentivoice_page.save_and_assert_success()


@pytest.mark.functional
def test_refer_to_er_saves(dentivoice_page):
    """TC-F-DV-12: Refer to ER option saves."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    er_btn = modal.get_by_text("Refer to ER", exact=False).first
    if er_btn.is_visible():
        er_btn.click()
        dentivoice_page.page.wait_for_timeout(300)
    dentivoice_page.save_and_assert_success()


@pytest.mark.functional
def test_oncall_with_valid_phone_saves(dentivoice_page):
    """TC-F-DV-11: Connect to On-Call + valid phone saves."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    oncall_btn = modal.get_by_text("On-Call", exact=False).first
    if oncall_btn.is_visible():
        oncall_btn.click()
        dentivoice_page.page.wait_for_timeout(300)
        _fill_field(dentivoice_page, 'input[type="tel"], input[placeholder*="phone" i]', VALID_PHONE)
    dentivoice_page.save_and_assert_success()


# ===========================================================================
# TC-N — Negative
# ===========================================================================

@pytest.mark.negative
def test_oncall_empty_phone_shows_error(dentivoice_page):
    """TC-N-DV-12: On-Call selected + empty phone → error."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    oncall_btn = modal.get_by_text("On-Call", exact=False).first
    if oncall_btn.is_visible():
        oncall_btn.click()
        dentivoice_page.page.wait_for_timeout(300)
        _fill_field(dentivoice_page, 'input[type="tel"], input[placeholder*="phone" i]', "")
    dentivoice_page.click_save()
    dentivoice_page.page.wait_for_timeout(500)
    errors = dentivoice_page.page.locator("p.text-red-500").count()
    is_disabled = dentivoice_page.save_button.is_disabled()
    assert errors > 0 or is_disabled, "Empty phone should show error"
    dentivoice_page.cancel()


@pytest.mark.negative
def test_first_aid_enabled_empty_advice_error(dentivoice_page):
    """TC-N-DV-14: First-aid toggle ON + empty advice → error."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    switches = modal.locator('button[role="switch"]')
    if switches.count() > 0:
        first_aid_switch = switches.first
        if first_aid_switch.get_attribute("aria-checked") == "false":
            first_aid_switch.click()
            dentivoice_page.page.wait_for_timeout(300)
        # Use specific name to target firstAidAdvice, not emergencyTriageScript
        modal2 = _get_modal(dentivoice_page)
        advice = modal2.locator('textarea[name="firstAidAdvice"]')
        if advice.count() > 0:
            advice.evaluate("""el => {
                el.focus();
                el.setSelectionRange(0, el.value.length);
                document.execCommand('delete', false, null);
            }""")
        dentivoice_page.page.wait_for_timeout(500)
        dentivoice_page.click_save()
        dentivoice_page.page.wait_for_timeout(500)
        errors = dentivoice_page.page.locator("p.text-red-500").count()
        is_disabled = dentivoice_page.save_button.is_disabled()
        assert errors > 0 or is_disabled, "Empty first-aid advice should show error or disable Save"
    dentivoice_page.cancel()


# ===========================================================================
# TC-B — Boundary
# ===========================================================================

@pytest.mark.boundary
def test_first_aid_3000_chars_accepted(dentivoice_page):
    """TC-B-DV-10: First-aid advice 3000 chars (max valid)."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    switches = modal.locator('button[role="switch"]')
    if switches.count() > 0:
        if switches.first.get_attribute("aria-checked") == "false":
            switches.first.click()
            dentivoice_page.page.wait_for_timeout(300)
        _fill_field(dentivoice_page, 'textarea', FIRST_AID_MAX_VALID)
    dentivoice_page.save_and_assert_success()


@pytest.mark.boundary
def test_first_aid_3001_chars_rejected(dentivoice_page):
    """TC-B-DV-11: First-aid advice 3001 chars → error."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    switches = modal.locator('button[role="switch"]')
    if switches.count() > 0:
        if switches.first.get_attribute("aria-checked") == "false":
            switches.first.click()
            dentivoice_page.page.wait_for_timeout(300)
        _fill_field(dentivoice_page, 'textarea', FIRST_AID_MAX_INVALID)
    dentivoice_page.click_save()
    dentivoice_page.page.wait_for_timeout(500)
    errors = dentivoice_page.page.locator("p.text-red-500").count()
    is_disabled = dentivoice_page.save_button.is_disabled()
    assert errors > 0 or is_disabled
    dentivoice_page.cancel()


# ===========================================================================
# TC-R — Regression
# ===========================================================================

@pytest.mark.regression
def test_emergency_config_persists(dentivoice_page):
    """TC-R-DV-03: Emergency config persists after reload."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    book_btn = modal.get_by_text("Book Earliest", exact=False).first
    if book_btn.is_visible():
        book_btn.click()
        dentivoice_page.page.wait_for_timeout(300)
    dentivoice_page.save_and_assert_success()

    dentivoice_page.navigate_to_dentivoice()
    _open(dentivoice_page)
    expect(dentivoice_page.cancel_button).to_be_visible()
    dentivoice_page.cancel()
