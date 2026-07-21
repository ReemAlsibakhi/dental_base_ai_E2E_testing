"""
tests/profile/test_edit_profile.py
Edit Profile — Name fields, Phone, Unicode, Security fields, Smoke.

Rules covered:
  R-FN-1 to R-FN-6  First Name validation
  R-LN-1 to R-LN-6  Last Name validation
  R-PH-1 to R-PH-4  Phone validation
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
    PHONE_INVALID, PHONE_ALPHA,
)


# ===========================================================================
# Helpers
# ===========================================================================

def _unique_value(current: str, option_a: str, option_b: str) -> str:
    """Return a value guaranteed to differ from current."""
    return option_b if current.strip() == option_a else option_a


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


def _fill_name(pp: ProfilePage, field: NameField, value: str) -> None:
    field.input(pp).clear()
    field.input(pp).fill(value)
    field.input(pp).press("Tab")


def _fill_phone(pp: ProfilePage, value: str) -> None:
    pp.phone_input.clear()
    pp.phone_input.fill(value)
    pp.phone_input.press("Tab")


# ===========================================================================
# Smoke
# ===========================================================================

@pytest.mark.smoke
@pytest.mark.functional
def test_valid_first_name_saves(profile_page: ProfilePage) -> None:
    """TC-SM-01: Valid first name saves and closes modal."""
    profile_page.open_edit_modal()
    current = profile_page.first_name_input.input_value()
    profile_page.first_name_input.click(click_count=3)
    profile_page.first_name_input.fill(_unique_value(current, "Lara", "Reem"))
    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


@pytest.mark.smoke
@pytest.mark.functional
def test_valid_last_name_saves(profile_page: ProfilePage) -> None:
    """TC-SM-02: Valid last name saves and closes modal."""
    profile_page.open_edit_modal()
    current = profile_page.last_name_input.input_value()
    profile_page.last_name_input.click(click_count=3)
    profile_page.last_name_input.fill(_unique_value(current, "Hassan", "Sibakhi"))
    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


@pytest.mark.smoke
@pytest.mark.functional
def test_valid_phone_saves(profile_page: ProfilePage) -> None:
    """TC-SM-03: Valid phone saves and closes modal."""
    profile_page.open_edit_modal()
    current = profile_page.phone_input.input_value()
    profile_page.phone_input.click(click_count=3)
    profile_page.phone_input.fill(_unique_value(current, "6035551234", "9995551234"))
    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


# ===========================================================================
# Name — Negative (modal stays open)
# ===========================================================================

@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.parametrize("field, test_id, value, error_key", INVALID_CASES)
def test_name_invalid_shows_error(
    profile_page_modal_open: ProfilePage,
    field: NameField, test_id: str, value: str, error_key: str,
) -> None:
    """TC-N: Invalid name shows correct inline error."""
    _fill_name(profile_page_modal_open, field, value)
    expect(field.error(profile_page_modal_open)).to_be_visible()
    expect(field.error(profile_page_modal_open)).to_contain_text(field.err(error_key))


# ===========================================================================
# Name — Functional (modal stays open)
# ===========================================================================

@pytest.mark.functional
@pytest.mark.parametrize("field, test_id, value", VALID_CASES)
def test_name_valid_no_error(
    profile_page_modal_open: ProfilePage,
    field: NameField, test_id: str, value: str,
) -> None:
    """TC-F: Valid name produces no inline error."""
    _fill_name(profile_page_modal_open, field, value)
    expect(field.error(profile_page_modal_open)).to_be_hidden()


# ===========================================================================
# Name — Boundary (modal stays open)
# ===========================================================================

@pytest.mark.boundary
@pytest.mark.parametrize("field", FIELDS, ids=["fn", "ln"])
def test_name_min_2_chars_accepted(profile_page_modal_open, field):
    """TC-B: 2 chars — minimum valid."""
    _fill_name(profile_page_modal_open, field, "Jo" if field.prefix == "fn" else "Li")
    expect(field.error(profile_page_modal_open)).to_be_hidden()


@pytest.mark.boundary
@pytest.mark.parametrize("field", FIELDS, ids=["fn", "ln"])
def test_name_1_char_triggers_error(profile_page_modal_open, field):
    """TC-B: 1 char triggers min error."""
    _fill_name(profile_page_modal_open, field, "J" if field.prefix == "fn" else "L")
    expect(field.error(profile_page_modal_open)).to_contain_text(ERR[f"{field.prefix}_min"])


@pytest.mark.boundary
@pytest.mark.parametrize("field", FIELDS, ids=["fn", "ln"])
def test_name_max_50_chars_accepted(profile_page_modal_open, field):
    """TC-B: 50 chars — maximum valid."""
    char = "A" if field.prefix == "fn" else "B"
    _fill_name(profile_page_modal_open, field, char * 50)
    expect(field.error(profile_page_modal_open)).to_be_hidden()


@pytest.mark.boundary
@pytest.mark.parametrize("field", FIELDS, ids=["fn", "ln"])
def test_name_51_chars_blocked(profile_page_modal_open, field):
    """TC-B: 51 chars — error or silent cap."""
    char = "A" if field.prefix == "fn" else "B"
    _fill_name(profile_page_modal_open, field, char * 51)
    value_in = field.input(profile_page_modal_open).input_value()
    error_visible = field.error(profile_page_modal_open).is_visible()
    assert error_visible or len(value_in) <= 50


# ===========================================================================
# Name — Submit + Usability + Regression
# ===========================================================================

@pytest.mark.functional
@pytest.mark.parametrize("field", FIELDS, ids=["fn", "ln"])
def test_name_valid_saves(profile_page, field):
    """TC-F: Valid name saves successfully."""
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
def test_name_error_clears_when_corrected(profile_page, field):
    """TC-U: Error clears when corrected."""
    profile_page.open_edit_modal()
    inp = field.input(profile_page)
    inp.clear(); inp.fill("Reem123" if field.prefix == "fn" else "Smith99"); inp.press("Tab")
    expect(field.error(profile_page)).to_contain_text(ERR[f"{field.prefix}_chars"])
    inp.clear(); inp.fill("Reem" if field.prefix == "fn" else "Smith"); inp.press("Tab")
    expect(field.error(profile_page)).to_be_hidden()
    profile_page.cancel_edit()


@pytest.mark.usability
@pytest.mark.parametrize("field", FIELDS, ids=["fn", "ln"])
def test_name_cancel_discards_invalid(profile_page, field):
    """TC-U: Cancel with invalid name closes modal."""
    profile_page.open_edit_modal()
    field.input(profile_page).clear(); field.input(profile_page).fill("Bad123"); field.input(profile_page).press("Tab")
    expect(field.error(profile_page)).to_be_visible()
    profile_page.cancel_edit()
    profile_page.assert_modal_is_closed()


@pytest.mark.regression
@pytest.mark.parametrize("field", FIELDS, ids=["fn", "ln"])
def test_name_fix_invalid_then_save(profile_page, field):
    """TC-R: Fix invalid name → save succeeds."""
    profile_page.open_edit_modal()
    inp = field.input(profile_page)
    inp.clear(); inp.fill("Bad@123"); inp.press("Tab")
    expect(field.error(profile_page)).to_contain_text(ERR[f"{field.prefix}_chars"])
    inp.clear(); inp.fill("Sara" if field.prefix == "fn" else "Ali"); inp.press("Tab")
    expect(field.error(profile_page)).to_be_hidden()
    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


# ===========================================================================
# Phone — Negative (modal stays open)
# ===========================================================================

@pytest.mark.negative
@pytest.mark.parametrize("test_id, value, error_key", PHONE_INVALID)
def test_phone_too_short_shows_error(profile_page_modal_open, test_id, value, error_key):
    """TC-N: Phone < 10 digits triggers error."""
    _fill_phone(profile_page_modal_open, value)
    expect(profile_page_modal_open.phone_error).to_be_visible()
    expect(profile_page_modal_open.phone_error).to_contain_text(ERR[error_key])


@pytest.mark.negative
def test_phone_alpha_stripped_silently(profile_page_modal_open):
    """TC-N: Alpha chars stripped silently."""
    _fill_phone(profile_page_modal_open, PHONE_ALPHA)
    value = profile_page_modal_open.phone_input.input_value()
    assert value == "" or value.isdigit()


# ===========================================================================
# Phone — Functional + Boundary
# ===========================================================================

@pytest.mark.functional
def test_phone_empty_is_optional(profile_page_modal_open):
    """TC-F: Empty phone accepted (optional)."""
    _fill_phone(profile_page_modal_open, "")
    expect(profile_page_modal_open.phone_error).to_be_hidden()


@pytest.mark.boundary
def test_phone_10_digits_accepted(profile_page_modal_open):
    """TC-B: 10 digits — minimum valid."""
    _fill_phone(profile_page_modal_open, "6035551234")
    expect(profile_page_modal_open.phone_error).to_be_hidden()


@pytest.mark.boundary
def test_phone_9_digits_triggers_error(profile_page_modal_open):
    """TC-B: 9 digits — one below minimum."""
    _fill_phone(profile_page_modal_open, "603555123")
    expect(profile_page_modal_open.phone_error).to_contain_text(ERR["ph_min_digits"])


@pytest.mark.boundary
def test_phone_maxlength_caps_at_10(profile_page_modal_open):
    """TC-B: 11 digits — silently capped at 10."""
    _fill_phone(profile_page_modal_open, "60355512345")
    value = profile_page_modal_open.phone_input.input_value()
    assert len("".join(c for c in value if c.isdigit())) <= 10
    expect(profile_page_modal_open.phone_error).to_be_hidden()


@pytest.mark.functional
@pytest.mark.smoke
def test_phone_valid_saves(profile_page):
    """TC-F: Valid phone saves successfully."""
    profile_page.open_edit_modal()
    current = profile_page.phone_input.input_value().strip()
    profile_page.phone_input.click(click_count=3)
    profile_page.phone_input.fill("6035551234" if current != "6035551234" else "9995551234")
    profile_page.phone_input.press("Tab")
    expect(profile_page.phone_error).to_be_hidden()
    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


@pytest.mark.regression
def test_phone_fix_short_then_save(profile_page):
    """TC-R: Fix short phone → save succeeds."""
    profile_page.open_edit_modal()
    _fill_phone(profile_page, "12345")
    expect(profile_page.phone_error).to_contain_text(ERR["ph_min_digits"])
    _fill_phone(profile_page, "6035551234")
    expect(profile_page.phone_error).to_be_hidden()
    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()
    profile_page.assert_modal_is_closed()


# ===========================================================================
# Unicode & Special Characters (Medium Priority)
# ===========================================================================

@pytest.mark.functional
@pytest.mark.parametrize("field,value", [
    ("fn", "رنا"), ("fn", "José"), ("fn", "Mary-Jane"),
    ("fn", "O'Brien"), ("fn", "Anne Marie"),
    ("ln", "سيباخي"), ("ln", "Müller"), ("ln", "Al-Hassan"),
    ("ln", "O'Neill"), ("ln", "Van Der Berg"),
], ids=["fn-arabic","fn-accented","fn-hyphen","fn-apostrophe","fn-space",
        "ln-arabic","ln-accented","ln-hyphen","ln-apostrophe","ln-space"])
def test_unicode_name_accepted(profile_page_modal_open, field, value):
    """TC-F: Unicode and special char names accepted."""
    inp = profile_page_modal_open.first_name_input if field == "fn" \
          else profile_page_modal_open.last_name_input
    err = profile_page_modal_open.first_name_error if field == "fn" \
          else profile_page_modal_open.last_name_error
    inp.clear(); inp.fill(value); inp.press("Tab")
    expect(err).to_be_hidden()


@pytest.mark.negative
@pytest.mark.parametrize("field,value,error_key", [
    ("fn", "Reem😊", "fn_chars"),
    ("ln", "Smith🎉", "ln_chars"),
], ids=["fn-emoji","ln-emoji"])
def test_emoji_in_name_rejected(profile_page_modal_open, field, value, error_key):
    """TC-N: Emoji in name triggers error."""
    inp = profile_page_modal_open.first_name_input if field == "fn" \
          else profile_page_modal_open.last_name_input
    err = profile_page_modal_open.first_name_error if field == "fn" \
          else profile_page_modal_open.last_name_error
    inp.clear(); inp.fill(value); inp.press("Tab")
    expect(err).to_be_visible()
    expect(err).to_contain_text(ERR[error_key])


@pytest.mark.boundary
def test_name_min_valid_with_hyphen(profile_page_modal_open):
    """TC-B: 'A-B' (3 chars with hyphen) — minimum valid with special char."""
    profile_page_modal_open.first_name_input.clear()
    profile_page_modal_open.first_name_input.fill("A-B")
    profile_page_modal_open.first_name_input.press("Tab")
    expect(profile_page_modal_open.first_name_error).to_be_hidden()
