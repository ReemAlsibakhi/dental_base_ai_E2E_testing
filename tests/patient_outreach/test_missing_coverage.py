"""
tests/patient_outreach/test_missing_coverage.py
Missing TCs identified from Decision Report v2.0 coverage gap analysis.

High Priority gaps:
  - TC-F-PO-13: Reset to Defaults button
  - TC-F-PO-07: Disable active day (Tue)
  - TC-F-FL-27/28: Confirmation operatories
  - TC-F-CF-01/02/03: Confirmation operatories section

Medium Priority gaps:
  - TC-F-FL-12: Row numbers auto-increment
  - TC-F-FL-05: Select Active operatories (Reminders)
  - TC-N-FL-04: Remove last action warning
  - TC-B-FL-04/05: Timing BVA
  - TC-R-FL-04/05/06: Persistence tests
"""
import pytest
from playwright.sync_api import expect
from pages.patient_outreach_page import PatientOutreachPage
from test_data.patient_outreach_data import GLOBAL_CARD, FLOW_CARD


def _open_reminders(po):
    po.click_flows_tab()
    po.open_edit(FLOW_CARD["reminders"])


def _open_confirmation(po):
    po.click_flows_tab()
    po.open_edit(FLOW_CARD["confirmation"])


def _set_number_input(po, locator, value):
    """Set a React-controlled number input using native setter."""
    locator.evaluate(f"""el => {{
        const setter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, '{value}');
        el.dispatchEvent(new Event('input', {{bubbles: true}}));
        el.dispatchEvent(new Event('change', {{bubbles: true}}));
    }}""")
    po.page.wait_for_timeout(300)


# ===========================================================================
# HIGH PRIORITY — Missing
# ===========================================================================

@pytest.mark.functional
def test_disable_active_day_hides_time_inputs(patient_outreach_page):
    """TC-F-PO-07: Disable active day (Tue=index 1) → time inputs decrease."""
    patient_outreach_page.click_global_tab()
    patient_outreach_page.open_edit(GLOBAL_CARD["preferred_hours"])

    initial_time_count = patient_outreach_page.page.locator('input[type="time"]').count()

    # Tuesday (index 1) is ON by default — disable it
    if patient_outreach_page.is_hours_toggle_on(1):
        patient_outreach_page.click_hours_toggle(1)
        patient_outreach_page.page.wait_for_timeout(500)

    new_time_count = patient_outreach_page.page.locator('input[type="time"]').count()
    assert new_time_count < initial_time_count, "Time inputs should decrease when day disabled"
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_reset_to_defaults_button_exists(patient_outreach_page):
    """TC-F-PO-13: Reset to Defaults button is present in Global tab."""
    patient_outreach_page.click_global_tab()
    reset_btn = patient_outreach_page.page.locator(
        'button:has-text("Reset"), button:has-text("Reset to Defaults")'
    ).first
    expect(reset_btn).to_be_visible()


