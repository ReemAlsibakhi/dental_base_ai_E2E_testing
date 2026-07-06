"""
tests/practice_profile/test_practice_address.py — Phase 3

Address fields: Street (PP·R8), City (PP·R9), State (PP·R10),
                ZIP (PP·R11), Timezone (PP·R12)
"""

import pytest
from playwright.sync_api import expect

from pages.practice_profile_page import PracticeProfilePage
from test_data.practice_profile_data import (
    PP_ERR,
    STREET_MIN_VALID, STREET_MIN_INVALID, STREET_MAX_VALID, STREET_MAX_INVALID,
    CITY_MIN_VALID, CITY_MIN_INVALID, CITY_MAX_VALID, CITY_MAX_INVALID,
    ZIP_VALID_5, ZIP_VALID_PLUS4, ZIP_INVALID_4, ZIP_INVALID_PLUS4, ZIP_INVALID_ALPHA,
)


def _fill(pp, locator, value):
    locator.scroll_into_view_if_needed()
    locator.clear()
    locator.fill(value)
    locator.press("Tab")
    pp.page.wait_for_timeout(300)


# ===========================================================================
# STREET (PP·R8)
# ===========================================================================

@pytest.mark.negative
def test_street_empty_shows_required(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.street_input, "")
    expect(practice_profile_form_open.street_error).to_be_visible()
    expect(practice_profile_form_open.street_error).to_contain_text("required")


@pytest.mark.negative
def test_street_whitespace_shows_required(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.street_input, "   ")
    expect(practice_profile_form_open.street_error).to_contain_text("required")


@pytest.mark.negative
def test_street_xss_rejected(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.street_input, "<script>alert(1)</script>")
    expect(practice_profile_form_open.street_error).to_be_visible()


@pytest.mark.boundary
def test_street_min_5_chars_accepted(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.street_input, STREET_MIN_VALID)
    expect(practice_profile_form_open.street_error).to_be_hidden()


@pytest.mark.boundary
def test_street_4_chars_triggers_min_error(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.street_input, STREET_MIN_INVALID)
    expect(practice_profile_form_open.street_error).to_be_visible()


@pytest.mark.boundary
def test_street_max_200_chars_accepted(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.street_input, STREET_MAX_VALID)
    expect(practice_profile_form_open.street_error).to_be_hidden()


@pytest.mark.boundary
def test_street_201_chars_triggers_max_error(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.street_input, STREET_MAX_INVALID)
    error_visible = practice_profile_form_open.street_error.is_visible()
    field_capped  = len(practice_profile_form_open.street_input.input_value()) <= 200
    assert error_visible or field_capped


# ===========================================================================
# CITY (PP·R9)
# ===========================================================================

@pytest.mark.negative
def test_city_empty_shows_required(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.city_input, "")
    expect(practice_profile_form_open.city_error).to_contain_text("required")


@pytest.mark.negative
def test_city_whitespace_shows_required(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.city_input, "   ")
    expect(practice_profile_form_open.city_error).to_contain_text("required")


@pytest.mark.negative
def test_city_xss_rejected(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.city_input, "<script>")
    expect(practice_profile_form_open.city_error).to_be_visible()


@pytest.mark.boundary
def test_city_min_2_chars_accepted(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.city_input, CITY_MIN_VALID)
    expect(practice_profile_form_open.city_error).to_be_hidden()


@pytest.mark.boundary
def test_city_1_char_triggers_min_error(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.city_input, CITY_MIN_INVALID)
    expect(practice_profile_form_open.city_error).to_be_visible()


@pytest.mark.boundary
def test_city_max_100_chars_accepted(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.city_input, CITY_MAX_VALID)
    expect(practice_profile_form_open.city_error).to_be_hidden()


@pytest.mark.boundary
def test_city_101_chars_triggers_max_error(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.city_input, CITY_MAX_INVALID)
    error_visible = practice_profile_form_open.city_error.is_visible()
    field_capped  = len(practice_profile_form_open.city_input.input_value()) <= 100
    assert error_visible or field_capped


# ===========================================================================
# ZIP (PP·R11)
# ===========================================================================

@pytest.mark.negative
def test_zip_empty_shows_required(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.zip_input, "")
    expect(practice_profile_form_open.zip_error).to_contain_text("required")


@pytest.mark.negative
def test_zip_letters_rejected(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.zip_input, ZIP_INVALID_ALPHA)
    expect(practice_profile_form_open.zip_error).to_be_visible()


@pytest.mark.boundary
def test_zip_5_digits_accepted(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.zip_input, ZIP_VALID_5)
    expect(practice_profile_form_open.zip_error).to_be_hidden()


@pytest.mark.boundary
def test_zip_4_digits_triggers_error(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.zip_input, ZIP_INVALID_4)
    expect(practice_profile_form_open.zip_error).to_be_visible()


@pytest.mark.boundary
def test_zip_plus4_format_accepted(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.zip_input, ZIP_VALID_PLUS4)
    expect(practice_profile_form_open.zip_error).to_be_hidden()


@pytest.mark.boundary
def test_zip_plus4_incomplete_rejected(practice_profile_form_open: PracticeProfilePage) -> None:
    _fill(practice_profile_form_open, practice_profile_form_open.zip_input, ZIP_INVALID_PLUS4)
    expect(practice_profile_form_open.zip_error).to_be_visible()


# ===========================================================================
# STATE + TIMEZONE (PP·R10/R12) — dropdowns required
# ===========================================================================

@pytest.mark.negative
def test_state_has_value_by_default(practice_profile_form_open: PracticeProfilePage) -> None:
    """State dropdown must have a selection — verified it is not empty."""
    practice_profile_form_open.state_select.scroll_into_view_if_needed()
    value = practice_profile_form_open.state_select.input_value()
    assert value != "", "State dropdown should have a default value"


@pytest.mark.negative
def test_timezone_has_value_by_default(practice_profile_form_open: PracticeProfilePage) -> None:
    """Timezone dropdown must have a selection."""
    practice_profile_form_open.timezone_select.scroll_into_view_if_needed()
    value = practice_profile_form_open.timezone_select.input_value()
    assert value != "", "Timezone dropdown should have a default value"
