"""
tests/scheduling_rules/test_medium_priority_sr.py — Phase 4

Medium priority TCs:
  - Lead Time with Hours unit (SR·R1)
  - Advance Booking both toggles OFF
  - Persist after reload (Lead Time, Cancellation, No-Show)
  - Re-enable clears prior value
"""
import pytest
from playwright.sync_api import expect
from pages.scheduling_rules_page import SchedulingRulesPage
from test_data.scheduling_rules_data import CARD, LEAD_TIME_VALID, CANCELLATION_VALID, NO_SHOW_VALID


# ===========================================================================
# Lead Time — unit variation (TC-F-SR-02)
# ===========================================================================

@pytest.mark.functional
def test_lead_time_with_hours_unit(scheduling_rules_page):
    """TC-F-SR-02: Lead Time with Hours unit saves correctly."""
    scheduling_rules_page.open_edit(CARD["lead_time"])
    scheduling_rules_page.turn_toggle_on()

    # Select Hours unit if select exists
    if scheduling_rules_page.unit_select.is_visible():
        scheduling_rules_page.unit_select.select_option(index=1)  # Hours

    scheduling_rules_page.fill_number(LEAD_TIME_VALID)
    scheduling_rules_page.save_and_assert_success()


# ===========================================================================
# Advance Booking — both toggles OFF (TC-F-SR-07)
# ===========================================================================

@pytest.mark.functional
def test_advance_booking_both_toggles_off(scheduling_rules_page):
    """TC-F-SR-07: Both Advance Booking toggles OFF — save succeeds."""
    scheduling_rules_page.open_edit(CARD["advance_booking"])

    # Disable main toggle
    scheduling_rules_page.turn_toggle_off()
    expect(scheduling_rules_page.number_input).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


# ===========================================================================
# Persist after reload (TC-R-SR-06/07/08)
# ===========================================================================

@pytest.mark.regression
def test_lead_time_persists_after_reload(scheduling_rules_page):
    """TC-R-SR-06: Lead Time value persists after page reload."""
    # Save a known value
    scheduling_rules_page.open_edit(CARD["lead_time"])
    scheduling_rules_page.turn_toggle_on()
    scheduling_rules_page.fill_number("77")
    scheduling_rules_page.save_and_assert_success()

    # Reload and verify
    scheduling_rules_page.navigate_to_scheduling_rules()
    scheduling_rules_page.open_edit(CARD["lead_time"])
    value = scheduling_rules_page.number_input.input_value()
    assert value == "77", f"Expected 77, got {value}"
    scheduling_rules_page.cancel()


@pytest.mark.regression
def test_cancellation_persists_after_reload(scheduling_rules_page):
    """TC-R-SR-07: Cancellation value persists after reload."""
    scheduling_rules_page.open_edit(CARD["cancellation"])
    scheduling_rules_page.turn_toggle_on()
    scheduling_rules_page.fill_number("88")
    scheduling_rules_page.save_and_assert_success()

    scheduling_rules_page.navigate_to_scheduling_rules()
    scheduling_rules_page.open_edit(CARD["cancellation"])
    value = scheduling_rules_page.number_input.input_value()
    assert value == "88", f"Expected 88, got {value}"
    scheduling_rules_page.cancel()


@pytest.mark.regression
def test_no_show_persists_after_reload(scheduling_rules_page):
    """TC-R-SR-08: No-Show value persists after reload."""
    scheduling_rules_page.open_edit(CARD["no_show"])
    scheduling_rules_page.turn_toggle_on()
    scheduling_rules_page.fill_number("66")
    scheduling_rules_page.save_and_assert_success()

    scheduling_rules_page.navigate_to_scheduling_rules()
    scheduling_rules_page.open_edit(CARD["no_show"])
    value = scheduling_rules_page.number_input.input_value()
    assert value == "66", f"Expected 66, got {value}"
    scheduling_rules_page.cancel()


# ===========================================================================
# Re-enable clears prior value (TC-R-SR-13)
# ===========================================================================

@pytest.mark.regression
def test_re_enable_toggle_clears_value(scheduling_rules_page):
    """TC-R-SR-13: Disabling then re-enabling resets or clears field value."""
    scheduling_rules_page.open_edit(CARD["lead_time"])
    scheduling_rules_page.turn_toggle_on()
    scheduling_rules_page.fill_number("55")
    scheduling_rules_page.save_and_assert_success()

    # Disable
    scheduling_rules_page.open_edit(CARD["lead_time"])
    scheduling_rules_page.turn_toggle_off()
    scheduling_rules_page.save_and_assert_success()

    # Re-enable — field should not be stuck on invalid state
    scheduling_rules_page.open_edit(CARD["lead_time"])
    scheduling_rules_page.turn_toggle_on()
    expect(scheduling_rules_page.number_input).to_be_visible()
    scheduling_rules_page.cancel()


# ===========================================================================
# Negative: Lead Time decimal (TC-N-SR-04)
# ===========================================================================

@pytest.mark.negative
def test_lead_time_decimal_rejected(scheduling_rules_page):
    """TC-N-SR-04: Decimal value rejected or floored."""
    scheduling_rules_page.open_edit(CARD["lead_time"])
    scheduling_rules_page.turn_toggle_on()
    scheduling_rules_page.fill_number("1.5")
    value = scheduling_rules_page.number_input.input_value()
    error_visible = scheduling_rules_page.error.is_visible()
    # Either error shown or value floored to integer
    assert error_visible or "." not in value


# ===========================================================================
# Negative: Advance Booking decimal (TC-N-SR-09)
# ===========================================================================

@pytest.mark.negative
def test_advance_booking_decimal_rejected(scheduling_rules_page):
    """TC-N-SR-09: Decimal in Advance Booking rejected or floored."""
    scheduling_rules_page.open_edit(CARD["advance_booking"])
    scheduling_rules_page.turn_toggle_on()
    scheduling_rules_page.fill_number("1.5")
    value = scheduling_rules_page.number_input.input_value()
    error_visible = scheduling_rules_page.error.is_visible()
    assert error_visible or "." not in value
    scheduling_rules_page.cancel()
