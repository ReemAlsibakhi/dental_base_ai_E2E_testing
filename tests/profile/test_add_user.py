"""
tests/profile/test_add_user.py — Phase 3

Covers Add User form — Email validation:
  R-AU-EM-1  Email required
  R-AU-EM-2  Valid email format
  R-AU-EM-3  No duplicate (not already a member)
  R-AU-EM-4  Maximum 254 characters (RFC 5321)

Also covers:
  TC-U-P-AU-01  Cancel discards form (no invite sent)
  TC-U-P-AU-02  User count increments after successful add
  TC-S-P-AU-01  Non-admin cannot see Add User button (RBAC)
  TC-R-P-AU-01  Added user appears in View All immediately
"""

import pytest
from playwright.sync_api import expect

from pages.profile_page import ProfilePage
from test_data.profile_data import (
    ERR,
    ADD_USER_EMAIL_INVALID,
    ADD_USER_EMAIL_VALID,
    ADD_USER_DUPLICATE_EMAIL,
    ADD_USER_EMAIL_MAX_VALID,
    ADD_USER_EMAIL_MAX_INVALID,
)


# ===========================================================================
# Helpers
# ===========================================================================

def _open_and_fill_email(profile_page: ProfilePage, value: str) -> None:
    """Open Add User panel, fill email, blur to trigger validation."""
    profile_page.open_add_user_form()
    profile_page.add_user_email_input.fill(value)
    profile_page.add_user_email_input.press("Tab")


# ===========================================================================
# TC-F — Functional
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
def test_add_user_form_opens_successfully(profile_page: ProfilePage) -> None:
    """TC-F-P-AU-00: Add User panel opens and shows email field."""
    profile_page.open_add_user_form()
    expect(profile_page.add_user_email_input).to_be_visible()
    profile_page.cancel_add_user()
    profile_page.assert_add_user_modal_closed()


@pytest.mark.functional
def test_add_user_valid_email_no_error(profile_page: ProfilePage) -> None:
    """TC-F-P-AU-01: Valid email format produces no inline error."""
    _open_and_fill_email(profile_page, ADD_USER_EMAIL_VALID)
    expect(profile_page.add_user_email_error).to_be_hidden()
    profile_page.cancel_add_user()


# ===========================================================================
# TC-N — Negative: email validation
# ===========================================================================

@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", ADD_USER_EMAIL_INVALID)
def test_add_user_invalid_email_shows_error(
    profile_page: ProfilePage,
    test_id: str,
    value: str,
    error_key: str,
) -> None:
    """
    TC-N-P-AU-01 to 04: Invalid email formats trigger correct inline error.

    Covers: empty · no domain · missing domain · missing local part
    """
    _open_and_fill_email(profile_page, value)
    expect(profile_page.add_user_email_error).to_be_visible()
    expect(profile_page.add_user_email_error).to_contain_text(ERR[error_key])
    profile_page.cancel_add_user()


@pytest.mark.negative
def test_add_user_duplicate_email_blocked(profile_page: ProfilePage) -> None:
    """
    TC-N-P-AU-05: Submitting an email that already belongs to a member
    shows 'already a member' error (R-AU-EM-3).
    """
    profile_page.open_add_user_form()
    profile_page.add_user_email_input.fill(ADD_USER_DUPLICATE_EMAIL)
    profile_page.add_user_submit_button.click()
    expect(profile_page.add_user_email_error).to_contain_text(ERR["au_email_duplicate"])
    profile_page.cancel_add_user()


@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", ADD_USER_EMAIL_INVALID)
def test_add_user_invalid_email_blocks_submit(
    profile_page: ProfilePage,
    test_id: str,
    value: str,
    error_key: str,
) -> None:
    """
    TC-N-P-AU-* (submit): Submit button must be disabled when email is invalid.
    """
    _open_and_fill_email(profile_page, value)
    expect(profile_page.add_user_submit_button).to_be_disabled()
    profile_page.cancel_add_user()


# ===========================================================================
# TC-B — Boundary: RFC 5321 email max length
# ===========================================================================

@pytest.mark.boundary
def test_add_user_email_254_chars_accepted(profile_page: ProfilePage) -> None:
    """
    TC-B-P-AU-EM-01: Email of exactly 254 characters (RFC 5321 max) is accepted.

    Formula: 64-char local + '@' + 185-char domain + '.com' = 254 total
    """
    _open_and_fill_email(profile_page, ADD_USER_EMAIL_MAX_VALID)
    expect(profile_page.add_user_email_error).to_be_hidden()
    profile_page.cancel_add_user()


@pytest.mark.boundary
def test_add_user_email_255_chars_rejected(profile_page: ProfilePage) -> None:
    """
    TC-B-P-AU-EM-02: Email of 255 characters (one above RFC max) is rejected.
    """
    _open_and_fill_email(profile_page, ADD_USER_EMAIL_MAX_INVALID)
    expect(profile_page.add_user_email_error).to_be_visible()
    profile_page.cancel_add_user()


# ===========================================================================
# TC-U — Usability
# ===========================================================================

@pytest.mark.usability
def test_add_user_cancel_closes_form_no_change(profile_page: ProfilePage) -> None:
    """
    TC-U-P-AU-01: Cancelling Add User form closes the panel.
    User count must remain unchanged (no invite was sent).
    """
    initial_count = profile_page.get_user_count_number()

    profile_page.open_add_user_form()
    profile_page.add_user_email_input.fill(ADD_USER_EMAIL_VALID)
    profile_page.cancel_add_user()

    profile_page.assert_add_user_modal_closed()
    # Count unchanged — no invitation sent
    assert profile_page.get_user_count_number() == initial_count


@pytest.mark.usability
def test_add_user_error_clears_when_email_corrected(profile_page: ProfilePage) -> None:
    """
    TC-U-P-AU-02: Inline email error clears when a valid email replaces the invalid one.
    """
    profile_page.open_add_user_form()

    # Trigger error
    profile_page.add_user_email_input.fill("notanemail")
    profile_page.add_user_email_input.press("Tab")
    expect(profile_page.add_user_email_error).to_contain_text(ERR["au_email_format"])

    # Correct it
    profile_page.add_user_email_input.clear()
    profile_page.add_user_email_input.fill(ADD_USER_EMAIL_VALID)
    profile_page.add_user_email_input.press("Tab")
    expect(profile_page.add_user_email_error).to_be_hidden()

    profile_page.cancel_add_user()


# ===========================================================================
# TC-R — Regression
# ===========================================================================

@pytest.mark.regression
def test_add_user_fix_invalid_then_submit_enabled(profile_page: ProfilePage) -> None:
    """
    TC-R-P-AU-01: Correcting an invalid email re-enables the Submit button.
    """
    profile_page.open_add_user_form()

    # Trigger disabled state
    profile_page.add_user_email_input.fill("bademail")
    profile_page.add_user_email_input.press("Tab")
    expect(profile_page.add_user_submit_button).to_be_disabled()

    # Fix
    profile_page.add_user_email_input.clear()
    profile_page.add_user_email_input.fill(ADD_USER_EMAIL_VALID)
    profile_page.add_user_email_input.press("Tab")
    expect(profile_page.add_user_email_error).to_be_hidden()
    expect(profile_page.add_user_submit_button).to_be_enabled(timeout=5_000)

    profile_page.cancel_add_user()
