"""
tests/patient_outreach/test_outreach_scheduling.py
Preferred Hours (PO·R4/R5) + Appointment Confirmation (FL·R11/R12).
"""

import pytest
from playwright.sync_api import expect

from pages.patient_outreach_page import PatientOutreachPage
from test_data.patient_outreach_data import GLOBAL_CARD, FLOW_CARD


# ===========================================================================
# Preferred Hours (PO·R4/R5)
# ===========================================================================

def _open_hours(po):
    po.click_global_tab()
    po.open_edit(GLOBAL_CARD["preferred_hours"])


@pytest.mark.functional
@pytest.mark.smoke
def test_preferred_hours_panel_opens(patient_outreach_page):
    """TC-F-PO-06: Panel opens with 7 day toggles."""
    _open_hours(patient_outreach_page)
    assert patient_outreach_page.get_hours_toggle_count() >= 7
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_enable_monday_shows_time_inputs(patient_outreach_page):
    """TC-F-PO-06: Enable Monday → time inputs appear."""
    _open_hours(patient_outreach_page)
    if not patient_outreach_page.is_hours_toggle_on(0):
        patient_outreach_page.click_hours_toggle(0)
    assert patient_outreach_page.page.locator('input[type="time"]').count() > 0
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_disable_active_day_hides_time_inputs(patient_outreach_page):
    """TC-F-PO-07: Disable active day → time inputs decrease."""
    _open_hours(patient_outreach_page)
    initial = patient_outreach_page.page.locator('input[type="time"]').count()
    if patient_outreach_page.is_hours_toggle_on(1):
        patient_outreach_page.click_hours_toggle(1)
        patient_outreach_page.page.wait_for_timeout(500)
    assert patient_outreach_page.page.locator('input[type="time"]').count() < initial
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_preferred_hours_save(patient_outreach_page):
    """TC-F-PO-08: Save preferred hours."""
    _open_hours(patient_outreach_page)
    patient_outreach_page.save()


@pytest.mark.functional
def test_discard_dialog_on_cancel_with_changes(patient_outreach_page):
    """TC-F-PO-10: Cancel with changes → Discard dialog."""
    _open_hours(patient_outreach_page)
    patient_outreach_page.click_hours_toggle(0)
    patient_outreach_page.cancel_button.click()
    patient_outreach_page.page.wait_for_timeout(500)
    expect(patient_outreach_page.discard_button).to_be_visible()
    patient_outreach_page.discard_button.click()


@pytest.mark.functional
def test_keep_editing_retains_changes(patient_outreach_page):
    """TC-F-PO-11: Keep Editing → panel stays open."""
    _open_hours(patient_outreach_page)
    patient_outreach_page.click_hours_toggle(0)
    patient_outreach_page.cancel_button.click()
    patient_outreach_page.page.wait_for_timeout(500)
    patient_outreach_page.keep_editing.click()
    expect(patient_outreach_page.save_button).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_cancel_without_changes_no_dialog(patient_outreach_page):
    """TC-F-PO-12: Cancel without changes → no dialog."""
    _open_hours(patient_outreach_page)
    patient_outreach_page.cancel_button.click()
    patient_outreach_page.page.wait_for_timeout(500)
    assert not patient_outreach_page.discard_button.is_visible()


@pytest.mark.regression
def test_preferred_hours_persist_after_reload(patient_outreach_page):
    """TC-R-PO-02: Hours persist after reload."""
    _open_hours(patient_outreach_page)
    was_on = patient_outreach_page.is_hours_toggle_on(0)
    patient_outreach_page.click_hours_toggle(0)
    patient_outreach_page.save()
    patient_outreach_page.navigate_to_patient_outreach()
    _open_hours(patient_outreach_page)
    assert patient_outreach_page.is_hours_toggle_on(0) != was_on
    patient_outreach_page.cancel()


# ===========================================================================
# Appointment Confirmation (FL·R11/R12)
# ===========================================================================

def _open_confirmation(po):
    po.click_flows_tab()
    po.open_edit(FLOW_CARD["confirmation"])


@pytest.mark.functional
@pytest.mark.smoke
def test_confirmation_panel_opens(patient_outreach_page):
    """TC-F-FL-21: Confirmation panel opens with toggle visible."""
    _open_confirmation(patient_outreach_page)
    expect(patient_outreach_page.toggle).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_confirmation_message_editable(patient_outreach_page):
    """TC-F-FL-25: Confirmation message textarea is editable."""
    _open_confirmation(patient_outreach_page)
    expect(patient_outreach_page.message_textarea).to_be_visible()
    patient_outreach_page.message_textarea.click(click_count=3)
    patient_outreach_page.message_textarea.type("Custom confirmation message")
    assert "Custom confirmation" in patient_outreach_page.message_textarea.input_value()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_confirmation_reset_to_default(patient_outreach_page):
    """TC-F-FL-26: Reset restores default message."""
    _open_confirmation(patient_outreach_page)
    patient_outreach_page.reset_default.scroll_into_view_if_needed()
    patient_outreach_page.reset_default.click()
    patient_outreach_page.page.wait_for_timeout(300)
    assert len(patient_outreach_page.message_textarea.input_value()) > 20
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_confirmation_operatories_section_visible(patient_outreach_page):
    """TC-F-CF-01: Operatories section visible."""
    _open_confirmation(patient_outreach_page)
    expect(patient_outreach_page.page.locator('button:has-text("Select all")')).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_confirmation_discard_dialog(patient_outreach_page):
    """TC-F-CF-03: Cancel with changes → Discard dialog."""
    _open_confirmation(patient_outreach_page)
    patient_outreach_page.message_textarea.click()
    patient_outreach_page.message_textarea.type("change")
    patient_outreach_page.cancel_button.click()
    patient_outreach_page.page.wait_for_timeout(500)
    expect(patient_outreach_page.discard_button).to_be_visible()
    patient_outreach_page.discard_button.click()


@pytest.mark.regression
def test_confirmation_message_persists(patient_outreach_page):
    """TC-R-FL-07: Custom message persists after reload."""
    _open_confirmation(patient_outreach_page)
    patient_outreach_page.message_textarea.click(click_count=3)
    patient_outreach_page.message_textarea.press("Control+a")
    patient_outreach_page.message_textarea.type("Persist test message")
    patient_outreach_page.save()
    patient_outreach_page.navigate_to_patient_outreach()
    _open_confirmation(patient_outreach_page)
    assert "Persist test message" in patient_outreach_page.message_textarea.input_value()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_confirmation_enable_flow(patient_outreach_page):
    """TC-F-FL-21: Enable Confirmation flow toggle → panel stays open."""
    _open_confirmation(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(0)
    patient_outreach_page.page.wait_for_timeout(300)
    expect(patient_outreach_page.toggle).to_be_visible()
    patient_outreach_page.cancel()
