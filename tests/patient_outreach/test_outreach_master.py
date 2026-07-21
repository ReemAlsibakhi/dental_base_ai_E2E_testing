"""
tests/patient_outreach/test_outreach_master.py
Master Switch (PO·R1-R3) + Smoke — Global tab.

Known bugs:
  DEF-PO-07: Reset fires without confirmation dialog
  DEF-PO-10: Sub-flow toggles not visually disabled when master OFF
"""

import pytest
from playwright.sync_api import expect

from pages.patient_outreach_page import PatientOutreachPage
from test_data.patient_outreach_data import GLOBAL_CARD, MASTER_TOGGLE, REMINDERS_TOGGLE, CONFIRMATION_TOGGLE


def _open(po):
    po.click_global_tab()
    po.open_edit(GLOBAL_CARD["master_switch"])


# ===========================================================================
# Smoke
# ===========================================================================

@pytest.mark.smoke
@pytest.mark.functional
def test_patient_outreach_global_tab_loads(patient_outreach_page):
    """TC-SM-PO-01: Global tab loads with Edit buttons visible."""
    patient_outreach_page.click_global_tab()
    assert patient_outreach_page.page.get_by_role("button", name="Edit").count() >= 2


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
    assert patient_outreach_page.page.get_by_role("button", name="Edit").count() >= 2


@pytest.mark.smoke
@pytest.mark.functional
def test_reminders_edit_opens(patient_outreach_page):
    """TC-SM-PO-04: Appointment Reminders edit panel opens."""
    patient_outreach_page.click_flows_tab()
    patient_outreach_page.open_edit(GLOBAL_CARD.get("reminders", 0))
    expect(patient_outreach_page.message_textarea).to_be_visible()
    patient_outreach_page.cancel()


# ===========================================================================
# Master Switch (PO·R1-R3)
# ===========================================================================

@pytest.mark.functional
def test_master_switch_enable(patient_outreach_page):
    """TC-F-PO-01: Enable Master Switch → saves."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(MASTER_TOGGLE)
    patient_outreach_page.save()


@pytest.mark.functional
def test_master_switch_disable(patient_outreach_page):
    """TC-F-PO-02: Disable Master Switch → saves."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_off(MASTER_TOGGLE)
    patient_outreach_page.save()


@pytest.mark.functional
def test_enable_reminders_flow(patient_outreach_page):
    """TC-F-PO-03: Enable Master + Reminders flow → saves."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(MASTER_TOGGLE)
    patient_outreach_page.turn_toggle_on(REMINDERS_TOGGLE)
    patient_outreach_page.save()


@pytest.mark.functional
def test_enable_confirmation_flow(patient_outreach_page):
    """TC-F-PO-04: Enable Master + Confirmation flow → saves."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(MASTER_TOGGLE)
    patient_outreach_page.turn_toggle_on(CONFIRMATION_TOGGLE)
    patient_outreach_page.save()


@pytest.mark.functional
def test_all_flows_off_with_master_on(patient_outreach_page):
    """TC-F-PO-05: Master ON but all flows OFF → saves."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(MASTER_TOGGLE)
    patient_outreach_page.turn_toggle_off(REMINDERS_TOGGLE)
    patient_outreach_page.turn_toggle_off(CONFIRMATION_TOGGLE)
    patient_outreach_page.save()


@pytest.mark.negative
@pytest.mark.xfail(reason="DEF-PO-10: Sub-flow toggles not visually disabled when master OFF")
def test_subflow_toggles_disabled_when_master_off(patient_outreach_page):
    """DEF-PO-10: Sub-flow toggles should be disabled when master is OFF."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_off(MASTER_TOGGLE)
    reminders_toggle = patient_outreach_page.page.locator('button[role="switch"]').nth(REMINDERS_TOGGLE)
    assert reminders_toggle.is_disabled()
    patient_outreach_page.cancel()


@pytest.mark.regression
def test_master_state_persists_after_reload(patient_outreach_page):
    """TC-R-PO-01: Master Switch state persists after reload."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(MASTER_TOGGLE)
    patient_outreach_page.save()
    patient_outreach_page.navigate_to_patient_outreach()
    patient_outreach_page.click_global_tab()
    patient_outreach_page.open_edit(GLOBAL_CARD["master_switch"])
    assert patient_outreach_page.is_toggle_on(MASTER_TOGGLE)
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_reset_to_defaults_button_exists(patient_outreach_page):
    """TC-F-PO-13: Reset to Defaults button is present."""
    patient_outreach_page.click_global_tab()
    reset_btn = patient_outreach_page.page.locator(
        'button:has-text("Reset"), button:has-text("Reset to Defaults")'
    ).first
    expect(reset_btn).to_be_visible()


@pytest.mark.negative
def test_reset_to_defaults_no_confirmation_dialog(patient_outreach_page):
    """DEF-PO-07: Reset fires without confirmation dialog."""
    patient_outreach_page.click_global_tab()
    reset_btn = patient_outreach_page.page.locator(
        'button:has-text("Reset"), button:has-text("Reset to Defaults")'
    ).first
    if reset_btn.is_visible():
        reset_btn.click()
        patient_outreach_page.page.wait_for_timeout(500)
        confirm = patient_outreach_page.page.locator(
            '[role="dialog"]:has-text("sure"), [role="dialog"]:has-text("Confirm")'
        )
        assert not confirm.is_visible(), "DEF-PO-07: Reset fires without confirmation"
