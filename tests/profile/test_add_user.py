"""
tests/profile/test_add_user.py
Add User — Email, Username, View All, Cancel.

Rules covered:
  R-AU-EM-1 to R-AU-EM-4  Email validation
  R-UN-1 to R-UN-6         Username validation
  R-VA-1 to R-VA-2         View All panel
"""

import pytest
from playwright.sync_api import expect

from pages.profile_page import ProfilePage
from test_data.profile_data import (
    ERR,
    ADD_USER_EMAIL_INVALID, ADD_USER_EMAIL_VALID,
    ADD_USER_DUPLICATE_EMAIL,
    ADD_USER_EMAIL_MAX_VALID, ADD_USER_EMAIL_MAX_INVALID,
    USERNAME_INVALID, USERNAME_VALID,
)

EXISTING_USERNAME = "reem_user"


# ===========================================================================
# Smoke
# ===========================================================================

@pytest.mark.smoke
@pytest.mark.functional
def test_add_user_form_opens_accepts_valid_email(profile_page: ProfilePage) -> None:
    """TC-SM-04: Add User form opens and accepts valid email."""
    profile_page.open_add_user_form()
    profile_page.add_user_email_input.fill("smoketest+auto@dentivoice.com")
    profile_page.add_user_email_input.press("Tab")
    profile_page.page.wait_for_timeout(300)
    expect(profile_page.add_user_email_error).to_be_hidden()
    profile_page.cancel_add_user()
    profile_page.assert_add_user_modal_closed()


# ===========================================================================
# Email — Negative (panel stays open)
# ===========================================================================

@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", ADD_USER_EMAIL_INVALID)
def test_invalid_email_shows_error(add_user_panel_open, test_id, value, error_key):
    """TC-N: Invalid email shows correct error."""
    add_user_panel_open.add_user_email_input.clear()
    add_user_panel_open.add_user_email_input.fill(value)
    add_user_panel_open.add_user_email_input.press("Tab")
    add_user_panel_open.page.wait_for_timeout(300)
    expect(add_user_panel_open.add_user_email_error).to_be_visible(timeout=5_000)
    expect(add_user_panel_open.add_user_email_error).to_contain_text(ERR[error_key])


# ===========================================================================
# Email — Functional + Boundary (panel stays open)
# ===========================================================================

@pytest.mark.functional
def test_valid_email_no_error(add_user_panel_open):
    """TC-F: Valid email produces no error."""
    add_user_panel_open.add_user_email_input.clear()
    add_user_panel_open.add_user_email_input.fill(ADD_USER_EMAIL_VALID)
    add_user_panel_open.add_user_email_input.press("Tab")
    add_user_panel_open.page.wait_for_timeout(300)
    expect(add_user_panel_open.add_user_email_error).to_be_hidden()


@pytest.mark.boundary
def test_email_254_chars_accepted(add_user_panel_open):
    """TC-B: 254 chars (RFC 5321 max) accepted."""
    add_user_panel_open.add_user_email_input.clear()
    add_user_panel_open.add_user_email_input.fill(ADD_USER_EMAIL_MAX_VALID)
    add_user_panel_open.add_user_email_input.press("Tab")
    add_user_panel_open.page.wait_for_timeout(300)
    expect(add_user_panel_open.add_user_email_error).to_be_hidden()


@pytest.mark.boundary
def test_email_255_chars_rejected(add_user_panel_open):
    """TC-B: 255 chars (one above max) rejected."""
    add_user_panel_open.add_user_email_input.clear()
    add_user_panel_open.add_user_email_input.fill(ADD_USER_EMAIL_MAX_INVALID)
    add_user_panel_open.add_user_email_input.press("Tab")
    add_user_panel_open.page.wait_for_timeout(300)
    expect(add_user_panel_open.add_user_email_error).to_be_visible(timeout=5_000)


