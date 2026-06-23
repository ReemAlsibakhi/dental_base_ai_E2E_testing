"""
tests/profile/test_edit_profile_last_name.py

Covers: TC-F-P-LN-*, TC-N-P-LN-*, TC-B-P-LN-*, TC-U-P-LN-*, TC-R-P-LN-*
Rules: R-LN-1 through R-LN-6
"""

import pytest
from pages.profile_page import ProfilePage
from test_data.profile_data import ERR, LAST_NAME_VALID, LAST_NAME_INVALID


# ===========================================================================
# TC-F | Functional — Valid inputs accepted
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.parametrize("test_id, value", LAST_NAME_VALID)
def test_last_name_valid_accepted(profile_page: ProfilePage, test_id: str, value: str) -> None:
    """Valid Last Names produce no inline error after blur."""
    profile_page.open_edit_modal()
    profile_page.edit_last_name(value, blur=True)
    profile_page.assert_no_last_name_error()


@pytest.mark.functional
@pytest.mark.smoke
def test_last_name_save_updates_profile_card(profile_page: ProfilePage) -> None:
    """TC-F-P-LN-01 (submit): Saving a valid Last Name updates the profile card."""
    profile_page.open_edit_modal()
    profile_page.edit_last_name("Hassan", blur=False)
    profile_page.save_and_assert_success()
    profile_page.assert_full_name_on_card("Hassan")


# ===========================================================================
# TC-N | Negative — Invalid inputs
# ===========================================================================

@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", LAST_NAME_INVALID)
def test_last_name_invalid_shows_inline_error(
    profile_page: ProfilePage, test_id: str, value: str, error_key: str
) -> None:
    """TC-N-P-LN-* — Invalid last name shows correct error after blur."""
    profile_page.open_edit_modal()
    profile_page.edit_last_name(value, blur=True)
    profile_page.assert_last_name_error(ERR[error_key])


@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", LAST_NAME_INVALID)
def test_last_name_invalid_blocks_save(
    profile_page: ProfilePage, test_id: str, value: str, error_key: str
) -> None:
    """TC-N-P-LN-* (submit): Save is blocked when Last Name is invalid."""
    profile_page.open_edit_modal()
    profile_page.edit_last_name(value, blur=True)
    profile_page.assert_save_blocked()


# ===========================================================================
# TC-U | Usability
# ===========================================================================

@pytest.mark.usability
def test_last_name_error_clears_after_correction(profile_page: ProfilePage) -> None:
    """TC-U-P-LN-01: Error clears when Last Name corrected."""
    profile_page.open_edit_modal()

    profile_page.edit_last_name("Smith99", blur=True)
    profile_page.assert_last_name_error(ERR["ln_chars"])

    profile_page.edit_last_name("Smith", blur=True)
    profile_page.assert_no_last_name_error()


# ===========================================================================
# TC-R | Regression
# ===========================================================================

@pytest.mark.regression
def test_last_name_fix_then_save(profile_page: ProfilePage) -> None:
    """TC-R-P-LN-01: Fix invalid Last Name → save succeeds."""
    profile_page.open_edit_modal()

    profile_page.edit_last_name("Hassan@1", blur=True)
    profile_page.assert_last_name_error(ERR["ln_chars"])

    profile_page.edit_last_name("Hassan", blur=True)
    profile_page.assert_no_last_name_error()
    profile_page.save_and_assert_success()
    profile_page.assert_full_name_on_card("Hassan")


@pytest.mark.regression
def test_last_name_cross_form_validation(profile_page: ProfilePage) -> None:
    """TC-R-P-LN-CROSS-01: Last Name validates identically in Add User form."""
    profile_page.open_add_user_form()

    cases = [
        ("Smith99", ERR["ln_chars"]),
        ("Al--Hassan", ERR["ln_consecutive"]),
        ("-Hassan", ERR["ln_leading"]),
    ]
    for value, expected_error in cases:
        profile_page.add_user_last_name_input.clear()
        profile_page.add_user_last_name_input.fill(value)
        profile_page.add_user_last_name_input.press("Tab")
        profile_page.assert_last_name_error(expected_error)
