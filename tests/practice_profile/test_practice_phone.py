"""
tests/practice_profile/test_practice_phone.py — Phase 3

Phone fields: Main Phone (PP·R4) + Emergency Phone (PP·R5)
Both share identical rules — parametrised over the field.

Rules:
  R*a  Required
  R*b  Min 10 digits
  R*d  Alpha chars stripped silently
  Max = 10 digits (silent cap — no test)
"""

import pytest
from playwright.sync_api import expect, Locator
from dataclasses import dataclass

from pages.practice_profile_page import PracticeProfilePage
from test_data.practice_profile_data import PP_ERR, PHONE_INVALID, PHONE_VALID


@dataclass
class PhoneField:
    name: str
    prefix: str

    def input(self, pp: PracticeProfilePage) -> Locator:
        return pp.main_phone_input if self.prefix == "main" else pp.emergency_phone_input

    def error(self, pp: PracticeProfilePage) -> Locator:
        return pp.main_phone_error if self.prefix == "main" else pp.emergency_phone_error


FIELDS = [
    PhoneField("Main Phone",      "main"),
    PhoneField("Emergency Phone", "emergency"),
]


def _fill(pp: PracticeProfilePage, field: PhoneField, value: str) -> None:
    inp = field.input(pp)
    inp.scroll_into_view_if_needed()
    inp.clear()
    inp.fill(value)
    inp.press("Tab")
    pp.page.wait_for_timeout(300)


# ===========================================================================
# TC-N — Negative (form stays open)
# ===========================================================================

@pytest.mark.negative
@pytest.mark.parametrize("field", FIELDS, ids=["main", "emergency"])
def test_phone_empty_shows_required_error(
    practice_profile_form_open: PracticeProfilePage,
    field: PhoneField,
) -> None:
    """TC-N-PP-03/16: Empty phone shows required error."""
    _fill(practice_profile_form_open, field, "")
    expect(field.error(practice_profile_form_open)).to_be_visible()
    expect(field.error(practice_profile_form_open)).to_contain_text("required")


@pytest.mark.negative
@pytest.mark.parametrize("field", FIELDS, ids=["main", "emergency"])
def test_phone_alpha_stripped_silently(
    practice_profile_form_open: PracticeProfilePage,
    field: PhoneField,
) -> None:
    """TC-N-PP-35/36: Alpha chars stripped silently — no alpha remains."""
    _fill(practice_profile_form_open, field, "abcdefghij")
    value = field.input(practice_profile_form_open).input_value()
    assert value == "" or value.isdigit(), \
        f"Expected digits-only or empty, got: '{value}'"


# ===========================================================================
# TC-B — Boundary (form stays open)
# ===========================================================================

@pytest.mark.boundary
@pytest.mark.parametrize("field", FIELDS, ids=["main", "emergency"])
def test_phone_exactly_10_digits_accepted(
    practice_profile_form_open: PracticeProfilePage,
    field: PhoneField,
) -> None:
    """TC-B-PP-24/26: Exactly 10 digits — minimum valid."""
    _fill(practice_profile_form_open, field, "6035551234")
    expect(field.error(practice_profile_form_open)).to_be_hidden()


@pytest.mark.boundary
@pytest.mark.parametrize("field", FIELDS, ids=["main", "emergency"])
def test_phone_9_digits_triggers_min_error(
    practice_profile_form_open: PracticeProfilePage,
    field: PhoneField,
) -> None:
    """TC-B-PP-25/27: 9 digits — one below minimum."""
    _fill(practice_profile_form_open, field, "603555123")
    expect(field.error(practice_profile_form_open)).to_contain_text(PP_ERR["phone_min"])
