"""
tests/insurance_billing/test_membership_plans.py
Membership Plans (IB-MEM-R1 to R4)
"""

import pytest
from playwright.sync_api import expect

from pages.insurance_billing_page import InsuranceBillingPage


def _open(ib):
    ib.open_edit(InsuranceBillingPage.CARD["membership_plans"])
    ib.page.wait_for_timeout(500)


# ===========================================================================
# IB-MEM-R1 — Plan Name
# ===========================================================================

@pytest.mark.functional
def test_plan_name_valid_saves(insurance_billing_page):
    """TC-F-IB2-04: Valid plan name saves."""
    _open(insurance_billing_page)
    current = insurance_billing_page.plan_name_input.input_value()
    new_name = "Premium Plan" if current != "Premium Plan" else "Basic Plan"
    insurance_billing_page.smart_fill(insurance_billing_page.plan_name_input, new_name)
    insurance_billing_page.save_and_assert_success()


@pytest.mark.negative
def test_plan_name_empty_blocked(insurance_billing_page):
    """TC-N-IB2-06: Empty plan name → Save disabled or error."""
    _open(insurance_billing_page)
    insurance_billing_page.plan_name_input.fill("")
    insurance_billing_page.plan_name_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    is_disabled = insurance_billing_page.save_button.is_disabled()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0
    insurance_billing_page.cancel()


@pytest.mark.security
def test_plan_name_xss_rejected(insurance_billing_page):
    """TC-S-IB2-02: XSS in plan name rejected."""
    _open(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.plan_name_input, "<script>alert(1)</script>"
    )
    insurance_billing_page.page.wait_for_timeout(500)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    is_disabled = insurance_billing_page.save_button.is_disabled()
    assert is_disabled or errors > 0
    insurance_billing_page.cancel()


@pytest.mark.usability
def test_plan_name_error_clears_when_corrected(insurance_billing_page):
    """TC-U-IB2-01: Plan name error clears when corrected."""
    _open(insurance_billing_page)
    insurance_billing_page.plan_name_input.fill("")
    insurance_billing_page.plan_name_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.smart_fill(insurance_billing_page.plan_name_input, "Basic Plan")
    insurance_billing_page.page.wait_for_timeout(500)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


@pytest.mark.regression
def test_plan_name_persists_after_save(insurance_billing_page):
    """TC-R-IB2-01: Plan name persists after save."""
    _open(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.plan_name_input, "Persist Test Plan"
    )
    insurance_billing_page.save_and_assert_success()
    _open(insurance_billing_page)
    assert "Persist Test Plan" in insurance_billing_page.plan_name_input.input_value()
    insurance_billing_page.cancel()


# ===========================================================================
# IB-MEM-R4 — Discount %
# ===========================================================================

@pytest.mark.functional
def test_discount_percentage_valid(insurance_billing_page):
    """TC-F-IB2-04: Valid discount % saves."""
    _open(insurance_billing_page)
    insurance_billing_page.discount_percentage_input.fill("20")
    insurance_billing_page.discount_percentage_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


@pytest.mark.negative
def test_discount_over_100_blocked(insurance_billing_page):
    """TC-N-IB2-07: Discount % > 100 → Save disabled."""
    _open(insurance_billing_page)
    insurance_billing_page.discount_percentage_input.fill("101")
    insurance_billing_page.discount_percentage_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    is_disabled = insurance_billing_page.save_button.is_disabled()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0
    insurance_billing_page.cancel()


@pytest.mark.negative
def test_discount_negative_blocked(insurance_billing_page):
    """TC-N-IB2-07b: Discount % negative → blocked."""
    _open(insurance_billing_page)
    insurance_billing_page.discount_percentage_input.fill("-1")
    insurance_billing_page.discount_percentage_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    is_disabled = insurance_billing_page.save_button.is_disabled()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0
    insurance_billing_page.cancel()


@pytest.mark.boundary
def test_discount_0_accepted(insurance_billing_page):
    """TC-B-IB2-04: Discount % = 0 — minimum valid."""
    _open(insurance_billing_page)
    insurance_billing_page.discount_percentage_input.fill("0")
    insurance_billing_page.discount_percentage_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


@pytest.mark.boundary
def test_discount_100_accepted(insurance_billing_page):
    """TC-B-IB2-05: Discount % = 100 — maximum valid."""
    _open(insurance_billing_page)
    insurance_billing_page.discount_percentage_input.fill("100")
    insurance_billing_page.discount_percentage_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


@pytest.mark.usability
def test_discount_save_disabled_proactively(insurance_billing_page):
    """TC-U-IB2-05: Save disabled proactively when discount invalid."""
    _open(insurance_billing_page)
    insurance_billing_page.discount_percentage_input.fill("150")
    insurance_billing_page.discount_percentage_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    assert insurance_billing_page.save_button.is_disabled(), \
        "Save should be disabled proactively for invalid discount %"
    insurance_billing_page.cancel()


# ===========================================================================
# IB-MEM-R3 — Annual Fee
# ===========================================================================

@pytest.mark.functional
def test_annual_fee_valid_saves(insurance_billing_page):
    """TC-F-IB2-05: Valid annual fee saves."""
    _open(insurance_billing_page)
    insurance_billing_page.annual_fee_input.fill("299")
    insurance_billing_page.annual_fee_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


@pytest.mark.negative
def test_annual_fee_negative_blocked(insurance_billing_page):
    """TC-N-IB2-08: Negative annual fee → blocked."""
    _open(insurance_billing_page)
    insurance_billing_page.annual_fee_input.fill("-1")
    insurance_billing_page.annual_fee_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    is_disabled = insurance_billing_page.save_button.is_disabled()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0
    insurance_billing_page.cancel()


@pytest.mark.boundary
def test_annual_fee_zero_accepted(insurance_billing_page):
    """TC-B-IB2-06: Annual fee = 0 — minimum valid."""
    _open(insurance_billing_page)
    insurance_billing_page.annual_fee_input.fill("0")
    insurance_billing_page.annual_fee_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


@pytest.mark.boundary
def test_annual_fee_large_value_accepted(insurance_billing_page):
    """TC-B-IB2-07: Large annual fee accepted."""
    _open(insurance_billing_page)
    insurance_billing_page.annual_fee_input.fill("9999")
    insurance_billing_page.annual_fee_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


# ===========================================================================
# Delete
# ===========================================================================

@pytest.mark.functional
def test_delete_plan_shows_confirmation(insurance_billing_page):
    """TC-F-IB2-15: Delete membership plan shows confirmation."""
    _open(insurance_billing_page)
    delete_btn = insurance_billing_page.modal.get_by_role("button", name="Delete").first
    if delete_btn.is_visible():
        delete_btn.click()
        insurance_billing_page.page.wait_for_timeout(500)
        insurance_billing_page.assert_delete_confirmation_shown()
        insurance_billing_page.cancel_delete()
    insurance_billing_page.cancel()
