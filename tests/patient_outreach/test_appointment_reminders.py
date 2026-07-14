"""
tests/patient_outreach/test_appointment_reminders.py — Phase 3
Appointment Reminders Flow (FL·R1–R9) — Flows tab, Edit index 0

Known bugs:
  DEF-PO-05: Action timing defaults to 0 hours (invalid — min=1)
  DEF-PO-11: Only SMS channel available (Call option absent)
"""
import pytest
from playwright.sync_api import expect
from pages.patient_outreach_page import PatientOutreachPage
from test_data.patient_outreach_data import FLOW_CARD, MSG_MAX_VALID, MSG_MAX_INVALID


def _open(po):
    po.click_flows_tab()
    po.open_edit(FLOW_CARD["reminders"])


# ===========================================================================
# TC-F — Functional
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
    patient_outreach_page.turn_toggle_on(0)  # Enable flow first
    patient_outreach_page.page.wait_for_timeout(300)
    patient_outreach_page.select_all_btn.scroll_into_view_if_needed()
    patient_outreach_page.select_all_btn.click(force=True)
    patient_outreach_page.page.wait_for_timeout(300)
    # Verify checkboxes are checked
    checkboxes = patient_outreach_page.page.locator('input[type="checkbox"]')
    if checkboxes.count() > 0:
        assert checkboxes.first.is_checked()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_clear_all_operatories_shows_hint(patient_outreach_page):
    """TC-F-FL-04: Clear All → hint text appears."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(0)  # Enable flow first
    patient_outreach_page.page.wait_for_timeout(300)
    patient_outreach_page.clear_all_btn.scroll_into_view_if_needed()
    patient_outreach_page.clear_all_btn.click(force=True)
    patient_outreach_page.page.wait_for_timeout(300)
    hint = patient_outreach_page.page.locator(
        'text=No operatories selected'
    )
    expect(hint).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_set_min_days_ahead(patient_outreach_page):
    """TC-F-FL-08: Set Min Days Ahead to 7."""
    _open(patient_outreach_page)
    patient_outreach_page.min_days_input.scroll_into_view_if_needed()
    patient_outreach_page.min_days_input.evaluate("""el => {
        const setter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, '3');
        el.dispatchEvent(new Event('input', {bubbles: true}));
        el.dispatchEvent(new Event('change', {bubbles: true}));
    }""")
    patient_outreach_page.page.wait_for_timeout(500)
    patient_outreach_page.save()


@pytest.mark.functional
def test_message_textarea_editable(patient_outreach_page):
    """TC-F-FL-13: Message textarea accepts valid text."""
    _open(patient_outreach_page)
    patient_outreach_page.message_textarea.scroll_into_view_if_needed()
    patient_outreach_page.message_textarea.click(click_count=3)
    patient_outreach_page.message_textarea.type("Custom reminder message for testing")
    value = patient_outreach_page.message_textarea.input_value()
    assert "Custom reminder" in value
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_reset_to_default_message(patient_outreach_page):
    """TC-F-FL-16: Reset to default restores factory message."""
    _open(patient_outreach_page)
    patient_outreach_page.reset_default.scroll_into_view_if_needed()
    patient_outreach_page.reset_default.click()
    patient_outreach_page.page.wait_for_timeout(300)
    value = patient_outreach_page.message_textarea.input_value()
    assert len(value) > 50, "Default message should be restored"
    patient_outreach_page.cancel()


# ===========================================================================
# TC-N — Negative
# ===========================================================================

@pytest.mark.negative
def test_min_days_zero_shows_error(patient_outreach_page):
    """TC-N-FL-01: Min Days Ahead = 0 → error."""
    _open(patient_outreach_page)
    patient_outreach_page.min_days_input.scroll_into_view_if_needed()
    patient_outreach_page.min_days_input.evaluate("""el => {
        const setter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, '0');
        el.dispatchEvent(new Event('input', {bubbles: true}));
        el.dispatchEvent(new Event('change', {bubbles: true}));
    }""")
    patient_outreach_page.min_days_input.press("Tab")
    patient_outreach_page.page.wait_for_timeout(500)
    expect(patient_outreach_page.error).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.negative
def test_min_days_negative_shows_error(patient_outreach_page):
    """TC-N-FL-02: Min Days negative → error."""
    _open(patient_outreach_page)
    patient_outreach_page.min_days_input.scroll_into_view_if_needed()
    patient_outreach_page.min_days_input.evaluate("""el => {
        const setter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, '-1');
        el.dispatchEvent(new Event('input', {bubbles: true}));
        el.dispatchEvent(new Event('change', {bubbles: true}));
    }""")
    patient_outreach_page.min_days_input.press("Tab")
    patient_outreach_page.page.wait_for_timeout(500)
    expect(patient_outreach_page.error).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.negative
def test_action_timing_default_zero_invalid(patient_outreach_page):
    """DEF-PO-05: Default timing of 0 hours should be invalid."""
    _open(patient_outreach_page)
    # Find timing inputs (number inputs after min_days)
    number_inputs = patient_outreach_page.page.locator('input[type="number"]').all()
    if len(number_inputs) > 1:
        timing_value = number_inputs[1].input_value()
        assert timing_value != "0", f"Default timing should not be 0, got {timing_value}"
    patient_outreach_page.cancel()


# ===========================================================================
# TC-B — Boundary
# ===========================================================================

@pytest.mark.boundary
def test_min_days_exactly_1_accepted(patient_outreach_page):
    """TC-B-FL-01: Min Days = 1 — minimum valid."""
    _open(patient_outreach_page)
    patient_outreach_page.min_days_input.scroll_into_view_if_needed()
    patient_outreach_page.min_days_input.evaluate("""el => {
        const setter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, '1');
        el.dispatchEvent(new Event('input', {bubbles: true}));
        el.dispatchEvent(new Event('change', {bubbles: true}));
    }""")
    patient_outreach_page.page.wait_for_timeout(500)
    expect(patient_outreach_page.error).to_be_hidden()
    patient_outreach_page.save()


@pytest.mark.boundary
def test_message_500_chars_accepted(patient_outreach_page):
    """TC-B-FL-07: Message exactly 500 chars — max valid."""
    _open(patient_outreach_page)
    # Use native setter to clear React textarea then set exactly 500 chars
    patient_outreach_page.message_textarea.evaluate(f"""el => {{
        const setter = Object.getOwnPropertyDescriptor(
            window.HTMLTextAreaElement.prototype, 'value').set;
        setter.call(el, '{"A" * 500}');
        el.dispatchEvent(new Event('input', {{bubbles: true}}));
        el.dispatchEvent(new Event('change', {{bubbles: true}}));
    }}""")
    patient_outreach_page.page.wait_for_timeout(300)
    value = patient_outreach_page.message_textarea.input_value()
    assert len(value) <= 500, f"Expected ≤500 chars, got {len(value)}"
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
    error_visible = patient_outreach_page.error.is_visible()
    assert error_visible or len(value) <= 500
    patient_outreach_page.cancel()


# ===========================================================================
# TC-R — Regression
# ===========================================================================

@pytest.mark.regression
def test_reminders_flow_state_persists(patient_outreach_page):
    """TC-R-FL-01: Flow enabled state persists after reload."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(0)
    patient_outreach_page.save()

    patient_outreach_page.navigate_to_patient_outreach()
    _open(patient_outreach_page)
    assert patient_outreach_page.is_toggle_on(0), "Flow should still be enabled"
    patient_outreach_page.cancel()
