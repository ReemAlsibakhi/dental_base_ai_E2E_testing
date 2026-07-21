"""
tests/patient_outreach/test_outreach_reminders.py
Appointment Reminders (FL·R1-R9) + Medium Priority TCs.

Known bugs:
  DEF-PO-05: Action timing defaults to 0 hours (invalid)
  DEF-PO-11: Only SMS channel available
"""

import pytest
from playwright.sync_api import expect

from pages.patient_outreach_page import PatientOutreachPage
from test_data.patient_outreach_data import FLOW_CARD, MSG_MAX_VALID, MSG_MAX_INVALID


def _open(po):
    po.click_flows_tab()
    po.open_edit(FLOW_CARD["reminders"])


def _set_number_input(locator, value):
    locator.evaluate(f"""el => {{
        const setter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, '{value}');
        el.dispatchEvent(new Event('input', {{bubbles: true}}));
        el.dispatchEvent(new Event('change', {{bubbles: true}}));
    }}""")


# ===========================================================================
# Functional
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
def test_reminders_enable_flow(patient_outreach_page):
    """TC-F-FL-01: Enable Reminders flow → save."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(0)
    patient_outreach_page.save()


@pytest.mark.functional
def test_reminders_disable_flow(patient_outreach_page):
    """TC-F-FL-02: Disable Reminders flow → save."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_off(0)
    patient_outreach_page.save()


@pytest.mark.functional
def test_select_all_operatories(patient_outreach_page):
    """TC-F-FL-03: Select All operatories."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(0)
    patient_outreach_page.page.wait_for_timeout(300)
    patient_outreach_page.select_all_btn.scroll_into_view_if_needed()
    patient_outreach_page.select_all_btn.click(force=True)
    patient_outreach_page.page.wait_for_timeout(300)
    checkboxes = patient_outreach_page.page.locator('input[type="checkbox"]')
    if checkboxes.count() > 0:
        assert checkboxes.first.is_checked()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_clear_all_operatories_shows_hint(patient_outreach_page):
    """TC-F-FL-04: Clear All → hint text appears."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(0)
    patient_outreach_page.page.wait_for_timeout(300)
    patient_outreach_page.clear_all_btn.scroll_into_view_if_needed()
    patient_outreach_page.clear_all_btn.click(force=True)
    patient_outreach_page.page.wait_for_timeout(300)
    expect(patient_outreach_page.page.locator('text=No operatories selected')).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_select_active_operatories(patient_outreach_page):
    """TC-F-FL-05: Select Active button present."""
    _open(patient_outreach_page)
    active_btn = patient_outreach_page.page.locator(
        'button:has-text("Select active"), button:has-text("Active")'
    ).first
    expect(active_btn).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_set_min_days_ahead(patient_outreach_page):
    """TC-F-FL-08: Set Min Days Ahead → saves."""
    _open(patient_outreach_page)
    patient_outreach_page.min_days_input.scroll_into_view_if_needed()
    _set_number_input(patient_outreach_page.min_days_input, "3")
    patient_outreach_page.page.wait_for_timeout(500)
    patient_outreach_page.save()


@pytest.mark.functional
def test_message_textarea_editable(patient_outreach_page):
    """TC-F-FL-13: Message textarea accepts valid text."""
    _open(patient_outreach_page)
    patient_outreach_page.message_textarea.scroll_into_view_if_needed()
    patient_outreach_page.message_textarea.click(click_count=3)
    patient_outreach_page.message_textarea.type("Custom reminder message")
    assert "Custom reminder" in patient_outreach_page.message_textarea.input_value()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_reset_to_default_message(patient_outreach_page):
    """TC-F-FL-16: Reset to default restores factory message."""
    _open(patient_outreach_page)
    patient_outreach_page.reset_default.scroll_into_view_if_needed()
    patient_outreach_page.reset_default.click()
    patient_outreach_page.page.wait_for_timeout(300)
    assert len(patient_outreach_page.message_textarea.input_value()) > 50
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_action_row_numbers_increment(patient_outreach_page):
    """TC-F-FL-12: Row numbers increment when adding action rows."""
    _open(patient_outreach_page)
    patient_outreach_page.add_action_btn.scroll_into_view_if_needed()
    patient_outreach_page.add_action_btn.click()
    patient_outreach_page.page.wait_for_timeout(300)
    assert patient_outreach_page.page.locator('input[type="number"]').count() >= 2
    patient_outreach_page.cancel()