@pytest.mark.boundary
def test_email_local_part_64_chars_accepted(add_user_panel_open):
    """TC-B: Local part 64 chars (RFC max) accepted."""
    add_user_panel_open.add_user_email_input.clear()
    add_user_panel_open.add_user_email_input.fill("a" * 64 + "@dentivoice.com")
    add_user_panel_open.add_user_email_input.press("Tab")
    add_user_panel_open.page.wait_for_timeout(300)
    expect(add_user_panel_open.add_user_email_error).to_be_hidden()


@pytest.mark.boundary
def test_email_local_part_65_chars_rejected(add_user_panel_open):
    """TC-B: Local part 65 chars rejected."""
    add_user_panel_open.add_user_email_input.clear()
    add_user_panel_open.add_user_email_input.fill("a" * 65 + "@dentivoice.com")
    add_user_panel_open.add_user_email_input.press("Tab")
    add_user_panel_open.page.wait_for_timeout(300)
    expect(add_user_panel_open.add_user_email_error).to_be_visible(timeout=5_000)


# ===========================================================================
# Email — Usability + Duplicate + Regression
# ===========================================================================

@pytest.mark.usability
def test_cancel_closes_form(profile_page):
    """TC-U: Cancel closes panel, user count unchanged."""
    initial_count = profile_page.get_user_count_number()
    profile_page.open_add_user_form()
    profile_page.add_user_email_input.fill(ADD_USER_EMAIL_VALID)
    profile_page.cancel_add_user()
    profile_page.assert_add_user_modal_closed()
    assert profile_page.get_user_count_number() == initial_count


@pytest.mark.usability
def test_email_error_clears_when_corrected(profile_page):
    """TC-U: Error clears when valid email replaces invalid."""
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
def test_duplicate_email_blocked(profile_page):
    """TC-N: Duplicate email shows 'already a member' error."""
    profile_page.open_add_user_form()
    profile_page.add_user_email_input.fill(ADD_USER_DUPLICATE_EMAIL)
    profile_page.add_user_submit_button.click()
    profile_page.page.wait_for_timeout(500)
    expect(profile_page.add_user_email_error).to_contain_text(ERR["au_email_duplicate"])
    profile_page.cancel_add_user()


@pytest.mark.regression
def test_fix_invalid_email_enables_submit(profile_page):
    """TC-R: Fixing invalid email re-enables Submit."""
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


# ===========================================================================
# Username — Negative (panel stays open)
# ===========================================================================

def _get_username_error(pp):
    return pp.page.locator('[aria-label="Add New User"] #username + p')


def _fill_username(pp, value):
    pp.add_user_username_input.clear()
    pp.add_user_username_input.fill(value)
    pp.add_user_username_input.press("Tab")
    pp.page.wait_for_timeout(300)


@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", USERNAME_INVALID)
def test_username_invalid_shows_error(add_user_panel_open, test_id, value, error_key):
    """TC-N: Invalid username shows correct error."""
    _fill_username(add_user_panel_open, value)
    expect(_get_username_error(add_user_panel_open)).to_be_visible()
    expect(_get_username_error(add_user_panel_open)).to_contain_text(ERR[error_key])


@pytest.mark.negative
def test_username_duplicate_blocked(profile_page):
    """TC-N: Duplicate username rejected."""
    profile_page.open_add_user_form()
    _fill_username(profile_page, EXISTING_USERNAME)
    expect(_get_username_error(profile_page)).to_be_visible(timeout=5_000)
    expect(_get_username_error(profile_page)).to_contain_text(ERR["un_duplicate"])
    profile_page.cancel_add_user()


@pytest.mark.negative
def test_username_case_insensitive_duplicate(profile_page):
    """TC-N: Case-insensitive duplicate rejected."""
    profile_page.open_add_user_form()
    _fill_username(profile_page, EXISTING_USERNAME.upper())
    expect(_get_username_error(profile_page)).to_be_visible(timeout=5_000)
    profile_page.cancel_add_user()


# ===========================================================================
# Username — Functional + Boundary
# ===========================================================================

