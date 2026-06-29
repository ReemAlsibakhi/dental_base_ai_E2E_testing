"""
tests/profile/test_add_user_email.py — Phase 3

Add User panel opens ONCE via add_user_panel_open fixture.
Tests that require submit/cancel use function-scoped profile_page.

Rules:
  R-AU-EM-1  Email required
  R-AU-EM-2  Valid email format
  R-AU-EM-3  Not already a member (duplicate)
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
# Helper — fill email and blur (panel already open)
# ===========================================================================

def _fill(pp: ProfilePage, value: str) -> None:
    pp.add_user_email_input.clear()
    pp.add_user_email_input.fill(value)
    pp.add_user_email_input.press("Tab")
    pp.page.wait_for_timeout(300)


# ===========================================================================
# TC-N — Negative (panel stays open)
# ===========================================================================

@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", ADD_USER_EMAIL_INVALID)
def test_add_user_invalid_email_shows_error(
    add_user_panel_open: ProfilePage,
    test_id: str,
    value: str,
    error_key: str,
) -> None:
    """TC-N-P-AU-01 to 04: Invalid email shows correct error after blur."""
    _fill(add_user_panel_open, value)
    expect(add_user_panel_open.add_user_email_error).to_be_visible(timeout=5_000)
    expect(add_user_panel_open.add_user_email_error).to_contain_text(ERR[error_key])


# ===========================================================================
# TC-F — Functional (panel stays open)
# ===========================================================================

@pytest.mark.functional
def test_add_user_valid_email_no_error(
    add_user_panel_open: ProfilePage,
) -> None:
    """TC-F-P-AU-01: Valid email produces no inline error."""
    _fill(add_user_panel_open, ADD_USER_EMAIL_VALID)
    expect(add_user_panel_open.add_user_email_error).to_be_hidden()


# ===========================================================================
# TC-B — Boundary (panel stays open)
# ===========================================================================

@pytest.mark.boundary
def test_add_user_email_254_chars_accepted(
    add_user_panel_open: ProfilePage,
) -> None:
    """TC-B-P-AU-EM-01: Exactly 254 chars (RFC 5321 max) accepted."""
    _fill(add_user_panel_open, ADD_USER_EMAIL_MAX_VALID)
    expect(add_user_panel_open.add_user_email_error).to_be_hidden()


@pytest.mark.boundary
def test_add_user_email_255_chars_rejected(
    add_user_panel_open: ProfilePage,
) -> None:
    """TC-B-P-AU-EM-02: 255 chars (one above max) rejected."""
    _fill(add_user_panel_open, ADD_USER_EMAIL_MAX_INVALID)
    expect(add_user_panel_open.add_user_email_error).to_be_visible(timeout=5_000)


# ===========================================================================
# TC-U + TC-N-duplicate + TC-R — these open/close panel themselves
# ===========================================================================

@pytest.mark.usability
def test_add_user_cancel_closes_form(profile_page: ProfilePage) -> None:
    """TC-U-P-AU-01: Cancel closes panel, user count unchanged."""
    initial_count = profile_page.get_user_count_number()
    profile_page.open_add_user_form()
    profile_page.add_user_email_input.fill(ADD_USER_EMAIL_VALID)
    profile_page.cancel_add_user()
    profile_page.assert_add_user_modal_closed()
    assert profile_page.get_user_count_number() == initial_count


@pytest.mark.usability
def test_add_user_error_clears_when_corrected(profile_page: ProfilePage) -> None:
    """TC-U-P-AU-02: Error clears when valid email replaces invalid."""
    profile_page.open_add_user_form()

    profile_page.add_user_email_input.fill("notanemail")
    profile_page.add_user_email_input.press("Tab")
    profile_page.page.wait_for_timeout(300)
    expect(profile_page.add_user_email_error).to_contain_text(ERR["au_email_format"])

    profile_page.add_user_email_input.clear()
    profile_page.add_user_email_input.fill(ADD_USER_EMAIL_VALID)
    profile_page.add_user_email_input.press("Tab")
    profile_page.page.wait_for_timeout(300)
    expect(profile_page.add_user_email_error).to_be_hidden()
    profile_page.cancel_add_user()


@pytest.mark.negative
def test_add_user_duplicate_email_blocked(profile_page: ProfilePage) -> None:
    """TC-N-P-AU-05: Duplicate email shows 'already a member' error."""
    profile_page.open_add_user_form()
    profile_page.add_user_email_input.fill(ADD_USER_DUPLICATE_EMAIL)
    profile_page.add_user_submit_button.click()
    profile_page.page.wait_for_timeout(500)
    expect(profile_page.add_user_email_error).to_contain_text(ERR["au_email_duplicate"])
    profile_page.cancel_add_user()


@pytest.mark.regression
def test_add_user_fix_invalid_then_submit_enabled(profile_page: ProfilePage) -> None:
    """TC-R-P-AU-01: Fixing invalid email re-enables Submit button."""
    profile_page.open_add_user_form()

    profile_page.add_user_email_input.fill("bademail")
    profile_page.add_user_email_input.press("Tab")
    profile_page.page.wait_for_timeout(300)

    profile_page.add_user_email_input.clear()
    profile_page.add_user_email_input.fill(ADD_USER_EMAIL_VALID)
    profile_page.add_user_email_input.press("Tab")
    profile_page.page.wait_for_timeout(300)
    expect(profile_page.add_user_email_error).to_be_hidden()
    expect(profile_page.add_user_submit_button).to_be_enabled(timeout=5_000)
    profile_page.cancel_add_user()
