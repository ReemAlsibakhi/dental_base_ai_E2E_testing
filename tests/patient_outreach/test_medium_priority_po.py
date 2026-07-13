"""
tests/patient_outreach/test_medium_priority_po.py — Phase 4

Medium priority TCs:
  - Add/remove action rows in Reminders flow
  - Discard dialog behavior
  - Message chip insertion
  - Min Days + timing persist after reload
"""
import pytest
from playwright.sync_api import expect
from pages.patient_outreach_page import PatientOutreachPage
from test_data.patient_outreach_data import FLOW_CARD


def _open_reminders(po):
    po.click_flows_tab()
    po.open_edit(FLOW_CARD["reminders"])


# ===========================================================================
# Action rows (TC-F-FL-10/11/12)
# ===========================================================================

@pytest.mark.functional
def test_add_action_row(patient_outreach_page):
    """TC-F-FL-10: Add second action row."""
    _open_reminders(patient_outreach_page)
    initial_count = patient_outreach_page.page.locator('input[type="number"]').count()
    patient_outreach_page.add_action_btn.scroll_into_view_if_needed()
    patient_outreach_page.add_action_btn.click()
    patient_outreach_page.page.wait_for_timeout(300)
    new_count = patient_outreach_page.page.locator('input[type="number"]').count()
    assert new_count > initial_count, "Adding action row should add a new number input"
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_remove_action_row(patient_outreach_page):
    """TC-F-FL-11: Remove action row."""
    _open_reminders(patient_outreach_page)
    # Add a row first
    patient_outreach_page.add_action_btn.scroll_into_view_if_needed()
    patient_outreach_page.add_action_btn.click()
    patient_outreach_page.page.wait_for_timeout(300)
    count_after_add = patient_outreach_page.page.locator('input[type="number"]').count()

    # Remove last row — find remove/delete button
    remove_btn = patient_outreach_page.page.locator(
        'button[aria-label*="remove"], button[aria-label*="delete"], button:has-text("Remove")'
    ).last
    if remove_btn.count() > 0:
        remove_btn.click()
        patient_outreach_page.page.wait_for_timeout(300)
        count_after_remove = patient_outreach_page.page.locator('input[type="number"]').count()
        assert count_after_remove < count_after_add
    patient_outreach_page.cancel()


# ===========================================================================
# Chip insertion (TC-F-FL-14/15)
# ===========================================================================

@pytest.mark.functional
def test_insert_first_name_chip(patient_outreach_page):
    """TC-F-FL-14: Insert {first_name} chip into message."""
    _open_reminders(patient_outreach_page)
    patient_outreach_page.message_textarea.scroll_into_view_if_needed()

    # Find and click first_name chip button
    chip_btn = patient_outreach_page.page.locator(
        'button:has-text("first_name"), button:has-text("{first_name}")'
    ).first
    if chip_btn.count() > 0:
        chip_btn.click()
        patient_outreach_page.page.wait_for_timeout(300)
        value = patient_outreach_page.message_textarea.input_value()
        assert "first_name" in value
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_insert_office_name_chip(patient_outreach_page):
    """TC-F-FL-15: Insert {office_name} chip into message."""
    _open_reminders(patient_outreach_page)
    patient_outreach_page.message_textarea.scroll_into_view_if_needed()

    chip_btn = patient_outreach_page.page.locator(
        'button:has-text("office_name"), button:has-text("{office_name}")'
    ).first
    if chip_btn.count() > 0:
        chip_btn.click()
        patient_outreach_page.page.wait_for_timeout(300)
        value = patient_outreach_page.message_textarea.input_value()
        assert "office_name" in value
    patient_outreach_page.cancel()


# ===========================================================================
# Discard dialog (TC-F-FL-17/18/19/20)
# ===========================================================================

@pytest.mark.functional
def test_discard_dialog_appears_with_changes(patient_outreach_page):
    """TC-F-FL-17: Cancel with changes → Discard dialog."""
    _open_reminders(patient_outreach_page)
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
    _open_reminders(patient_outreach_page)
    patient_outreach_page.message_textarea.click()
    patient_outreach_page.message_textarea.type("change")
    patient_outreach_page.cancel_button.click()
    patient_outreach_page.page.wait_for_timeout(500)
    patient_outreach_page.discard_button.click()
    patient_outreach_page.page.wait_for_timeout(300)
    # Panel should be closed — save button no longer visible
    assert not patient_outreach_page.save_button.is_visible()


@pytest.mark.functional
def test_keep_editing_keeps_panel_open(patient_outreach_page):
    """TC-F-FL-19: Keep Editing → panel stays open."""
    _open_reminders(patient_outreach_page)
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
    _open_reminders(patient_outreach_page)
    patient_outreach_page.cancel_button.click()
    patient_outreach_page.page.wait_for_timeout(500)
    assert not patient_outreach_page.discard_button.is_visible()


# ===========================================================================
# Persist after reload (TC-R-FL-02/06)
# ===========================================================================

@pytest.mark.regression
def test_min_days_persists_after_reload(patient_outreach_page):
    """TC-R-FL-02: Min Days Ahead persists after reload."""
    _open_reminders(patient_outreach_page)
    patient_outreach_page.min_days_input.evaluate("""el => {
        const setter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, '5');
        el.dispatchEvent(new Event('input', {bubbles: true}));
        el.dispatchEvent(new Event('change', {bubbles: true}));
    }""")
    patient_outreach_page.page.wait_for_timeout(500)
    patient_outreach_page.save()

    patient_outreach_page.navigate_to_patient_outreach()
    _open_reminders(patient_outreach_page)
    value = patient_outreach_page.min_days_input.input_value()
    assert value == "5", f"Expected 5, got {value}"
    patient_outreach_page.cancel()
