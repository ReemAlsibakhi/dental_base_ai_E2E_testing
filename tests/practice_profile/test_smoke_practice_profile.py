"""
tests/practice_profile/test_smoke_practice_profile.py — Phase 1

4 smoke tests — one per field group.
All use function-scoped practice_profile_page (opens + closes form per test).

Exit criterion: all 4 pass consistently headed + headless.
"""

import pytest
from playwright.sync_api import expect

from pages.practice_profile_page import PracticeProfilePage


@pytest.mark.smoke
@pytest.mark.functional
def test_practice_profile_edit_form_opens(
    practice_profile_page: PracticeProfilePage,
) -> None:
    """TC-SM-PP-01: Edit Practice Information form opens with all required fields."""
    expect(practice_profile_page.legal_name_input).to_be_visible()
    expect(practice_profile_page.dba_name_input).to_be_visible()
    expect(practice_profile_page.street_input).to_be_visible()
    expect(practice_profile_page.city_input).to_be_visible()
    expect(practice_profile_page.zip_input).to_be_visible()
    practice_profile_page.cancel()


@pytest.mark.smoke
@pytest.mark.functional
def test_legal_name_valid_saves(
    practice_profile_page: PracticeProfilePage,
) -> None:
    """TC-SM-PP-02: Valid Legal Name saves successfully."""
    current = practice_profile_page.legal_name_input.input_value().strip()
    new_val = "Smile Dental Group" if current != "Smile Dental Group" else "DentiVoice Clinic"

    practice_profile_page.legal_name_input.click(click_count=3)
    practice_profile_page.legal_name_input.fill(new_val)
    expect(practice_profile_page.save_button).to_be_enabled(timeout=5_000)
    practice_profile_page.save_and_assert_success()


@pytest.mark.smoke
@pytest.mark.functional
def test_address_fields_visible(
    practice_profile_page: PracticeProfilePage,
) -> None:
    """TC-SM-PP-03: Address group fields all visible in form."""
    expect(practice_profile_page.street_input).to_be_visible()
    expect(practice_profile_page.city_input).to_be_visible()
    expect(practice_profile_page.state_select).to_be_visible()
    expect(practice_profile_page.zip_input).to_be_visible()
    expect(practice_profile_page.timezone_select).to_be_visible()
    practice_profile_page.cancel()


@pytest.mark.smoke
@pytest.mark.functional
def test_optional_fields_visible(
    practice_profile_page: PracticeProfilePage,
) -> None:
    """TC-SM-PP-04: Optional fields (email, website, description) visible."""
    expect(practice_profile_page.email_input).to_be_visible()
    expect(practice_profile_page.website_input).to_be_visible()
    expect(practice_profile_page.description_input).to_be_visible()
    practice_profile_page.cancel()
