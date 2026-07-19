"""
tests/dentivoice/test_call_transfer.py — Phase 3
Call Transfer (DV·R19-R22) — Edit index 3
"""
import pytest
from playwright.sync_api import expect
from pages.dentivoice_page import DentiVoicePage
from test_data.dentivoice_data import DV_ERR, VALID_PHONE


def _open(dv):
    dv.open_edit(DentiVoicePage.CARD["call_transfer"])
    dv.page.wait_for_timeout(500)


def _get_modal(dv):
    return dv.page.locator('[role="dialog"]')


def _fill_field(dv, selector, value):
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
def test_call_transfer_panel_opens(dentivoice_page):
    """TC-F-DV-15: Call Transfer panel opens."""
    _open(dentivoice_page)
    expect(dentivoice_page.cancel_button).to_be_visible()
    dentivoice_page.cancel()


@pytest.mark.functional
def test_transfer_toggle_on_saves(dentivoice_page):
    """TC-F-DV-15: Enable transfer toggle → saves."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    toggle = modal.locator('button[role="switch"]').first
    if toggle.get_attribute("aria-checked") == "false":
        toggle.click()
        dentivoice_page.page.wait_for_timeout(500)
    dentivoice_page.save_and_assert_success()


@pytest.mark.functional
def test_transfer_toggle_off_saves(dentivoice_page):
    """TC-F-DV-16: Disable transfer → saves."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    toggle = modal.locator('button[role="switch"]').first
    if toggle.get_attribute("aria-checked") == "true":
        toggle.click()
        dentivoice_page.page.wait_for_timeout(500)
    dentivoice_page.save_and_assert_success()


# ===========================================================================
# TC-N — Negative
# ===========================================================================

@pytest.mark.negative
def test_rule_name_empty_shows_error(dentivoice_page):
    """TC-N-DV-18: Rule name empty → error."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    toggle = modal.locator('button[role="switch"]').first
    if toggle.get_attribute("aria-checked") == "false":
        toggle.click()
        dentivoice_page.page.wait_for_timeout(500)
    _fill_field(dentivoice_page, 'input[type="text"]', "")
    dentivoice_page.click_save()
    dentivoice_page.page.wait_for_timeout(500)
    errors = dentivoice_page.page.locator("p.text-red-500").count()
    is_disabled = dentivoice_page.save_button.is_disabled()
    assert errors > 0 or is_disabled, "Empty rule name should show error"
    dentivoice_page.cancel()


@pytest.mark.negative
def test_rule_phone_empty_shows_error(dentivoice_page):
    """TC-N-DV-20: Rule phone empty → error."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    toggle = modal.locator('button[role="switch"]').first
    if toggle.get_attribute("aria-checked") == "false":
        toggle.click()
        dentivoice_page.page.wait_for_timeout(500)
    _fill_field(dentivoice_page, 'input[type="tel"], input[placeholder*="phone" i]', "")
    dentivoice_page.click_save()
    dentivoice_page.page.wait_for_timeout(500)
    errors = dentivoice_page.page.locator("p.text-red-500").count()
    is_disabled = dentivoice_page.save_button.is_disabled()
    assert errors > 0 or is_disabled, "Empty phone should show error"
    dentivoice_page.cancel()


@pytest.mark.negative
def test_rule_name_101_chars_rejected(dentivoice_page):
    """TC-N-DV-19: Rule name 101 chars → error."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    toggle = modal.locator('button[role="switch"]').first
    if toggle.get_attribute("aria-checked") == "false":
        toggle.click()
        dentivoice_page.page.wait_for_timeout(500)
    _fill_field(dentivoice_page, 'input[type="text"]', "A" * 101)
    dentivoice_page.click_save()
    dentivoice_page.page.wait_for_timeout(500)
    errors = dentivoice_page.page.locator("p.text-red-500").count()
    is_disabled = dentivoice_page.save_button.is_disabled()
    assert errors > 0 or is_disabled
    dentivoice_page.cancel()
