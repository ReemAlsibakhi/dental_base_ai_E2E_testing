"""
pages/insurance_billing_page.py
Page Object Model — Insurance & Billing tab.

URL: /settings?settingTab=Insurance+%26+Billing
Cards (Edit button index):
  18 → Coverage (Accepted Insurance Plans)
  19 → Membership Plans
  20 → Finance
  21 → Service Pricing
  22 → Active Offers
  23 → Pricing Policy
"""

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

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate(self) -> None:
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    def open_edit(self, card_name: str) -> None:
        """Open Edit panel by card heading h3 text — uses XPath sibling search."""
        # Each card row has h3 + Edit button as siblings in a flex container
        # XPath: find h3 with text → go up to row div → find Edit button inside
        edit_btn = self.page.locator(
            f"//h3[contains(text(),'{card_name}')]"
            "/ancestor::div[contains(@class,'flex')][2]"
            "//button[normalize-space()='Edit']"
        ).first
        edit_btn.scroll_into_view_if_needed()
        edit_btn.click()
        self.page.wait_for_timeout(500)

    # ------------------------------------------------------------------
    # Modal
    # ------------------------------------------------------------------

    @property
    def modal(self) -> Locator:
        return self.page.locator('[role="dialog"]')

    @property
    def save_button(self) -> Locator:
        return self.modal.get_by_role("button", name="Save Changes")

    @property
    def cancel_button(self) -> Locator:
        return self.modal.get_by_role("button", name="Cancel")

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
        js = """() => {
            const b = [...document.querySelectorAll('button')]
                .find(b => b.textContent.trim() === 'Save Changes');
            return b && !b.disabled;
        }"""
        self.page.wait_for_function(js, timeout=10_000)
        self.save_button.click(force=True)
        expect(self.page.get_by_text("saved successfully")).to_be_visible(timeout=10_000)

    def click_save(self) -> None:
        self.save_button.click(force=True)
        self.page.wait_for_timeout(500)

    @property
    def error(self) -> Locator:
        return self.modal.locator("p.text-red-500").first

    # ------------------------------------------------------------------
    # Coverage
    # ------------------------------------------------------------------

    @property
    def accept_all_toggle(self) -> Locator:
        return self.modal.locator('button[role="switch"]').first

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

    @property
    def add_custom_button(self) -> Locator:
        return self.modal.get_by_role("button", name="Add Custom")

    # ------------------------------------------------------------------
    # Membership Plans
    # ------------------------------------------------------------------

    @property
    def plan_name_input(self) -> Locator:
        return self.modal.locator('input[name="name"]')

    @property
    def annual_fee_input(self) -> Locator:
        return self.modal.locator('input[name="annualFee"]')

    @property
    def discount_percentage_input(self) -> Locator:
        return self.modal.locator('input[name="discountPercentage"]')

    # ------------------------------------------------------------------
    # Finance
    # ------------------------------------------------------------------

    @property
    def provider_name_input(self) -> Locator:
        return self.modal.locator('input[placeholder*="CareCredit"]')

    @property
    def provider_description(self) -> Locator:
        return self.modal.locator('textarea[placeholder*="Most popular"]')

    @property
    def provider_website(self) -> Locator:
        return self.modal.locator('input[placeholder*="carecredit.com"]')

    @property
    def provider_apr(self) -> Locator:
        return self.modal.locator('input[placeholder="26.99"]')

    @property
    def provider_key_features(self) -> Locator:
        return self.modal.locator('textarea[placeholder*="No prepayment"]')

    @property
    def in_house_financing_toggle(self) -> Locator:
        return self.modal.locator('button[role="switch"]').last

    # ------------------------------------------------------------------
    # Service Pricing
    # ------------------------------------------------------------------

    @property
    def cdt_code_input(self) -> Locator:
        return self.modal.locator('input[name="cdtCode"]')

    @property
    def service_name_input(self) -> Locator:
        return self.modal.locator('input[name="serviceName"]')

    @property
    def service_price_input(self) -> Locator:
        return self.modal.locator('input[name="price"]')

    # ------------------------------------------------------------------
    # Active Offers
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Pricing Policy
    # ------------------------------------------------------------------

    @property
    def good_faith_toggle(self) -> Locator:
        return self.modal.locator('button[role="switch"]').first

    @property
    def custom_ai_script(self) -> Locator:
        return self.modal.locator('textarea').first

    def select_pricing_option(self, text: str) -> None:
        self.modal.get_by_text(text, exact=False).first.click()
        self.page.wait_for_timeout(300)

    # ------------------------------------------------------------------
    # Delete operations
    # ------------------------------------------------------------------

    def confirm_delete(self) -> None:
        self.page.get_by_role("button", name="Delete").last.click()
        self.page.wait_for_timeout(500)

    def assert_delete_confirmation_shown(self) -> None:
        expect(self.page.get_by_text("cannot be undone")).to_be_visible()
