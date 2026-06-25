"""
tests/profile/test_add_user_username.py — Phase 3

Covers Add User form — Username validation:
  R-UN-1  Required
  R-UN-2  Min 3 chars, max 30 chars
  R-UN-3  Lowercase letters, numbers, hyphens, underscores, dots only
  R-UN-4  No consecutive special characters
  R-UN-5  Must start and end with letter or number
  R-UN-6  Must be unique (duplicate check)

⚠️  FIELD CONFIRMED: #username input exists in the Add New User panel.
    Selector: [aria-label="Add New User"] #username
"""

import pytest
from playwright.sync_api import expect, Locator

from pages.profile_page import ProfilePage
from test_data.profile_data import ERR, USERNAME_INVALID, USERNAME_VALID


# ===========================================================================
# Helpers
# ===========================================================================

def _get_username_error(profile_page: ProfilePage) -> Locator:
    """Return the error locator for the username field in Add User panel."""
    return profile_page.page.locator(
        '[aria-label="Add New User"] #username + p'
    )


def _open_and_fill_username(profile_page: ProfilePage, value: str) -> None:
    """Open Add User panel, fill username field, blur."""
    profile_page.open_add_user_form()
    profile_page.add_user_username_input.fill(value)
    profile_page.add_user_username_input.press("Tab")


# ===========================================================================
# TC-F — Functional: valid usernames accepted
# ===========================================================================

@pytest.mark.functional
@pytest.mark.parametrize("test_id, value", USERNAME_VALID)
def test_username_valid_no_error(
    profile_page: ProfilePage,
    test_id: str,
    value: str,
) -> None:
    """TC-F-P-UN-*: Valid username values produce no inline error after blur."""
    _open_and_fill_username(profile_page, value)
    expect(_get_username_error(profile_page)).to_be_hidden()
    profile_page.cancel_add_user()


# ===========================================================================
# TC-N — Negative: invalid usernames show correct error
# ===========================================================================

@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", USERNAME_INVALID)
def test_username_invalid_shows_error(
    profile_page: ProfilePage,
    test_id: str,
    value: str,
    error_key: str,
) -> None:
    """
    TC-N-P-UN-*: Every invalid username shows the correct inline error.

    Covers: R-UN-1 (required) · R-UN-2 (min/max) · R-UN-3 (chars) ·
            R-UN-4 (consecutive) · R-UN-5 (start/end)
    """
    _open_and_fill_username(profile_page, value)
    err_locator = _get_username_error(profile_page)
    expect(err_locator).to_be_visible()
    expect(err_locator).to_contain_text(ERR[error_key])
    profile_page.cancel_add_user()


@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", USERNAME_INVALID)
def test_username_invalid_blocks_submit(
    profile_page: ProfilePage,
    test_id: str,
    value: str,
    error_key: str,
) -> None:
    """
    TC-N-P-UN-* (submit): Submit must be disabled when username is invalid.
    """
    _open_and_fill_username(profile_page, value)
    expect(profile_page.add_user_submit_button).to_be_disabled()
    profile_page.cancel_add_user()


# ===========================================================================
# TC-B — Boundary
# ===========================================================================

@pytest.mark.boundary
def test_username_exact_min_3_chars_accepted(profile_page: ProfilePage) -> None:
    """TC-B-P-UN-01: Exactly 3 characters is the minimum valid username."""
    _open_and_fill_username(profile_page, "abc")
    expect(_get_username_error(profile_page)).to_be_hidden()
    profile_page.cancel_add_user()


@pytest.mark.boundary
def test_username_2_chars_triggers_min_error(profile_page: ProfilePage) -> None:
    """TC-B-P-UN-02: 2 characters (one below min) triggers min-length error."""
    _open_and_fill_username(profile_page, "ab")
    expect(_get_username_error(profile_page)).to_contain_text(ERR["un_min"])
    profile_page.cancel_add_user()


@pytest.mark.boundary
def test_username_exact_max_30_chars_accepted(profile_page: ProfilePage) -> None:
    """TC-B-P-UN-04: Exactly 30 characters is the maximum valid username."""
    _open_and_fill_username(profile_page, "a" * 30)
    expect(_get_username_error(profile_page)).to_be_hidden()
    profile_page.cancel_add_user()


@pytest.mark.boundary
def test_username_31_chars_triggers_max_error(profile_page: ProfilePage) -> None:
    """TC-B-P-UN-05: 31 characters (one above max) triggers max-length error."""
    _open_and_fill_username(profile_page, "a" * 31)
    expect(_get_username_error(profile_page)).to_contain_text(ERR["un_max"])
    profile_page.cancel_add_user()


# ===========================================================================
# TC-R — Regression
# ===========================================================================

@pytest.mark.regression
def test_username_error_clears_when_corrected(profile_page: ProfilePage) -> None:
    """
    TC-R-P-UN-01: Inline error disappears when username is corrected.
    """
    profile_page.open_add_user_form()
    err_locator = _get_username_error(profile_page)

    # Trigger error
    profile_page.add_user_username_input.fill("UPPERCASE")
    profile_page.add_user_username_input.press("Tab")
    expect(err_locator).to_contain_text(ERR["un_chars"])

    # Fix
    profile_page.add_user_username_input.clear()
    profile_page.add_user_username_input.fill("validuser")
    profile_page.add_user_username_input.press("Tab")
    expect(err_locator).to_be_hidden()

    profile_page.cancel_add_user()


@pytest.mark.regression
@pytest.mark.security
def test_username_xss_payload_rejected(profile_page: ProfilePage) -> None:
    """
    TC-S-P-UN-01: XSS payload in username is rejected by char validation (R-UN-3).

    Security: the app must never accept script-injection characters in username.
    """
    _open_and_fill_username(profile_page, "<script>alert(1)</script>")
    expect(_get_username_error(profile_page)).to_be_visible()
    expect(_get_username_error(profile_page)).to_contain_text(ERR["un_chars"])
    profile_page.cancel_add_user()


# ===========================================================================
# Auto-cleanup fixture — prevents cascade failures
# ===========================================================================

@pytest.fixture(autouse=True)
def close_any_open_panel(profile_page: ProfilePage):
    """Guarantee no modal is left open after each test."""
    yield
    try:
        if profile_page.add_user_modal.is_visible():
            profile_page.add_user_cancel_button.click()
    except Exception:
        pass
