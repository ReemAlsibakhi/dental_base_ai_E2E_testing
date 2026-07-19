"""
tests/dentivoice/test_call_transfer.py — Phase 3
Call Transfer (DV·R19-R22) — Edit index 3

Confirmed DOM (live):
  Toggle:   button[role="switch"] nth(0) — aria-checked
  After opening panel, fields appear immediately:
    Name:      input[placeholder*="Office Reception"]
    Phone:     input[placeholder*="555-123-4567"]
    Condition: textarea[placeholder*="When a patient"]
  Add Rule button: disabled until all fields filled — don't click it
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


def _fill_field(dv, placeholder, value):
    """Fill input by placeholder inside modal."""
    modal = _get_modal(dv)
    field = modal.locator(f'input[placeholder*="{placeholder}"]').first
    field.click()
    dv.page.wait_for_timeout(100)
    field.evaluate("""el => {
        el.focus();
        el.setSelectionRange(0, el.value.length);
        document.execCommand('delete', false, null);
    }""")
    dv.page.wait_for_timeout(200)
    if value:
        field.evaluate(f"""el => {{
            el.focus();
            document.execCommand('insertText', false, {repr(value)});
        }}""")
    dv.page.wait_for_timeout(300)


def _fill_condition(dv, value):
    """Fill condition textarea inside modal."""
    modal = _get_modal(dv)
    field = modal.locator('textarea').first
    field.click()
    dv.page.wait_for_timeout(100)
    field.evaluate("""el => {
        el.focus();
        el.setSelectionRange(0, el.value.length);
        document.execCommand('delete', false, null);
    }""")
    dv.page.wait_for_timeout(200)
    if value:
        field.evaluate(f"""el => {{
            el.focus();
            document.execCommand('insertText', false, {repr(value)});
        }}""")
    dv.page.wait_for_timeout(300)


def _ensure_toggle(dv, target: bool):
    modal = _get_modal(dv)
    toggle = modal.locator('button[role="switch"]').nth(0)
    current = toggle.get_attribute("aria-checked") == "true"
    if current != target:
        toggle.click(force=True)
        dv.page.wait_for_timeout(500)


def _open_add_form(dv):
    """Click Add button to show rule form fields."""
    modal = _get_modal(dv)
    # Add button (#2 confirmed from Console) opens the rule form
    add_btn = modal.get_by_role("button", name="Add").first
    add_btn.click(force=True)
    dv.page.wait_for_timeout(500)


def _submit_rule(dv):
    """Click Add Rule button to submit the filled rule."""
    modal = _get_modal(dv)
    add_rule_btn = modal.get_by_role("button", name="Add Rule")
    add_rule_btn.click(force=True)
    dv.page.wait_for_timeout(500)


def _fill_and_add_rule(dv, name="Front Desk", phone="555-123-4567", condition="When patient asks"):
    """Full flow: open form → fill fields → click Add Rule."""
    _open_add_form(dv)
    _fill_field(dv, "Office Reception", name)
    _fill_field(dv, "555", phone)
    _fill_condition(dv, condition)
    _submit_rule(dv)


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
    """TC-F-DV-15: Call Transfer ON + rule → saves."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    toggle = modal.locator('button[role="switch"]').nth(0)
    # If OFF → turn ON first
    if toggle.get_attribute("aria-checked") == "false":
        toggle.click(force=True)
        dentivoice_page.page.wait_for_timeout(500)
    # Add a rule to enable Save button
    _fill_and_add_rule(dentivoice_page)
    dentivoice_page.save_and_assert_success()


