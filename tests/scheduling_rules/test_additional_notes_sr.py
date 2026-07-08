"""
tests/scheduling_rules/test_additional_notes_sr.py — Phase 3
Additional Notes (SR·R4) — card index 7
"""
import pytest
from playwright.sync_api import expect
from pages.scheduling_rules_page import SchedulingRulesPage
from test_data.scheduling_rules_data import CARD, NOTES_MAX_VALID, NOTES_MAX_INVALID


@pytest.mark.functional
@pytest.mark.smoke
def test_notes_valid_text_saves(scheduling_rules_page):
    """TC-F-SR-16: Enter valid notes and save."""
    scheduling_rules_page.open_edit(CARD["additional_notes"])
    scheduling_rules_page.notes_textarea.scroll_into_view_if_needed()
    scheduling_rules_page.notes_textarea.click(click_count=3)
    scheduling_rules_page.notes_textarea.type("Valid scheduling notes")
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.functional
def test_notes_clear_saves(scheduling_rules_page):
    """TC-F-SR-17: Clear notes and save."""
    scheduling_rules_page.open_edit(CARD["additional_notes"])
    scheduling_rules_page.notes_textarea.scroll_into_view_if_needed()
    scheduling_rules_page.notes_textarea.click(click_count=3)
    scheduling_rules_page.notes_textarea.press("Control+a")
    scheduling_rules_page.notes_textarea.press("Delete")
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.boundary
def test_notes_1000_chars_accepted(scheduling_rules_page):
    """TC-B: Exactly 1000 chars — max valid."""
    scheduling_rules_page.open_edit(CARD["additional_notes"])
    scheduling_rules_page.notes_textarea.scroll_into_view_if_needed()
    scheduling_rules_page.notes_textarea.click(click_count=3)
    scheduling_rules_page.notes_textarea.press("Control+a")
    scheduling_rules_page.notes_textarea.type(NOTES_MAX_VALID)
    error = scheduling_rules_page.page.locator('p[id$="-error"]')
    expect(error).to_be_hidden()
    scheduling_rules_page.cancel()


@pytest.mark.boundary
def test_notes_1001_chars_blocked(scheduling_rules_page):
    """TC-B: 1001 chars — above max, should be rejected or capped."""
    scheduling_rules_page.open_edit(CARD["additional_notes"])
    scheduling_rules_page.notes_textarea.scroll_into_view_if_needed()
    scheduling_rules_page.notes_textarea.click(click_count=3)
    scheduling_rules_page.notes_textarea.press("Control+a")
    scheduling_rules_page.notes_textarea.type(NOTES_MAX_INVALID)
    value = scheduling_rules_page.notes_textarea.input_value()
    error = scheduling_rules_page.page.locator('p[id$="-error"]')
    assert error.is_visible() or len(value) <= 1000
    scheduling_rules_page.cancel()


@pytest.mark.negative
@pytest.mark.security
def test_notes_xss_behavior(scheduling_rules_page):
    """TC-N-SR-18: XSS payload — check behavior."""
    scheduling_rules_page.open_edit(CARD["additional_notes"])
    scheduling_rules_page.notes_textarea.scroll_into_view_if_needed()
    scheduling_rules_page.notes_textarea.click(click_count=3)
    scheduling_rules_page.notes_textarea.type("<script>alert(1)</script>")
    # Save and verify no script execution
    scheduling_rules_page.save_and_assert_success()
    # Verify script tag not executed (page still functional)
    assert scheduling_rules_page.page.locator('button:has-text("Edit")').count() > 0
