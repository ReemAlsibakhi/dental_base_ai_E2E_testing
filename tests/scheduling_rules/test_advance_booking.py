"""
tests/scheduling_rules/test_advance_booking.py — Phase 3
Advance Booking (SR·R2) — card index 1
"""
import pytest
from playwright.sync_api import expect
from pages.scheduling_rules_page import SchedulingRulesPage
from test_data.scheduling_rules_data import CARD, ADVANCE_BOOKING_VALID


def _open(sr):
    sr.open_edit(CARD["advance_booking"])
    sr.turn_toggle_on()


@pytest.mark.functional
@pytest.mark.smoke
def test_advance_booking_enable_and_save(scheduling_rules_page):
    """TC-F-SR-04: Enable with valid value and save."""
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number(ADVANCE_BOOKING_VALID)
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.functional
def test_advance_booking_disable_hides_field(scheduling_rules_page):
    """TC-F-SR-05: Disable toggle hides field."""
    scheduling_rules_page.open_edit(CARD["advance_booking"])
    scheduling_rules_page.turn_toggle_off()
    expect(scheduling_rules_page.number_input).to_be_hidden()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_advance_booking_zero_shows_error(scheduling_rules_page):
    """TC-N-SR-06: Value 0 shows error."""
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_advance_booking_negative_shows_error(scheduling_rules_page):
    """TC-N-SR-07: Negative shows error."""
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number("-1")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.boundary
def test_advance_booking_exactly_1_accepted(scheduling_rules_page):
    """TC-B-SR-04: Exactly 1 — minimum valid."""
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number("1")
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.boundary
def test_advance_booking_zero_triggers_error(scheduling_rules_page):
    """TC-B-SR-05: 0 — below minimum."""
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.regression
def test_advance_booking_fix_invalid_then_save(scheduling_rules_page):
    """TC-R-SR-12: Fix invalid → save succeeds."""
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.fill_number(ADVANCE_BOOKING_VALID)
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()
