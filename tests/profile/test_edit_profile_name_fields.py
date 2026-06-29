"""
tests/profile/test_edit_profile_name_fields.py — Phase 2 (optimised)

Modal opens ONCE at module start — stays open for all negative/valid tests.
Only tests that submit or cancel re-open the modal after.

Both fields share identical rules — parametrised over the field itself.
"""

import pytest
from playwright.sync_api import expect, Locator
from dataclasses import dataclass
from typing import List, Tuple

from pages.profile_page import ProfilePage
from test_data.profile_data import (
    ERR,
    FIRST_NAME_INVALID, FIRST_NAME_VALID,
    LAST_NAME_INVALID,  LAST_NAME_VALID,
)


# ===========================================================================
# Field descriptor
# ===========================================================================

@dataclass
class NameField:
    name: str
    prefix: str
    invalid: List[Tuple]
    valid: List[Tuple]

    def input(self, pp: ProfilePage) -> Locator:
        return pp.first_name_input if self.prefix == "fn" else pp.last_name_input

    def error(self, pp: ProfilePage) -> Locator:
        return pp.first_name_error if self.prefix == "fn" else pp.last_name_error

    def err(self, key: str) -> str:
        return ERR[key.replace("fn_", f"{self.prefix}_")
                      .replace("ln_", f"{self.prefix}_")]


