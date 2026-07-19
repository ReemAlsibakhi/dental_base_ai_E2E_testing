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


def _fill_by_placeholder(dv, placeholder_fragment, value):
    """Fill input by placeholder text inside modal."""
    modal = _get_modal(dv)
    field = modal.locator(f'input[placeholder*="{placeholder_fragment}"]').first
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
    _ensure_toggle(dentivoice_page, False)
    dentivoice_page.page.wait_for_timeout(300)
    _ensure_toggle(dentivoice_page, True)
    dentivoice_page.save_and_assert_success()


@pytest.mark.functional
def test_transfer_toggle_off_saves(dentivoice_page):
    """TC-F-DV-16: Disable transfer → saves."""
    _open(dentivoice_page)
    _ensure_toggle(dentivoice_page, True)
    dentivoice_page.page.wait_for_timeout(300)
    _ensure_toggle(dentivoice_page, False)
    dentivoice_page.save_and_assert_success()


# ===========================================================================
# TC-F — Rule fields visibility
# ===========================================================================

@pytest.mark.functional
def test_add_rule_reveals_fields(dentivoice_page):
    """TC-F-DV: Add rule button reveals Name + Phone + Condition fields."""
    _open(dentivoice_page)
    _ensure_toggle(dentivoice_page, True)
    _click_add_rule(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    # Verify rule fields appear after Add — use placeholder selectors
    name_field = modal.locator('input[placeholder*="Office Reception"]')
    phone_field = modal.locator('input[placeholder*="555"]')
    condition_field = modal.locator('textarea[placeholder*="When a patient"]')
    assert name_field.count() >= 1, "Name field should appear"
    assert phone_field.count() >= 1, "Phone field should appear"
    assert condition_field.count() >= 1, "Condition field should appear"
    dentivoice_page.cancel()


@pytest.mark.functional
def test_add_rule_save_disabled_when_empty(dentivoice_page):
    """TC-N: New rule with empty fields → Save stays disabled."""
    _open(dentivoice_page)
    _ensure_toggle(dentivoice_page, True)
    _click_add_rule(dentivoice_page)
    dentivoice_page.page.wait_for_timeout(500)
    # Save should be disabled when rule fields are empty
    is_disabled = dentivoice_page.save_button.is_disabled()
    assert is_disabled, "Save should be disabled with empty rule fields"
    dentivoice_page.cancel()


@pytest.mark.negative
def test_rule_phone_invalid_blocked(dentivoice_page):
    """TC-N-DV-21: Invalid phone format → Save disabled."""
    _open(dentivoice_page)
    _ensure_toggle(dentivoice_page, True)
    _click_add_rule(dentivoice_page)
    _fill_by_placeholder(dentivoice_page, "Office Reception", "Front Desk")
    _fill_by_placeholder(dentivoice_page, "555", "not-a-phone!!!")
    dentivoice_page.page.wait_for_timeout(800)
    is_disabled = dentivoice_page.save_button.is_disabled()
    errors = dentivoice_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0, "Invalid phone should be blocked"
    dentivoice_page.cancel()


@pytest.mark.negative
def test_rule_condition_empty_blocked(dentivoice_page):
    """TC-N-DV-22: Rule condition empty → Save disabled."""
    _open(dentivoice_page)
    _ensure_toggle(dentivoice_page, True)
    _click_add_rule(dentivoice_page)
    _fill_by_placeholder(dentivoice_page, "Office Reception", "Front Desk")
    _fill_by_placeholder(dentivoice_page, "555", "555-123-4567")
    # Leave condition empty
    dentivoice_page.page.wait_for_timeout(500)
    is_disabled = dentivoice_page.save_button.is_disabled()
    errors = dentivoice_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0, "Empty condition should block save"
    dentivoice_page.cancel()


@pytest.mark.boundary
def test_rule_condition_500_chars_accepted(dentivoice_page):
    """TC-B-DV-13: Rule condition 500 chars (max valid) → saves."""
    _open(dentivoice_page)
    _ensure_toggle(dentivoice_page, True)
    _click_add_rule(dentivoice_page)
    # Fill all required fields
    _fill_by_placeholder(dentivoice_page, "Office Reception", "Front Desk")
    _fill_by_placeholder(dentivoice_page, "555", "555-123-4567")
    modal = _get_modal(dentivoice_page)
    condition = modal.locator('textarea').first
    condition.click()
    dentivoice_page.page.wait_for_timeout(100)
    condition.evaluate("""el => {
        el.focus();
        el.setSelectionRange(0, el.value.length);
        document.execCommand('delete', false, null);
    }""")
    dentivoice_page.page.wait_for_timeout(200)
    condition.evaluate("""el => {
        el.focus();
        document.execCommand('insertText', false, 'A'.repeat(500));
    }""")
    dentivoice_page.page.wait_for_timeout(500)
    dentivoice_page.save_and_assert_success()


@pytest.mark.negative
def test_rule_name_101_chars_rejected(dentivoice_page):
    """TC-N-DV-19: Rule name 101 chars → Save disabled or error."""
    _open(dentivoice_page)
    _ensure_toggle(dentivoice_page, True)
    _click_add_rule(dentivoice_page)
    _fill_by_placeholder(dentivoice_page, "Office Reception", "A" * 101)
    dentivoice_page.page.wait_for_timeout(800)
    is_disabled = dentivoice_page.save_button.is_disabled()
    errors = dentivoice_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0, "101-char rule name should be rejected"
    dentivoice_page.cancel()
