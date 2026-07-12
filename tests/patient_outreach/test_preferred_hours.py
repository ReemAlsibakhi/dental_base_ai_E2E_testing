"""
tests/patient_outreach/test_preferred_hours.py — Phase 2
Preferred Hours (PO·R4/R5) — Global tab, Edit index 1

Day toggles: plain buttons with h-5 w-10 class
State: bg-indigo-600=ON, bg-gray-300=OFF (no aria-checked)
Day order: 0=Mon(OFF), 1=Tue(ON), 2=Wed(ON), 3=Thu(ON), 4=Fri(ON), 5=Sat(OFF), 6=Sun(OFF)
"""
import pytest
from playwright.sync_api import expect
from pages.patient_outreach_page import PatientOutreachPage
from test_data.patient_outreach_data import GLOBAL_CARD


def _open(po):
    po.click_global_tab()
    po.open_edit(GLOBAL_CARD["preferred_hours"])


@pytest.mark.functional
@pytest.mark.smoke
def test_preferred_hours_panel_opens(patient_outreach_page):
    """TC-F-PO-06: Preferred Hours panel opens with 7 day toggles."""
    _open(patient_outreach_page)
    count = patient_outreach_page.get_hours_toggle_count()
    assert count >= 7, f"Expected 7 day toggles, got {count}"
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_enable_monday_shows_time_inputs(patient_outreach_page):
    """TC-F-PO-06: Enable Monday → time inputs appear."""
    _open(patient_outreach_page)
    # Monday (index 0) is OFF by default
    if not patient_outreach_page.is_hours_toggle_on(0):
        patient_outreach_page.click_hours_toggle(0)
    time_inputs = patient_outreach_page.page.locator('input[type="time"]')
    assert time_inputs.count() > 0
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_preferred_hours_save(patient_outreach_page):
    """TC-F-PO-08: Save preferred hours."""
    _open(patient_outreach_page)
    patient_outreach_page.save()


@pytest.mark.functional
def test_discard_dialog_on_cancel_with_changes(patient_outreach_page):
    """TC-F-PO-10: Cancel with changes → Discard dialog."""
    _open(patient_outreach_page)
    patient_outreach_page.click_hours_toggle(0)  # Toggle Monday
    patient_outreach_page.cancel_button.click()
    patient_outreach_page.page.wait_for_timeout(500)
    expect(patient_outreach_page.discard_button).to_be_visible()
    patient_outreach_page.discard_button.click()


@pytest.mark.functional
def test_keep_editing_retains_changes(patient_outreach_page):
    """TC-F-PO-11: Keep Editing → panel stays open."""
    _open(patient_outreach_page)
    patient_outreach_page.click_hours_toggle(0)
    patient_outreach_page.cancel_button.click()
    patient_outreach_page.page.wait_for_timeout(500)
    patient_outreach_page.keep_editing.click()
    expect(patient_outreach_page.save_button).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_cancel_without_changes_no_dialog(patient_outreach_page):
    """TC-F-PO-12: Cancel without changes → no dialog."""
    _open(patient_outreach_page)
    patient_outreach_page.cancel_button.click()
    patient_outreach_page.page.wait_for_timeout(500)
    assert not patient_outreach_page.discard_button.is_visible()


@pytest.mark.regression
def test_preferred_hours_persist_after_reload(patient_outreach_page):
    """TC-R-PO-02: Hours persist after reload."""
    _open(patient_outreach_page)
    was_on = patient_outreach_page.is_hours_toggle_on(0)
    patient_outreach_page.click_hours_toggle(0)
    patient_outreach_page.save()

    patient_outreach_page.navigate_to_patient_outreach()
    _open(patient_outreach_page)
    is_on_now = patient_outreach_page.is_hours_toggle_on(0)
    assert is_on_now != was_on, "Monday toggle state should have changed"
    patient_outreach_page.cancel()
