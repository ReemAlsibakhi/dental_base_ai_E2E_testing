"""
tests/scheduling_rules/test_scheduling_policies.py
Time-based policies — Lead Time, Advance Booking, Cancellation, No-Show.

Rules covered:
  SR·R1  Minimum Lead Time
  SR·R2  Advance Booking
  SR·R5  Cancellation Policy
  SR·R6  No-Show Policy
"""

import pytest
from playwright.sync_api import expect

from pages.scheduling_rules_page import SchedulingRulesPage
from test_data.scheduling_rules_data import (
    CARD,
    LEAD_TIME_VALID, LEAD_TIME_MIN_VALID,
    ADVANCE_BOOKING_VALID,
    CANCELLATION_VALID, CANCELLATION_MAX_VALID, CANCELLATION_MAX_PLUS1,
    NO_SHOW_VALID, NO_SHOW_MAX_VALID, NO_SHOW_MAX_PLUS1,
)


# ===========================================================================
# Helpers
# ===========================================================================

def _open_lead_time(sr): sr.open_edit(CARD["lead_time"]); sr.turn_toggle_on()
def _open_advance(sr): sr.open_edit(CARD["advance_booking"]); sr.turn_toggle_on()
def _open_cancellation(sr): sr.open_edit(CARD["cancellation"]); sr.turn_toggle_on()
def _open_no_show(sr): sr.open_edit(CARD["no_show"]); sr.turn_toggle_on()


# ===========================================================================
# Lead Time (SR·R1)
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
def test_lead_time_enable_and_save(scheduling_rules_page):
    """TC-F-SR-01: Enable Lead Time with valid value → saves."""
    _open_lead_time(scheduling_rules_page)
    scheduling_rules_page.fill_number(LEAD_TIME_VALID)
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.functional
def test_lead_time_disable_hides_field(scheduling_rules_page):
    """TC-F-SR-03: Disabling toggle hides number input."""
    scheduling_rules_page.open_edit(CARD["lead_time"])
    scheduling_rules_page.turn_toggle_off()
    expect(scheduling_rules_page.number_input).to_be_hidden()
    scheduling_rules_page.cancel()