@pytest.mark.functional
@pytest.mark.parametrize("test_id, value", USERNAME_VALID)
def test_username_valid_no_error(add_user_panel_open, test_id, value):
    """TC-F: Valid username produces no error."""
    _fill_username(add_user_panel_open, value)
    expect(_get_username_error(add_user_panel_open)).to_be_hidden()


@pytest.mark.boundary
def test_username_min_3_chars_accepted(add_user_panel_open):
    """TC-B: 3 chars — minimum valid."""
    _fill_username(add_user_panel_open, "abc")
    expect(_get_username_error(add_user_panel_open)).to_be_hidden()


@pytest.mark.boundary
def test_username_2_chars_triggers_error(add_user_panel_open):
    """TC-B: 2 chars — one below minimum."""
    _fill_username(add_user_panel_open, "ab")
    expect(_get_username_error(add_user_panel_open)).to_contain_text(ERR["un_min"])


@pytest.mark.boundary
def test_username_max_30_chars_accepted(add_user_panel_open):
    """TC-B: 30 chars — maximum valid."""
    _fill_username(add_user_panel_open, "a" * 30)
    expect(_get_username_error(add_user_panel_open)).to_be_hidden()


@pytest.mark.boundary
def test_username_31_chars_triggers_error(add_user_panel_open):
    """TC-B: 31 chars — one above maximum."""
    _fill_username(add_user_panel_open, "a" * 31)
    expect(_get_username_error(add_user_panel_open)).to_contain_text(ERR["un_max"])


# ===========================================================================
# Username — Regression + Security
# ===========================================================================

@pytest.mark.regression
def test_username_error_clears_when_corrected(profile_page):
    """TC-R: Error disappears when username corrected."""
    profile_page.open_add_user_form()
    _fill_username(profile_page, "UPPERCASE")
    expect(_get_username_error(profile_page)).to_contain_text(ERR["un_chars"])
    _fill_username(profile_page, "validuser")
    expect(_get_username_error(profile_page)).to_be_hidden()
    profile_page.cancel_add_user()


@pytest.mark.regression
@pytest.mark.security
def test_username_xss_rejected(profile_page):
    """TC-S: XSS payload rejected by char validation."""
    profile_page.open_add_user_form()
    _fill_username(profile_page, "<script>alert(1)</script>")
    expect(_get_username_error(profile_page)).to_be_visible()
    expect(_get_username_error(profile_page)).to_contain_text(ERR["un_chars"])
    profile_page.cancel_add_user()


# ===========================================================================
# View All
# ===========================================================================

@pytest.mark.functional
def test_view_all_opens_with_user_rows(profile_page):
    """TC-F: View All shows at least one user row."""
    profile_page.open_view_all()
    expect(profile_page.view_all_modal).to_be_visible()
    expect(profile_page.view_all_user_rows.first).to_be_visible()
    profile_page.view_all_modal.locator('button[aria-label="Close panel"]').click()


@pytest.mark.functional
def test_view_all_count_matches_card(profile_page):
    """TC-F: Row count equals 'N users' on card."""
    card_count = profile_page.get_user_count_number()
    profile_page.open_view_all()
    row_count = profile_page.get_view_all_row_count()
    profile_page.view_all_modal.locator('button[aria-label="Close panel"]').click()
    assert row_count == card_count


@pytest.mark.regression
def test_name_updates_in_view_all_after_edit(profile_page):
    """TC-R: Name change reflected in View All immediately."""
    profile_page.open_edit_modal()
    current = profile_page.last_name_input.input_value().strip()
    new_name = "Hassan" if current != "Hassan" else "Sibakhi"
    profile_page.last_name_input.click(click_count=3)
    profile_page.last_name_input.fill(new_name)
    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.open_view_all()
    expect(profile_page.page.get_by_text(new_name).first).to_be_visible()
    profile_page.view_all_modal.locator('button[aria-label="Close panel"]').click()
