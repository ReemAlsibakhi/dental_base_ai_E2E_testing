"""
tests/patient_outreach/test_smoke_patient_outreach.py — Phase 1
4 smoke tests covering both sub-tabs and key panels.
"""
import pytest
from playwright.sync_api import expect
from pages.patient_outreach_page import PatientOutreachPage
from test_data.patient_outreach_data import GLOBAL_CARD, FLOW_CARD


@pytest.mark.smoke
@pytest.mark.functional
def test_patient_outreach_global_tab_loads(patient_outreach_page):
    """TC-SM-PO-01: Global tab loads with Master Switch and Preferred Hours."""
    patient_outreach_page.click_global_tab()
    edit_btns = patient_outreach_page.page.get_by_role("button", name="Edit")
    assert edit_btns.count() >= 2


@pytest.mark.smoke
@pytest.mark.functional
def test_master_switch_edit_opens(patient_outreach_page):
    """TC-SM-PO-02: Master Switch edit panel opens with toggle."""
    patient_outreach_page.click_global_tab()
    patient_outreach_page.open_edit(GLOBAL_CARD["master_switch"])
    expect(patient_outreach_page.toggle).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.smoke
@pytest.mark.functional
def test_flows_tab_loads(patient_outreach_page):
    """TC-SM-PO-03: Flows tab loads with Reminders and Confirmation cards."""
    patient_outreach_page.click_flows_tab()
    edit_btns = patient_outreach_page.page.get_by_role("button", name="Edit")
    assert edit_btns.count() >= 2


@pytest.mark.smoke
@pytest.mark.functional
def test_reminders_edit_opens(patient_outreach_page):
    """TC-SM-PO-04: Appointment Reminders edit panel opens."""
    patient_outreach_page.click_flows_tab()
    patient_outreach_page.open_edit(FLOW_CARD["reminders"])
    expect(patient_outreach_page.message_textarea).to_be_visible()
    patient_outreach_page.cancel()
