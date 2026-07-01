"""
tests/practice_profile/test_smoke_practice_profile.py — Phase 1

Form opens ONCE via practice_profile_form_open fixture.
All 4 smoke tests share the same open form — no re-navigation.

Exit criterion: all 4 pass consistently headed + headless.
"""

import pytest
from playwright.sync_api import expect

from pages.practice_profile_page import PracticeProfilePage


@pytest.mark.smoke
@pytest.mark.functional
def test_practice_profile_edit_form_opens(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-SM-PP-01: Edit form opens with all required fields visible."""
    expect(practice_profile_form_open.legal_name_input).to_be_visible()
    expect(practice_profile_form_open.dba_name_input).to_be_visible()
    expect(practice_profile_form_open.street_input).to_be_visible()
    expect(practice_profile_form_open.city_input).to_be_visible()
    expect(practice_profile_form_open.zip_input).to_be_visible()


@pytest.mark.smoke
@pytest.mark.functional
def test_legal_name_valid_no_error(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-SM-PP-02: Valid Legal Name produces no inline error."""
    practice_profile_form_open.fill_legal_name("DentiVoice Clinic LLC")
    expect(practice_profile_form_open.legal_name_error).to_be_hidden()


@pytest.mark.smoke
@pytest.mark.functional
def test_address_fields_visible(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-SM-PP-03: Address group fields all visible in form."""
    expect(practice_profile_form_open.street_input).to_be_visible()
    expect(practice_profile_form_open.city_input).to_be_visible()
    expect(practice_profile_form_open.state_select).to_be_visible()
    expect(practice_profile_form_open.zip_input).to_be_visible()
    expect(practice_profile_form_open.timezone_select).to_be_visible()


@pytest.mark.smoke
@pytest.mark.functional
def test_optional_fields_visible(
    practice_profile_form_open: PracticeProfilePage,
) -> None:
    """TC-SM-PP-04: Optional fields visible in form."""
    expect(practice_profile_form_open.email_input).to_be_visible()
    expect(practice_profile_form_open.website_input).to_be_visible()
    expect(practice_profile_form_open.description_input).to_be_visible()
