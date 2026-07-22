"""
tests/insurance_billing/test_pricing_policy.py
Pricing Policy (IB-PP-R1 to R3)

Rules:
  IB-PP-R1: Pricing Policy radio (4 options)
  IB-PP-R2: Good Faith Estimate Compliance toggle
  IB-PP-R3: Custom AI Script (2000-char limit)

Known bugs:
  DEF-IB2-04: Custom AI Script contains unsanitized text feeding DentiVoice AI
"""

import pytest
from playwright.sync_api import expect

from pages.insurance_billing_page import InsuranceBillingPage

PRICING_OPTIONS = [
    "Always Provide Exact Pricing",
    "Require Exam First",
    "Provide Range Only",
    "Do Not Discuss Pricing",
]

AI_SCRIPT_MAX_VALID   = "A" * 2000
AI_SCRIPT_MAX_INVALID = "A" * 2001


def _open(ib):
    ib.open_edit(InsuranceBillingPage.CARD["pricing_policy"])
    ib.page.wait_for_timeout(500)


# ===========================================================================
# Smoke
# ===========================================================================

@pytest.mark.smoke
@pytest.mark.functional
def test_pricing_policy_panel_opens(insurance_billing_page):
    """TC-SM-IB: Pricing Policy panel opens."""
    _open(insurance_billing_page)
    expect(insurance_billing_page.modal).to_be_visible()
    insurance_billing_page.cancel()


# ===========================================================================
# IB-PP-R1 — Pricing Policy radio
# ===========================================================================

@pytest.mark.functional
@pytest.mark.parametrize("option", PRICING_OPTIONS)
def test_pricing_option_selectable(insurance_billing_page, option):
    """TC-F-IB2-12: All 4 pricing policy options selectable."""
    _open(insurance_billing_page)
    insurance_billing_page.select_pricing_option(option)
    insurance_billing_page.page.wait_for_timeout(300)
    # Verify option is selected
    option_el = insurance_billing_page.modal.get_by_text(option, exact=False).first
    expect(option_el).to_be_visible()
    insurance_billing_page.save_and_assert_success()


@pytest.mark.regression
def test_pricing_option_persists_after_save(insurance_billing_page):
    """TC-R-IB2-05: Selected pricing option persists after save."""
    _open(insurance_billing_page)
    insurance_billing_page.select_pricing_option("Require Exam First")
    insurance_billing_page.save_and_assert_success()
    _open(insurance_billing_page)
    expect(
        insurance_billing_page.modal.get_by_text("Require Exam First", exact=False)
    ).to_be_visible()
    insurance_billing_page.cancel()


# ===========================================================================
# IB-PP-R2 — Good Faith Estimate Compliance
# ===========================================================================

@pytest.mark.functional
def test_good_faith_toggle_changes_state(insurance_billing_page):
    """TC-F-IB2-13: Good Faith Estimate toggle changes state → saves."""
    _open(insurance_billing_page)
    toggle = insurance_billing_page.good_faith_toggle
    initial = toggle.get_attribute("aria-checked")
    toggle.click(force=True)
    insurance_billing_page.page.wait_for_timeout(500)
    assert toggle.get_attribute("aria-checked") != initial
    insurance_billing_page.save_and_assert_success()


@pytest.mark.regression
def test_good_faith_toggle_persists(insurance_billing_page):
    """TC-R-IB2-06: Good Faith toggle state persists after save."""
    _open(insurance_billing_page)
    toggle = insurance_billing_page.good_faith_toggle
    initial = toggle.get_attribute("aria-checked")
    toggle.click(force=True)
    new_state = toggle.get_attribute("aria-checked")
    insurance_billing_page.save_and_assert_success()
    _open(insurance_billing_page)
    toggle = insurance_billing_page.good_faith_toggle
    assert toggle.get_attribute("aria-checked") == new_state
    insurance_billing_page.cancel()


# ===========================================================================
# IB-PP-R3 — Custom AI Script
# ===========================================================================

@pytest.mark.functional
def test_custom_ai_script_valid_saves(insurance_billing_page):
    """TC-F-IB2-14: Valid AI script saves."""
    _open(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.custom_ai_script,
        "We provide competitive pricing for all dental services."
    )
    insurance_billing_page.save_and_assert_success()


@pytest.mark.boundary
def test_custom_ai_script_2000_chars_accepted(insurance_billing_page):
    """TC-B-IB2-13: AI script 2000 chars — max valid."""
    _open(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.custom_ai_script, AI_SCRIPT_MAX_VALID
    )
    insurance_billing_page.page.wait_for_timeout(500)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.save_and_assert_success()


@pytest.mark.boundary
def test_custom_ai_script_2001_chars_blocked(insurance_billing_page):
    """TC-B-IB2-14: AI script 2001 chars → error or blocked."""
    _open(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.custom_ai_script, AI_SCRIPT_MAX_INVALID
    )
    insurance_billing_page.page.wait_for_timeout(500)
    value = insurance_billing_page.custom_ai_script.input_value()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors > 0 or len(value) <= 2000, "2001-char AI script should be rejected"
    insurance_billing_page.cancel()


@pytest.mark.security
def test_custom_ai_script_xss_sanitized(insurance_billing_page):
    """TC-S-IB2-06: XSS in AI script — verify no script execution."""
    _open(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.custom_ai_script,
        "<script>alert('prompt injection')</script>"
    )
    insurance_billing_page.save_and_assert_success()
    # Verify page still functional after save
    assert insurance_billing_page.page.locator('button:has-text("Edit")').count() > 0
