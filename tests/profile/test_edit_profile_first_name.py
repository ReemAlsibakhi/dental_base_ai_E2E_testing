"""
tests/profile/test_edit_profile_first_name.py

Covers: TC-F-P-FN-*, TC-N-P-FN-*, TC-B-P-FN-*, TC-U-P-FN-*, TC-R-P-FN-*
Rules: R-FN-1 through R-FN-6
"""

import pytest
from playwright.sync_api import expect

from pages.profile_page import ProfilePage
from test_data.profile_data import ERR, FIRST_NAME_VALID, FIRST_NAME_INVALID


# ---------------------------------------------------------------------------
# Helper to open the modal once per parameterised set
# ---------------------------------------------------------------------------

def _open_modal(profile_page: ProfilePage) -> None:
    profile_page.open_edit_modal()


# ===========================================================================
# TC-F | Functional — Valid inputs accepted
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.parametrize("test_id, value", FIRST_NAME_VALID)
def test_first_name_valid_accepted(profile_page: ProfilePage, test_id: str, value: str) -> None:
    """TC-F-P-FN-01 through FN-07 + boundary valid cases.

    Each valid First Name should produce no inline error after blur.
    """
    _open_modal(profile_page)
    profile_page.edit_first_name(value, blur=True)
    profile_page.assert_no_first_name_error()


@pytest.mark.functional
@pytest.mark.smoke
def test_first_name_save_updates_profile_card(profile_page: ProfilePage) -> None:
    """TC-F-P-FN-01 (submit): Saving a valid First Name updates the profile card.

    Maps to: TC-F-P-FN-01 (submit assertion)
    """
    new_name = "Lara"
    _open_modal(profile_page)
    profile_page.edit_first_name(new_name, blur=False)
    profile_page.save_and_assert_success()
    profile_page.assert_full_name_on_card(new_name)


# ===========================================================================
# TC-N | Negative — Invalid inputs show correct errors
# ===========================================================================

@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", FIRST_NAME_INVALID)
def test_first_name_invalid_shows_inline_error(
    profile_page: ProfilePage, test_id: str, value: str, error_key: str
) -> None:
    """TC-N-P-FN-* — Invalid first name shows the correct inline error after blur.

    Covers: empty, whitespace, min length, max length, disallowed chars,
            consecutive specials, leading/trailing specials.
    """
    expected_error = ERR[error_key]
    _open_modal(profile_page)
    profile_page.edit_first_name(value, blur=True)
    profile_page.assert_first_name_error(expected_error)


@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", FIRST_NAME_INVALID)
def test_first_name_invalid_blocks_save(
    profile_page: ProfilePage, test_id: str, value: str, error_key: str
) -> None:
    """TC-N-P-FN-* (submit): Save is blocked when First Name is invalid."""
    _open_modal(profile_page)
    profile_page.edit_first_name(value, blur=True)
    profile_page.assert_save_blocked()


# ===========================================================================
# TC-U | Usability — Error recovery
# ===========================================================================

@pytest.mark.usability
def test_first_name_error_clears_after_correction(profile_page: ProfilePage) -> None:
    """TC-U-P-FN-01: Error disappears when First Name is corrected.

    Steps: invalid → blur → error shown → correct → blur → error gone.
    """
    _open_modal(profile_page)

    # Trigger error
    profile_page.edit_first_name("Reem123", blur=True)
    profile_page.assert_first_name_error(ERR["fn_chars"])

    # Correct it
    profile_page.edit_first_name("Reem", blur=True)
    profile_page.assert_no_first_name_error()


@pytest.mark.usability
def test_first_name_error_clears_on_valid_unicode(profile_page: ProfilePage) -> None:
    """TC-U-P-FN-02: Unicode input (Arabic) accepted; any prior error clears."""
    _open_modal(profile_page)
    profile_page.edit_first_name("Reem123", blur=True)
    profile_page.assert_first_name_error(ERR["fn_chars"])

    profile_page.edit_first_name("رنا", blur=True)
    profile_page.assert_no_first_name_error()


# ===========================================================================
# TC-R | Regression
# ===========================================================================

@pytest.mark.regression
def test_first_name_fix_then_save_succeeds(profile_page: ProfilePage) -> None:
    """TC-R-P-FN-01: Fix invalid First Name then save — succeeds with no stale error."""
    _open_modal(profile_page)

    # Enter invalid
    profile_page.edit_first_name("Reem123", blur=True)
    profile_page.assert_first_name_error(ERR["fn_chars"])

    # Fix and save
    profile_page.edit_first_name("Reem", blur=True)
    profile_page.assert_no_first_name_error()
    profile_page.save_and_assert_success()
    profile_page.assert_full_name_on_card("Reem")


@pytest.mark.regression
def test_first_name_change_updates_full_name_card(profile_page: ProfilePage) -> None:
    """TC-R-P-FN-02: Profile card Full Name updates immediately after save (no reload)."""
    _open_modal(profile_page)
    profile_page.edit_first_name("Lara", blur=False)
    profile_page.save_and_assert_success()

    # Verify card updated without page navigation
    profile_page.assert_full_name_on_card("Lara")
    # TODO: also assert sidebar username if the sidebar shows the name
