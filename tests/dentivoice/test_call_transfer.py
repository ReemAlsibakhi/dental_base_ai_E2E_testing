"""
tests/dentivoice/test_call_transfer.py — Phase 3
Call Transfer (DV·R19-R22) — Edit index 3

Confirmed selectors (live DOM):
  Main toggle:    button[role="switch"] nth(0) — aria-checked
  Add rule btn:   button with text "Add"
  Rule fields appear ONLY after clicking Add:
    Name:      input[type="text"] nth(0) — placeholder "e.g., Office Reception"
    Phone:     input[type="text"] nth(1) — placeholder "555-123-4567"
    Condition: textarea
"""
import pytest
from playwright.sync_api import expect
from pages.dentivoice_page import DentiVoicePage
from test_data.dentivoice_data import VALID_PHONE


def _open(dv):
    dv.open_edit(DentiVoicePage.CARD["call_transfer"])
    dv.page.wait_for_timeout(500)


def _get_modal(dv):
    return dv.page.locator('[role="dialog"]')


def _click_add_rule(dv):
    """Click Add button to reveal rule fields."""
    modal = _get_modal(dv)
    add_btn = modal.get_by_role("button", name="Add").first
    add_btn.scroll_into_view_if_needed()
    add_btn.click()
    dv.page.wait_for_timeout(500)


def _fill_text(dv, index, value):
    """Fill input[type=text] by index inside modal."""
    modal = _get_modal(dv)
    field = modal.locator('input[type="text"]').nth(index)
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


def _ensure_toggle(dv, target_state: bool):
    """Ensure main toggle is ON (True) or OFF (False)."""
    modal = _get_modal(dv)
    toggle = modal.locator('button[role="switch"]').nth(0)
    current = toggle.get_attribute("aria-checked") == "true"
    if current != target_state:
        toggle.click()
        dv.page.wait_for_timeout(500)


# ===========================================================================
# TC-F — Functional
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
def test_call_transfer_panel_opens(dentivoice_page):
    """TC-F: Call Transfer panel opens."""
    _open(dentivoice_page)
    expect(dentivoice_page.cancel_button).to_be_visible()
    dentivoice_page.cancel()


@pytest.mark.functional
def test_transfer_toggle_on_saves(dentivoice_page):
    """TC-F-DV-15: Enable transfer toggle → saves."""
    _open(dentivoice_page)
    _ensure_toggle(dentivoice_page, False)  # Turn OFF first
    dentivoice_page.page.wait_for_timeout(300)
    _ensure_toggle(dentivoice_page, True)   # Then ON → dirty state
    dentivoice_page.save_and_assert_success()


@pytest.mark.functional
def test_transfer_toggle_off_saves(dentivoice_page):
    """TC-F-DV-16: Disable transfer → saves."""
    _open(dentivoice_page)
    _ensure_toggle(dentivoice_page, True)   # ON first
    dentivoice_page.page.wait_for_timeout(300)
    _ensure_toggle(dentivoice_page, False)  # Then OFF → dirty state
    dentivoice_page.save_and_assert_success()


# ===========================================================================
# TC-N — Negative
# ===========================================================================

@pytest.mark.negative
def test_rule_name_empty_shows_error(dentivoice_page):
    """TC-N-DV-18: Rule name empty → error."""
    _open(dentivoice_page)
    _ensure_toggle(dentivoice_page, True)
    _click_add_rule(dentivoice_page)
    # Leave name empty, fill valid phone
    _fill_text(dentivoice_page, 1, VALID_PHONE)  # phone = index 1
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
    _ensure_toggle(dentivoice_page, True)
    _click_add_rule(dentivoice_page)
    # Fill name, leave phone empty
    _fill_text(dentivoice_page, 0, "Office Reception")  # name = index 0
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
    _ensure_toggle(dentivoice_page, True)
    _click_add_rule(dentivoice_page)
    _fill_text(dentivoice_page, 0, "A" * 101)
    dentivoice_page.click_save()
    dentivoice_page.page.wait_for_timeout(500)
    errors = dentivoice_page.page.locator("p.text-red-500").count()
    is_disabled = dentivoice_page.save_button.is_disabled()
    assert errors > 0 or is_disabled
    dentivoice_page.cancel()
