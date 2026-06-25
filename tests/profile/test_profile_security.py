"""
tests/profile/test_profile_security.py — Phase 3

Covers RBAC and session security tests:
  TC-S-P-SES-02  Non-admin cannot access Edit Profile button
  TC-S-P-AU-01   Non-admin cannot see Add User button
  TC-S-P-VA-01   Non-admin cannot see View All button
  TC-S-P-SES-03  Email field is read-only in Edit Profile modal
  TC-S-P-SES-04  Edit modal does not expose sensitive fields beyond name/phone

NOTE: TC-S-P-SES-01 (back button after logout) is Manual — see Decision Report.
NOTE: Non-admin tests use profile_page_non_admin fixture which requires
      NON_ADMIN_EMAIL and NON_ADMIN_PASSWORD in .env to be configured.
      Tests will be skipped if non-admin credentials are not provided.
"""

import pytest
from playwright.sync_api import expect, Page

from pages.profile_page import ProfilePage


# ===========================================================================
# TC-S — RBAC: Non-admin restrictions
# ===========================================================================

@pytest.mark.security
def test_non_admin_cannot_see_edit_button(
    profile_page_non_admin: ProfilePage,
) -> None:
    """
    TC-S-P-SES-02: Non-admin user does not see the Edit Profile button.

    The Edit button is an admin-only action. A non-admin loading /settings
    must never see a way to modify profile information.
    """
    expect(profile_page_non_admin.edit_profile_button).to_be_hidden()


@pytest.mark.security
def test_non_admin_cannot_see_add_user_button(
    profile_page_non_admin: ProfilePage,
) -> None:
    """
    TC-S-P-AU-01: Non-admin user does not see the Add User button (RBAC).

    Only admins can invite new users. The Add User button must be hidden
    for non-admin roles.
    """
    expect(profile_page_non_admin.add_user_button).to_be_hidden()


@pytest.mark.security
def test_non_admin_cannot_see_view_all_button(
    profile_page_non_admin: ProfilePage,
) -> None:
    """
    TC-S-P-VA-01: Non-admin user cannot see or access the View All button.
    """
    expect(profile_page_non_admin.view_all_button).to_be_hidden()


# ===========================================================================
# TC-S — Edit modal field security
# ===========================================================================

@pytest.mark.security
@pytest.mark.functional
def test_email_field_not_editable_in_edit_modal(profile_page: ProfilePage) -> None:
    """
    TC-S-P-SES-03: Email is read-only — no email input exists in Edit Profile modal.

    Email is a Keycloak-managed field. The Edit Profile modal must not
    expose an editable email input — doing so could allow account takeover.
    """
    profile_page.open_edit_modal()

    # No editable email input should exist inside the modal
    email_input_in_modal = profile_page.page.locator(
        '[role="dialog"][aria-label="Edit Profile"] input[type="email"]'
    )
    expect(email_input_in_modal).to_be_hidden()

    # Verify only the expected fields exist: first_name, last_name, phone_number
    visible_inputs = profile_page.page.locator(
        '[role="dialog"][aria-label="Edit Profile"] input:visible'
    )
    # Should be 3 inputs max: first name, last name, phone
    count = visible_inputs.count()
    assert count <= 3, (
        f"Expected at most 3 visible inputs in Edit modal, found {count}. "
        "An unexpected field may be exposed."
    )

    profile_page.cancel_edit()


@pytest.mark.security
def test_edit_modal_contains_expected_fields_only(profile_page: ProfilePage) -> None:
    """
    TC-S-P-SES-04: Edit Profile modal exposes only first_name, last_name, phone_number.

    Verifies the modal does not accidentally expose admin-only or sensitive fields
    such as role, status, or practice_name.
    """
    profile_page.open_edit_modal()

    modal = profile_page.page.locator('[role="dialog"][aria-label="Edit Profile"]')

    # These fields MUST be present
    expect(modal.locator('#first_name')).to_be_visible()
    expect(modal.locator('#last_name')).to_be_visible()
    expect(modal.locator('#phone_number')).to_be_visible()

    # These fields MUST NOT be present
    for forbidden in ['#role', '#status', '#practice_name', '#email']:
        expect(modal.locator(forbidden)).to_be_hidden()

    profile_page.cancel_edit()


# ===========================================================================
# TC-S — Settings page access control
# ===========================================================================

@pytest.mark.security
def test_settings_page_accessible_to_admin(admin_page: Page) -> None:
    """
    TC-S-P-SES-05: Admin can access /settings and sees Profile Information card.
    """
    admin_page.goto("/settings", wait_until="commit")
    expect(admin_page.locator("text=Profile Information")).to_be_visible(timeout=15_000)


@pytest.mark.security
def test_settings_page_accessible_to_non_admin(
    profile_page_non_admin: ProfilePage,
) -> None:
    """
    TC-S-P-SES-06: Non-admin can view /settings but with restricted actions.

    Non-admin should see their profile info but not edit/admin controls.
    """
    # Page loads without error
    expect(profile_page_non_admin.page.locator(
        "text=Profile Information"
    )).to_be_visible(timeout=15_000)
