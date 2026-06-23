"""
tests/profile/test_add_user.py

Covers: TC-F-P-AU-*, TC-N-P-AU-*, TC-U-P-AU-*, TC-S-P-AU-*, TC-R-P-AU-*
Rules: R-AU-EM-1 (Required) · R-AU-EM-2 (Format) · R-AU-EM-3 (Not duplicate)
"""

import pytest
from playwright.sync_api import expect

from pages.profile_page import ProfilePage
from test_data.profile_data import (
    ERR,
    ADD_USER_EMAIL_VALID,
    ADD_USER_EMAIL_INVALID,
    ADD_USER_DUPLICATE_EMAIL,
)


# ===========================================================================
# TC-F | Functional
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
def test_add_user_valid_email_accepted(profile_page: ProfilePage) -> None:
    """TC-F-P-AU-01: Valid email in Add User triggers invitation flow."""
    profile_page.open_add_user_form()
    profile_page.add_user_email_input.fill(ADD_USER_EMAIL_VALID)
    profile_page.add_user_submit_button.click()
    # Expect success: modal closes OR success message shown
    # TODO: adjust assertion to match the actual success state
    profile_page.assert_add_user_modal_closed()


# ===========================================================================
# TC-N | Negative — Email validation
# ===========================================================================

@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", ADD_USER_EMAIL_INVALID)
def test_add_user_invalid_email_shows_error(
    profile_page: ProfilePage, test_id: str, value: str, error_key: str
) -> None:
    """TC-N-P-AU-01/02/03/04: Invalid email format shows inline error."""
    profile_page.open_add_user_form()
    profile_page.add_user_email_input.fill(value)
    profile_page.add_user_email_input.press("Tab")
    profile_page.assert_add_user_email_error(ERR[error_key])


@pytest.mark.negative
def test_add_user_duplicate_email_blocked(profile_page: ProfilePage) -> None:
    """TC-N-P-AU-05: Email belonging to existing member triggers 'already a member' error."""
    profile_page.open_add_user_form()
    profile_page.add_user_email_input.fill(ADD_USER_DUPLICATE_EMAIL)
    profile_page.add_user_submit_button.click()
    profile_page.assert_add_user_email_error(ERR["au_email_duplicate"])


# ===========================================================================
# TC-U | Usability
# ===========================================================================

@pytest.mark.usability
def test_add_user_cancel_closes_form_no_invite(profile_page: ProfilePage) -> None:
    """TC-U-P-AU-01: Cancelling Add User form sends no invitation."""
    initial_count = profile_page.get_user_count_number()

    profile_page.open_add_user_form()
    profile_page.add_user_email_input.fill("newuser@test.com")
    profile_page.cancel_add_user()

    profile_page.assert_add_user_modal_closed()
    # Count must remain the same — no invitation was sent
    assert profile_page.get_user_count_number() == initial_count


@pytest.mark.usability
def test_add_user_count_increments_after_success(profile_page: ProfilePage) -> None:
    """TC-U-P-AU-02: User count on Account Users card increments immediately after Add User."""
    initial_count = profile_page.get_user_count_number()

    profile_page.open_add_user_form()
    profile_page.add_user_email_input.fill(ADD_USER_EMAIL_VALID)
    profile_page.add_user_submit_button.click()
    profile_page.assert_add_user_modal_closed()

    new_count = profile_page.get_user_count_number()
    assert new_count == initial_count + 1, (
        f"Expected count {initial_count + 1}, got {new_count}"
    )


# ===========================================================================
# TC-S | Security
# ===========================================================================

@pytest.mark.security
def test_non_admin_cannot_see_add_user_button(profile_page_non_admin: ProfilePage) -> None:
    """TC-S-P-AU-01: Non-admin user does not see the Add User button (RBAC)."""
    profile_page_non_admin.assert_hidden(profile_page_non_admin.add_user_button)


# ===========================================================================
# TC-R | Regression
# ===========================================================================

@pytest.mark.regression
def test_added_user_appears_in_view_all(profile_page: ProfilePage) -> None:
    """TC-R-P-AU-01: New user appears in View All immediately (no reload)."""
    profile_page.open_add_user_form()
    profile_page.add_user_email_input.fill(ADD_USER_EMAIL_VALID)
    profile_page.add_user_submit_button.click()
    profile_page.assert_add_user_modal_closed()

    profile_page.open_view_all()
    # The invited email should appear in the list
    expect(profile_page.page.get_by_text(ADD_USER_EMAIL_VALID)).to_be_visible()


@pytest.mark.regression
def test_first_name_validates_identically_in_add_user(profile_page: ProfilePage) -> None:
    """TC-R-P-FN-CROSS-01: First Name rules identical in Add User and Edit Profile."""
    profile_page.open_add_user_form()

    cross_cases = [
        ("Reem123", ERR["fn_chars"]),
        ("Mary--Jane", ERR["fn_consecutive"]),
        ("-Reem", ERR["fn_leading"]),
    ]
    for value, expected_error in cross_cases:
        profile_page.add_user_first_name_input.clear()
        profile_page.add_user_first_name_input.fill(value)
        profile_page.add_user_first_name_input.press("Tab")
        # Reuse the shared error locator — error text is identical to Edit Profile
        profile_page.assert_first_name_error(expected_error)
