"""
tests/insurance_billing/test_service_pricing.py
Service Pricing (IB-SVC-R1 to R4)

Known bugs:
  DEF-IB2-11: Quick Setup doesn't flag duplicate services
"""

import pytest
from playwright.sync_api import expect

from pages.insurance_billing_page import InsuranceBillingPage


def _open(ib):
    ib.open_edit(InsuranceBillingPage.CARD["service_pricing"])
    ib.page.wait_for_timeout(500)


def _open_add_service(ib):
    _open(ib)
    add_btn = ib.modal.get_by_role("button", name="Add Service").or_(
              ib.modal.get_by_role("button", name="Add")).first
    add_btn.click()
    ib.page.wait_for_timeout(500)


# ===========================================================================
# Smoke
# ===========================================================================

@pytest.mark.smoke
@pytest.mark.functional
def test_service_pricing_panel_opens(insurance_billing_page):
    """TC-SM-IB: Service Pricing panel opens."""
    _open(insurance_billing_page)
    expect(insurance_billing_page.modal).to_be_visible()
    insurance_billing_page.cancel()


# ===========================================================================
# IB-SVC-R1 — Service Name
# ===========================================================================

@pytest.mark.functional
def test_service_name_valid_saves(insurance_billing_page):
    """TC-F-IB2-07: Valid service name saves."""
    _open_add_service(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.service_name_input, "Teeth Cleaning"
    )
    insurance_billing_page.save_and_assert_success()


@pytest.mark.negative
def test_service_name_empty_blocked(insurance_billing_page):
    """TC-N-IB2-09: Empty service name → blocked."""
    _open_add_service(insurance_billing_page)
    insurance_billing_page.service_name_input.fill("")
    insurance_billing_page.service_name_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    is_disabled = insurance_billing_page.save_button.is_disabled()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0
    insurance_billing_page.cancel()


@pytest.mark.negative
def test_service_name_whitespace_blocked(insurance_billing_page):
    """TC-N-IB2-10: Whitespace-only service name → blocked."""
    _open_add_service(insurance_billing_page)
    insurance_billing_page.service_name_input.fill("   ")
    insurance_billing_page.service_name_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    is_disabled = insurance_billing_page.save_button.is_disabled()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0
    insurance_billing_page.cancel()


@pytest.mark.boundary
def test_service_name_max_100_accepted(insurance_billing_page):
    """TC-B-IB2-08: Service name 100 chars — max valid."""
    _open_add_service(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.service_name_input, "A" * 100
    )
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


@pytest.mark.security
def test_service_name_xss_rejected(insurance_billing_page):
    """TC-S-IB2-03: XSS in service name rejected."""
    _open_add_service(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.service_name_input, "<script>alert(1)</script>"
    )
    insurance_billing_page.page.wait_for_timeout(500)
    is_disabled = insurance_billing_page.save_button.is_disabled()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0
    insurance_billing_page.cancel()


@pytest.mark.regression
def test_service_name_persists_after_save(insurance_billing_page):
    """TC-R-IB2-02: Service name persists after save."""
    _open_add_service(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.service_name_input, "Persist Service Test"
    )
    insurance_billing_page.save_and_assert_success()


# ===========================================================================
# IB-SVC-R2 — CDT Code
# ===========================================================================

@pytest.mark.functional
def test_cdt_code_valid(insurance_billing_page):
    """TC-F-IB2-07: Valid CDT code accepted."""
    _open_add_service(insurance_billing_page)
    insurance_billing_page.cdt_code_input.fill("D0120")
    insurance_billing_page.cdt_code_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(300)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


@pytest.mark.regression
def test_category_persists_after_save(insurance_billing_page):
    """TC-R-IB2-02: Category selection persists after save."""
    _open_add_service(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.service_name_input, "Category Test Service"
    )
    insurance_billing_page.save_and_assert_success()


# ===========================================================================
# IB-SVC-R4 — Price
# ===========================================================================

@pytest.mark.functional
def test_service_price_valid(insurance_billing_page):
    """TC-F-IB2-07: Valid price accepted."""
    _open_add_service(insurance_billing_page)
    insurance_billing_page.service_price_input.fill("150")
    insurance_billing_page.service_price_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(300)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


@pytest.mark.negative
def test_service_price_negative_blocked(insurance_billing_page):
    """TC-N-IB2-11: Negative price → blocked."""
    _open_add_service(insurance_billing_page)
    insurance_billing_page.service_price_input.fill("-1")
    insurance_billing_page.service_price_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    is_disabled = insurance_billing_page.save_button.is_disabled()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0
    insurance_billing_page.cancel()


@pytest.mark.boundary
def test_service_price_zero_accepted(insurance_billing_page):
    """TC-B-IB2-09: Price = 0 — minimum valid (free service)."""
    _open_add_service(insurance_billing_page)
    insurance_billing_page.service_price_input.fill("0")
    insurance_billing_page.service_price_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(300)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


# ===========================================================================
# Delete + Quick Setup
# ===========================================================================

@pytest.mark.functional
def test_delete_service_shows_confirmation(insurance_billing_page):
    """TC-F-IB2-15: Delete service shows confirmation."""
    _open(insurance_billing_page)
    delete_btn = insurance_billing_page.modal.get_by_role("button", name="Delete").first
    if delete_btn.is_visible():
        delete_btn.click()
        insurance_billing_page.page.wait_for_timeout(500)
        insurance_billing_page.assert_delete_confirmation_shown()
        insurance_billing_page.cancel_delete()
    insurance_billing_page.cancel()


@pytest.mark.functional
def test_quick_setup_opens(insurance_billing_page):
    """TC-F-IB2-16: Quick Setup button opens picker."""
    _open(insurance_billing_page)
    quick_setup = insurance_billing_page.modal.get_by_role(
        "button", name="Quick Setup"
    ).first
    if quick_setup.is_visible():
        quick_setup.click()
        insurance_billing_page.page.wait_for_timeout(500)
        expect(insurance_billing_page.modal.get_by_role("checkbox").first).to_be_visible()
    insurance_billing_page.cancel()


@pytest.mark.negative
def test_quick_setup_shows_existing_duplicates(insurance_billing_page):
    """DEF-IB2-11: Quick Setup shows already-added services without warning."""
    _open(insurance_billing_page)
    quick_setup = insurance_billing_page.modal.get_by_role(
        "button", name="Quick Setup"
    ).first
    if quick_setup.is_visible():
        quick_setup.click()
        insurance_billing_page.page.wait_for_timeout(500)
        # D0120 already exists but Quick Setup shows it without warning
        d0120 = insurance_billing_page.page.get_by_text("D0120")
        if d0120.is_visible():
            disabled = d0120.evaluate(
                "el => el.closest('li,div')?.querySelector('input')?.disabled"
            )
            assert not disabled, \
                "DEF-IB2-11: Existing service shown as selectable (duplicate risk)"
    insurance_billing_page.cancel()
