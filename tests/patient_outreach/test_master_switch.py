"""
tests/patient_outreach/test_master_switch.py — Phase 2
Master Switch (PO·R1/R2/R3) — Global tab, Edit index 0

Toggle indices in panel:
  0 = Master Switch (Enable all outreach)
  1 = Appointment Reminders
  2 = Appointment Confirmation

Known bugs:
  DEF-PO-10: Sub-flow toggles not visually disabled when master OFF
"""
import pytest
from playwright.sync_api import expect
from pages.patient_outreach_page import PatientOutreachPage
from test_data.patient_outreach_data import GLOBAL_CARD, MASTER_TOGGLE, REMINDERS_TOGGLE, CONFIRMATION_TOGGLE


def _open(po):
    po.click_global_tab()
    po.open_edit(GLOBAL_CARD["master_switch"])


@pytest.mark.functional
@pytest.mark.smoke
def test_master_switch_enable(patient_outreach_page):
    """TC-F-PO-01: Enable Master Switch and save."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(MASTER_TOGGLE)
    patient_outreach_page.save()


@pytest.mark.functional
def test_master_switch_disable(patient_outreach_page):
    """TC-F-PO-02: Disable Master Switch and save."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_off(MASTER_TOGGLE)
    patient_outreach_page.save()


@pytest.mark.functional
def test_enable_reminders_flow(patient_outreach_page):
    """TC-F-PO-03: Enable Master + Reminders flow."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(MASTER_TOGGLE)
    patient_outreach_page.turn_toggle_on(REMINDERS_TOGGLE)
    patient_outreach_page.save()


@pytest.mark.functional
def test_enable_confirmation_flow(patient_outreach_page):
    """TC-F-PO-04: Enable Master + Confirmation flow."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(MASTER_TOGGLE)
    patient_outreach_page.turn_toggle_on(CONFIRMATION_TOGGLE)
    patient_outreach_page.save()


@pytest.mark.functional
def test_all_flows_off_with_master_on(patient_outreach_page):
    """TC-F-PO-05: Master ON but all flows OFF."""
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
    # Should be disabled when master is OFF
    assert reminders_toggle.is_disabled(), "Reminders toggle should be disabled when master is OFF"
    patient_outreach_page.cancel()


@pytest.mark.regression
def test_master_state_persists_after_reload(patient_outreach_page):
    """TC-R-PO-01: Master Switch state persists after reload."""
    _open(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(MASTER_TOGGLE)
    patient_outreach_page.save()

    # Reload and verify
    patient_outreach_page.navigate_to_patient_outreach()
    patient_outreach_page.click_global_tab()
    patient_outreach_page.open_edit(GLOBAL_CARD["master_switch"])
    assert patient_outreach_page.is_toggle_on(MASTER_TOGGLE), "Master toggle should still be ON"
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_reset_to_defaults_button_exists(patient_outreach_page):
    """TC-F-PO-13: Reset to Defaults button is present in Global tab."""
    patient_outreach_page.click_global_tab()
    reset_btn = patient_outreach_page.page.locator(
        'button:has-text("Reset"), button:has-text("Reset to Defaults")'
    ).first
    expect(reset_btn).to_be_visible()


@pytest.mark.negative
def test_reset_to_defaults_no_confirmation_dialog(patient_outreach_page):
    """DEF-PO-07: Reset to Defaults fires without confirmation dialog."""
    patient_outreach_page.click_global_tab()
    reset_btn = patient_outreach_page.page.locator(
        'button:has-text("Reset"), button:has-text("Reset to Defaults")'
    ).first
    if reset_btn.is_visible():
        reset_btn.click()
        patient_outreach_page.page.wait_for_timeout(500)
        confirm_dialog = patient_outreach_page.page.locator(
            '[role="dialog"]:has-text("sure"), [role="dialog"]:has-text("Confirm")'
        )
        assert not confirm_dialog.is_visible(), "DEF-PO-07: Reset fires without confirmation"
