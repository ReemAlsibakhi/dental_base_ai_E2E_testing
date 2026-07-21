"""
tests/practice_profile/test_practice_details.py
Optional details — Description (PP·R13), Parking (PP·R14),
Landmarks (PP·R15), Additional Notes (PP·R16).
"""

import pytest
from playwright.sync_api import expect

from pages.practice_profile_page import PracticeProfilePage
from test_data.practice_profile_data import PP_ERR, DESC_MAX_VALID, DESC_MAX_INVALID


def _fill(pp, locator, value):
    locator.scroll_into_view_if_needed()
    locator.clear(); locator.fill(value); locator.press("Tab")
    pp.page.wait_for_timeout(300)


# ===========================================================================
# Description (PP·R13)
# ===========================================================================

@pytest.mark.functional
def test_description_counter_updates(practice_profile_form_open):
    practice_profile_form_open.description_input.scroll_into_view_if_needed()
    practice_profile_form_open.description_input.clear()
    practice_profile_form_open.description_input.fill("Hello")
    counter = practice_profile_form_open.page.locator('[id$="-counter"]')
    assert "5" in counter.inner_text()


@pytest.mark.boundary
def test_description_500_chars_accepted(practice_profile_form_open):
    _fill(practice_profile_form_open, practice_profile_form_open.description_input, DESC_MAX_VALID)
    expect(practice_profile_form_open.description_error).to_be_hidden()


@pytest.mark.boundary
def test_description_501_chars_blocked(practice_profile_form_open):
    _fill(practice_profile_form_open, practice_profile_form_open.description_input, DESC_MAX_INVALID)
    value = practice_profile_form_open.description_input.input_value()
    assert practice_profile_form_open.description_error.is_visible() or len(value) <= 500


@pytest.mark.negative
@pytest.mark.security
@pytest.mark.xfail(reason="DEF-PP-07: App accepts <script> in text areas")
def test_description_xss_rejected(practice_profile_form_open):
    _fill(practice_profile_form_open, practice_profile_form_open.description_input, "<script>alert(1)</script>")
    expect(practice_profile_form_open.description_error).to_be_visible()


# ===========================================================================
# Parking (PP·R14)
# ===========================================================================

@pytest.mark.functional
def test_parking_toggle_on(practice_profile_form_open):
    toggle = practice_profile_form_open.parking_toggle
    toggle.scroll_into_view_if_needed()
    if toggle.get_attribute("data-state") != "checked":
        toggle.click()
    practice_profile_form_open.page.wait_for_timeout(300)
    assert toggle.get_attribute("data-state") == "checked"


@pytest.mark.functional
def test_parking_toggle_off(practice_profile_form_open):
    toggle = practice_profile_form_open.parking_toggle
    toggle.scroll_into_view_if_needed()
    if toggle.get_attribute("data-state") == "checked":
        toggle.click()
    practice_profile_form_open.page.wait_for_timeout(300)
    assert toggle.get_attribute("data-state") == "unchecked"


# ===========================================================================
# Landmarks (PP·R15)
# ===========================================================================

@pytest.mark.boundary
def test_landmarks_500_chars_accepted(practice_profile_form_open):
    _fill(practice_profile_form_open, practice_profile_form_open.landmarks_input, "A" * 500)
    error = practice_profile_form_open.page.locator('[name="landmarks"] ~ p[id$="-error"]')
    expect(error).to_be_hidden()


@pytest.mark.boundary
def test_landmarks_501_chars_blocked(practice_profile_form_open):
    _fill(practice_profile_form_open, practice_profile_form_open.landmarks_input, "A" * 501)
    value = practice_profile_form_open.landmarks_input.input_value()
    error = practice_profile_form_open.page.locator('[name="landmarks"] ~ p[id$="-error"]')
    assert error.is_visible() or len(value) <= 500


@pytest.mark.negative
@pytest.mark.security
@pytest.mark.xfail(reason="DEF-PP-07: App accepts <script> in text areas")
def test_landmarks_xss_rejected(practice_profile_form_open):
    _fill(practice_profile_form_open, practice_profile_form_open.landmarks_input, "<script>alert(1)</script>")
    error = practice_profile_form_open.page.locator('[name="landmarks"] ~ p[id$="-error"]')
    expect(error).to_be_visible()


# ===========================================================================
# Additional Notes (PP·R16)
# ===========================================================================

@pytest.mark.boundary
def test_additional_notes_500_chars_accepted(practice_profile_form_open):
    _fill(practice_profile_form_open, practice_profile_form_open.additional_notes, "A" * 500)
    error = practice_profile_form_open.page.locator('[name="practiceInfoAdditionalNotes"] ~ p[id$="-error"]')
    expect(error).to_be_hidden()


@pytest.mark.boundary
def test_additional_notes_501_chars_blocked(practice_profile_form_open):
    _fill(practice_profile_form_open, practice_profile_form_open.additional_notes, "A" * 501)
    value = practice_profile_form_open.additional_notes.input_value()
    error = practice_profile_form_open.page.locator('[name="practiceInfoAdditionalNotes"] ~ p[id$="-error"]')
    assert error.is_visible() or len(value) <= 500


@pytest.mark.negative
@pytest.mark.security
@pytest.mark.xfail(reason="DEF-PP-07: App accepts <script> in text areas")
def test_additional_notes_xss_rejected(practice_profile_form_open):
    _fill(practice_profile_form_open, practice_profile_form_open.additional_notes, "<script>alert(1)</script>")
    error = practice_profile_form_open.page.locator('[name="practiceInfoAdditionalNotes"] ~ p[id$="-error"]')
    expect(error).to_be_visible()
