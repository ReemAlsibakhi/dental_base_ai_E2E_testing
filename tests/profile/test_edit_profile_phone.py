"""
tests/profile/test_edit_profile_phone.py

Covers: TC-F-P-PH-*, TC-N-P-PH-*, TC-B-P-PH-*, TC-R-P-PH-*
Rules: R-PH-1 (Optional) · R-PH-2 (Min 10 digits) · R-PH-3 (Digits only)
"""

import pytest
from playwright.sync_api import expect

from pages.profile_page import ProfilePage
from test_data.profile_data import ERR, PHONE_VALID, PHONE_INVALID, PHONE_ALPHA


# ===========================================================================
# TC-F | Functional
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
def test_phone_add_valid_number(profile_page: ProfilePage) -> None:
    """TC-F-P-PH-01: Adding a formatted phone number saves successfully."""
    profile_page.open_edit_modal()
    profile_page.edit_phone("(603) 555-1234", blur=False)
    profile_page.save_and_assert_success()
    # Profile card should show the formatted number (exact format may vary)
    expect(profile_page.phone_display).not_to_contain_text("No phone")


@pytest.mark.functional
def test_phone_empty_is_optional(profile_page: ProfilePage) -> None:
    """TC-F-P-PH-02: Saving with empty phone is allowed (R-PH-1)."""
    profile_page.open_edit_modal()
    profile_page.edit_phone("", blur=False)
    profile_page.save_and_assert_success()
    expect(profile_page.phone_display).to_contain_text("No phone")


# ===========================================================================
# TC-N | Negative
# ===========================================================================

@pytest.mark.negative
def test_phone_too_short_shows_error(profile_page: ProfilePage) -> None:
    """TC-N-P-PH-01: Phone with fewer than 10 digits triggers inline error."""
    profile_page.open_edit_modal()
    profile_page.edit_phone("12345", blur=True)
    profile_page.assert_phone_error(ERR["ph_min_digits"])


@pytest.mark.negative
def test_phone_alpha_chars_stripped(profile_page: ProfilePage) -> None:
    """TC-N-P-PH-02: Alphabetic characters are stripped (R-PH-3).

    After stripping, the field is effectively empty or triggers the min-digits
    error — both outcomes are acceptable per the spec.
    """
    profile_page.open_edit_modal()
    profile_page.edit_phone(PHONE_ALPHA, blur=True)

    # Acceptable outcomes: field is treated as empty (no error) OR shows min-digits error
    # The test confirms no data is accepted as-is
    value_after_strip = profile_page.phone_input.input_value()
    assert value_after_strip == "" or value_after_strip.isdigit(), (
        f"Expected digits or empty after alpha strip, got: '{value_after_strip}'"
    )


# ===========================================================================
# TC-B | Boundary
# ===========================================================================

@pytest.mark.boundary
def test_phone_exactly_10_digits_accepted(profile_page: ProfilePage) -> None:
    """TC-B-P-PH-01: Exactly 10 digits is the minimum valid phone number."""
    profile_page.open_edit_modal()
    profile_page.edit_phone("6035551234", blur=True)
    profile_page.assert_no_phone_error()
    profile_page.save_and_assert_success()


@pytest.mark.boundary
def test_phone_9_digits_blocked(profile_page: ProfilePage) -> None:
    """TC-B-P-PH-02: 9 digits (one below minimum) triggers error."""
    profile_page.open_edit_modal()
    profile_page.edit_phone("603555123", blur=True)
    profile_page.assert_phone_error(ERR["ph_min_digits"])


# ===========================================================================
# TC-R | Regression
# ===========================================================================

@pytest.mark.regression
def test_phone_fix_short_then_save(profile_page: ProfilePage) -> None:
    """TC-R-P-PH-01: Correcting a short phone clears error and allows save."""
    profile_page.open_edit_modal()

    profile_page.edit_phone("12345", blur=True)
    profile_page.assert_phone_error(ERR["ph_min_digits"])

    profile_page.edit_phone("6035551234", blur=True)
    profile_page.assert_no_phone_error()
    profile_page.save_and_assert_success()