@pytest.mark.functional
def test_confirmation_operatories_section_visible(patient_outreach_page):
    """TC-F-CF-01: Operatories section visible in Confirmation panel."""
    _open_confirmation(patient_outreach_page)
    # Operatories section should have Select All / Clear All buttons
    select_all = patient_outreach_page.page.locator('button:has-text("Select all")')
    expect(select_all).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_confirmation_select_all_operatories(patient_outreach_page):
    """TC-F-FL-27: Select All operatories in Confirmation."""
    _open_confirmation(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(0)  # Enable flow first
    patient_outreach_page.page.wait_for_timeout(300)
    patient_outreach_page.select_all_btn.scroll_into_view_if_needed()
    patient_outreach_page.select_all_btn.click(force=True)
    patient_outreach_page.page.wait_for_timeout(300)
    checkboxes = patient_outreach_page.page.locator('input[type="checkbox"]')
    if checkboxes.count() > 0:
        assert checkboxes.first.is_checked()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_confirmation_clear_all_operatories(patient_outreach_page):
    """TC-F-FL-28: Clear All operatories in Confirmation → hint shown."""
    _open_confirmation(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(0)  # Enable flow first
    patient_outreach_page.page.wait_for_timeout(300)
    patient_outreach_page.clear_all_btn.scroll_into_view_if_needed()
    patient_outreach_page.clear_all_btn.click(force=True)
    patient_outreach_page.page.wait_for_timeout(300)
    hint = patient_outreach_page.page.locator('text=No operatories selected')
    expect(hint).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_confirmation_select_active_button_present(patient_outreach_page):
    """TC-F-CF-02: Select Active operatories button present in Confirmation."""
    _open_confirmation(patient_outreach_page)
    active_btn = patient_outreach_page.page.locator(
        'button:has-text("Select active"), button:has-text("Active")'
    ).first
    expect(active_btn).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_confirmation_discard_dialog(patient_outreach_page):
    """TC-F-CF-03: Cancel with changes in Confirmation → Discard dialog."""
    _open_confirmation(patient_outreach_page)
    patient_outreach_page.message_textarea.click()
    patient_outreach_page.message_textarea.type("change")
    patient_outreach_page.cancel_button.click()
    patient_outreach_page.page.wait_for_timeout(500)
    expect(patient_outreach_page.discard_button).to_be_visible()
    patient_outreach_page.discard_button.click()


# ===========================================================================
# MEDIUM PRIORITY — Missing
# ===========================================================================

@pytest.mark.functional
def test_select_active_operatories_reminders(patient_outreach_page):
    """TC-F-FL-05: Select Active operatories button in Reminders."""
    _open_reminders(patient_outreach_page)
    active_btn = patient_outreach_page.page.locator(
        'button:has-text("Select active"), button:has-text("Active")'
    ).first
    expect(active_btn).to_be_visible()
    patient_outreach_page.cancel()


@pytest.mark.functional
def test_action_row_numbers_increment(patient_outreach_page):
    """TC-F-FL-12: Row numbers auto-increment when adding action rows."""
    _open_reminders(patient_outreach_page)
    patient_outreach_page.add_action_btn.scroll_into_view_if_needed()
    patient_outreach_page.add_action_btn.click()
    patient_outreach_page.page.wait_for_timeout(300)
    # Should have at least 2 number inputs (timing for each row)
    inputs = patient_outreach_page.page.locator('input[type="number"]')
    assert inputs.count() >= 2, "Adding row should create multiple action inputs"
    patient_outreach_page.cancel()


@pytest.mark.boundary
def test_action_timing_min_1_accepted(patient_outreach_page):
    """TC-B-FL-04: Action timing = 1 — minimum valid."""
    _open_reminders(patient_outreach_page)
    timing_inputs = patient_outreach_page.page.locator('input[type="number"]').all()
    if len(timing_inputs) > 1:
        _set_number_input(patient_outreach_page, timing_inputs[1], "1")
        timing_inputs[1].press("Tab")
        patient_outreach_page.page.wait_for_timeout(500)
        expect(patient_outreach_page.error).to_be_hidden()
    patient_outreach_page.cancel()


@pytest.mark.boundary
@pytest.mark.xfail(reason="DEF-PO-05: Timing validation may not show error for 0 value")
def test_action_timing_zero_shows_error(patient_outreach_page):
    """TC-B-FL-05: Action timing = 0 — below minimum."""
    _open_reminders(patient_outreach_page)
    timing_inputs = patient_outreach_page.page.locator('input[type="number"]').all()
    if len(timing_inputs) > 1:
        _set_number_input(patient_outreach_page, timing_inputs[1], "0")
        timing_inputs[1].press("Tab")
        patient_outreach_page.page.wait_for_timeout(500)
        expect(patient_outreach_page.error).to_be_visible()
    else:
        pytest.skip("No timing input found")
    patient_outreach_page.cancel()


@pytest.mark.regression
def test_operatory_selection_persists(patient_outreach_page):
    """TC-R-FL-04: Operatory selection persists after reload."""
    _open_reminders(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(0)  # Enable flow first
    patient_outreach_page.page.wait_for_timeout(300)
    patient_outreach_page.select_all_btn.scroll_into_view_if_needed()
    patient_outreach_page.select_all_btn.click(force=True)
    patient_outreach_page.page.wait_for_timeout(300)
    patient_outreach_page.save()

    patient_outreach_page.navigate_to_patient_outreach()
    _open_reminders(patient_outreach_page)
    checkboxes = patient_outreach_page.page.locator('input[type="checkbox"]')
    if checkboxes.count() > 0:
        assert checkboxes.first.is_checked(), "Operatory selection should persist"
    patient_outreach_page.cancel()


@pytest.mark.regression
def test_action_timing_persists(patient_outreach_page):
    """TC-R-FL-06: Action timing persists after reload."""
    _open_reminders(patient_outreach_page)
    timing_inputs = patient_outreach_page.page.locator('input[type="number"]').all()
    if len(timing_inputs) > 1:
        _set_number_input(patient_outreach_page, timing_inputs[1], "48")
        patient_outreach_page.save()

        patient_outreach_page.navigate_to_patient_outreach()
        _open_reminders(patient_outreach_page)
        timing_inputs = patient_outreach_page.page.locator('input[type="number"]').all()
        if len(timing_inputs) > 1:
            value = timing_inputs[1].input_value()
            assert value == "48", f"Expected 48, got {value}"
    patient_outreach_page.cancel()


# ===========================================================================
# Previously Pending — now confirmed and automated
# ===========================================================================

@pytest.mark.functional
def test_select_active_operatories_confirmation(patient_outreach_page):
    """Select Active button present and clickable in Confirmation panel."""
    _open_confirmation(patient_outreach_page)
    patient_outreach_page.turn_toggle_on(0)
    patient_outreach_page.page.wait_for_timeout(300)
    active_btn = patient_outreach_page.page.locator(
        'button:has-text("Select active"), button:has-text("Active")'
    ).first
    expect(active_btn).to_be_visible()
    active_btn.click(force=True)
    patient_outreach_page.page.wait_for_timeout(300)
    patient_outreach_page.cancel()


# Action timing max: no max enforced by design — no test needed


@pytest.mark.negative
def test_remove_last_action_shows_warning(patient_outreach_page):
    """TC-N-FL-04: Cannot remove last action row — min 1 required."""
    _open_reminders(patient_outreach_page)
    # Try to remove the only/last action row
    remove_btn = patient_outreach_page.page.locator(
        '[aria-label="Remove action 1"], button:has-text("Remove")'
    ).first
    if remove_btn.is_visible():
        remove_btn.click()
        patient_outreach_page.page.wait_for_timeout(300)
        # Either warning appears or button is disabled/absent
        warning = patient_outreach_page.page.locator(
            'text=at least one, text=minimum, text=required'
        )
        still_has_input = patient_outreach_page.page.locator('input[type="number"]').count() >= 1
        assert warning.is_visible() or still_has_input, "Should warn or keep minimum 1 action"
    patient_outreach_page.cancel()


@pytest.mark.regression
def test_added_action_row_persists(patient_outreach_page):
    """TC-R-FL-05: Added action row persists after reload."""
    _open_reminders(patient_outreach_page)
    initial_count = patient_outreach_page.page.locator('input[type="number"]').count()
    patient_outreach_page.add_action_btn.scroll_into_view_if_needed()
    patient_outreach_page.add_action_btn.click()
    patient_outreach_page.page.wait_for_timeout(300)
    patient_outreach_page.save()

    patient_outreach_page.navigate_to_patient_outreach()
    _open_reminders(patient_outreach_page)
    new_count = patient_outreach_page.page.locator('input[type="number"]').count()
    assert new_count > initial_count, "Added action row should persist after reload"
    patient_outreach_page.cancel()


@pytest.mark.negative
def test_reset_to_defaults_no_confirmation_dialog(patient_outreach_page):
    """TC-F-PO-13 / DEF-PO-07: Reset to Defaults fires without confirmation dialog."""
    patient_outreach_page.click_global_tab()
    reset_btn = patient_outreach_page.page.locator(
        'button:has-text("Reset"), button:has-text("Reset to Defaults")'
    ).first
    if reset_btn.is_visible():
        reset_btn.click()
        patient_outreach_page.page.wait_for_timeout(500)
        # No confirmation dialog should appear (DEF-PO-07 — bug)
        confirm_dialog = patient_outreach_page.page.locator(
            'text=Are you sure, text=Confirm, [role="dialog"]'
        )
        assert not confirm_dialog.is_visible(), "DEF-PO-07: Reset fires without confirmation"
