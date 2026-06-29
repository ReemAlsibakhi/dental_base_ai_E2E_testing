"""
tests/profile/test_edit_profile_phone.py — Phase 2 (optimised)

Modal opens ONCE via profile_page_modal_open fixture.
Tests that require save/cancel use function-scoped profile_page.

Rules:
  R-PH-1  Optional — empty accepted
  R-PH-2  Minimum 10 digits
  R-PH-3  Alpha chars stripped silently
  R-PH-4  Maximum 10 digits via maxlength (silent cap)
"""

import pytest
from playwright.sync_api import expect

from pages.profile_page import ProfilePage
from test_data.profile_data import ERR, PHONE_INVALID, PHONE_ALPHA


# ===========================================================================
# Helper — fill phone and blur (modal already open)
# ===========================================================================

def _fill(pp: ProfilePage, value: str) -> None:
    pp.phone_input.clear()
    pp.phone_input.fill(value)
    pp.phone_input.press("Tab")


# ===========================================================================
# TC-N — Negative (modal stays open)
# ===========================================================================

@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", PHONE_INVALID)
def test_phone_too_short_shows_error(
    profile_page_modal_open: ProfilePage,
    test_id: str,
    value: str,
    error_key: str,
) -> None:
    """TC-N-P-PH-01: Phone with fewer than 10 digits triggers inline error."""
    _fill(profile_page_modal_open, value)
    expect(profile_page_modal_open.phone_error).to_be_visible()
    expect(profile_page_modal_open.phone_error).to_contain_text(ERR[error_key])


@pytest.mark.negative
def test_phone_alpha_chars_stripped_silently(
    profile_page_modal_open: ProfilePage,
) -> None:
    """TC-N-P-PH-02: Alpha chars stripped silently — no alpha remains in field."""
    _fill(profile_page_modal_open, PHONE_ALPHA)
    value_after = profile_page_modal_open.phone_input.input_value()
    assert value_after == "" or value_after.isdigit(), (
        f"Expected digits-only or empty after alpha strip, got: '{value_after}'"
    )


# ===========================================================================
# TC-F — Functional (modal stays open)
# ===========================================================================

@pytest.mark.functional
def test_phone_empty_is_optional(
    profile_page_modal_open: ProfilePage,
) -> None:
    """TC-F-P-PH-02: Empty phone is allowed (R-PH-1 — optional)."""
    _fill(profile_page_modal_open, "")
    expect(profile_page_modal_open.phone_error).to_be_hidden()


# ===========================================================================
# TC-B — Boundary (modal stays open)
# ===========================================================================

@pytest.mark.boundary
def test_phone_exactly_10_digits_accepted(
    profile_page_modal_open: ProfilePage,
) -> None:
    """TC-B-P-PH-01: Exactly 10 digits — minimum valid."""
    _fill(profile_page_modal_open, "6035551234")
    expect(profile_page_modal_open.phone_error).to_be_hidden()


@pytest.mark.boundary
def test_phone_9_digits_triggers_min_error(
    profile_page_modal_open: ProfilePage,
) -> None:
    """TC-B-P-PH-02: 9 digits — one below minimum."""
    _fill(profile_page_modal_open, "603555123")
    expect(profile_page_modal_open.phone_error).to_contain_text(ERR["ph_min_digits"])


@pytest.mark.boundary
def test_phone_maxlength_caps_at_10_digits(
    profile_page_modal_open: ProfilePage,
) -> None:
    """TC-B-P-PH-03: 11 digits — field caps silently at 10 (R-PH-4)."""
    _fill(profile_page_modal_open, "60355512345")
    value_after = profile_page_modal_open.phone_input.input_value()
    digit_count = len("".join(c for c in value_after if c.isdigit()))
    assert digit_count <= 10, (
        f"Expected ≤10 digits after maxlength cap, got {digit_count}: '{value_after}'"
    )
    expect(profile_page_modal_open.phone_error).to_be_hidden()


# ===========================================================================
# TC-F (submit) + TC-R — these open/close modal themselves
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
def test_phone_valid_10_digits_saves(profile_page: ProfilePage) -> None:
    """TC-F-P-PH-01: Valid 10-digit phone saves successfully."""
    profile_page.open_edit_modal()
    current = profile_page.phone_input.input_value().strip()
    new_value = "6035551234" if current != "6035551234" else "9995551234"

    profile_page.phone_input.click(click_count=3)
    profile_page.phone_input.fill(new_value)
    profile_page.phone_input.press("Tab")

    expect(profile_page.phone_error).to_be_hidden()
    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


@pytest.mark.regression
def test_phone_fix_short_then_save_succeeds(profile_page: ProfilePage) -> None:
    """TC-R-P-PH-01: Fixing short phone clears error and allows save."""
    profile_page.open_edit_modal()

    profile_page.phone_input.clear()
    profile_page.phone_input.fill("12345")
    profile_page.phone_input.press("Tab")
    expect(profile_page.phone_error).to_contain_text(ERR["ph_min_digits"])

    profile_page.phone_input.clear()
    profile_page.phone_input.fill("6035551234")
    profile_page.phone_input.press("Tab")
    expect(profile_page.phone_error).to_be_hidden()

    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()
