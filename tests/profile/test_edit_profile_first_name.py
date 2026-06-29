"""
tests/profile/test_edit_profile_first_name.py — Phase 2

Covers all First Name validation rules from the Decision Report:
  R-FN-1  Required
  R-FN-2  Min 2 characters
  R-FN-3  Max 50 characters
  R-FN-4  Letters, spaces, hyphens, apostrophes only
  R-FN-5  No consecutive special characters
  R-FN-6  Must start and end with a letter

Test suites: Negative · Boundary · Usability · Regression
"""

import pytest
from playwright.sync_api import expect

from pages.profile_page import ProfilePage
from test_data.profile_data import ERR, FIRST_NAME_INVALID, FIRST_NAME_VALID


# ===========================================================================
# Helpers
# ===========================================================================

def _open_and_fill(profile_page: ProfilePage, value: str) -> None:
    """Open Edit modal, fill First Name, blur to trigger validation."""
    profile_page.open_edit_modal()
    profile_page.first_name_input.clear()
    profile_page.first_name_input.fill(value)
    profile_page.first_name_input.press("Tab")


# ===========================================================================
# TC-N — Negative: invalid inputs show correct inline error
# ===========================================================================

@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.parametrize("test_id, value, error_key", FIRST_NAME_INVALID)
def test_first_name_invalid_shows_error(
    profile_page: ProfilePage,
    test_id: str,
    value: str,
    error_key: str,
) -> None:
    """
    TC-N-P-FN-*: Every invalid First Name input shows the correct error after blur.

    Requirements: R-FN-1 (required) · R-FN-2 (min) · R-FN-3 (max) ·
                  R-FN-4 (chars) · R-FN-5 (consecutive) · R-FN-6 (start/end)
    """
    expected = ERR[error_key]
    _open_and_fill(profile_page, value)
    expect(profile_page.first_name_error).to_be_visible()
    expect(profile_page.first_name_error).to_contain_text(expected)




# ===========================================================================
# TC-B — Boundary: exact min and max values
# ===========================================================================

@pytest.mark.boundary
def test_first_name_exact_min_2_chars_accepted(profile_page: ProfilePage) -> None:
    """TC-B-P-FN-01: Exactly 2 characters is the minimum valid First Name."""
    _open_and_fill(profile_page, "Jo")
    expect(profile_page.first_name_error).to_be_hidden()


@pytest.mark.boundary
def test_first_name_1_char_triggers_min_error(profile_page: ProfilePage) -> None:
    """TC-B-P-FN-02: 1 character (one below min) triggers min-length error."""
    _open_and_fill(profile_page, "J")
    expect(profile_page.first_name_error).to_contain_text(ERR["fn_min"])


@pytest.mark.boundary
def test_first_name_exact_max_50_chars_accepted(profile_page: ProfilePage) -> None:
    """TC-B-P-FN-03: Exactly 50 characters is the maximum valid First Name."""
    _open_and_fill(profile_page, "A" * 50)
    expect(profile_page.first_name_error).to_be_hidden()


@pytest.mark.boundary
def test_first_name_51_chars_triggers_max_error(profile_page: ProfilePage) -> None:
    """TC-B-P-FN-04: 51 characters (one above max) triggers max-length error."""
    _open_and_fill(profile_page, "A" * 51)
    expect(profile_page.first_name_error).to_contain_text(ERR["fn_max"])


# ===========================================================================
# TC-F — Functional: valid inputs produce no error
# ===========================================================================

@pytest.mark.functional
@pytest.mark.parametrize("test_id, value", FIRST_NAME_VALID)
def test_first_name_valid_no_error(
    profile_page: ProfilePage,
    test_id: str,
    value: str,
) -> None:
    """TC-F-P-FN-*: Valid First Name values produce no inline error after blur."""
    _open_and_fill(profile_page, value)
    expect(profile_page.first_name_error).to_be_hidden()


@pytest.mark.functional
@pytest.mark.smoke
def test_first_name_valid_saves_and_updates_card(profile_page: ProfilePage) -> None:
    """
    TC-F-P-FN-01 (submit): Saving a valid First Name shows success toast.

    Uses a value different from the current one to ensure Save is enabled.
    """
    profile_page.open_edit_modal()
    current = profile_page.first_name_input.input_value()
    new_value = "Lara" if current.strip() != "Lara" else "Reem"

    profile_page.first_name_input.click(click_count=3)
    profile_page.first_name_input.fill(new_value)

    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


# ===========================================================================
# TC-U — Usability: error recovery
# ===========================================================================

@pytest.mark.usability
def test_first_name_error_clears_when_corrected(profile_page: ProfilePage) -> None:
    """
    TC-U-P-FN-01: Inline error disappears when First Name is corrected.

    Steps: type invalid → blur → error shown → type valid → blur → error gone.
    """
    profile_page.open_edit_modal()

    # Trigger error
    profile_page.first_name_input.clear()
    profile_page.first_name_input.fill("Reem123")
    profile_page.first_name_input.press("Tab")
    expect(profile_page.first_name_error).to_contain_text(ERR["fn_chars"])

    # Correct the value
    profile_page.first_name_input.clear()
    profile_page.first_name_input.fill("Reem")
    profile_page.first_name_input.press("Tab")
    expect(profile_page.first_name_error).to_be_hidden()


@pytest.mark.usability
def test_first_name_cancel_discards_invalid_state(profile_page: ProfilePage) -> None:
    """
    TC-U-P-FN-02: Cancelling with invalid First Name closes modal without saving.
    """
    profile_page.open_edit_modal()
    profile_page.first_name_input.clear()
    profile_page.first_name_input.fill("Reem123")
    profile_page.first_name_input.press("Tab")
    expect(profile_page.first_name_error).to_be_visible()

    profile_page.cancel_edit()
    profile_page.assert_modal_is_closed()


# ===========================================================================
# TC-R — Regression
# ===========================================================================

@pytest.mark.regression
def test_first_name_fix_invalid_then_save_succeeds(profile_page: ProfilePage) -> None:
    """
    TC-R-P-FN-01: Fix an invalid First Name → Save succeeds.

    Verifies no stale error state remains after correction.
    """
    profile_page.open_edit_modal()

    # Trigger error
    profile_page.first_name_input.clear()
    profile_page.first_name_input.fill("Reem123")
    profile_page.first_name_input.press("Tab")
    expect(profile_page.first_name_error).to_contain_text(ERR["fn_chars"])

    # Fix and save
    profile_page.first_name_input.clear()
    profile_page.first_name_input.fill("Sara")
    profile_page.first_name_input.press("Tab")
    expect(profile_page.first_name_error).to_be_hidden()

    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


@pytest.mark.regression
def test_first_name_no_error_on_valid_submit(profile_page: ProfilePage) -> None:
    """
    TC-R-P-FN-02: No stale error shown when submitting after valid entry.
    """
    profile_page.open_edit_modal()
    current = profile_page.first_name_input.input_value()
    new_value = "Nour" if current.strip() != "Nour" else "Reem"

    profile_page.first_name_input.click(click_count=3)
    profile_page.first_name_input.fill(new_value)
    expect(profile_page.first_name_error).to_be_hidden()

    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
