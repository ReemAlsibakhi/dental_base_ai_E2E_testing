"""
tests/patient_outreach/test_preferred_hours.py — Phase 2
Preferred Hours (PO·R4/R5) — Global tab, Edit index 1

Day toggles in panel (confirmed from live DOM):
  Mon=OFF, Tue=ON, Wed=ON, Thu=ON, Fri=ON, Sat=OFF, Sun=OFF

Time inputs appear only when day toggle is ON.
Discard dialog appears when Cancel clicked with unsaved changes.
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
    """TC-F-PO-06: Preferred Hours panel opens with day toggles."""
    _open(patient_outreach_page)
    # Panel should have multiple switches (one per day)
    toggles = patient_outreach_page.page.locator('button[role="switch"]')
    assert toggles.count() >= 7, "Expected 7 day toggles"
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_enable_monday_shows_time_inputs(patient_outreach_page):
    """TC-F-PO-06: Enable Monday toggle → time inputs appear."""
    _open(patient_outreach_page)
    # Monday is index 0 (OFF by default)
    mon_toggle = patient_outreach_page.page.locator('button[role="switch"]').nth(0)
    if mon_toggle.get_attribute("data-state") != "checked":
        mon_toggle.click()
        patient_outreach_page.page.wait_for_timeout(500)
    # Time inputs should now be visible
    time_inputs = patient_outreach_page.page.locator('input[type="time"]')
    assert time_inputs.count() > 0, "Time inputs should appear when day is enabled"
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_disable_active_day_hides_time_inputs(patient_outreach_page):
    """TC-F-PO-07: Disable active day (Tue) → time inputs hidden."""
    _open(patient_outreach_page)
    # Tuesday is index 1 (ON by default)
    tue_toggle = patient_outreach_page.page.locator('button[role="switch"]').nth(1)
    initial_time_count = patient_outreach_page.page.locator('input[type="time"]').count()

    if tue_toggle.get_attribute("data-state") == "checked":
        tue_toggle.click()
        patient_outreach_page.page.wait_for_timeout(500)

    new_time_count = patient_outreach_page.page.locator('input[type="time"]').count()
    assert new_time_count < initial_time_count, "Time inputs should decrease when day disabled"
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_preferred_hours_save(patient_outreach_page):
    """TC-F-PO-08: Save preferred hours."""
    _open(patient_outreach_page)
    patient_outreach_page.save()


@pytest.mark.functional
def test_discard_dialog_on_cancel_with_changes(patient_outreach_page):
    """TC-F-PO-10: Cancel with unsaved changes → Discard dialog appears."""
    _open(patient_outreach_page)
    # Make a change
    mon_toggle = patient_outreach_page.page.locator('button[role="switch"]').nth(0)
    mon_toggle.click()
    patient_outreach_page.page.wait_for_timeout(300)

    # Click Cancel
    patient_outreach_page.cancel_button.click()
    patient_outreach_page.page.wait_for_timeout(500)

    # Discard dialog should appear
    expect(patient_outreach_page.discard_button).to_be_visible()
    # Click Discard to close
    patient_outreach_page.discard_button.click()


@pytest.mark.functional
def test_keep_editing_retains_changes(patient_outreach_page):
    """TC-F-PO-11: Keep Editing → panel stays open with changes."""
    _open(patient_outreach_page)
    mon_toggle = patient_outreach_page.page.locator('button[role="switch"]').nth(0)
    mon_toggle.click()
    patient_outreach_page.page.wait_for_timeout(300)

    patient_outreach_page.cancel_button.click()
    patient_outreach_page.page.wait_for_timeout(500)

    # Click Keep Editing
    patient_outreach_page.keep_editing.click()
    patient_outreach_page.page.wait_for_timeout(300)

    # Panel should still be open
    expect(patient_outreach_page.save_button).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_cancel_without_changes_no_dialog(patient_outreach_page):
    """TC-F-PO-12: Cancel without changes → no discard dialog."""
    _open(patient_outreach_page)
    patient_outreach_page.cancel_button.click()
    patient_outreach_page.page.wait_for_timeout(500)
    # No discard dialog should appear
    assert not patient_outreach_page.discard_button.is_visible()


@pytest.mark.regression
def test_preferred_hours_persist_after_reload(patient_outreach_page):
    """TC-R-PO-02: Custom hours persist after reload."""
    _open(patient_outreach_page)
    # Enable Monday
    mon_toggle = patient_outreach_page.page.locator('button[role="switch"]').nth(0)
    if mon_toggle.get_attribute("data-state") != "checked":
        mon_toggle.click()
        patient_outreach_page.page.wait_for_timeout(300)
    patient_outreach_page.save()

    # Reload and verify
    patient_outreach_page.navigate_to_patient_outreach()
    patient_outreach_page.click_global_tab()
    patient_outreach_page.open_edit(GLOBAL_CARD["preferred_hours"])
    mon_toggle = patient_outreach_page.page.locator('button[role="switch"]').nth(0)
    assert mon_toggle.get_attribute("data-state") == "checked", "Monday should still be enabled"
    patient_outreach_page.cancel()
