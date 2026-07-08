"""
tests/scheduling_rules/test_cancellation_policy.py — Phase 2
Cancellation Policy (SR·R5) — card index 2
DEF-SR-03: Max 720 not enforced
"""
import pytest
from playwright.sync_api import expect
from pages.scheduling_rules_page import SchedulingRulesPage
from test_data.scheduling_rules_data import CARD, CANCELLATION_VALID, CANCELLATION_MAX_VALID, CANCELLATION_MAX_PLUS1


def _open(sr):
    sr.open_edit(CARD["cancellation"])
    sr.turn_toggle_on()


@pytest.mark.functional
@pytest.mark.smoke
def test_cancellation_enable_and_save(scheduling_rules_page):
    _open(scheduling_rules_page)
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
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_cancellation_empty_shows_error(scheduling_rules_page):
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number("")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.negative
def test_cancellation_negative_shows_error(scheduling_rules_page):
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number("-1")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.boundary
def test_cancellation_exactly_1_accepted(scheduling_rules_page):
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number("1")
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.boundary
def test_cancellation_zero_triggers_error(scheduling_rules_page):
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.boundary
def test_cancellation_max_720_accepted(scheduling_rules_page):
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number(CANCELLATION_MAX_VALID)
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.boundary
@pytest.mark.xfail(reason="DEF-SR-03: Max 720 not enforced — 721 saves without error")
def test_cancellation_721_rejected(scheduling_rules_page):
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number(CANCELLATION_MAX_PLUS1)
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.regression
def test_cancellation_fix_invalid_then_save(scheduling_rules_page):
    _open(scheduling_rules_page)
    scheduling_rules_page.fill_number("0")
    expect(scheduling_rules_page.error).to_be_visible()
    scheduling_rules_page.fill_number(CANCELLATION_VALID)
    expect(scheduling_rules_page.error).to_be_hidden()
    scheduling_rules_page.save_and_assert_success()
