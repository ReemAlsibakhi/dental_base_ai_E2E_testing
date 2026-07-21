"""
tests/practice_profile/test_practice_info.py
Practice Info — Legal Name, DBA Name, Phone fields, Practice Type, Smoke.

Rules covered:
  PP·R1  Legal Name validation
  PP·R2  DBA Name validation
  PP·R3  Practice Type dropdown
  PP·R4  Main Phone validation
  PP·R5  Emergency Phone validation
"""

import pytest
from playwright.sync_api import expect, Locator
from dataclasses import dataclass
from typing import List, Tuple

from pages.practice_profile_page import PracticeProfilePage
from test_data.practice_profile_data import (
    PP_ERR,
    LEGAL_NAME_VALID, LEGAL_NAME_INVALID,
    DBA_NAME_VALID,   DBA_NAME_INVALID,
    PHONE_INVALID, PHONE_VALID,
)


# ===========================================================================
# Name field descriptor
# ===========================================================================

@dataclass
class NameField:
    name: str
    prefix: str
    invalid: List[Tuple]
    valid: List[Tuple]

    def input(self, pp: PracticeProfilePage) -> Locator:
        return pp.legal_name_input if self.prefix == "ln" else pp.dba_name_input

    def error(self, pp: PracticeProfilePage) -> Locator:
        return pp.legal_name_error if self.prefix == "ln" else pp.dba_name_error


@dataclass
class PhoneField:
    name: str
    prefix: str

    def input(self, pp: PracticeProfilePage) -> Locator:
        return pp.main_phone_input if self.prefix == "main" else pp.emergency_phone_input

    def error(self, pp: PracticeProfilePage) -> Locator:
        return pp.main_phone_error if self.prefix == "main" else pp.emergency_phone_error


NAME_FIELDS = [
    NameField("Legal Name", "ln",  LEGAL_NAME_INVALID, LEGAL_NAME_VALID),
    NameField("DBA Name",   "dba", DBA_NAME_INVALID,   DBA_NAME_VALID),
]

PHONE_FIELDS = [
    PhoneField("Main Phone",      "main"),
    PhoneField("Emergency Phone", "emergency"),
]

NAME_INVALID_CASES = [
    pytest.param(f, tid, val, ekey, id=f"{f.prefix}-{tid}")
    for f in NAME_FIELDS for tid, val, ekey in f.invalid
]

NAME_VALID_CASES = [
    pytest.param(f, tid, val, id=f"{f.prefix}-{tid}")
    for f in NAME_FIELDS for tid, val in f.valid
]


def _fill_name(pp, field, value):
    inp = field.input(pp)
    inp.scroll_into_view_if_needed()
    inp.clear(); inp.fill(value); inp.press("Tab")
    pp.page.wait_for_timeout(300)


def _fill_phone(pp, field, value):
    inp = field.input(pp)
    inp.scroll_into_view_if_needed()
    inp.clear(); inp.fill(value); inp.press("Tab")
    pp.page.wait_for_timeout(300)


# ===========================================================================
# Smoke
# ===========================================================================

@pytest.mark.smoke
@pytest.mark.functional
def test_edit_form_opens(practice_profile_form_open: PracticeProfilePage) -> None:
    """TC-SM-PP-01: Edit form opens with required fields visible."""
    practice_profile_form_open.legal_name_input.scroll_into_view_if_needed()
    expect(practice_profile_form_open.legal_name_input).to_be_visible()
    expect(practice_profile_form_open.dba_name_input).to_be_visible()


@pytest.mark.smoke
@pytest.mark.functional
def test_address_fields_visible(practice_profile_form_open: PracticeProfilePage) -> None:
    """TC-SM-PP-03: Address group fields visible."""
    for locator in [practice_profile_form_open.street_input,
                    practice_profile_form_open.city_input,
                    practice_profile_form_open.zip_input,
                    practice_profile_form_open.state_select,
                    practice_profile_form_open.timezone_select]:
        locator.scroll_into_view_if_needed()
        expect(locator).to_be_visible()


@pytest.mark.smoke
@pytest.mark.functional
def test_optional_fields_visible(practice_profile_form_open: PracticeProfilePage) -> None:
    """TC-SM-PP-04: Optional fields visible."""
    for locator in [practice_profile_form_open.email_input,
                    practice_profile_form_open.website_input,
                    practice_profile_form_open.description_input]:
        locator.scroll_into_view_if_needed()
        expect(locator).to_be_visible()


# ===========================================================================
# Name — Negative / Positive / Boundary
# ===========================================================================

@pytest.mark.negative
@pytest.mark.parametrize("field, test_id, value, error_key", NAME_INVALID_CASES)
def test_name_invalid_shows_error(practice_profile_form_open, field, test_id, value, error_key):
    """TC-N: Invalid name shows correct error."""
    _fill_name(practice_profile_form_open, field, value)
    expect(field.error(practice_profile_form_open)).to_be_visible()
    expect(field.error(practice_profile_form_open)).to_contain_text(PP_ERR[error_key])


@pytest.mark.functional
@pytest.mark.parametrize("field, test_id, value", NAME_VALID_CASES)
def test_name_valid_no_error(practice_profile_form_open, field, test_id, value):
    """TC-F: Valid name produces no error."""
    _fill_name(practice_profile_form_open, field, value)
    expect(field.error(practice_profile_form_open)).to_be_hidden()


@pytest.mark.boundary
@pytest.mark.parametrize("field", NAME_FIELDS, ids=["ln", "dba"])
def test_name_min_2_chars_accepted(practice_profile_form_open, field):
    """TC-B: 2 chars — minimum valid."""
    _fill_name(practice_profile_form_open, field, "AB")
    expect(field.error(practice_profile_form_open)).to_be_hidden()


