"""
tests/practice_profile/test_practice_name_fields.py — Phase 2

Legal Name (PP·R1) + DBA Name (PP·R2) share identical rules.
Parametrised over the field — zero duplication.

Form opens ONCE via practice_profile_form_open fixture.
Tests that save use function-scoped practice_profile_page.

Rules covered:
  R*1a  Required
  R*1b  Min 2 chars
  R*1c  Max 150 chars
  R*1d  Allowed chars (Unicode letters/digits/spaces/-/'/./ &/,)
  R*1f  No consecutive special characters
  R*1g  Must start and end with letter or digit
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
)


# ===========================================================================
# Field descriptor — same pattern as Module 1 NameField
# ===========================================================================

@dataclass
class PracticeNameField:
    name: str
    prefix: str      # 'ln' or 'dba'
    invalid: List[Tuple]
    valid: List[Tuple]

    def input(self, pp: PracticeProfilePage) -> Locator:
        return pp.legal_name_input if self.prefix == "ln" else pp.dba_name_input

    def error(self, pp: PracticeProfilePage) -> Locator:
        return pp.legal_name_error if self.prefix == "ln" else pp.dba_name_error

    def err(self, key: str) -> str:
        return PP_ERR[key]


FIELDS = [
    PracticeNameField("Legal Name", "ln",  LEGAL_NAME_INVALID, LEGAL_NAME_VALID),
    PracticeNameField("DBA Name",   "dba", DBA_NAME_INVALID,   DBA_NAME_VALID),
]

INVALID_CASES = [
    pytest.param(field, tid, val, ekey, id=f"{field.prefix}-{tid}")
    for field in FIELDS
    for tid, val, ekey in field.invalid
]

VALID_CASES = [
    pytest.param(field, tid, val, id=f"{field.prefix}-{tid}")
    for field in FIELDS
    for tid, val in field.valid
]


# ===========================================================================
# Helper
# ===========================================================================

def _fill(pp: PracticeProfilePage, field: PracticeNameField, value: str) -> None:
    """Fill field and blur — form must already be open."""
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
@pytest.mark.regression
@pytest.mark.parametrize("field, test_id, value, error_key", INVALID_CASES)
def test_practice_name_invalid_shows_error(
    practice_profile_form_open: PracticeProfilePage,
    field: PracticeNameField,
    test_id: str,
    value: str,
    error_key: str,
) -> None:
    """TC-N-PP-*: Invalid name value shows correct inline error."""
    _fill(practice_profile_form_open, field, value)
    expect(field.error(practice_profile_form_open)).to_be_visible()
    expect(field.error(practice_profile_form_open)).to_contain_text(field.err(error_key))


# ===========================================================================
# TC-F — Functional: valid values no error (form stays open)
# ===========================================================================

@pytest.mark.functional
@pytest.mark.parametrize("field, test_id, value", VALID_CASES)
def test_practice_name_valid_no_error(
    practice_profile_form_open: PracticeProfilePage,
    field: PracticeNameField,
    test_id: str,
    value: str,
) -> None:
    """TC-F-PP-*: Valid name produces no inline error."""
    _fill(practice_profile_form_open, field, value)
    expect(field.error(practice_profile_form_open)).to_be_hidden()


# ===========================================================================
# TC-B — Boundary (form stays open)
# ===========================================================================

@pytest.mark.boundary
@pytest.mark.parametrize("field", FIELDS, ids=["ln", "dba"])
def test_practice_name_exact_min_2_accepted(
    practice_profile_form_open: PracticeProfilePage,
    field: PracticeNameField,
) -> None:
    """TC-B-PP-01/11: Exactly 2 characters — minimum valid."""
    _fill(practice_profile_form_open, field, "AB")
    expect(field.error(practice_profile_form_open)).to_be_hidden()


@pytest.mark.boundary
@pytest.mark.parametrize("field", FIELDS, ids=["ln", "dba"])
def test_practice_name_1_char_triggers_min_error(
    practice_profile_form_open: PracticeProfilePage,
    field: PracticeNameField,
) -> None:
    """TC-B-PP-02/12: 1 character — one below minimum."""
    _fill(practice_profile_form_open, field, "A")
    expect(field.error(practice_profile_form_open)).to_contain_text(
        PP_ERR[f"{field.prefix}_min"]
    )


@pytest.mark.boundary
@pytest.mark.parametrize("field", FIELDS, ids=["ln", "dba"])
def test_practice_name_exact_max_150_accepted(
    practice_profile_form_open: PracticeProfilePage,
    field: PracticeNameField,
) -> None:
    """TC-B-PP-09/13: Exactly 150 characters — maximum valid."""
    _fill(practice_profile_form_open, field, "A" * 150)
    expect(field.error(practice_profile_form_open)).to_be_hidden()


@pytest.mark.boundary
@pytest.mark.parametrize("field", FIELDS, ids=["ln", "dba"])
def test_practice_name_151_chars_triggers_max_error(
    practice_profile_form_open: PracticeProfilePage,
    field: PracticeNameField,
) -> None:
    """TC-B-PP-10/14: 151 characters — one above maximum."""
    _fill(practice_profile_form_open, field, "A" * 151)
    expect(field.error(practice_profile_form_open)).to_contain_text(
        PP_ERR[f"{field.prefix}_max"]
    )


# ===========================================================================
# TC-F (submit) + TC-R — open/close form themselves
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.xfail(reason="DEF-PP-05: Toast text unconfirmed — needs live verification")
@pytest.mark.parametrize("field", FIELDS, ids=["ln", "dba"])
def test_practice_name_valid_saves(
    practice_profile_page: PracticeProfilePage,
    field: PracticeNameField,
) -> None:
    """TC-F-PP-01: Valid name saves successfully."""
    inp = field.input(practice_profile_page)
    inp.scroll_into_view_if_needed()
    current = inp.input_value().strip()
    new_val = "Smile Dental Group" if current != "Smile Dental Group" else "DentiVoice Clinic"

    inp.click(click_count=3)
    inp.fill(new_val)
    expect(practice_profile_page.save_button).to_be_enabled(timeout=5_000)
    practice_profile_page.save_and_assert_success()


@pytest.mark.regression
@pytest.mark.xfail(reason="DEF-PP-05: Toast text unconfirmed — needs live verification")
@pytest.mark.parametrize("field", FIELDS, ids=["ln", "dba"])
def test_practice_name_fix_invalid_then_save(
    practice_profile_page: PracticeProfilePage,
    field: PracticeNameField,
) -> None:
    """TC-R-PP-05: Fix invalid name → save succeeds."""
    inp = field.input(practice_profile_page)
    err = field.error(practice_profile_page)

    inp.scroll_into_view_if_needed()
    inp.clear()
    inp.fill("Clinic--Care")
    inp.press("Tab")
    expect(err).to_contain_text(PP_ERR[f"{field.prefix}_consecutive"])

    inp.clear()
    inp.fill("Smile Dental")
    inp.press("Tab")
    expect(err).to_be_hidden()
    expect(practice_profile_page.save_button).to_be_enabled(timeout=5_000)
    practice_profile_page.save_and_assert_success()
