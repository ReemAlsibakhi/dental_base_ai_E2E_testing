"""
pages/insurance_billing_page.py
Page Object Model — Insurance & Billing tab.

Save pattern (confirmed from live DOM):
  - Toggle-only: Save Changes → API response
  - New Plan form: Save Plan (local) → Save Changes → API response
"""

import uuid
from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class InsuranceBillingPage(BasePage):

    URL = "/settings?settingTab=Insurance+%26+Billing"

    CARD = {
        "coverage":         "Coverage",
        "membership_plans": "Membership Plans",
        "finance":          "Finance",
        "service_pricing":  "Service Pricing",
        "active_offers":    "Active Offers",
        "pricing_policy":   "Pricing Policy",
    }

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @staticmethod
    def unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:6]}"

    # Navigation

    def navigate(self) -> None:
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    def open_edit(self, card_name: str) -> None:
        edit_btn = self.page.locator(
            f"//h3[contains(text(),'{card_name}')]"
            "/ancestor::div[contains(@class,'flex')][2]"
            "//button[normalize-space()='Edit']"
        ).first
        edit_btn.scroll_into_view_if_needed()
        edit_btn.click()
        self.page.wait_for_timeout(500)

    # Modal

    @property
    def modal(self) -> Locator:
        return self.page.locator('[role="dialog"]')

    @property
    def save_button(self) -> Locator:
        return self.modal.get_by_role("button", name="Save Changes")

    @property
    def cancel_button(self) -> Locator:
        return self.modal.get_by_role("button", name="Cancel")

    @property
    def save_plan_button(self) -> Locator:
        return self.modal.get_by_role("button", name="Save Plan")

    @property
    def error(self) -> Locator:
        return self.modal.locator("p[id$='-error']").first

    def cancel(self) -> None:
        try:
            if self.cancel_button.is_visible():
                self.cancel_button.click()
                self.page.wait_for_timeout(300)
                discard = self.page.get_by_role("button", name="Discard")
                if discard.is_visible():
                    discard.click()
        except Exception:
            pass

    def save_and_assert_success(self) -> None:
        """Click Save Changes and verify via API response."""
        self.save_button.scroll_into_view_if_needed()
        with self.page.expect_response(
            lambda r: r.request.method in ("POST", "PUT", "PATCH")
                      and r.status in (200, 201, 204),
            timeout=10_000
        ):
            self.save_button.click()

    def save_plan_and_assert_success(self) -> None:
        """Save Plan (local state) then Save Changes (API)."""
        self.save_plan_button.scroll_into_view_if_needed()
        self.save_plan_button.click()
        self.page.wait_for_timeout(500)
        self.save_and_assert_success()

    def click_save(self) -> None:
        self.save_button.click(force=True)
        self.page.wait_for_timeout(500)

    def assert_delete_confirmation_shown(self) -> None:
        expect(self.page.get_by_text("cannot be undone")).to_be_visible()

    # Coverage

    @property
    def accept_all_toggle(self) -> Locator:
        return self.modal.locator('button[role="switch"]').first

    @property
    def add_custom_button(self) -> Locator:
        return self.modal.get_by_role("button", name="Add Custom")

    @property
    def insurance_name_input(self) -> Locator:
        return self.modal.locator('input[name="name"]')

    @property
    def payer_id_input(self) -> Locator:
        return self.modal.locator('input[name="payerId"]')

    @property
    def preventive_input(self) -> Locator:
        return self.modal.locator('input[name="preventiveCoverage"]')

    @property
    def basic_input(self) -> Locator:
        return self.modal.locator('input[name="basicCoverage"]')

    @property
    def major_input(self) -> Locator:
        return self.modal.locator('input[name="majorCoverage"]')

    @property
    def orthodontic_input(self) -> Locator:
        return self.modal.locator('input[name="orthodonticCoverage"]')

    @property
    def additional_notes(self) -> Locator:
        return self.modal.locator('textarea').first

    def fill_coverage_percentage(self, locator: Locator, value: str) -> None:
        locator.scroll_into_view_if_needed()
        locator.fill(value)
        locator.press("Tab")
        self.page.wait_for_timeout(300)

    def add_plan(self, name: str = None, payer_id: str = "12345") -> None:
        """Open Add Custom → fill required fields → Save Plan → Save Changes."""
        name = name or self.unique("Plan")
        self.add_custom_button.click()
        self.page.wait_for_timeout(500)
        self.smart_fill(self.insurance_name_input, name)
        self.insurance_name_input.press("Tab")
        self.page.wait_for_timeout(300)
        self.smart_fill(self.payer_id_input, payer_id)
        self.payer_id_input.press("Tab")
        self.page.wait_for_timeout(300)
        self.save_plan_and_assert_success()

    # Membership Plans

    @property
    def plan_name_input(self) -> Locator:
        return self.modal.locator('input[name="name"]')

    @property
    def annual_fee_input(self) -> Locator:
        return self.modal.locator('input[name="annualFee"]')

    @property
    def discount_percentage_input(self) -> Locator:
        return self.modal.locator('input[name="discountPercentage"]')

    # Finance

    @property
    def provider_name_input(self) -> Locator:
        return self.modal.locator('input[placeholder*="CareCredit"]')

    @property
    def provider_description(self) -> Locator:
        return self.modal.locator('textarea[placeholder*="Most popular"]')

    @property
    def provider_apr(self) -> Locator:
        return self.modal.locator('input[placeholder="26.99"]')

    @property
    def provider_key_features(self) -> Locator:
        return self.modal.locator('textarea[placeholder*="No prepayment"]')

    @property
    def in_house_financing_toggle(self) -> Locator:
        return self.modal.locator('button[role="switch"]').last

    # Service Pricing

    @property
    def cdt_code_input(self) -> Locator:
        return self.modal.locator('input[name="cdtCode"]')

    @property
    def service_name_input(self) -> Locator:
        return self.modal.locator('input[name="serviceName"]')

    @property
    def service_price_input(self) -> Locator:
        return self.modal.locator('input[name="price"]')

    # Active Offers

    @property
    def offer_name_input(self) -> Locator:
        return self.modal.locator('input[name="name"]')

    @property
    def promotional_price_input(self) -> Locator:
        return self.modal.locator('input[name="price"]')

    @property
    def original_price_input(self) -> Locator:
        return self.modal.locator('input[name="originalPrice"]')

    @property
    def included_services_textarea(self) -> Locator:
        return self.modal.locator('textarea[placeholder*="services separated"]')

    @property
    def restrictions_textarea(self) -> Locator:
        return self.modal.locator('textarea[name="restrictions"]')

    @property
    def expiration_days_input(self) -> Locator:
        return self.modal.locator('input[name="expirationDays"]')

    # Pricing Policy

    @property
    def good_faith_toggle(self) -> Locator:
        return self.modal.locator('button[role="switch"]').first

    @property
    def custom_ai_script(self) -> Locator:
        return self.modal.locator('textarea').first

    def select_pricing_option(self, text: str) -> None:
        self.modal.get_by_text(text, exact=False).first.click()
        self.page.wait_for_timeout(300)
