"""
tests/profile/test_edit_profile_last_name.py — Phase 2

Covers all Last Name validation rules:
  R-LN-1  Required
  R-LN-2  Min 2 characters
  R-LN-3  Max 50 characters
  R-LN-4  Letters, spaces, hyphens, apostrophes only
  R-LN-5  No consecutive special characters
  R-LN-6  Must start and end with a letter

Cross-form note: Last Name applies identical rules in both
Edit Profile modal AND Add User form (TC-R-P-LN-CROSS-01).
"""

import pytest
from playwright.sync_api import expect

from pages.profile_page import ProfilePage
from test_data.profile_data import ERR, LAST_NAME_INVALID, LAST_NAME_VALID


# ===========================================================================
# Helpers
# ===========================================================================

def _open_and_fill(profile_page: ProfilePage, value: str) -> None:
    profile_page.open_edit_modal()
    profile_page.last_name_input.clear()
    profile_page.last_name_input.fill(value)
    profile_page.last_name_input.press("Tab")


# ===========================================================================
# TC-N — Negative: invalid inputs show correct inline error
# ===========================================================================

@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.parametrize("test_id, value, error_key", LAST_NAME_INVALID)
def test_last_name_invalid_shows_error(
    profile_page: ProfilePage,
    test_id: str,
    value: str,
    error_key: str,
) -> None:
    """
    TC-N-P-LN-*: Every invalid Last Name shows the correct error after blur.

    Requirements: R-LN-1 · R-LN-2 · R-LN-3 · R-LN-4 · R-LN-5 · R-LN-6
    """
    expected = ERR[error_key]
    _open_and_fill(profile_page, value)
    expect(profile_page.last_name_error).to_be_visible()
    expect(profile_page.last_name_error).to_contain_text(expected)




# ===========================================================================
# TC-B — Boundary
# ===========================================================================

@pytest.mark.boundary
def test_last_name_exact_min_2_chars_accepted(profile_page: ProfilePage) -> None:
    """TC-B-P-LN-01: Exactly 2 characters is the minimum valid Last Name."""
    _open_and_fill(profile_page, "Li")
    expect(profile_page.last_name_error).to_be_hidden()


@pytest.mark.boundary
def test_last_name_1_char_triggers_min_error(profile_page: ProfilePage) -> None:
    """TC-B-P-LN-02: 1 character triggers min-length error."""
    _open_and_fill(profile_page, "L")
    expect(profile_page.last_name_error).to_contain_text(ERR["ln_min"])


@pytest.mark.boundary
def test_last_name_exact_max_50_chars_accepted(profile_page: ProfilePage) -> None:
    """TC-B-P-LN-03: Exactly 50 characters is the maximum valid Last Name."""
    _open_and_fill(profile_page, "B" * 50)
    expect(profile_page.last_name_error).to_be_hidden()


@pytest.mark.boundary
def test_last_name_51_chars_triggers_max_error(profile_page: ProfilePage) -> None:
    """TC-B-P-LN-04: 51 characters triggers max-length error."""
    _open_and_fill(profile_page, "B" * 51)
    expect(profile_page.last_name_error).to_contain_text(ERR["ln_max"])


# ===========================================================================
# TC-F — Functional: valid inputs produce no error
# ===========================================================================

@pytest.mark.functional
@pytest.mark.parametrize("test_id, value", LAST_NAME_VALID)
def test_last_name_valid_no_error(
    profile_page: ProfilePage,
    test_id: str,
    value: str,
) -> None:
    """TC-F-P-LN-*: Valid Last Name values produce no inline error after blur."""
    _open_and_fill(profile_page, value)
    expect(profile_page.last_name_error).to_be_hidden()


@pytest.mark.functional
@pytest.mark.smoke
def test_last_name_valid_saves_successfully(profile_page: ProfilePage) -> None:
    """TC-F-P-LN-01 (submit): Saving a valid Last Name shows success toast."""
    profile_page.open_edit_modal()
    current = profile_page.last_name_input.input_value()
    new_value = "Hassan" if current.strip() != "Hassan" else "Sibakhi"

    profile_page.last_name_input.click(click_count=3)
    profile_page.last_name_input.fill(new_value)

    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


# ===========================================================================
# TC-U — Usability: error recovery
# ===========================================================================

@pytest.mark.usability
def test_last_name_error_clears_when_corrected(profile_page: ProfilePage) -> None:
    """
    TC-U-P-LN-01: Inline error disappears when Last Name is corrected.
    """
    profile_page.open_edit_modal()

    profile_page.last_name_input.clear()
    profile_page.last_name_input.fill("Smith99")
    profile_page.last_name_input.press("Tab")
    expect(profile_page.last_name_error).to_contain_text(ERR["ln_chars"])

    profile_page.last_name_input.clear()
    profile_page.last_name_input.fill("Smith")
    profile_page.last_name_input.press("Tab")
    expect(profile_page.last_name_error).to_be_hidden()


@pytest.mark.usability
def test_last_name_cancel_discards_invalid_state(profile_page: ProfilePage) -> None:
    """
    TC-U-P-LN-02: Cancelling with invalid Last Name closes modal without saving.
    """
    profile_page.open_edit_modal()
    profile_page.last_name_input.clear()
    profile_page.last_name_input.fill("Smith99")
    profile_page.last_name_input.press("Tab")
    expect(profile_page.last_name_error).to_be_visible()

    profile_page.cancel_edit()
    profile_page.assert_modal_is_closed()


# ===========================================================================
# TC-R — Regression
# ===========================================================================

@pytest.mark.regression
def test_last_name_fix_invalid_then_save_succeeds(profile_page: ProfilePage) -> None:
    """
    TC-R-P-LN-01: Fix an invalid Last Name → Save succeeds with no stale error.
    """
    profile_page.open_edit_modal()

    profile_page.last_name_input.clear()
    profile_page.last_name_input.fill("Hassan@1")
    profile_page.last_name_input.press("Tab")
    expect(profile_page.last_name_error).to_contain_text(ERR["ln_chars"])

    profile_page.last_name_input.clear()
    profile_page.last_name_input.fill("Hassan")
    profile_page.last_name_input.press("Tab")
    expect(profile_page.last_name_error).to_be_hidden()

    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


@pytest.mark.regression
def test_last_name_validates_same_in_add_user_form(profile_page: ProfilePage) -> None:
    """
    TC-R-P-LN-CROSS-01: Last Name rules are identical in Add User form.

    Verifies that the same validation logic is applied consistently
    across both the Edit Profile modal and the Add User panel.
    """
    profile_page.open_add_user_form()

    cross_cases = [
        ("Smith99",    ERR["ln_chars"]),
        ("Al--Hassan", ERR["ln_consecutive"]),
        ("-Hassan",    ERR["ln_start_end"]),
    ]

    for value, expected_error in cross_cases:
        profile_page.add_user_last_name_input.clear()
        profile_page.add_user_last_name_input.fill(value)
        profile_page.add_user_last_name_input.press("Tab")
        expect(profile_page.add_user_last_name_input.locator(
            "xpath=following-sibling::p"
        )).to_contain_text(expected_error)

    profile_page.cancel_add_user()
