"""
tests/profile/test_smoke.py — Phase 1 Smoke Suite

4 tests covering core happy-path actions end-to-end.
Each test reads the CURRENT value and changes it — guarantees Save is always enabled.
"""

import pytest
from playwright.sync_api import expect
from pages.profile_page import ProfilePage


def _unique_value(current: str, option_a: str, option_b: str) -> str:
    """Return a value guaranteed to differ from current."""
    return option_b if current.strip() == option_a else option_a


@pytest.mark.smoke
@pytest.mark.functional
def test_valid_first_name_saves_successfully(profile_page: ProfilePage) -> None:
    """TC-F-P-FN-01 — Valid First Name saves successfully."""
    profile_page.open_edit_modal()

    current = profile_page.first_name_input.input_value()
    new_value = _unique_value(current, "Lara", "Reem")

    profile_page.first_name_input.click(click_count=3)
    profile_page.first_name_input.fill(new_value)

    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


@pytest.mark.smoke
@pytest.mark.functional
def test_valid_last_name_saves_successfully(profile_page: ProfilePage) -> None:
    """TC-F-P-LN-01 — Valid Last Name saves successfully."""
    profile_page.open_edit_modal()

    current = profile_page.last_name_input.input_value()
    new_value = _unique_value(current, "Hassan", "Sibakhi")

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
    new_value = _unique_value(current, "6035551234", "9995551234")

    profile_page.phone_input.click(click_count=3)
    profile_page.phone_input.fill(new_value)

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
    profile_page.page.wait_for_timeout(300)

    expect(profile_page.add_user_email_error).to_be_hidden()

    profile_page.cancel_add_user()
    profile_page.assert_add_user_modal_closed()
