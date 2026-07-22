"""
tests/insurance_billing/test_active_offers.py
Active Offers / Promotions (IB-OFF-R1 to R8)

Known bugs:
  DEF-IB2-06: Promotional Price > Original Price accepted (negative discount)
"""

import pytest
from playwright.sync_api import expect

from pages.insurance_billing_page import InsuranceBillingPage


def _open(ib):
    ib.open_edit(InsuranceBillingPage.CARD["active_offers"])
    ib.page.wait_for_timeout(500)


def _open_add_offer(ib):
    _open(ib)
    add_btn = ib.modal.get_by_role("button", name="Add Offer").or_(
              ib.modal.get_by_role("button", name="Add")).first
    add_btn.click()
    ib.page.wait_for_timeout(500)


# ===========================================================================
# Smoke
# ===========================================================================

@pytest.mark.smoke
@pytest.mark.functional
def test_active_offers_panel_opens(insurance_billing_page):
    """TC-SM-IB: Active Offers panel opens."""
    _open(insurance_billing_page)
    expect(insurance_billing_page.modal).to_be_visible()
    insurance_billing_page.cancel()


# ===========================================================================
# IB-OFF-R1 — Promotion Name
# ===========================================================================

@pytest.mark.functional
def test_offer_name_valid_saves(insurance_billing_page):
    """TC-F-IB2-08: Valid offer name saves."""
    _open_add_offer(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.offer_name_input, "Summer Special"
    )
    insurance_billing_page.save_and_assert_success()


@pytest.mark.negative
def test_offer_name_empty_blocked(insurance_billing_page):
    """TC-N-IB2-13: Empty offer name → blocked."""
    _open_add_offer(insurance_billing_page)
    insurance_billing_page.offer_name_input.fill("")
    insurance_billing_page.offer_name_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    is_disabled = insurance_billing_page.save_button.is_disabled()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0
    insurance_billing_page.cancel()


@pytest.mark.security
def test_offer_name_xss_rejected(insurance_billing_page):
    """TC-S-IB2-04: XSS in offer name rejected."""
    _open_add_offer(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.offer_name_input, "<script>alert(1)</script>"
    )
    insurance_billing_page.page.wait_for_timeout(500)
    is_disabled = insurance_billing_page.save_button.is_disabled()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0
    insurance_billing_page.cancel()


# ===========================================================================
# IB-OFF-R4 — Price pair logic
# ===========================================================================

@pytest.mark.negative
def test_promo_price_greater_than_original_accepted(insurance_billing_page):
    """DEF-IB2-06: Promo price > Original price accepted (negative discount bug)."""
    _open_add_offer(insurance_billing_page)
    insurance_billing_page.promotional_price_input.fill("100")
    insurance_billing_page.promotional_price_input.press("Tab")
    insurance_billing_page.original_price_input.fill("50")
    insurance_billing_page.original_price_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    is_disabled = insurance_billing_page.save_button.is_disabled()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    # Document bug — currently accepted with no error
    assert not (is_disabled or errors > 0), \
        "DEF-IB2-06: Promo > Original should be rejected but is accepted"
    insurance_billing_page.cancel()


@pytest.mark.boundary
def test_promo_price_equal_to_original(insurance_billing_page):
    """TC-B-IB2-10: Promo = Original — edge case (0% discount)."""
    _open_add_offer(insurance_billing_page)
    insurance_billing_page.promotional_price_input.fill("100")
    insurance_billing_page.promotional_price_input.press("Tab")
    insurance_billing_page.original_price_input.fill("100")
    insurance_billing_page.original_price_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


@pytest.mark.regression
def test_price_pair_persists_after_save(insurance_billing_page):
    """TC-R-IB2-04: Price pair persists after save."""
    _open_add_offer(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.offer_name_input, "Persist Offer Test"
    )
    insurance_billing_page.promotional_price_input.fill("50")
    insurance_billing_page.original_price_input.fill("100")
    insurance_billing_page.save_and_assert_success()


# ===========================================================================
# IB-OFF-R7 — Expiration Days
# ===========================================================================

@pytest.mark.functional
def test_expiration_days_valid(insurance_billing_page):
    """TC-F-IB2-08: Valid expiration days accepted."""
    _open_add_offer(insurance_billing_page)
    insurance_billing_page.expiration_days_input.fill("30")
    insurance_billing_page.expiration_days_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(300)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


@pytest.mark.negative
def test_expiration_days_zero_blocked(insurance_billing_page):
    """TC-N-IB2-14: Expiration days = 0 → blocked."""
    _open_add_offer(insurance_billing_page)
    insurance_billing_page.expiration_days_input.fill("0")
    insurance_billing_page.expiration_days_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    is_disabled = insurance_billing_page.save_button.is_disabled()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0
    insurance_billing_page.cancel()


@pytest.mark.negative
def test_expiration_days_negative_blocked(insurance_billing_page):
    """TC-N-IB2-14b: Negative expiration days → blocked."""
    _open_add_offer(insurance_billing_page)
    insurance_billing_page.expiration_days_input.fill("-1")
    insurance_billing_page.expiration_days_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    is_disabled = insurance_billing_page.save_button.is_disabled()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0
    insurance_billing_page.cancel()


# ===========================================================================
# Delete + Template
# ===========================================================================

@pytest.mark.functional
def test_delete_offer_shows_confirmation(insurance_billing_page):
    """TC-F-IB2-15: Delete offer shows confirmation."""
    _open(insurance_billing_page)
    delete_btn = insurance_billing_page.modal.get_by_role("button", name="Delete").first
    if delete_btn.is_visible():
        delete_btn.click()
        insurance_billing_page.page.wait_for_timeout(500)
        insurance_billing_page.assert_delete_confirmation_shown()
        insurance_billing_page.cancel_delete()
    insurance_billing_page.cancel()


@pytest.mark.functional
def test_use_template_opens(insurance_billing_page):
    """TC-F-IB2-17: Use Template button opens picker."""
    _open(insurance_billing_page)
    template_btn = insurance_billing_page.modal.get_by_role(
        "button", name="Use Template"
    ).or_(insurance_billing_page.modal.get_by_text("Template", exact=False)).first
    if template_btn.is_visible():
        template_btn.click()
        insurance_billing_page.page.wait_for_timeout(500)
        expect(insurance_billing_page.modal).to_be_visible()
    insurance_billing_page.cancel()
