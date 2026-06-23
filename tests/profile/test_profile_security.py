"""
tests/profile/test_profile_security.py

Covers: TC-S-P-SES-01, TC-S-P-SES-02
Rules: Auth / Session · RBAC
"""

import pytest
from playwright.sync_api import expect, Page

from pages.profile_page import ProfilePage
from pages.login_page import LoginPage


# ===========================================================================
# TC-S | Security — Session
# ===========================================================================

@pytest.mark.security
def test_settings_not_accessible_after_logout(admin_page: Page) -> None:
    """TC-S-P-SES-01: After logout, navigating back to /settings redirects to login.

    The browser Back button / direct URL must not render settings to a
    logged-out user.
    """
    admin_page.goto("/settings")
    admin_page.wait_for_load_state("networkidle")

    # TODO: Replace with the actual logout button/link selector
    admin_page.locator('[data-testid="logout-btn"]').click()   # TODO
    admin_page.wait_for_url("**/login**")

    # Attempt to go back
    admin_page.go_back()
    # Must be redirected to login, not render settings
    expect(admin_page).to_have_url(
        lambda url: "/login" in url or "/settings" not in url
    )


@pytest.mark.security
def test_non_admin_edit_button_absent(profile_page_non_admin: ProfilePage) -> None:
    """TC-S-P-SES-02: Non-admin cannot see or use the Edit Profile button."""
    profile_page_non_admin.assert_hidden(profile_page_non_admin.edit_profile_button)


# ===========================================================================
# Additional — Email field is read-only (DEF-P-02 gap coverage)
# ===========================================================================

@pytest.mark.functional
def test_email_field_not_editable_in_edit_modal(profile_page: ProfilePage) -> None:
    """Gap from coverage matrix: email read-only — no edit cursor in modal.

    The email is displayed on the profile card but must not appear as an
    editable field inside the Edit Profile modal.
    """
    profile_page.open_edit_modal()
    # Email input must NOT be present in the modal
    email_in_modal = profile_page.page.locator('[data-testid="email-input"]')  # TODO
    expect(email_in_modal).to_be_hidden()
