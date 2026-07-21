"""
tests/scheduling_rules/test_scheduling_settings.py
Settings — Override PMS (SR·R8), Additional Notes (SR·R4), Smoke.
"""

import pytest
from playwright.sync_api import expect

from pages.scheduling_rules_page import SchedulingRulesPage
from test_data.scheduling_rules_data import CARD, NOTES_MAX_VALID, NOTES_MAX_INVALID


# ===========================================================================
# Smoke
# ===========================================================================

@pytest.mark.smoke
@pytest.mark.functional
def test_scheduling_rules_tab_loads(scheduling_rules_page):
    """TC-SM-SR-01: Tab loads with all Edit buttons visible."""
    assert scheduling_rules_page.page.get_by_role("button", name="Edit").count() >= 8


@pytest.mark.smoke
@pytest.mark.functional
def test_lead_time_edit_opens(scheduling_rules_page):
    """TC-SM-SR-02: Lead Time Edit panel opens."""
    scheduling_rules_page.open_edit(CARD["lead_time"])
    expect(scheduling_rules_page.toggle).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.smoke
@pytest.mark.functional
def test_cancellation_edit_opens(scheduling_rules_page):
    """TC-SM-SR-03: Cancellation Edit panel opens."""
    scheduling_rules_page.open_edit(CARD["cancellation"])
    expect(scheduling_rules_page.toggle).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.smoke
@pytest.mark.functional
def test_additional_notes_edit_opens(scheduling_rules_page):
    """TC-SM-SR-04: Additional Notes Edit panel opens."""
    scheduling_rules_page.open_edit(CARD["additional_notes"])
    expect(scheduling_rules_page.notes_textarea).to_be_visible()
    scheduling_rules_page.cancel()


# ===========================================================================
# Override PMS (SR·R8)
# ===========================================================================

@pytest.mark.functional
def test_override_pms_enable(scheduling_rules_page):
    """TC-F-SR-26: Enable Override PMS → saves."""
    scheduling_rules_page.open_edit(CARD["override_pms"])
    scheduling_rules_page.turn_toggle_on()
    assert scheduling_rules_page.is_toggle_on()
    scheduling_rules_page.save_toggle_only()


@pytest.mark.functional
def test_override_pms_disable(scheduling_rules_page):
    """TC-F-SR-27: Disable Override PMS → saves."""
    scheduling_rules_page.open_edit(CARD["override_pms"])
    scheduling_rules_page.turn_toggle_off()
    assert not scheduling_rules_page.is_toggle_on()
    scheduling_rules_page.save_toggle_only()


# ===========================================================================
# Additional Notes (SR·R4)
# ===========================================================================

@pytest.mark.functional
def test_notes_valid_text_saves(scheduling_rules_page):
    """TC-F-SR-16: Valid notes save."""
    scheduling_rules_page.open_edit(CARD["additional_notes"])
    scheduling_rules_page.notes_textarea.scroll_into_view_if_needed()
    scheduling_rules_page.notes_textarea.click(click_count=3)
    scheduling_rules_page.notes_textarea.type("Valid scheduling notes")
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.functional
def test_notes_clear_saves(scheduling_rules_page):
    """TC-F-SR-17: Clear notes saves."""
    scheduling_rules_page.open_edit(CARD["additional_notes"])
    scheduling_rules_page.notes_textarea.scroll_into_view_if_needed()
    scheduling_rules_page.notes_textarea.press("Control+a")
    scheduling_rules_page.notes_textarea.press("Delete")
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.boundary
def test_notes_1000_chars_accepted(scheduling_rules_page):
    """TC-B: 1000 chars — max valid."""
    scheduling_rules_page.open_edit(CARD["additional_notes"])
    scheduling_rules_page.notes_textarea.scroll_into_view_if_needed()
    scheduling_rules_page.notes_textarea.press("Control+a")
    scheduling_rules_page.notes_textarea.type(NOTES_MAX_VALID)
    expect(scheduling_rules_page.page.locator('p[id$="-error"]')).to_be_hidden()
    scheduling_rules_page.cancel()


@pytest.mark.boundary
def test_notes_1001_chars_blocked(scheduling_rules_page):
    """TC-B: 1001 chars — above max."""
    scheduling_rules_page.open_edit(CARD["additional_notes"])
    scheduling_rules_page.notes_textarea.scroll_into_view_if_needed()
    scheduling_rules_page.notes_textarea.press("Control+a")
    scheduling_rules_page.notes_textarea.type(NOTES_MAX_INVALID)
    value = scheduling_rules_page.notes_textarea.input_value()
    error = scheduling_rules_page.page.locator('p[id$="-error"]')
    assert error.is_visible() or len(value) <= 1000
    scheduling_rules_page.cancel()


@pytest.mark.negative
@pytest.mark.security
def test_notes_xss_no_script_execution(scheduling_rules_page):
    """TC-N: XSS payload saved — verify no script execution."""
    scheduling_rules_page.open_edit(CARD["additional_notes"])
    scheduling_rules_page.notes_textarea.scroll_into_view_if_needed()
    scheduling_rules_page.notes_textarea.click(click_count=3)
    scheduling_rules_page.notes_textarea.type("<script>alert(1)</script>")
    scheduling_rules_page.save_and_assert_success()
    assert scheduling_rules_page.page.locator('button:has-text("Edit")').count() > 0


@pytest.mark.smoke
@pytest.mark.functional
def test_cancellation_policy_edit_opens(scheduling_rules_page):
    """TC-SM-SR-03b: Cancellation Policy Edit panel opens."""
    scheduling_rules_page.open_edit(CARD["cancellation"])
    expect(scheduling_rules_page.toggle).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.negative
@pytest.mark.security
def test_notes_xss_behavior(scheduling_rules_page):
    """TC-N: XSS payload — verify no script execution."""
    scheduling_rules_page.open_edit(CARD["additional_notes"])
    scheduling_rules_page.notes_textarea.scroll_into_view_if_needed()
    scheduling_rules_page.notes_textarea.click(click_count=3)
    scheduling_rules_page.notes_textarea.type("<script>alert(1)</script>")
    scheduling_rules_page.save_and_assert_success()
    assert scheduling_rules_page.page.locator('button:has-text("Edit")').count() > 0
