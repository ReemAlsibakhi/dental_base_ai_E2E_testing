"""
tests/scheduling_rules/test_lead_time.py — Phase 2
Minimum Lead Time (SR·R1) — card index 0
"""
import pytest
from playwright.sync_api import expect
from pages.scheduling_rules_page import SchedulingRulesPage
from test_data.scheduling_rules_data import CARD, LEAD_TIME_VALID, LEAD_TIME_MIN_VALID


def _open(sr):
    sr.open_edit(CARD["lead_time"])
    sr.turn_toggle_on()


@pytest.mark.functional
@pytest.mark.smoke
def test_lead_time_enable_and_save(scheduling_rules_page):
    """TC-F-SR-01: Enable Lead Time with valid value and save."""
    _open(scheduling_rules_page)
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


@pytest.mark.negative
def test_lead_time_zero_shows_error(scheduling_rules_page):
    """TC-N-SR-01: Value 0 shows error."""
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_lead_time_empty_shows_error(scheduling_rules_page):
    """TC-N-SR-02: Empty shows error."""
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number("")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_lead_time_negative_shows_error(scheduling_rules_page):
    """TC-N-SR-03: Negative shows error."""
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number("-1")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.boundary
def test_lead_time_exactly_1_accepted(scheduling_rules_page):
    """TC-B-SR-01: Exactly 1 — minimum valid."""
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number(LEAD_TIME_MIN_VALID)
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.boundary
def test_lead_time_zero_triggers_min_error(scheduling_rules_page):
    """TC-B-SR-02: 0 — below minimum."""
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.boundary
def test_lead_time_large_value_accepted(scheduling_rules_page):
    """TC-B-SR-03: Large value (1000) — no upper bound."""
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number("1000")
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.regression
def test_lead_time_fix_invalid_then_save(scheduling_rules_page):
    """TC-R-SR-01: Fix invalid → save succeeds."""
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.fill_number(LEAD_TIME_VALID)
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.negative
@pytest.mark.xfail(reason="DEF-SR-01: Lead Time defaults to 0 on enable (min=1 violated)")
def test_lead_time_default_on_enable_is_not_zero(scheduling_rules_page):
    """DEF-SR-01: Default on enable should be ≥ 1."""
    scheduling_rules_page.open_edit(CARD["lead_time"])
    scheduling_rules_page.turn_toggle_on()
    value = scheduling_rules_page.number_input.input_value()
    assert int(value) >= 1, f"Default should be ≥ 1, got {value}"
    scheduling_rules_page.cancel()
