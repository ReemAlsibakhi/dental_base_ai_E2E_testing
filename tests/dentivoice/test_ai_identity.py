"""
tests/dentivoice/test_ai_identity.py — Phase 2
AI Identity panel (DV·R1, R2, R4) — Edit index 0

Known bugs:
  DEF-DV-03: Min 2 chars not enforced — 1-char name accepted
"""
import pytest
from playwright.sync_api import expect
from pages.dentivoice_page import DentiVoicePage
from test_data.dentivoice_data import (
    DV_ERR, VALID_AI_NAME,
    AI_NAME_MIN_VALID, AI_NAME_MIN_BELOW,
    AI_NAME_MAX_VALID, AI_NAME_MAX_PLUS1,
)


def _open(dv):
    dv.open_edit(DentiVoicePage.CARD["ai_identity"])


# ===========================================================================
# TC-F — Functional
# ===========================================================================

@pytest.mark.functional
@pytest.mark.smoke
def test_ai_name_valid_saves(dentivoice_page):
    """TC-F-DV-01: Valid assistant name saves successfully."""
    import random
    _open(dentivoice_page)
    # Use random suffix to guarantee dirty state regardless of current value
    name = f"Sofia{random.randint(10, 99)}"
    dentivoice_page.fill_ai_name(name)
    dentivoice_page.save_and_assert_success()


@pytest.mark.functional
def test_personality_all_options_selectable(dentivoice_page):
    """TC-F-DV-02: All 5 personality options are selectable."""
    _open(dentivoice_page)
    options = dentivoice_page.personality.evaluate(
        "el => [...el.options].map(o => o.value).filter(v => v)"
    )
    assert len(options) >= 5, f"Expected 5 personality options, got {len(options)}"
    dentivoice_page.cancel()


@pytest.mark.functional
def test_ai_disclosure_toggle(dentivoice_page):
    """TC-F-DV-03: AI Transparency Disclosure toggle can be toggled."""
    _open(dentivoice_page)
    initial = dentivoice_page.is_toggle_on(0)
    dentivoice_page.click_toggle(0)
    assert dentivoice_page.is_toggle_on(0) != initial
    dentivoice_page.cancel()


# ===========================================================================
# TC-N — Negative
# ===========================================================================

@pytest.mark.negative
def test_ai_name_empty_shows_error(dentivoice_page):
    """TC-N-DV-01: Empty name → Save disabled + error after debounce (~800ms)."""
    _open(dentivoice_page)
    dentivoice_page.fill_ai_name("")
    dentivoice_page.page.wait_for_timeout(1000)
    is_disabled = dentivoice_page.save_button.is_disabled()
    error_count = dentivoice_page.page.locator("p.text-red-500").count()
    assert is_disabled or error_count > 0, "Empty name should disable Save or show error"
    dentivoice_page.cancel()


@pytest.mark.negative
def test_ai_name_whitespace_shows_error(dentivoice_page):
    """TC-N-DV-02: Whitespace-only name → treated as empty → Save disabled."""
    _open(dentivoice_page)
    dentivoice_page.fill_ai_name("   ")
    dentivoice_page.page.wait_for_timeout(1000)
    # Whitespace is treated same as empty — Save disabled OR error shown
    is_disabled = dentivoice_page.save_button.is_disabled()
    error_count = dentivoice_page.page.locator("p.text-red-500").count()
    # If whitespace accepted → log as behavior (not strict assert)
    if not is_disabled and error_count == 0:
        dentivoice_page.click_save()
        dentivoice_page.page.wait_for_timeout(500)
        error_count = dentivoice_page.page.locator("p.text-red-500").count()
    assert is_disabled or error_count > 0, "Whitespace name should be rejected"
    dentivoice_page.cancel()


@pytest.mark.negative
def test_ai_name_numbers_rejected(dentivoice_page):
    """TC-N-DV-04: Numbers in name → chars error."""
    _open(dentivoice_page)
    dentivoice_page.fill_ai_name("Sofia123")
    dentivoice_page.click_save()
    expect(dentivoice_page.error).to_contain_text(DV_ERR["name_chars"])
    dentivoice_page.cancel()


@pytest.mark.negative
def test_ai_name_xss_rejected(dentivoice_page):
    """TC-N-DV-05: XSS in name → chars error."""
    _open(dentivoice_page)
    dentivoice_page.fill_ai_name("<script>alert(1)</script>")
    dentivoice_page.click_save()
    expect(dentivoice_page.error).to_be_visible()
    dentivoice_page.cancel()





# ===========================================================================
# TC-B — Boundary
# ===========================================================================

@pytest.mark.boundary
def test_ai_name_2_chars_accepted(dentivoice_page):
    """TC-B-DV-01: Name = 2 chars (min valid)."""
    _open(dentivoice_page)
    dentivoice_page.fill_ai_name(AI_NAME_MIN_VALID)
    dentivoice_page.save_and_assert_success()


@pytest.mark.boundary
def test_ai_name_1_char_rejected(dentivoice_page):
    """TC-B-DV-02: Name = 1 char → rejected (DEF-DV-03 resolved)."""
    _open(dentivoice_page)
    dentivoice_page.fill_ai_name(AI_NAME_MIN_BELOW)
    dentivoice_page.page.wait_for_timeout(1000)
    is_disabled = dentivoice_page.save_button.is_disabled()
    error_count = dentivoice_page.page.locator("p.text-red-500").count()
    assert is_disabled or error_count > 0, "1-char name should be rejected"
    dentivoice_page.cancel()


@pytest.mark.boundary
def test_ai_name_30_chars_accepted(dentivoice_page):
    """TC-B-DV-03: Name = 30 chars (max valid)."""
    _open(dentivoice_page)
    dentivoice_page.fill_ai_name(AI_NAME_MAX_VALID)
    dentivoice_page.save_and_assert_success()


@pytest.mark.boundary
def test_ai_name_31_chars_rejected(dentivoice_page):
    """TC-B-DV-04: Name = 31 pronounceable chars → max length error."""
    _open(dentivoice_page)
    dentivoice_page.fill_ai_name(AI_NAME_MAX_PLUS1)
    dentivoice_page.click_save()
    expect(dentivoice_page.error).to_contain_text(DV_ERR["name_max"])
    dentivoice_page.cancel()
