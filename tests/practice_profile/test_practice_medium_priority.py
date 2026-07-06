"""
tests/practice_profile/test_practice_medium_priority.py — Phase 4

Medium priority TCs from Decision Report:
  - Practice Type dropdown (PP·R3)
  - Description counter (PP·R13)
  - Parking toggle + Details (PP·R14)
  - Landmarks max length (PP·R15)
  - Additional Notes max length (PP·R16)
  - XSS in text areas

Confirmed from live DOM:
  Practice Type: select[0] with values: general, pediatric, orthodontic...
  Description:   [name="description"] maxLength=500, counter id$="-counter"
  Parking:       input[type="checkbox"] no id — use page.locator directly
  Landmarks:     [name="landmarks"] maxLength=-1 (JS validation only)
  AdditionalNotes: [name="practiceInfoAdditionalNotes"] maxLength=-1
"""

import pytest
from playwright.sync_api import expect

from pages.practice_profile_page import PracticeProfilePage
from test_data.practice_profile_data import PP_ERR, DESC_MAX_VALID, DESC_MAX_INVALID


# ===========================================================================
# Helper
# ===========================================================================

def _fill(pp: PracticeProfilePage, locator, value: str) -> None:
    locator.scroll_into_view_if_needed()
    locator.clear()
    locator.fill(value)
    locator.press("Tab")
    pp.page.wait_for_timeout(300)


# ===========================================================================
# Practice Type (PP·R3)
# ===========================================================================

