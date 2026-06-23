"""
tests/profile/test_account_users_view_all.py

Covers: TC-F-P-VA-*, TC-S-P-VA-*, TC-R-P-VA-*
Rules: R-VA-1 (View All displays complete user list with correct columns)
"""

import pytest
from playwright.sync_api import expect

from pages.profile_page import ProfilePage
from test_data.profile_data import ADD_USER_EMAIL_VALID


# ===========================================================================
# TC-F | Functional
# ===========================================================================

@pytest.mark.functional
def test_view_all_opens_complete_user_list(profile_page: ProfilePage) -> None:
    """TC-F-P-VA-01: View All shows list with name, email, role, status columns."""
    profile_page.open_view_all()
    expect(profile_page.view_all_modal).to_be_visible()
    # At least one user row must be visible
    expect(profile_page.view_all_user_rows.first).to_be_visible()
    # TODO: add column-level assertions once selectors for columns are confirmed


@pytest.mark.functional
def test_view_all_count_matches_account_users_card(profile_page: ProfilePage) -> None:
    """TC-F-P-VA-02: Row count in View All equals the 'N users with access' count."""
    card_count = profile_page.get_user_count_number()
    profile_page.open_view_all()
    row_count = profile_page.get_view_all_row_count()
    assert row_count == card_count, (
        f"View All shows {row_count} rows but card says {card_count} users"
    )


# ===========================================================================
# TC-S | Security
# ===========================================================================

@pytest.mark.security
def test_non_admin_cannot_access_view_all(profile_page_non_admin: ProfilePage) -> None:
    """TC-S-P-VA-01: Non-admin cannot see or click View All (RBAC)."""
    profile_page_non_admin.assert_hidden(profile_page_non_admin.view_all_button)


# ===========================================================================
# TC-R | Regression
# ===========================================================================

@pytest.mark.regression
def test_name_in_view_all_updates_after_profile_name_change(profile_page: ProfilePage) -> None:
    """TC-R-P-VA-01: Changing name in Edit Profile is reflected in View All immediately."""
    new_last = "Hassan"

    # Change the Last Name
    profile_page.open_edit_modal()
    profile_page.edit_last_name(new_last, blur=False)
    profile_page.save_and_assert_success()

    # Open View All and verify the current user row reflects the new name
    profile_page.open_view_all()
    expect(profile_page.page.get_by_text(new_last)).to_be_visible()