@pytest.mark.functional
def test_lead_time_with_hours_unit(scheduling_rules_page):
    """TC-F-SR-02: Lead Time with Hours unit saves correctly."""
    _open_lead_time(scheduling_rules_page)
    if scheduling_rules_page.unit_select.is_visible():
        scheduling_rules_page.unit_select.select_option(index=1)
    scheduling_rules_page.fill_number(LEAD_TIME_VALID)
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.negative
def test_lead_time_zero_shows_error(scheduling_rules_page):
    _open_lead_time(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_lead_time_empty_shows_error(scheduling_rules_page):
    _open_lead_time(scheduling_rules_page)
    scheduling_rules_page.fill_number("")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_lead_time_negative_shows_error(scheduling_rules_page):
    _open_lead_time(scheduling_rules_page)
    scheduling_rules_page.fill_number("-1")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_lead_time_decimal_rejected(scheduling_rules_page):
    """TC-N-SR-04: Decimal rejected or floored."""
    _open_lead_time(scheduling_rules_page)
    scheduling_rules_page.fill_number("1.5")
    value = scheduling_rules_page.number_input.input_value()
    assert scheduling_rules_page.error.is_visible() or "." not in value
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_lead_time_default_on_enable_not_zero(scheduling_rules_page):
    scheduling_rules_page.open_edit(CARD["lead_time"])
    scheduling_rules_page.turn_toggle_on()
    value = scheduling_rules_page.number_input.input_value()
    assert int(value) >= 1, f"Default should be ≥ 1, got {value}"
    scheduling_rules_page.cancel()


@pytest.mark.boundary
def test_lead_time_min_1_accepted(scheduling_rules_page):
    _open_lead_time(scheduling_rules_page)
    scheduling_rules_page.fill_number(LEAD_TIME_MIN_VALID)
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.boundary
def test_lead_time_large_value_accepted(scheduling_rules_page):
    _open_lead_time(scheduling_rules_page)
    scheduling_rules_page.fill_number("1000")
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.regression
def test_lead_time_fix_invalid_then_save(scheduling_rules_page):
    _open_lead_time(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.fill_number(LEAD_TIME_VALID)
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.regression
def test_lead_time_persists_after_reload(scheduling_rules_page):
    _open_lead_time(scheduling_rules_page)
    scheduling_rules_page.fill_number("77")
    scheduling_rules_page.save_and_assert_success()
    scheduling_rules_page.navigate_to_scheduling_rules()
    scheduling_rules_page.open_edit(CARD["lead_time"])
    assert scheduling_rules_page.number_input.input_value() == "77"
    scheduling_rules_page.cancel()


@pytest.mark.regression
def test_lead_time_re_enable_clears_value(scheduling_rules_page):
    _open_lead_time(scheduling_rules_page)
    scheduling_rules_page.fill_number("55")
    scheduling_rules_page.save_and_assert_success()
    scheduling_rules_page.open_edit(CARD["lead_time"])
    scheduling_rules_page.turn_toggle_off()
    scheduling_rules_page.save_and_assert_success()
    scheduling_rules_page.open_edit(CARD["lead_time"])
    scheduling_rules_page.turn_toggle_on()
    expect(scheduling_rules_page.number_input).to_be_visible()
    scheduling_rules_page.cancel()


# ===========================================================================
# Advance Booking (SR·R2)
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
def test_advance_booking_enable_and_save(scheduling_rules_page):
    _open_advance(scheduling_rules_page)
    scheduling_rules_page.fill_number(ADVANCE_BOOKING_VALID)
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.functional
def test_advance_booking_disable_hides_field(scheduling_rules_page):
    scheduling_rules_page.open_edit(CARD["advance_booking"])
    scheduling_rules_page.turn_toggle_off()
    expect(scheduling_rules_page.number_input).to_be_hidden()
    scheduling_rules_page.cancel()


@pytest.mark.functional
def test_advance_booking_both_toggles_off(scheduling_rules_page):
    scheduling_rules_page.open_edit(CARD["advance_booking"])
    scheduling_rules_page.turn_toggle_off()
    expect(scheduling_rules_page.number_input).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.negative
def test_advance_booking_zero_shows_error(scheduling_rules_page):
    _open_advance(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_advance_booking_negative_shows_error(scheduling_rules_page):
    _open_advance(scheduling_rules_page)
    scheduling_rules_page.fill_number("-1")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_advance_booking_decimal_rejected(scheduling_rules_page):
    _open_advance(scheduling_rules_page)
    scheduling_rules_page.fill_number("1.5")
    value = scheduling_rules_page.number_input.input_value()
    assert scheduling_rules_page.error.is_visible() or "." not in value
    scheduling_rules_page.cancel()


@pytest.mark.boundary
def test_advance_booking_min_1_accepted(scheduling_rules_page):
    _open_advance(scheduling_rules_page)
    scheduling_rules_page.fill_number("1")
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.regression
def test_advance_booking_fix_invalid_then_save(scheduling_rules_page):
    _open_advance(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.fill_number(ADVANCE_BOOKING_VALID)
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


# ===========================================================================
# Cancellation Policy (SR·R5)
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
def test_cancellation_enable_and_save(scheduling_rules_page):
    _open_cancellation(scheduling_rules_page)
    scheduling_rules_page.fill_number(CANCELLATION_VALID)
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.functional
def test_cancellation_disable_hides_field(scheduling_rules_page):
    scheduling_rules_page.open_edit(CARD["cancellation"])
    scheduling_rules_page.turn_toggle_off()
    expect(scheduling_rules_page.number_input).to_be_hidden()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_cancellation_zero_shows_error(scheduling_rules_page):
    _open_cancellation(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_cancellation_empty_shows_error(scheduling_rules_page):
    _open_cancellation(scheduling_rules_page)
    scheduling_rules_page.fill_number("")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_cancellation_negative_shows_error(scheduling_rules_page):
    _open_cancellation(scheduling_rules_page)
    scheduling_rules_page.fill_number("-1")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.boundary
def test_cancellation_min_1_accepted(scheduling_rules_page):
    _open_cancellation(scheduling_rules_page)
    scheduling_rules_page.fill_number("1")
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.boundary
def test_cancellation_max_720_accepted(scheduling_rules_page):
    _open_cancellation(scheduling_rules_page)
    scheduling_rules_page.fill_number(CANCELLATION_MAX_VALID)
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.boundary
@pytest.mark.xfail(reason="DEF-SR-03: Max 720 not enforced")
def test_cancellation_721_rejected(scheduling_rules_page):
    _open_cancellation(scheduling_rules_page)
    scheduling_rules_page.fill_number(CANCELLATION_MAX_PLUS1)
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.regression
def test_cancellation_fix_invalid_then_save(scheduling_rules_page):
    _open_cancellation(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.fill_number(CANCELLATION_VALID)
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.regression
def test_cancellation_persists_after_reload(scheduling_rules_page):
    _open_cancellation(scheduling_rules_page)
    scheduling_rules_page.fill_number("88")
    scheduling_rules_page.save_and_assert_success()
    scheduling_rules_page.navigate_to_scheduling_rules()
    scheduling_rules_page.open_edit(CARD["cancellation"])
    assert scheduling_rules_page.number_input.input_value() == "88"
    scheduling_rules_page.cancel()


# ===========================================================================
# No-Show Policy (SR·R6)
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
def test_no_show_enable_and_save(scheduling_rules_page):
    _open_no_show(scheduling_rules_page)
    scheduling_rules_page.fill_number(NO_SHOW_VALID)
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.functional
def test_no_show_disable_hides_field(scheduling_rules_page):
    scheduling_rules_page.open_edit(CARD["no_show"])
    scheduling_rules_page.turn_toggle_off()
    expect(scheduling_rules_page.number_input).to_be_hidden()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_no_show_zero_shows_error(scheduling_rules_page):
    _open_no_show(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_no_show_empty_shows_error(scheduling_rules_page):
    _open_no_show(scheduling_rules_page)
    scheduling_rules_page.fill_number("")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_no_show_negative_shows_error(scheduling_rules_page):
    _open_no_show(scheduling_rules_page)
    scheduling_rules_page.fill_number("-1")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.boundary
def test_no_show_min_1_accepted(scheduling_rules_page):
    _open_no_show(scheduling_rules_page)
    scheduling_rules_page.fill_number("1")
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.boundary
def test_no_show_max_720_accepted(scheduling_rules_page):
    _open_no_show(scheduling_rules_page)
    scheduling_rules_page.fill_number(NO_SHOW_MAX_VALID)
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.boundary
@pytest.mark.xfail(reason="DEF-SR-04: Max 720 not enforced")
def test_no_show_721_rejected(scheduling_rules_page):
    _open_no_show(scheduling_rules_page)
    scheduling_rules_page.fill_number(NO_SHOW_MAX_PLUS1)
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.regression
def test_no_show_fix_invalid_then_save(scheduling_rules_page):
    _open_no_show(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.fill_number(NO_SHOW_VALID)
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.regression
def test_no_show_persists_after_reload(scheduling_rules_page):
    _open_no_show(scheduling_rules_page)
    scheduling_rules_page.fill_number("66")
    scheduling_rules_page.save_and_assert_success()
    scheduling_rules_page.navigate_to_scheduling_rules()
    scheduling_rules_page.open_edit(CARD["no_show"])
    assert scheduling_rules_page.number_input.input_value() == "66"
    scheduling_rules_page.cancel()

# Boundary aliases (duplicate boundary checks with original names)

@pytest.mark.boundary
def test_lead_time_exactly_1_accepted(scheduling_rules_page):
    _open_lead_time(scheduling_rules_page)
    scheduling_rules_page.fill_number("1")
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.boundary
def test_lead_time_zero_triggers_min_error(scheduling_rules_page):
    _open_lead_time(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_lead_time_default_on_enable_is_not_zero(scheduling_rules_page):
    scheduling_rules_page.open_edit(CARD["lead_time"])
    scheduling_rules_page.turn_toggle_on()
    value = scheduling_rules_page.number_input.input_value()
    assert int(value) >= 1
    scheduling_rules_page.cancel()


@pytest.mark.regression
def test_re_enable_toggle_clears_value(scheduling_rules_page):
    _open_lead_time(scheduling_rules_page)
    scheduling_rules_page.fill_number("55")
    scheduling_rules_page.save_and_assert_success()
    scheduling_rules_page.open_edit(CARD["lead_time"])
    scheduling_rules_page.turn_toggle_off()
    scheduling_rules_page.save_and_assert_success()
    scheduling_rules_page.open_edit(CARD["lead_time"])
    scheduling_rules_page.turn_toggle_on()
    expect(scheduling_rules_page.number_input).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.boundary
def test_advance_booking_exactly_1_accepted(scheduling_rules_page):
    _open_advance(scheduling_rules_page)
    scheduling_rules_page.fill_number("1")
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.boundary
def test_advance_booking_zero_triggers_error(scheduling_rules_page):
    _open_advance(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.boundary
def test_cancellation_exactly_1_accepted(scheduling_rules_page):
    _open_cancellation(scheduling_rules_page)
    scheduling_rules_page.fill_number("1")
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.boundary
def test_cancellation_zero_triggers_error(scheduling_rules_page):
    _open_cancellation(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.boundary
def test_no_show_exactly_1_accepted(scheduling_rules_page):
    _open_no_show(scheduling_rules_page)
    scheduling_rules_page.fill_number("1")
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.boundary
def test_no_show_zero_triggers_error(scheduling_rules_page):
    _open_no_show(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()