FIELDS = [
    NameField("First Name", "fn", FIRST_NAME_INVALID, FIRST_NAME_VALID),
    NameField("Last Name",  "ln", LAST_NAME_INVALID,  LAST_NAME_VALID),
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
# Helper — fill field and blur (modal already open)
# ===========================================================================

def _fill(pp: ProfilePage, field: NameField, value: str) -> None:
    """Fill the field and blur — modal must already be open."""
    field.input(pp).clear()
    field.input(pp).fill(value)
    field.input(pp).press("Tab")


# ===========================================================================
# TC-N — Negative: modal stays open, just fill + check error
# ===========================================================================

@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.parametrize("field, test_id, value, error_key", INVALID_CASES)
def test_name_invalid_shows_error(
    profile_page_modal_open: ProfilePage,
    field: NameField,
    test_id: str,
    value: str,
    error_key: str,
) -> None:
    """
    TC-N-P-FN/LN-*: Invalid name shows correct inline error.
    Modal stays open between tests — no re-navigation.
    """
    _fill(profile_page_modal_open, field, value)
    expect(field.error(profile_page_modal_open)).to_be_visible()
    expect(field.error(profile_page_modal_open)).to_contain_text(field.err(error_key))


# ===========================================================================
# TC-F — Functional: valid inputs no error (modal stays open)
# ===========================================================================

@pytest.mark.functional
@pytest.mark.parametrize("field, test_id, value", VALID_CASES)
def test_name_valid_no_error(
    profile_page_modal_open: ProfilePage,
    field: NameField,
    test_id: str,
    value: str,
) -> None:
    """TC-F-P-FN/LN-*: Valid name produces no inline error."""
    _fill(profile_page_modal_open, field, value)
    expect(field.error(profile_page_modal_open)).to_be_hidden()


# ===========================================================================
# TC-B — Boundary (modal stays open)
# ===========================================================================

@pytest.mark.boundary
@pytest.mark.parametrize("field", FIELDS, ids=["fn", "ln"])
def test_name_exact_min_2_chars_accepted(
    profile_page_modal_open: ProfilePage, field: NameField
) -> None:
    """TC-B-*-01: Exactly 2 characters — minimum valid."""
    _fill(profile_page_modal_open, field, "Jo" if field.prefix == "fn" else "Li")
    expect(field.error(profile_page_modal_open)).to_be_hidden()


@pytest.mark.boundary
@pytest.mark.parametrize("field", FIELDS, ids=["fn", "ln"])
def test_name_1_char_triggers_min_error(
    profile_page_modal_open: ProfilePage, field: NameField
) -> None:
    """TC-B-*-02: 1 character triggers min-length error."""
    _fill(profile_page_modal_open, field, "J" if field.prefix == "fn" else "L")
    expect(field.error(profile_page_modal_open)).to_contain_text(
        ERR[f"{field.prefix}_min"]
    )


@pytest.mark.boundary
@pytest.mark.parametrize("field", FIELDS, ids=["fn", "ln"])
def test_name_exact_max_50_chars_accepted(
    profile_page_modal_open: ProfilePage, field: NameField
) -> None:
    """TC-B-*-03: Exactly 50 characters — maximum valid."""
    char = "A" if field.prefix == "fn" else "B"
    _fill(profile_page_modal_open, field, char * 50)
    expect(field.error(profile_page_modal_open)).to_be_hidden()


@pytest.mark.boundary
@pytest.mark.parametrize("field", FIELDS, ids=["fn", "ln"])
def test_name_51_chars_blocked(
    profile_page_modal_open: ProfilePage, field: NameField
) -> None:
    """TC-B-*-04: 51 chars — error shown OR field silently capped."""
    char = "A" if field.prefix == "fn" else "B"
    _fill(profile_page_modal_open, field, char * 51)

    value_in_field = field.input(profile_page_modal_open).input_value()
    error_visible  = field.error(profile_page_modal_open).is_visible()
    field_capped   = len(value_in_field) <= 50

    assert error_visible or field_capped, (
        f"{field.name}: expected error or cap at 50, "
        f"got {len(value_in_field)} chars with no error"
    )


# ===========================================================================
# TC-F (submit) + TC-U + TC-R — these open/close modal themselves
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.parametrize("field", FIELDS, ids=["fn", "ln"])
def test_name_valid_saves_successfully(
    profile_page: ProfilePage, field: NameField
) -> None:
    """TC-F-*-01: Saving a valid name shows success toast and closes panel."""
    profile_page.open_edit_modal()
    current = field.input(profile_page).input_value().strip()
    new_value = ("Lara" if current != "Lara" else "Reem") if field.prefix == "fn" \
           else ("Hassan" if current != "Hassan" else "Sibakhi")

    field.input(profile_page).click(click_count=3)
    field.input(profile_page).fill(new_value)
    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


@pytest.mark.usability
@pytest.mark.parametrize("field", FIELDS, ids=["fn", "ln"])
def test_name_error_clears_when_corrected(
    profile_page: ProfilePage, field: NameField
) -> None:
    """TC-U-*-01: Inline error disappears when corrected."""
    profile_page.open_edit_modal()
    inp = field.input(profile_page)

    inp.clear()
    inp.fill("Reem123" if field.prefix == "fn" else "Smith99")
    inp.press("Tab")
    expect(field.error(profile_page)).to_contain_text(ERR[f"{field.prefix}_chars"])

    inp.clear()
    inp.fill("Reem" if field.prefix == "fn" else "Smith")
    inp.press("Tab")
    expect(field.error(profile_page)).to_be_hidden()
    profile_page.cancel_edit()


@pytest.mark.usability
@pytest.mark.parametrize("field", FIELDS, ids=["fn", "ln"])
def test_name_cancel_discards_invalid_state(
    profile_page: ProfilePage, field: NameField
) -> None:
    """TC-U-*-02: Cancelling with invalid name closes modal."""
    profile_page.open_edit_modal()
    field.input(profile_page).clear()
    field.input(profile_page).fill("Bad123")
    field.input(profile_page).press("Tab")
    expect(field.error(profile_page)).to_be_visible()
    profile_page.cancel_edit()
    profile_page.assert_modal_is_closed()


@pytest.mark.regression
@pytest.mark.parametrize("field", FIELDS, ids=["fn", "ln"])
def test_name_fix_invalid_then_save_succeeds(
    profile_page: ProfilePage, field: NameField
) -> None:
    """TC-R-*-01: Fix invalid name → save succeeds."""
    profile_page.open_edit_modal()
    inp = field.input(profile_page)

    inp.clear()
    inp.fill("Bad@123")
    inp.press("Tab")
    expect(field.error(profile_page)).to_contain_text(ERR[f"{field.prefix}_chars"])

    inp.clear()
    inp.fill("Sara" if field.prefix == "fn" else "Ali")
    inp.press("Tab")
    expect(field.error(profile_page)).to_be_hidden()
    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()