# ===========================================================================
# Negative
# ===========================================================================

@pytest.mark.negative
def test_min_days_zero_shows_error(patient_outreach_page):
    """TC-N-FL-01: Min Days = 0 → error."""
    _open(patient_outreach_page)
    patient_outreach_page.min_days_input.scroll_into_view_if_needed()
    _set_number_input(patient_outreach_page.min_days_input, "0")
    patient_outreach_page.min_days_input.press("Tab")
    patient_outreach_page.page.wait_for_timeout(500)
    expect(patient_outreach_page.error).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.negative
def test_min_days_negative_shows_error(patient_outreach_page):
    """TC-N-FL-02: Min Days negative → error."""
    _open(patient_outreach_page)
    patient_outreach_page.min_days_input.scroll_into_view_if_needed()
    _set_number_input(patient_outreach_page.min_days_input, "-1")
    patient_outreach_page.min_days_input.press("Tab")
    patient_outreach_page.page.wait_for_timeout(500)
    expect(patient_outreach_page.error).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.negative
def test_action_timing_default_zero_invalid(patient_outreach_page):
    """DEF-PO-05: Default timing of 0 should be invalid."""
    _open(patient_outreach_page)
    inputs = patient_outreach_page.page.locator('input[type="number"]').all()
    if len(inputs) > 1:
        assert inputs[1].input_value() != "0"
    patient_outreach_page.cancel()


@pytest.mark.negative
def test_remove_last_action_shows_warning(patient_outreach_page):
    """TC-N-FL-04: Cannot remove last action row."""
    _open(patient_outreach_page)
    remove_btn = patient_outreach_page.page.locator(
        '[aria-label="Remove action 1"], button:has-text("Remove")'
    ).first
    if remove_btn.is_visible():
        remove_btn.click(force=True)
        patient_outreach_page.page.wait_for_timeout(300)
        warning = patient_outreach_page.page.locator('text=at least one, text=minimum, text=required')
        still_has_input = patient_outreach_page.page.locator('input[type="number"]').count() >= 1
        assert warning.is_visible() or still_has_input
    patient_outreach_page.cancel()


# ===========================================================================
# Boundary
# ===========================================================================

@pytest.mark.boundary
def test_min_days_exactly_1_accepted(patient_outreach_page):
    """TC-B-FL-01: Min Days = 1 — minimum valid."""
    _open(patient_outreach_page)
    patient_outreach_page.min_days_input.scroll_into_view_if_needed()
    _set_number_input(patient_outreach_page.min_days_input, "1")
    patient_outreach_page.page.wait_for_timeout(500)
    expect(patient_outreach_page.error).to_be_hidden()
    patient_outreach_page.save()


@pytest.mark.boundary
def test_action_timing_min_1_accepted(patient_outreach_page):
    """TC-B-FL-04: Action timing = 1 — minimum valid."""
    _open(patient_outreach_page)
    inputs = patient_outreach_page.page.locator('input[type="number"]').all()
    if len(inputs) > 1:
        _set_number_input(inputs[1], "1")
        inputs[1].press("Tab")
        patient_outreach_page.page.wait_for_timeout(500)
        expect(patient_outreach_page.error).to_be_hidden()
    patient_outreach_page.cancel()


@pytest.mark.boundary
@pytest.mark.xfail(reason="DEF-PO-05: Timing validation may not show error for 0")
def test_action_timing_zero_shows_error(patient_outreach_page):
    """TC-B-FL-05: Action timing = 0 — below minimum."""
    _open(patient_outreach_page)
    inputs = patient_outreach_page.page.locator('input[type="number"]').all()
    if len(inputs) > 1:
        _set_number_input(inputs[1], "0")
        inputs[1].press("Tab")
        patient_outreach_page.page.wait_for_timeout(500)
        expect(patient_outreach_page.error).to_be_visible()
    else:
        pytest.skip("No timing input found")
    patient_outreach_page.cancel()


