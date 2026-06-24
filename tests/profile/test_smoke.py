"""
tests/profile/test_smoke.py — Phase 1 Smoke Suite

4 tests that must pass before any other phase begins.
Each test covers one core happy-path action end-to-end:

  TC-F-P-FN-01 — Valid First Name saves successfully
  TC-F-P-LN-01 — Valid Last Name saves successfully
  TC-F-P-PH-01 — Valid Phone Number saves successfully
  TC-F-P-AU-01 — Valid email accepted in Add User form

Exit criterion: ALL 4 pass consistently in --headed and --headless modes.

Markers: @smoke — runs on every CI deploy (fast, ~2 min total)
"""

import pytest
from playwright.sync_api import expect
from pages.profile_page import ProfilePage


# ---------------------------------------------------------------------------
# TC-F-P-FN-01 — Valid First Name saves successfully
# ---------------------------------------------------------------------------

@pytest.mark.smoke
@pytest.mark.functional
def test_valid_first_name_saves_successfully(profile_page: ProfilePage) -> None:
    """
    TC-F-P-FN-01
    Steps:
      1. Settings → Profile → Edit
      2. First Name: "Reem" → Save Changes
    Expected:
      - Success toast appears
      - Edit panel closes
    """
    profile_page.open_edit_modal()

    # Clear and fill First Name with a valid value
    profile_page.edit_first_name("Reem", blur=False)

    # Save and assert success toast
    profile_page.save_and_assert_success()

    # Panel must close after successful save
    profile_page.assert_modal_is_closed()


# ---------------------------------------------------------------------------
# TC-F-P-LN-01 — Valid Last Name saves successfully
# ---------------------------------------------------------------------------

@pytest.mark.smoke
@pytest.mark.functional
def test_valid_last_name_saves_successfully(profile_page: ProfilePage) -> None:
    """
    TC-F-P-LN-01
    Steps:
      1. Settings → Profile → Edit
      2. Last Name: "Sibakhi" → Save Changes
    Expected:
      - Success toast appears
      - Edit panel closes
    """
    profile_page.open_edit_modal()

    profile_page.edit_last_name("Sibakhi", blur=False)

    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


# ---------------------------------------------------------------------------
# TC-F-P-PH-01 — Valid Phone Number saves successfully
# ---------------------------------------------------------------------------

@pytest.mark.smoke
@pytest.mark.functional
def test_valid_phone_saves_successfully(profile_page: ProfilePage) -> None:
    """
    TC-F-P-PH-01
    Steps:
      1. Settings → Profile → Edit
      2. Phone Number: "6035551234" (10 digits) → Save Changes
    Expected:
      - No inline error
      - Success toast appears
      - Edit panel closes
    """
    profile_page.open_edit_modal()

    profile_page.edit_phone("6035551234", blur=True)

    # No inline error
    profile_page.assert_no_phone_error()

    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


# ---------------------------------------------------------------------------
# TC-F-P-AU-01 — Add User form accepts valid email
# ---------------------------------------------------------------------------

@pytest.mark.smoke
@pytest.mark.functional
def test_add_user_form_opens_and_accepts_valid_email(profile_page: ProfilePage) -> None:
    """
    TC-F-P-AU-01
    Steps:
      1. Settings → Profile → Add User
      2. Email: fill with a valid format → observe no inline error
    Expected:
      - Add User panel opens
      - Email field accepts valid format (no inline error after blur)
    Note:
      We do NOT submit here to avoid actually inviting a real user on every
      smoke run. We verify the form opens and accepts valid input, then cancel.
    """
    profile_page.open_add_user_form()

    # Fill valid email and blur — no inline error expected
    profile_page.add_user_email_input.fill("smoketest+auto@dentivoice.com")
    profile_page.add_user_email_input.press("Tab")

    # No error should appear on valid email
    expect(profile_page.add_user_email_error).to_be_hidden()

    # Cancel — do not send a real invitation on every smoke run
    profile_page.cancel_add_user()
    profile_page.assert_add_user_modal_closed()
