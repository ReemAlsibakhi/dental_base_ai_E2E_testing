"""
tests/profile/test_add_user.py — Phase 3

Covers Add User form — Email validation:
  R-AU-EM-1  Email required
  R-AU-EM-2  Valid email format
  R-AU-EM-3  No duplicate (not already a member)
  R-AU-EM-4  Maximum 254 characters (RFC 5321)
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
# Auto-cleanup: close any open panel after each test
# ===========================================================================

@pytest.fixture(autouse=True)
def close_any_open_panel(profile_page: ProfilePage):
    """Guarantee no modal is left open after each test — prevents cascade failures."""
    yield
    # Close Add User panel if still open
    try:
        if profile_page.add_user_modal.is_visible():
            profile_page.add_user_cancel_button.click()
    except Exception:
        pass
    # Close Edit panel if still open
    try:
        if profile_page.edit_modal.is_visible():
            profile_page.close_panel_button.click()
    except Exception:
        pass


# ===========================================================================
# Helpers
# ===========================================================================

def _open_and_fill_email(profile_page: ProfilePage, value: str) -> None:
    """Open Add User panel, fill email field, press Tab to trigger validation."""
    profile_page.open_add_user_form()
    profile_page.add_user_email_input.fill(value)
    profile_page.add_user_email_input.press("Tab")
    # Small wait for validation to render
    profile_page.page.wait_for_timeout(300)


# ===========================================================================
# TC-F — Functional
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
def test_add_user_form_opens_successfully(profile_page: ProfilePage) -> None:
    """TC-F-P-AU-00: Add User panel opens and shows email field."""
    profile_page.open_add_user_form()
    expect(profile_page.add_user_email_input).to_be_visible()


@pytest.mark.functional
def test_add_user_valid_email_no_error(profile_page: ProfilePage) -> None:
    """TC-F-P-AU-01: Valid email format produces no inline error after blur."""
    _open_and_fill_email(profile_page, ADD_USER_EMAIL_VALID)
    expect(profile_page.add_user_email_error).to_be_hidden()


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
    """
    expected = ERR[error_key]
    _open_and_fill_email(profile_page, value)
    expect(profile_page.add_user_email_error).to_be_visible(timeout=5_000)
    expect(profile_page.add_user_email_error).to_contain_text(expected)


@pytest.mark.negative
def test_add_user_duplicate_email_blocked(profile_page: ProfilePage) -> None:
    """
    TC-N-P-AU-05: Submitting an email already in the system shows 'already a member'.
    """
    profile_page.open_add_user_form()
    profile_page.add_user_email_input.fill(ADD_USER_DUPLICATE_EMAIL)
    profile_page.add_user_submit_button.click()
    profile_page.page.wait_for_timeout(500)
    expect(profile_page.add_user_email_error).to_contain_text(
        ERR["au_email_duplicate"]
    )


# ===========================================================================
# TC-B — Boundary: RFC 5321 email max length
# ===========================================================================

@pytest.mark.boundary
def test_add_user_email_254_chars_accepted(profile_page: ProfilePage) -> None:
    """TC-B-P-AU-EM-01: Email of exactly 254 chars (RFC 5321 max) is accepted."""
    _open_and_fill_email(profile_page, ADD_USER_EMAIL_MAX_VALID)
    expect(profile_page.add_user_email_error).to_be_hidden()


@pytest.mark.boundary
def test_add_user_email_255_chars_rejected(profile_page: ProfilePage) -> None:
    """TC-B-P-AU-EM-02: Email of 255 chars (one above RFC max) is rejected."""
    _open_and_fill_email(profile_page, ADD_USER_EMAIL_MAX_INVALID)
    expect(profile_page.add_user_email_error).to_be_visible(timeout=5_000)


# ===========================================================================
# TC-U — Usability
# ===========================================================================

@pytest.mark.usability
def test_add_user_cancel_closes_form(profile_page: ProfilePage) -> None:
    """
    TC-U-P-AU-01: Cancelling Add User form closes the panel.
    User count must remain unchanged (no invite sent).
    """
    initial_count = profile_page.get_user_count_number()

    profile_page.open_add_user_form()
    profile_page.add_user_email_input.fill(ADD_USER_EMAIL_VALID)
    profile_page.cancel_add_user()

    profile_page.assert_add_user_modal_closed()
    assert profile_page.get_user_count_number() == initial_count


@pytest.mark.usability
def test_add_user_error_clears_when_email_corrected(profile_page: ProfilePage) -> None:
    """TC-U-P-AU-02: Inline error clears when a valid email replaces the invalid one."""
    profile_page.open_add_user_form()

    # Trigger error
    profile_page.add_user_email_input.fill("notanemail")
    profile_page.add_user_email_input.press("Tab")
    profile_page.page.wait_for_timeout(300)
    expect(profile_page.add_user_email_error).to_contain_text(ERR["au_email_format"])

    # Fix
    profile_page.add_user_email_input.clear()
    profile_page.add_user_email_input.fill(ADD_USER_EMAIL_VALID)
    profile_page.add_user_email_input.press("Tab")
    profile_page.page.wait_for_timeout(300)
    expect(profile_page.add_user_email_error).to_be_hidden()


# ===========================================================================
# TC-R — Regression
# ===========================================================================

@pytest.mark.regression
def test_add_user_fix_invalid_then_submit_enabled(profile_page: ProfilePage) -> None:
    """TC-R-P-AU-01: Correcting an invalid email re-enables the Submit button."""
    profile_page.open_add_user_form()

    profile_page.add_user_email_input.fill("bademail")
    profile_page.add_user_email_input.press("Tab")
    profile_page.page.wait_for_timeout(300)
    expect(profile_page.add_user_submit_button).to_be_disabled()

    profile_page.add_user_email_input.clear()
    profile_page.add_user_email_input.fill(ADD_USER_EMAIL_VALID)
    profile_page.add_user_email_input.press("Tab")
    profile_page.page.wait_for_timeout(300)
    expect(profile_page.add_user_email_error).to_be_hidden()
    expect(profile_page.add_user_submit_button).to_be_enabled(timeout=5_000)