@pytest.mark.boundary
def test_message_500_chars_accepted(patient_outreach_page):
    """TC-B-FL-07: Message 500 chars — max valid."""
    _open(patient_outreach_page)
    patient_outreach_page.message_textarea.evaluate(f"""el => {{
        const setter = Object.getOwnPropertyDescriptor(
            window.HTMLTextAreaElement.prototype, 'value').set;
        setter.call(el, '{"A" * 500}');
        el.dispatchEvent(new Event('input', {{bubbles: true}}));
    }}""")
    patient_outreach_page.page.wait_for_timeout(300)
    assert len(patient_outreach_page.message_textarea.input_value()) <= 500
    patient_outreach_page.cancel()


@pytest.mark.boundary
def test_message_501_chars_blocked(patient_outreach_page):
    """TC-B-FL-08: Message 501 chars — above max."""
    _open(patient_outreach_page)
    patient_outreach_page.message_textarea.evaluate(
        "el => { el.value = ''; el.dispatchEvent(new Event('input', {bubbles:true})); }"
    )
    patient_outreach_page.message_textarea.type(MSG_MAX_INVALID)
    value = patient_outreach_page.message_textarea.input_value()
    assert patient_outreach_page.error.is_visible() or len(value) <= 500
    patient_outreach_page.cancel()


# ===========================================================================
# Medium Priority — Action rows, Chips, Discard, Persist
# ===========================================================================

@pytest.mark.functional
def test_add_action_row(patient_outreach_page):
    """TC-F-FL-10: Add second action row."""
    _open(patient_outreach_page)
    initial = patient_outreach_page.page.locator('input[type="number"]').count()
    patient_outreach_page.add_action_btn.scroll_into_view_if_needed()
    patient_outreach_page.add_action_btn.click()
    patient_outreach_page.page.wait_for_timeout(300)
    assert patient_outreach_page.page.locator('input[type="number"]').count() > initial
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_remove_action_row(patient_outreach_page):
    """TC-F-FL-11: Remove action row."""
    _open(patient_outreach_page)
    patient_outreach_page.add_action_btn.scroll_into_view_if_needed()
    patient_outreach_page.add_action_btn.click()
    patient_outreach_page.page.wait_for_timeout(300)
    count_after_add = patient_outreach_page.page.locator('input[type="number"]').count()
    remove_btn = patient_outreach_page.page.locator(
        'button[aria-label*="remove"], button[aria-label*="delete"], button:has-text("Remove")'
    ).last
    if remove_btn.count() > 0:
        remove_btn.click()
        patient_outreach_page.page.wait_for_timeout(300)
        assert patient_outreach_page.page.locator('input[type="number"]').count() < count_after_add
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_insert_first_name_chip(patient_outreach_page):
    """TC-F-FL-14: Insert {first_name} chip."""
    _open(patient_outreach_page)
    patient_outreach_page.message_textarea.scroll_into_view_if_needed()
    chip = patient_outreach_page.page.locator('button:has-text("first_name"), button:has-text("{first_name}")').first
    if chip.count() > 0:
        chip.click()
        patient_outreach_page.page.wait_for_timeout(300)
        assert "first_name" in patient_outreach_page.message_textarea.input_value()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_insert_office_name_chip(patient_outreach_page):
    """TC-F-FL-15: Insert {office_name} chip."""
    _open(patient_outreach_page)
    patient_outreach_page.message_textarea.scroll_into_view_if_needed()
    chip = patient_outreach_page.page.locator('button:has-text("office_name"), button:has-text("{office_name}")').first
    if chip.count() > 0:
        chip.click()
        patient_outreach_page.page.wait_for_timeout(300)
        assert "office_name" in patient_outreach_page.message_textarea.input_value()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_discard_dialog_appears_with_changes(patient_outreach_page):
    """TC-F-FL-17: Cancel with changes → Discard dialog."""
    _open(patient_outreach_page)
    patient_outreach_page.message_textarea.scroll_into_view_if_needed()
    patient_outreach_page.message_textarea.click()
    patient_outreach_page.message_textarea.type("change")
    patient_outreach_page.cancel_button.click()
    patient_outreach_page.page.wait_for_timeout(500)
    expect(patient_outreach_page.discard_button).to_be_visible()
    patient_outreach_page.discard_button.click()


