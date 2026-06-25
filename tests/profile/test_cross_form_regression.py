"""
tests/profile/test_cross_form_regression.py — Phase 2

Cross-form regression tests verify that validation rules are identical
across both the Edit Profile modal and the Add User panel.

TC-R-P-FN-CROSS-01: First Name rules same in both forms
TC-R-P-LN-CROSS-01: Last Name rules same in both forms (also in last_name file)

These are high-priority regression tests — they catch the common pattern
where a developer updates validation in one form but forgets the other.
"""

import pytest
from playwright.sync_api import expect

from pages.profile_page import ProfilePage
from test_data.profile_data import ERR


@pytest.mark.regression
def test_first_name_validates_same_in_add_user_form(profile_page: ProfilePage) -> None:
    """
    TC-R-P-FN-CROSS-01: First Name rules are identical in Edit Profile and Add User.

    Tests 3 representative rules across both forms:
      - Disallowed chars (R-FN-4)
      - Consecutive specials (R-FN-5)
      - Must start with letter (R-FN-6)
    """
    profile_page.open_add_user_form()

    cross_cases = [
        ("Reem123",    ERR["fn_chars"]),
        ("Mary--Jane", ERR["fn_consecutive"]),
        ("-Reem",      ERR["fn_start_end"]),
    ]

    for value, expected_error in cross_cases:
        inp = profile_page.add_user_first_name_input
        inp.clear()
        inp.fill(value)
        inp.press("Tab")

        # Error must appear immediately after the input
        error = profile_page.page.locator(
            '[aria-label="Add New User"] #first_name + p'
        )
        expect(error).to_be_visible()
        expect(error).to_contain_text(expected_error)

    profile_page.cancel_add_user()


@pytest.mark.regression
def test_last_name_validates_same_in_add_user_form(profile_page: ProfilePage) -> None:
    """
    TC-R-P-LN-CROSS-01: Last Name rules are identical in Edit Profile and Add User.
    """
    profile_page.open_add_user_form()

    cross_cases = [
        ("Smith99",    ERR["ln_chars"]),
        ("Al--Hassan", ERR["ln_consecutive"]),
        ("-Hassan",    ERR["ln_start_end"]),
    ]

    for value, expected_error in cross_cases:
        inp = profile_page.add_user_last_name_input
        inp.clear()
        inp.fill(value)
        inp.press("Tab")

        error = profile_page.page.locator(
            '[aria-label="Add New User"] #last_name + p'
        )
        expect(error).to_be_visible()
        expect(error).to_contain_text(expected_error)

    profile_page.cancel_add_user()
