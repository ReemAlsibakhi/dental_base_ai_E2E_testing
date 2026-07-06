"""
tests/practice_profile/test_practice_email_website.py — Phase 3

Email (PP·R6): optional, valid format, max 254 chars
Website (PP·R7): optional, must start with http/https, max 2048 chars
"""

import pytest
from playwright.sync_api import expect

from pages.practice_profile_page import PracticeProfilePage
from test_data.practice_profile_data import (
    PP_ERR,
    EMAIL_VALID, EMAIL_INVALID, EMAIL_MAX_VALID, EMAIL_MAX_INVALID,
    WEBSITE_VALID, WEBSITE_INVALID, WEBSITE_MAX_VALID, WEBSITE_MAX_INVALID,
)


def _fill(pp, locator, value):
    locator.scroll_into_view_if_needed()
    locator.clear()
    locator.fill(value)
    locator.press("Tab")
    pp.page.wait_for_timeout(300)


# ===========================================================================
# EMAIL (PP·R6)
# ===========================================================================

@pytest.mark.functional
def test_email_empty_is_optional(practice_profile_form_open: PracticeProfilePage) -> None:
    """TC-F-PP-03: Empty email is allowed (optional field)."""
    _fill(practice_profile_form_open, practice_profile_form_open.email_input, "")
    expect(practice_profile_form_open.email_error).to_be_hidden()


@pytest.mark.functional
def test_email_valid_format_accepted(practice_profile_form_open: PracticeProfilePage) -> None:
    """TC-F-PP-02: Valid email format accepted."""
    _fill(practice_profile_form_open, practice_profile_form_open.email_input, EMAIL_VALID)
    expect(practice_profile_form_open.email_error).to_be_hidden()


@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", EMAIL_INVALID)
def test_email_invalid_format_shows_error(
    practice_profile_form_open: PracticeProfilePage,
    test_id: str, value: str, error_key: str,
) -> None:
    """TC-N-PP-06/37/38: Invalid email format shows error."""
    _fill(practice_profile_form_open, practice_profile_form_open.email_input, value)
    expect(practice_profile_form_open.email_error).to_be_visible()
    expect(practice_profile_form_open.email_error).to_contain_text(PP_ERR[error_key])


@pytest.mark.negative
@pytest.mark.security
def test_email_xss_rejected(practice_profile_form_open: PracticeProfilePage) -> None:
    """TC-S-PP-13: XSS payload in email is rejected."""
    _fill(practice_profile_form_open, practice_profile_form_open.email_input, "<script>alert(1)</script>@test.com")
    expect(practice_profile_form_open.email_error).to_be_visible()


@pytest.mark.boundary
def test_email_254_chars_accepted(practice_profile_form_open: PracticeProfilePage) -> None:
    """TC-B-PP-21: 254-char email (RFC 5321 max) accepted."""
    _fill(practice_profile_form_open, practice_profile_form_open.email_input, EMAIL_MAX_VALID)
    expect(practice_profile_form_open.email_error).to_be_hidden()


@pytest.mark.boundary
def test_email_255_chars_rejected(practice_profile_form_open: PracticeProfilePage) -> None:
    """TC-B-PP-22: 255-char email (above max) rejected."""
    _fill(practice_profile_form_open, practice_profile_form_open.email_input, EMAIL_MAX_INVALID)
    expect(practice_profile_form_open.email_error).to_be_visible()


# ===========================================================================
# WEBSITE (PP·R7)
# ===========================================================================

@pytest.mark.functional
def test_website_empty_is_optional(practice_profile_form_open: PracticeProfilePage) -> None:
    """Website is optional — empty accepted."""
    _fill(practice_profile_form_open, practice_profile_form_open.website_input, "")
    expect(practice_profile_form_open.website_error).to_be_hidden()


@pytest.mark.functional
def test_website_https_accepted(practice_profile_form_open: PracticeProfilePage) -> None:
    """TC-F-PP-03: Valid https URL accepted."""
    _fill(practice_profile_form_open, practice_profile_form_open.website_input, WEBSITE_VALID)
    expect(practice_profile_form_open.website_error).to_be_hidden()


@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", WEBSITE_INVALID)
def test_website_invalid_scheme_shows_error(
    practice_profile_form_open: PracticeProfilePage,
    test_id: str, value: str, error_key: str,
) -> None:
    """TC-N-PP-07/39/21: Missing/wrong scheme or javascript: blocked."""
    _fill(practice_profile_form_open, practice_profile_form_open.website_input, value)
    expect(practice_profile_form_open.website_error).to_be_visible()


@pytest.mark.boundary
@pytest.mark.xfail(reason="DEF-PP-03: Website rejects 2048-char URL — actual max < 2048 (violates PP·R7d)")
def test_website_max_2048_chars_accepted(practice_profile_form_open: PracticeProfilePage) -> None:
    """TC-B-PP-NEW-05: 2048-char URL (max) accepted per PP·R7d.
    KNOWN BUG: App rejects URLs before reaching 2048 chars.
    """
    _fill(practice_profile_form_open, practice_profile_form_open.website_input, WEBSITE_MAX_VALID)
    expect(practice_profile_form_open.website_error).to_be_hidden()


@pytest.mark.boundary
def test_website_2049_chars_rejected(practice_profile_form_open: PracticeProfilePage) -> None:
    """TC-B-PP-NEW-06: 2049-char URL (above max) rejected."""
    _fill(practice_profile_form_open, practice_profile_form_open.website_input, WEBSITE_MAX_INVALID)
    error_visible = practice_profile_form_open.website_error.is_visible()
    field_capped  = len(practice_profile_form_open.website_input.input_value()) <= 2048
    assert error_visible or field_capped