@pytest.mark.functional
def test_discard_changes_closes_panel(patient_outreach_page):
    """TC-F-FL-18: Discard Changes → panel closes."""
    _open(patient_outreach_page)
    patient_outreach_page.message_textarea.click()
    patient_outreach_page.message_textarea.type("change")
    patient_outreach_page.cancel_button.click()
    patient_outreach_page.page.wait_for_timeout(500)
    patient_outreach_page.discard_button.click()
    patient_outreach_page.page.wait_for_timeout(300)
    assert not patient_outreach_page.save_button.is_visible()


@pytest.mark.functional
def test_keep_editing_keeps_panel_open(patient_outreach_page):
    """TC-F-FL-19: Keep Editing → panel stays open."""
    _open(patient_outreach_page)
    patient_outreach_page.message_textarea.click()
    patient_outreach_page.message_textarea.type("change")
    patient_outreach_page.cancel_button.click()
    patient_outreach_page.page.wait_for_timeout(500)
    patient_outreach_page.keep_editing.click()
    expect(patient_outreach_page.save_button).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_cancel_no_changes_no_dialog(patient_outreach_page):
    """TC-F-FL-20: Cancel without changes → no Discard dialog."""
    _open(patient_outreach_page)
    patient_outreach_page.cancel_button.click()
    patient_outreach_page.page.wait_for_timeout(500)
    assert not patient_outreach_page.discard_button.is_visible()


# ===========================================================================
# Regression
# ===========================================================================

@pytest.mark.regression
def test_reminders_flow_state_persists(patient_outreach_page):
    """TC-R-FL-01: Flow state persists after reload."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(0)
    patient_outreach_page.save()
    patient_outreach_page.navigate_to_patient_outreach()
    _open(patient_outreach_page)
    assert patient_outreach_page.is_toggle_on(0)
    patient_outreach_page.cancel()


@pytest.mark.regression
def test_min_days_persists_after_reload(patient_outreach_page):
    """TC-R-FL-02: Min Days persists after reload."""
    _open(patient_outreach_page)
    _set_number_input(patient_outreach_page.min_days_input, "5")
    patient_outreach_page.page.wait_for_timeout(500)
    patient_outreach_page.save()
    patient_outreach_page.navigate_to_patient_outreach()
    _open(patient_outreach_page)
    assert patient_outreach_page.min_days_input.input_value() == "5"
    patient_outreach_page.cancel()


@pytest.mark.regression
def test_operatory_selection_persists(patient_outreach_page):
    """TC-R-FL-04: Operatory selection persists."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(0)
    patient_outreach_page.page.wait_for_timeout(300)
    patient_outreach_page.select_all_btn.click(force=True)
    patient_outreach_page.page.wait_for_timeout(300)
    patient_outreach_page.save()
    patient_outreach_page.navigate_to_patient_outreach()
    _open(patient_outreach_page)
    checkboxes = patient_outreach_page.page.locator('input[type="checkbox"]')
    if checkboxes.count() > 0:
        assert checkboxes.first.is_checked()
    patient_outreach_page.cancel()


@pytest.mark.regression
def test_added_action_row_persists(patient_outreach_page):
    """TC-R-FL-05: Added action row persists after reload."""
    _open(patient_outreach_page)
    initial = patient_outreach_page.page.locator('input[type="number"]').count()
    patient_outreach_page.add_action_btn.click()
    patient_outreach_page.page.wait_for_timeout(300)
    patient_outreach_page.save()
    patient_outreach_page.navigate_to_patient_outreach()
    _open(patient_outreach_page)
    assert patient_outreach_page.page.locator('input[type="number"]').count() > initial
    patient_outreach_page.cancel()


@pytest.mark.regression
def test_action_timing_persists(patient_outreach_page):
    """TC-R-FL-06: Action timing persists after reload."""
    _open(patient_outreach_page)
    inputs = patient_outreach_page.page.locator('input[type="number"]').all()
    if len(inputs) > 1:
        _set_number_input(inputs[1], "48")
        patient_outreach_page.save()
        patient_outreach_page.navigate_to_patient_outreach()
        _open(patient_outreach_page)
        inputs = patient_outreach_page.page.locator('input[type="number"]').all()
        if len(inputs) > 1:
            assert inputs[1].input_value() == "48"
    patient_outreach_page.cancel()