@pytest.mark.boundary
@pytest.mark.parametrize("field", NAME_FIELDS, ids=["ln", "dba"])
def test_name_1_char_triggers_error(practice_profile_form_open, field):
    """TC-B: 1 char — below minimum."""
    _fill_name(practice_profile_form_open, field, "A")
    expect(field.error(practice_profile_form_open)).to_contain_text(PP_ERR[f"{field.prefix}_min"])


@pytest.mark.boundary
@pytest.mark.parametrize("field", NAME_FIELDS, ids=["ln", "dba"])
def test_name_max_150_chars_accepted(practice_profile_form_open, field):
    """TC-B: 150 chars — maximum valid."""
    _fill_name(practice_profile_form_open, field, "A" * 150)
    expect(field.error(practice_profile_form_open)).to_be_hidden()


@pytest.mark.boundary
@pytest.mark.parametrize("field", NAME_FIELDS, ids=["ln", "dba"])
def test_name_151_chars_triggers_error(practice_profile_form_open, field):
    """TC-B: 151 chars — above maximum."""
    _fill_name(practice_profile_form_open, field, "A" * 151)
    expect(field.error(practice_profile_form_open)).to_contain_text(PP_ERR[f"{field.prefix}_max"])


@pytest.mark.functional
@pytest.mark.parametrize("field", NAME_FIELDS, ids=["ln", "dba"])
def test_name_valid_saves(practice_profile_page, field):
    """TC-F: Valid name saves successfully."""
    inp = field.input(practice_profile_page)
    inp.scroll_into_view_if_needed()
    current = inp.input_value().strip()
    new_val = "Smile Dental Group" if current != "Smile Dental Group" else "DentiVoice Clinic"
    inp.click(click_count=3); inp.fill(new_val)
    expect(practice_profile_page.save_button).to_be_enabled(timeout=5_000)
    practice_profile_page.save_and_assert_success()


@pytest.mark.regression
@pytest.mark.parametrize("field", NAME_FIELDS, ids=["ln", "dba"])
def test_name_fix_invalid_then_save(practice_profile_page, field):
    """TC-R: Fix invalid → save succeeds."""
    inp = field.input(practice_profile_page)
    inp.scroll_into_view_if_needed()
    inp.clear(); inp.fill("Clinic--Care"); inp.press("Tab")
    expect(field.error(practice_profile_page)).to_contain_text(PP_ERR[f"{field.prefix}_consecutive"])
    inp.clear(); inp.fill("Smile Dental"); inp.press("Tab")
    expect(field.error(practice_profile_page)).to_be_hidden()
    practice_profile_page.save_and_assert_success()


# ===========================================================================
# Phone — Negative / Boundary
# ===========================================================================

@pytest.mark.negative
@pytest.mark.parametrize("field", PHONE_FIELDS, ids=["main", "emergency"])
def test_phone_empty_shows_required(practice_profile_form_open, field):
    """TC-N: Empty phone shows required error."""
    _fill_phone(practice_profile_form_open, field, "")
    expect(field.error(practice_profile_form_open)).to_contain_text("required")


@pytest.mark.negative
@pytest.mark.parametrize("field", PHONE_FIELDS, ids=["main", "emergency"])
def test_phone_alpha_stripped_silently(practice_profile_form_open, field):
    """TC-N: Alpha chars stripped silently."""
    _fill_phone(practice_profile_form_open, field, "abcdefghij")
    value = field.input(practice_profile_form_open).input_value()
    assert value == "" or value.isdigit()


@pytest.mark.boundary
@pytest.mark.parametrize("field", PHONE_FIELDS, ids=["main", "emergency"])
def test_phone_10_digits_accepted(practice_profile_form_open, field):
    """TC-B: 10 digits — minimum valid."""
    _fill_phone(practice_profile_form_open, field, "6035551234")
    expect(field.error(practice_profile_form_open)).to_be_hidden()


@pytest.mark.boundary
@pytest.mark.parametrize("field", PHONE_FIELDS, ids=["main", "emergency"])
def test_phone_9_digits_triggers_error(practice_profile_form_open, field):
    """TC-B: 9 digits — below minimum."""
    _fill_phone(practice_profile_form_open, field, "603555123")
    expect(field.error(practice_profile_form_open)).to_contain_text(PP_ERR["phone_min"])


# ===========================================================================
# Practice Type (PP·R3)
# ===========================================================================

@pytest.mark.functional
def test_practice_type_has_default(practice_profile_form_open):
    """TC-F: Practice Type has a default value."""
    practice_profile_form_open.practice_type_select.scroll_into_view_if_needed()
    assert practice_profile_form_open.practice_type_select.input_value() != ""


@pytest.mark.functional
def test_practice_type_all_options_available(practice_profile_form_open):
    """TC-F: All practice type options present."""
    practice_profile_form_open.practice_type_select.scroll_into_view_if_needed()
    options = practice_profile_form_open.practice_type_select.evaluate(
        "el => [...el.options].map(o => o.value)"
    )
    for opt in ["general", "pediatric", "orthodontic", "oral_surgery", "periodontic", "endodontic"]:
        assert opt in options


@pytest.mark.functional
def test_practice_type_can_select_pediatric(practice_profile_form_open):
    """TC-F: Practice Type accepts valid selection."""
    practice_profile_form_open.practice_type_select.scroll_into_view_if_needed()
    practice_profile_form_open.practice_type_select.select_option("pediatric")
    assert practice_profile_form_open.practice_type_select.input_value() == "pediatric"