@pytest.mark.functional
def test_transfer_toggle_off_saves(dentivoice_page):
    """TC-F-DV-16: Call Transfer OFF → saves."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    toggle = modal.locator('button[role="switch"]').nth(0)
    # If already OFF → turn ON first to create dirty state when we turn OFF
    if toggle.get_attribute("aria-checked") == "false":
        toggle.click(force=True)
        dentivoice_page.page.wait_for_timeout(500)
        dentivoice_page.save_and_assert_success()
        # Reopen and turn OFF
        _open(dentivoice_page)
        modal = _get_modal(dentivoice_page)
        toggle = modal.locator('button[role="switch"]').nth(0)
    toggle.click(force=True)
    dentivoice_page.page.wait_for_timeout(500)
    assert toggle.get_attribute("aria-checked") == "false"
    dentivoice_page.save_and_assert_success()


# ===========================================================================
# TC-F — Rule fields
# ===========================================================================

@pytest.mark.functional
def test_rule_fields_visible(dentivoice_page):
    """TC-F-DV: Rule fields visible after clicking Add."""
    _open(dentivoice_page)
    _ensure_toggle(dentivoice_page, True)
    _open_add_form(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    expect(modal.locator('input[placeholder*="Office Reception"]').first).to_be_visible()
    expect(modal.locator('input[placeholder*="555"]').first).to_be_visible()
    expect(modal.locator('textarea').first).to_be_visible()
    dentivoice_page.cancel()


@pytest.mark.functional
def test_add_rule_save_disabled_when_empty(dentivoice_page):
    """TC-N: Form open with empty fields → Add Rule disabled."""
    _open(dentivoice_page)
    _ensure_toggle(dentivoice_page, True)
    _open_add_form(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    add_rule_btn = modal.get_by_role("button", name="Add Rule")
    assert add_rule_btn.is_disabled(), "Add Rule should be disabled when fields empty"
    dentivoice_page.cancel()


# ===========================================================================
# TC-N — Negative
# ===========================================================================

@pytest.mark.negative
def test_rule_phone_invalid_blocked(dentivoice_page):
    """TC-N-DV-21: Invalid phone format → Save disabled or error."""
    _open(dentivoice_page)
    _ensure_toggle(dentivoice_page, True)
    _open_add_form(dentivoice_page)
    _fill_field(dentivoice_page, "Office Reception", "Front Desk")
    _fill_field(dentivoice_page, "555", "not-a-phone!!!")
    _fill_condition(dentivoice_page, "When patient calls")
    dentivoice_page.page.wait_for_timeout(800)
    is_disabled = dentivoice_page.save_button.is_disabled()
    if not is_disabled:
        dentivoice_page.click_save()
        dentivoice_page.page.wait_for_timeout(500)
        errors = dentivoice_page.page.locator("p.text-red-500").count()
        assert errors > 0, "Invalid phone should show error"
    dentivoice_page.cancel()


@pytest.mark.negative
def test_rule_condition_empty_blocked(dentivoice_page):
    """TC-N-DV-22: Empty condition → Save disabled."""
    _open(dentivoice_page)
    _ensure_toggle(dentivoice_page, True)
    _open_add_form(dentivoice_page)
    _fill_field(dentivoice_page, "Office Reception", "Front Desk")
    _fill_field(dentivoice_page, "555", "555-123-4567")
    # Leave condition empty
    dentivoice_page.page.wait_for_timeout(500)
    is_disabled = dentivoice_page.save_button.is_disabled()
    assert is_disabled, "Empty condition should keep Save disabled"
    dentivoice_page.cancel()


@pytest.mark.negative
def test_rule_name_101_chars_rejected(dentivoice_page):
    """TC-N-DV-19: Rule name 101 chars → Save disabled or error."""
    _open(dentivoice_page)
    _ensure_toggle(dentivoice_page, True)
    _open_add_form(dentivoice_page)
    _fill_field(dentivoice_page, "Office Reception", "A" * 101)
    _fill_field(dentivoice_page, "555", "555-123-4567")
    _fill_condition(dentivoice_page, "When patient asks")
    dentivoice_page.page.wait_for_timeout(800)
    is_disabled = dentivoice_page.save_button.is_disabled()
    if not is_disabled:
        dentivoice_page.click_save()
        dentivoice_page.page.wait_for_timeout(500)
        errors = dentivoice_page.page.locator("p.text-red-500").count()
        assert errors > 0
    dentivoice_page.cancel()


# ===========================================================================
# TC-B — Boundary
# ===========================================================================

@pytest.mark.boundary
def test_rule_condition_500_chars_accepted(dentivoice_page):
    """TC-B-DV-13: Rule condition 500 chars (max valid) → saves."""
    _open(dentivoice_page)
    _ensure_toggle(dentivoice_page, True)
    _open_add_form(dentivoice_page)
    _fill_field(dentivoice_page, "Office Reception", "Front Desk")
    _fill_field(dentivoice_page, "555", "555-123-4567")
    modal = _get_modal(dentivoice_page)
    condition = modal.locator('textarea').first
    condition.click()
    condition.evaluate("""el => {
        el.focus();
        document.execCommand('insertText', false, 'A'.repeat(500));
    }""")
    dentivoice_page.page.wait_for_timeout(500)
    dentivoice_page.save_and_assert_success()
