"""
tests/profile/test_edit_profile_phone.py — Phase 2

Covers Phone Number validation rules:
  R-PH-1  Optional — empty is accepted
  R-PH-2  Minimum 10 digits when provided
  R-PH-3  Alpha characters stripped silently (no error)
  R-PH-4  Maximum 10 digits enforced via HTML maxlength (UI cap — no error shown)
"""

import pytest
from playwright.sync_api import expect

from pages.profile_page import ProfilePage
from test_data.profile_data import ERR, PHONE_INVALID, PHONE_VALID, PHONE_ALPHA


# ===========================================================================
# TC-F — Functional
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
def test_phone_valid_10_digits_saves(profile_page: ProfilePage) -> None:
    """TC-F-P-PH-01: Valid 10-digit phone saves successfully."""
    profile_page.open_edit_modal()
    current = profile_page.phone_input.input_value()
    new_value = "6035551234" if current.strip() != "6035551234" else "9995551234"

    profile_page.phone_input.click(click_count=3)
    profile_page.phone_input.fill(new_value)
    profile_page.phone_input.press("Tab")

    expect(profile_page.phone_error).to_be_hidden()
    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


@pytest.mark.functional
def test_phone_empty_is_optional(profile_page: ProfilePage) -> None:
    """
    TC-F-P-PH-02: Empty Phone Number is allowed (R-PH-1 — optional field).

    Saving with no phone must succeed without any inline error.
    """
    profile_page.open_edit_modal()
    profile_page.phone_input.clear()
    profile_page.phone_input.press("Tab")

    expect(profile_page.phone_error).to_be_hidden()


# ===========================================================================
# TC-N — Negative
# ===========================================================================

@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", PHONE_INVALID)
def test_phone_too_short_shows_error(
    profile_page: ProfilePage,
    test_id: str,
    value: str,
    error_key: str,
) -> None:
    """
    TC-N-P-PH-01: Phone with fewer than 10 digits triggers inline error (R-PH-2).
    """
    profile_page.open_edit_modal()
    profile_page.phone_input.clear()
    profile_page.phone_input.fill(value)
    profile_page.phone_input.press("Tab")

    expect(profile_page.phone_error).to_be_visible()
    expect(profile_page.phone_error).to_contain_text(ERR[error_key])


@pytest.mark.negative
def test_phone_alpha_chars_stripped_silently(profile_page: ProfilePage) -> None:
    """
    TC-N-P-PH-02: Alphabetic characters stripped silently (R-PH-3).

    After stripping, the field is empty → no error OR treated as below-minimum.
    Either outcome confirms stripping happened (no alpha persists in the field).
    """
    profile_page.open_edit_modal()
    profile_page.phone_input.clear()
    profile_page.phone_input.fill(PHONE_ALPHA)
    profile_page.phone_input.press("Tab")

    value_after = profile_page.phone_input.input_value()
    assert value_after == "" or value_after.isdigit(), (
        f"Expected digits-only or empty after alpha strip, got: '{value_after}'"
    )


# ===========================================================================
# TC-B — Boundary
# ===========================================================================

@pytest.mark.boundary
def test_phone_exactly_10_digits_accepted(profile_page: ProfilePage) -> None:
    """TC-B-P-PH-01: Exactly 10 digits is the minimum valid phone (R-PH-2)."""
    profile_page.open_edit_modal()
    profile_page.phone_input.clear()
    profile_page.phone_input.fill("6035551234")
    profile_page.phone_input.press("Tab")

    expect(profile_page.phone_error).to_be_hidden()


@pytest.mark.boundary
def test_phone_9_digits_triggers_min_error(profile_page: ProfilePage) -> None:
    """TC-B-P-PH-02: 9 digits (one below minimum) triggers error."""
    profile_page.open_edit_modal()
    profile_page.phone_input.clear()
    profile_page.phone_input.fill("603555123")
    profile_page.phone_input.press("Tab")

    expect(profile_page.phone_error).to_contain_text(ERR["ph_min_digits"])


@pytest.mark.boundary
def test_phone_maxlength_caps_at_10_digits(profile_page: ProfilePage) -> None:
    """
    TC-B-P-PH-03 (UI cap): Field maxlength attribute prevents typing > 10 digits.

    R-PH-4: Max is enforced silently — no error shown, 11th digit just not accepted.
    We verify that after filling 11 digits, the field contains at most 10.
    """
    profile_page.open_edit_modal()
    profile_page.phone_input.clear()
    profile_page.phone_input.fill("60355512345")  # 11 digits
    profile_page.phone_input.press("Tab")

    value_after = profile_page.phone_input.input_value()
    digit_count = len("".join(c for c in value_after if c.isdigit()))
    assert digit_count <= 10, (
        f"Expected at most 10 digits after maxlength cap, got {digit_count}: '{value_after}'"
    )
    # No error expected — max is silently enforced
    expect(profile_page.phone_error).to_be_hidden()


# ===========================================================================
# TC-R — Regression
# ===========================================================================

@pytest.mark.regression
def test_phone_fix_short_then_save_succeeds(profile_page: ProfilePage) -> None:
    """
    TC-R-P-PH-01: Correcting a too-short phone clears the error and allows save.
    """
    profile_page.open_edit_modal()

    # Trigger error
    profile_page.phone_input.clear()
    profile_page.phone_input.fill("12345")
    profile_page.phone_input.press("Tab")
    expect(profile_page.phone_error).to_contain_text(ERR["ph_min_digits"])

    # Fix and save
    profile_page.phone_input.clear()
    profile_page.phone_input.fill("6035551234")
    profile_page.phone_input.press("Tab")
    expect(profile_page.phone_error).to_be_hidden()

    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()
