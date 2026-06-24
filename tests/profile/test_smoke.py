"""
tests/profile/test_smoke.py — Phase 1 Smoke Suite
4 tests covering core happy-path actions end-to-end.
"""

import pytest
from playwright.sync_api import expect
from pages.profile_page import ProfilePage


@pytest.mark.smoke
@pytest.mark.functional
def test_valid_first_name_saves_successfully(profile_page: ProfilePage) -> None:
    """TC-F-P-FN-01 — Valid First Name saves successfully."""
    profile_page.open_edit_modal()

    # Type a new value that differs from current — form enables Save only on change
    current = profile_page.first_name_input.input_value()
    new_value = "Lara" if current.strip() != "Lara" else "Reem"

    profile_page.first_name_input.click(click_count=3)
    profile_page.first_name_input.fill(new_value)

    # Wait for Save button to become enabled
    profile_page.modal_save_button.wait_for(state="visible")
    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)

    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


@pytest.mark.smoke
@pytest.mark.functional
def test_valid_last_name_saves_successfully(profile_page: ProfilePage) -> None:
    """TC-F-P-LN-01 — Valid Last Name saves successfully."""
    profile_page.open_edit_modal()

    current = profile_page.last_name_input.input_value()
    new_value = "Hassan" if current.strip() != "Hassan" else "Sibakhi"

    profile_page.last_name_input.click(click_count=3)
    profile_page.last_name_input.fill(new_value)

    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


@pytest.mark.smoke
@pytest.mark.functional
def test_valid_phone_saves_successfully(profile_page: ProfilePage) -> None:
    """TC-F-P-PH-01 — Valid Phone Number saves successfully."""
    profile_page.open_edit_modal()

    current = profile_page.phone_input.input_value()
    new_value = "6035551234" if current.strip() != "6035551234" else "9995551234"

    profile_page.phone_input.click(click_count=3)
    profile_page.phone_input.fill(new_value)

    profile_page.assert_no_phone_error()
    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


@pytest.mark.smoke
@pytest.mark.functional
def test_add_user_form_opens_and_accepts_valid_email(profile_page: ProfilePage) -> None:
    """TC-F-P-AU-01 — Add User form opens and accepts valid email."""
    profile_page.open_add_user_form()

    profile_page.add_user_email_input.fill("smoketest+auto@dentivoice.com")
    profile_page.add_user_email_input.press("Tab")

    expect(profile_page.add_user_email_error).to_be_hidden()

    profile_page.cancel_add_user()
    profile_page.assert_add_user_modal_closed()
