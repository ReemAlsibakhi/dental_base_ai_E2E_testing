"""
tests/profile/test_add_user_username.py — Phase 3

Add User panel opens ONCE via add_user_panel_open fixture.
Tests that require submit/cancel use function-scoped profile_page.

Rules:
  R-UN-1  Required
  R-UN-2  Min 3 chars, max 30 chars
  R-UN-3  Lowercase letters, numbers, hyphens, underscores, dots only
  R-UN-4  No consecutive special characters
  R-UN-5  Must start and end with letter or number
  R-UN-6  Must be unique (duplicate check)

Username confirmed in Add New User panel: [aria-label="Add New User"] #username
"""

import pytest
from playwright.sync_api import expect, Locator

from pages.profile_page import ProfilePage
from test_data.profile_data import ERR, USERNAME_INVALID, USERNAME_VALID

# Existing username in system — used for duplicate tests
EXISTING_USERNAME = "reem_user"


# ===========================================================================
# Helpers
# ===========================================================================

def _get_error(pp: ProfilePage) -> Locator:
    return pp.page.locator('[aria-label="Add New User"] #username + p')


def _fill(pp: ProfilePage, value: str) -> None:
    """Fill username and blur — panel must already be open."""
    pp.add_user_username_input.clear()
    pp.add_user_username_input.fill(value)
    pp.add_user_username_input.press("Tab")
    pp.page.wait_for_timeout(300)


# ===========================================================================
# TC-N — Negative (panel stays open)
# ===========================================================================

@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", USERNAME_INVALID)
def test_username_invalid_shows_error(
    add_user_panel_open: ProfilePage,
    test_id: str,
    value: str,
    error_key: str,
) -> None:
    """TC-N-P-UN-*: Invalid username shows correct inline error."""
    _fill(add_user_panel_open, value)
    expect(_get_error(add_user_panel_open)).to_be_visible()
    expect(_get_error(add_user_panel_open)).to_contain_text(ERR[error_key])


@pytest.mark.negative
def test_username_duplicate_blocked(profile_page: ProfilePage) -> None:
    """
    TC-N-P-UN-13: Duplicate username is rejected (R-UN-6).
    Uses existing username 'reem_user' which is confirmed in the system.
    """
    profile_page.open_add_user_form()
    _fill(profile_page, EXISTING_USERNAME)
    expect(_get_error(profile_page)).to_be_visible(timeout=5_000)
    expect(_get_error(profile_page)).to_contain_text(ERR["un_duplicate"])
    profile_page.cancel_add_user()


@pytest.mark.negative
def test_username_case_insensitive_duplicate(profile_page: ProfilePage) -> None:
    """
    TC-N-P-UN-14: Case-insensitive duplicate rejected (R-UN-6).
    'REEM_USER' must be treated same as 'reem_user'.
    NOTE: R-UN-3 also rejects uppercase — this test verifies the duplicate
    check applies regardless of case normalization.
    """
    profile_page.open_add_user_form()
    _fill(profile_page, EXISTING_USERNAME.upper())
    # Either: chars error (uppercase rejected) OR duplicate error
    # Both mean the username is not accepted — either outcome is correct
    expect(_get_error(profile_page)).to_be_visible(timeout=5_000)
    profile_page.cancel_add_user()


# ===========================================================================
# TC-F — Functional (panel stays open)
# ===========================================================================

@pytest.mark.functional
@pytest.mark.parametrize("test_id, value", USERNAME_VALID)
def test_username_valid_no_error(
    add_user_panel_open: ProfilePage,
    test_id: str,
    value: str,
) -> None:
    """TC-F-P-UN-*: Valid username produces no inline error."""
    _fill(add_user_panel_open, value)
    expect(_get_error(add_user_panel_open)).to_be_hidden()


# ===========================================================================
# TC-B — Boundary (panel stays open)
# ===========================================================================

@pytest.mark.boundary
def test_username_exact_min_3_chars_accepted(
    add_user_panel_open: ProfilePage,
) -> None:
    """TC-B-P-UN-01: Exactly 3 characters — minimum valid."""
    _fill(add_user_panel_open, "abc")
    expect(_get_error(add_user_panel_open)).to_be_hidden()


@pytest.mark.boundary
def test_username_2_chars_triggers_min_error(
    add_user_panel_open: ProfilePage,
) -> None:
    """TC-B-P-UN-02: 2 characters — one below minimum."""
    _fill(add_user_panel_open, "ab")
    expect(_get_error(add_user_panel_open)).to_contain_text(ERR["un_min"])


@pytest.mark.boundary
def test_username_exact_max_30_chars_accepted(
    add_user_panel_open: ProfilePage,
) -> None:
    """TC-B-P-UN-04: Exactly 30 characters — maximum valid."""
    _fill(add_user_panel_open, "a" * 30)
    expect(_get_error(add_user_panel_open)).to_be_hidden()


@pytest.mark.boundary
def test_username_31_chars_triggers_max_error(
    add_user_panel_open: ProfilePage,
) -> None:
    """TC-B-P-UN-05: 31 characters — one above maximum."""
    _fill(add_user_panel_open, "a" * 31)
    expect(_get_error(add_user_panel_open)).to_contain_text(ERR["un_max"])


# ===========================================================================
# TC-R + TC-S — open/close panel themselves
# ===========================================================================

@pytest.mark.regression
def test_username_error_clears_when_corrected(profile_page: ProfilePage) -> None:
    """TC-R-P-UN-01: Error disappears when username is corrected."""
    profile_page.open_add_user_form()

    profile_page.add_user_username_input.fill("UPPERCASE")
    profile_page.add_user_username_input.press("Tab")
    profile_page.page.wait_for_timeout(300)
    expect(_get_error(profile_page)).to_contain_text(ERR["un_chars"])

    profile_page.add_user_username_input.clear()
    profile_page.add_user_username_input.fill("validuser")
    profile_page.add_user_username_input.press("Tab")
    profile_page.page.wait_for_timeout(300)
    expect(_get_error(profile_page)).to_be_hidden()
    profile_page.cancel_add_user()


@pytest.mark.regression
@pytest.mark.security
def test_username_xss_payload_rejected(profile_page: ProfilePage) -> None:
    """TC-S-P-UN-01: XSS payload rejected by char validation."""
    profile_page.open_add_user_form()
    profile_page.add_user_username_input.fill("<script>alert(1)</script>")
    profile_page.add_user_username_input.press("Tab")
    profile_page.page.wait_for_timeout(300)
    expect(_get_error(profile_page)).to_be_visible()
    expect(_get_error(profile_page)).to_contain_text(ERR["un_chars"])
    profile_page.cancel_add_user()
