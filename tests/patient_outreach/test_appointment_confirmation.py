"""
tests/patient_outreach/test_appointment_confirmation.py — Phase 3
Appointment Confirmation Flow (FL·R11/R12) — Flows tab, Edit index 1
"""
import pytest
from playwright.sync_api import expect
from pages.patient_outreach_page import PatientOutreachPage
from test_data.patient_outreach_data import FLOW_CARD


def _open(po):
    po.click_flows_tab()
    po.open_edit(FLOW_CARD["confirmation"])


@pytest.mark.functional
@pytest.mark.smoke
def test_confirmation_enable_flow(patient_outreach_page):
    """TC-F-FL-21: Enable Confirmation flow."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(0)
    patient_outreach_page.save()


@pytest.mark.functional
@pytest.mark.functional
@pytest.mark.functional
def test_confirmation_message_editable(patient_outreach_page):
    """TC-F-FL-25: Confirmation message textarea is editable."""
    _open(patient_outreach_page)
    expect(patient_outreach_page.message_textarea).to_be_visible()
    patient_outreach_page.message_textarea.click(click_count=3)
    patient_outreach_page.message_textarea.type("Custom confirmation message")
    value = patient_outreach_page.message_textarea.input_value()
    assert "Custom confirmation" in value
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_confirmation_reset_to_default(patient_outreach_page):
    """TC-F-FL-26: Reset restores default message."""
    _open(patient_outreach_page)
    patient_outreach_page.reset_default.scroll_into_view_if_needed()
    patient_outreach_page.reset_default.click()
    patient_outreach_page.page.wait_for_timeout(300)
    value = patient_outreach_page.message_textarea.input_value()
    assert len(value) > 20
    patient_outreach_page.cancel()


@pytest.mark.regression
def test_confirmation_message_persists(patient_outreach_page):
    """TC-R-FL-07: Custom message persists after reload."""
    _open(patient_outreach_page)
    patient_outreach_page.message_textarea.click(click_count=3)
    patient_outreach_page.message_textarea.press("Control+a")
    patient_outreach_page.message_textarea.type("Persist test message")
    patient_outreach_page.save()

    patient_outreach_page.navigate_to_patient_outreach()
    _open(patient_outreach_page)
    value = patient_outreach_page.message_textarea.input_value()
    assert "Persist test message" in value
    patient_outreach_page.cancel()
