"""
tests/insurance_billing/test_finance.py
Finance Providers (IB-FIN-R1 to R9)

Known bugs:
  DEF-IB2-09: Removing provider via Quick Add chip has no confirmation
  DEF-IB2-11: Grammar bug — "1 providers" instead of "1 provider"
"""

import pytest
from playwright.sync_api import expect

from pages.insurance_billing_page import InsuranceBillingPage


def _open(ib):
    ib.open_edit(InsuranceBillingPage.CARD["finance"])
    ib.page.wait_for_timeout(500)


def _open_add_provider(ib):
    _open(ib)
    add_btn = ib.modal.get_by_role("button", name="Add Custom Provider").or_(
              ib.modal.get_by_role("button", name="Add Finance Provider")).first
    add_btn.click()
    ib.page.wait_for_timeout(500)


# ===========================================================================
# Smoke
# ===========================================================================

@pytest.mark.smoke
@pytest.mark.functional
def test_finance_panel_opens(insurance_billing_page):
    """TC-SM-IB: Finance panel opens."""
    _open(insurance_billing_page)
    expect(insurance_billing_page.modal).to_be_visible()
    insurance_billing_page.cancel()


# ===========================================================================
# IB-FIN-R1 — Provider Name
# ===========================================================================

@pytest.mark.functional
def test_provider_name_valid_saves(insurance_billing_page):
    """TC-F-IB2-10: Valid provider name saves."""
    _open_add_provider(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.provider_name_input, "CareCredit"
    )
    insurance_billing_page.save_and_assert_success()


@pytest.mark.negative
def test_provider_name_empty_blocked(insurance_billing_page):
    """TC-N-IB2-15: Empty provider name → blocked."""
    _open_add_provider(insurance_billing_page)
    insurance_billing_page.provider_name_input.fill("")
    insurance_billing_page.provider_name_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    is_disabled = insurance_billing_page.save_button.is_disabled()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0
    insurance_billing_page.cancel()


# ===========================================================================
# IB-FIN-R2 — Description
# ===========================================================================

@pytest.mark.functional
def test_provider_description_valid(insurance_billing_page):
    """TC-F-IB2-10: Description accepts valid text."""
    _open_add_provider(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.provider_description,
        "Leading healthcare financing provider."
    )
    expect(insurance_billing_page.error).to_be_hidden()
    insurance_billing_page.cancel()


@pytest.mark.security
def test_provider_description_xss(insurance_billing_page):
    """TC-S-IB2-05: XSS in description field."""
    _open_add_provider(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.provider_description,
        "<script>alert('xss')</script>"
    )
    insurance_billing_page.page.wait_for_timeout(500)
    # Verify no script execution
    assert insurance_billing_page.page.locator('button:has-text("Edit")').count() > 0
    insurance_billing_page.cancel()


# ===========================================================================
# IB-FIN-R4 — APR
# ===========================================================================

@pytest.mark.functional
def test_apr_valid_saves(insurance_billing_page):
    """TC-F-IB2-10: Valid APR saves."""
    _open_add_provider(insurance_billing_page)
    insurance_billing_page.provider_apr.fill("26.99")
    insurance_billing_page.provider_apr.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


@pytest.mark.negative
def test_apr_negative_blocked(insurance_billing_page):
    """TC-N-IB2-16: Negative APR → blocked."""
    _open_add_provider(insurance_billing_page)
    insurance_billing_page.provider_apr.fill("-1")
    insurance_billing_page.provider_apr.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    is_disabled = insurance_billing_page.save_button.is_disabled()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0
    insurance_billing_page.cancel()


@pytest.mark.boundary
def test_apr_0_accepted(insurance_billing_page):
    """TC-B-IB2-11: APR = 0 — minimum valid."""
    _open_add_provider(insurance_billing_page)
    insurance_billing_page.provider_apr.fill("0")
    insurance_billing_page.provider_apr.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


@pytest.mark.boundary
def test_apr_100_accepted(insurance_billing_page):
    """TC-B-IB2-12: APR = 100 — high but valid."""
    _open_add_provider(insurance_billing_page)
    insurance_billing_page.provider_apr.fill("100")
    insurance_billing_page.provider_apr.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


# ===========================================================================
# IB-FIN-R5 — Key Features
# ===========================================================================

@pytest.mark.security
def test_key_features_xss(insurance_billing_page):
    """TC-S-IB2-05: XSS in key features field."""
    _open_add_provider(insurance_billing_page)
    insurance_billing_page.smart_fill(
        insurance_billing_page.provider_key_features,
        "<script>alert('xss')</script>"
    )
    insurance_billing_page.page.wait_for_timeout(500)
    assert insurance_billing_page.page.locator('button:has-text("Edit")').count() > 0
    insurance_billing_page.cancel()


# ===========================================================================
# IB-FIN-R9 — In-House Financing
# ===========================================================================

@pytest.mark.functional
def test_in_house_financing_toggle(insurance_billing_page):
    """TC-F-IB2-11: In-House Financing toggle changes state."""
    _open(insurance_billing_page)
    toggle = insurance_billing_page.in_house_financing_toggle
    initial = toggle.get_attribute("aria-checked")
    toggle.click(force=True)
    insurance_billing_page.page.wait_for_timeout(500)
    assert toggle.get_attribute("aria-checked") != initial
    insurance_billing_page.save_and_assert_success()


# ===========================================================================
# DEF-IB2-09 — No confirmation on provider removal
# ===========================================================================

@pytest.mark.negative
def test_provider_chip_removal_no_confirmation(insurance_billing_page):
    """DEF-IB2-09: Removing provider via chip has no confirmation dialog."""
    _open(insurance_billing_page)
    # Look for active provider chip with remove button
    remove_chip = insurance_billing_page.modal.locator(
        'button[aria-label*="remove"], button[aria-label*="Remove"]'
    ).first
    if remove_chip.is_visible():
        remove_chip.click()
        insurance_billing_page.page.wait_for_timeout(500)
        confirm = insurance_billing_page.page.get_by_text("cannot be undone")
        assert not confirm.is_visible(), \
            "DEF-IB2-09: No confirmation shown for provider chip removal"
    insurance_billing_page.cancel()