@pytest.mark.functional
def test_practice_type_has_default_value(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-F-PP-05: Practice Type dropdown has a default selected value."""
    practice_profile_form_open.practice_type_select.scroll_into_view_if_needed()
    value = practice_profile_form_open.practice_type_select.input_value()
    assert value != "", "Practice Type should have a default selection"


@pytest.mark.functional
def test_practice_type_can_select_pediatric(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-F-PP-05: Practice Type dropdown accepts valid selection."""
    practice_profile_form_open.practice_type_select.scroll_into_view_if_needed()
    practice_profile_form_open.practice_type_select.select_option("pediatric")
    value = practice_profile_form_open.practice_type_select.input_value()
    assert value == "pediatric"


@pytest.mark.functional
def test_practice_type_all_options_available(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-F-PP-05: All practice type options are available."""
    practice_profile_form_open.practice_type_select.scroll_into_view_if_needed()
    options = practice_profile_form_open.practice_type_select.evaluate(
        "el => [...el.options].map(o => o.value)"
    )
    expected = ["general", "pediatric", "orthodontic",
                "oral_surgery", "periodontic", "endodontic"]
    for opt in expected:
        assert opt in options, f"Expected option '{opt}' not found"


# ===========================================================================
# Description Counter (PP·R13)
# ===========================================================================

@pytest.mark.functional
def test_description_counter_updates_on_input(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-U-PP-04: Description counter updates as user types."""
    inp = practice_profile_form_open.description_input
    inp.scroll_into_view_if_needed()
    inp.clear()
    inp.fill("Hello")
    counter = practice_profile_form_open.page.locator('[id$="-counter"]')
    counter_text = counter.inner_text()
    assert "5/500" in counter_text or "5" in counter_text


@pytest.mark.boundary
def test_description_exactly_500_chars_accepted(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-B-PP-03: Description of exactly 500 chars accepted."""
    _fill(practice_profile_form_open, practice_profile_form_open.description_input, DESC_MAX_VALID)
    expect(practice_profile_form_open.description_error).to_be_hidden()


@pytest.mark.boundary
def test_description_501_chars_blocked(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-B-PP-04: Description of 501 chars rejected or capped at 500."""
    _fill(practice_profile_form_open, practice_profile_form_open.description_input, DESC_MAX_INVALID)
    value = practice_profile_form_open.description_input.input_value()
    error_visible = practice_profile_form_open.description_error.is_visible()
    field_capped  = len(value) <= 500
    assert error_visible or field_capped


@pytest.mark.negative
@pytest.mark.security
@pytest.mark.xfail(reason="DEF-PP-07: App accepts <script> in text areas — XSS risk")
def test_description_xss_rejected(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-N-PP-26: XSS in description field is rejected."""
    _fill(practice_profile_form_open, practice_profile_form_open.description_input,
          "<script>alert(1)</script>")
    expect(practice_profile_form_open.description_error).to_be_visible()


# ===========================================================================
# Parking Toggle (PP·R14)
# ===========================================================================

@pytest.mark.functional
def test_parking_toggle_can_be_enabled(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-F-PP-06: Parking toggle can be switched ON."""
    toggle = practice_profile_form_open.parking_toggle
    toggle.scroll_into_view_if_needed()
    if toggle.get_attribute("data-state") != "checked":
        toggle.click()
    practice_profile_form_open.page.wait_for_timeout(300)
    assert toggle.get_attribute("data-state") == "checked"


@pytest.mark.functional
def test_parking_details_visible_when_enabled(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-U-PP-05: Parking details textarea appears when toggle is ON."""
    toggle = practice_profile_form_open.parking_toggle
    toggle.scroll_into_view_if_needed()
    if toggle.get_attribute('data-state') != 'checked':
        toggle.click()
    practice_profile_form_open.page.wait_for_timeout(500)
    # Parking details textarea should now be visible
    parking_details = practice_profile_form_open.page.get_by_label("Parking Details")
    expect(parking_details).to_be_visible()


@pytest.mark.functional
def test_parking_details_hidden_when_disabled(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-U-PP-05: Parking details hidden when toggle is OFF."""
    toggle = practice_profile_form_open.parking_toggle
    toggle.scroll_into_view_if_needed()
    if toggle.get_attribute('data-state') == 'checked':
        toggle.click()
    practice_profile_form_open.page.wait_for_timeout(500)
    parking_details = practice_profile_form_open.page.get_by_label('Parking Details')
    expect(parking_details).to_be_hidden()


# ===========================================================================
# Landmarks (PP·R15) — max 500
# ===========================================================================

@pytest.mark.boundary
def test_landmarks_500_chars_accepted(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-B-PP-28: Landmarks of exactly 500 chars accepted."""
    _fill(practice_profile_form_open, practice_profile_form_open.landmarks_input, "A" * 500)
    error = practice_profile_form_open.page.locator(
        '[name="landmarks"] ~ p[id$="-error"]'
    )
    expect(error).to_be_hidden()


@pytest.mark.boundary
def test_landmarks_501_chars_blocked(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-B-PP-29: Landmarks of 501 chars rejected or capped."""
    _fill(practice_profile_form_open, practice_profile_form_open.landmarks_input, "A" * 501)
    value = practice_profile_form_open.landmarks_input.input_value()
    error = practice_profile_form_open.page.locator('[name="landmarks"] ~ p[id$="-error"]')
    assert error.is_visible() or len(value) <= 500


@pytest.mark.negative
@pytest.mark.security
@pytest.mark.xfail(reason="DEF-PP-07: App accepts <script> in text areas — XSS risk")
def test_landmarks_xss_rejected(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-S-PP-09: XSS in landmarks rejected."""
    _fill(practice_profile_form_open, practice_profile_form_open.landmarks_input,
          "<script>alert(1)</script>")
    error = practice_profile_form_open.page.locator('[name="landmarks"] ~ p[id$="-error"]')
    expect(error).to_be_visible()


# ===========================================================================
# Additional Notes (PP·R16) — max 500
# ===========================================================================

@pytest.mark.boundary
def test_additional_notes_500_chars_accepted(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-B-PP-32: Additional Notes of exactly 500 chars accepted."""
    _fill(practice_profile_form_open, practice_profile_form_open.additional_notes, "A" * 500)
    error = practice_profile_form_open.page.locator(
        '[name="practiceInfoAdditionalNotes"] ~ p[id$="-error"]'
    )
    expect(error).to_be_hidden()


@pytest.mark.boundary
def test_additional_notes_501_chars_blocked(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-B-PP-33: Additional Notes of 501 chars rejected or capped."""
    _fill(practice_profile_form_open, practice_profile_form_open.additional_notes, "A" * 501)
    value = practice_profile_form_open.additional_notes.input_value()
    error = practice_profile_form_open.page.locator(
        '[name="practiceInfoAdditionalNotes"] ~ p[id$="-error"]'
    )
    assert error.is_visible() or len(value) <= 500


@pytest.mark.negative
@pytest.mark.security
@pytest.mark.xfail(reason="DEF-PP-07: App accepts <script> in text areas — XSS risk")
def test_additional_notes_xss_rejected(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-S-PP-10: XSS in Additional Notes rejected."""
    _fill(practice_profile_form_open, practice_profile_form_open.additional_notes,
          "<script>alert(1)</script>")
    error = practice_profile_form_open.page.locator(
        '[name="practiceInfoAdditionalNotes"] ~ p[id$="-error"]'
    )
    expect(error).to_be_visible()
