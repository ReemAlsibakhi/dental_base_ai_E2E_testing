"""
tests/profile/test_medium_priority.py — Phase 4

Medium-priority tests from the Decision Report:
  - Unicode names (Arabic, accented Latin)
  - Emoji rejection
  - Email local part boundary (TC-B-P-AU-EM-03/04)

Modal/panel opens ONCE via fixtures — no re-navigation per test.
"""

import pytest
from playwright.sync_api import expect

from pages.profile_page import ProfilePage
from test_data.profile_data import ERR


# ===========================================================================
# Name fields — Unicode valid cases (modal stays open)
# ===========================================================================

@pytest.mark.functional
@pytest.mark.parametrize("field,value", [
    ("fn", "رنا"),       # Arabic First Name
    ("fn", "José"),      # Accented Latin First Name
    ("fn", "Mary-Jane"), # Hyphen middle First Name
    ("fn", "O'Brien"),   # Apostrophe First Name
    ("fn", "Anne Marie"),# Internal space First Name
    ("ln", "سيباخي"),    # Arabic Last Name
    ("ln", "Müller"),    # Accented Latin Last Name
    ("ln", "Al-Hassan"), # Hyphen Last Name
    ("ln", "O'Neill"),   # Apostrophe Last Name
    ("ln", "Van Der Berg"), # Multi-space Last Name
], ids=[
    "fn-arabic", "fn-accented", "fn-hyphen", "fn-apostrophe", "fn-space",
    "ln-arabic", "ln-accented", "ln-hyphen", "ln-apostrophe", "ln-space",
])
def test_unicode_name_accepted(
    profile_page_modal_open: ProfilePage,
    field: str,
    value: str,
) -> None:
    """TC-F-P-FN/LN-*: Unicode and special char names produce no error."""
    inp = profile_page_modal_open.first_name_input if field == "fn" \
          else profile_page_modal_open.last_name_input
    err = profile_page_modal_open.first_name_error if field == "fn" \
          else profile_page_modal_open.last_name_error

    inp.clear()
    inp.fill(value)
    inp.press("Tab")
    expect(err).to_be_hidden()


# ===========================================================================
# Name fields — Emoji rejection (modal stays open)
# ===========================================================================

@pytest.mark.negative
@pytest.mark.parametrize("field,value,error_key", [
    ("fn", "Reem😊", "fn_chars"),
    ("ln", "Smith🎉", "ln_chars"),
], ids=["fn-emoji", "ln-emoji"])
def test_emoji_in_name_rejected(
    profile_page_modal_open: ProfilePage,
    field: str,
    value: str,
    error_key: str,
) -> None:
    """TC-N-P-FN/LN-06: Emoji in name triggers chars error."""
    inp = profile_page_modal_open.first_name_input if field == "fn" \
          else profile_page_modal_open.last_name_input
    err = profile_page_modal_open.first_name_error if field == "fn" \
          else profile_page_modal_open.last_name_error

    inp.clear()
    inp.fill(value)
    inp.press("Tab")
    expect(err).to_be_visible()
    expect(err).to_contain_text(ERR[error_key])


# ===========================================================================
# Email local part boundary (TC-B-P-AU-EM-03/04)
# Panel stays open
# ===========================================================================

@pytest.mark.boundary
def test_email_local_part_64_chars_accepted(
    add_user_panel_open: ProfilePage,
) -> None:
    """
    TC-B-P-AU-EM-03: Email local part of exactly 64 chars is accepted.
    local@domain.com where local = 64 chars = max per RFC 5321.
    """
    email = "a" * 64 + "@dentivoice.com"
    add_user_panel_open.add_user_email_input.clear()
    add_user_panel_open.add_user_email_input.fill(email)
    add_user_panel_open.add_user_email_input.press("Tab")
    add_user_panel_open.page.wait_for_timeout(300)
    expect(add_user_panel_open.add_user_email_error).to_be_hidden()


@pytest.mark.boundary
def test_email_local_part_65_chars_rejected(
    add_user_panel_open: ProfilePage,
) -> None:
    """
    TC-B-P-AU-EM-04: Email local part of 65 chars (one above max) is rejected.
    """
    email = "a" * 65 + "@dentivoice.com"
    add_user_panel_open.add_user_email_input.clear()
    add_user_panel_open.add_user_email_input.fill(email)
    add_user_panel_open.add_user_email_input.press("Tab")
    add_user_panel_open.page.wait_for_timeout(300)
    expect(add_user_panel_open.add_user_email_error).to_be_visible(timeout=5_000)


# ===========================================================================
# Name field — min valid with hyphen boundary (TC-B-P-FN-06)
# ===========================================================================

@pytest.mark.boundary
def test_name_min_valid_with_hyphen(
    profile_page_modal_open: ProfilePage,
) -> None:
    """
    TC-B-P-FN-06: Minimum valid name containing a hyphen: 'A-B' (3 chars).
    Tests R-FN-5/6 combined at the boundary.
    """
    profile_page_modal_open.first_name_input.clear()
    profile_page_modal_open.first_name_input.fill("A-B")
    profile_page_modal_open.first_name_input.press("Tab")
    expect(profile_page_modal_open.first_name_error).to_be_hidden()
