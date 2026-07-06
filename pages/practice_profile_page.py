"""
pages/practice_profile_page.py — Page Object for Settings → Practice Profile & Hours tab.

All selectors confirmed from live DOM inspection (2026-06).

Confirmed name attributes:
  legalName, dbaName, email, website
  address.street, address.city, address.zipCode
  landmarks, description, practiceInfoAdditionalNotes

Selectors without name/id (use label-based):
  Practice Type → select (type=select, no name) — located by label
  Main Phone    → input[type=tel] with label "Main Phone"
  Emergency     → input[type=tel] with label "Emergency Phone"
  State         → select with label "State"
  Timezone      → select with label "Timezone" / value "Pacific/Honolulu"
  Parking       → input[type=checkbox]
"""

from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class PracticeProfilePage(BasePage):

    # Navigation
    _SETTINGS_URL          = "/settings"
    _PRACTICE_PROFILE_TAB  = 'button:has-text("Practice Profile & Hours")'
    # Edit button scoped to Practice Information section
    # 23 Edit buttons exist — only 1 is visible (the Practice Info one)
    # Grandparent contains "Practice Information" text
    _EDIT_BUTTON           = '[class*="min-w-\\[74px\\]"] button'

    # Edit form — confirmed name attributes
    _LEGAL_NAME_INPUT      = '[name="legalName"]'
    _DBA_NAME_INPUT        = '[name="dbaName"]'
    _EMAIL_INPUT           = '[name="email"]'
    _WEBSITE_INPUT         = '[name="website"]'
    _STREET_INPUT          = '[name="address.street"]'
    _CITY_INPUT            = '[name="address.city"]'
    _ZIP_INPUT             = '[name="address.zipCode"]'
    _LANDMARKS_INPUT       = '[name="landmarks"]'
    _DESCRIPTION_INPUT     = '[name="description"]'
    _ADDITIONAL_NOTES      = '[name="practiceInfoAdditionalNotes"]'

    # Selects — no id/name confirmed from DOM
    # Order inside dialog: [0]=Practice Type, [1]=State, [2]=Timezone
    _PRACTICE_TYPE_SELECT  = 'select'   # nth(0)
    _STATE_SELECT          = 'select'   # nth(1)
    _TIMEZONE_SELECT       = 'select'   # nth(2)

    # Phone — type=tel, located by label
    _MAIN_PHONE_INPUT      = '#phone'
    _EMERGENCY_PHONE_INPUT = '#emergencyPhone'

    # Parking toggle
    _PARKING_TOGGLE        = 'input[type="checkbox"]'

    # Buttons
    _SAVE_BUTTON           = 'button:has-text("Save")'
    _CANCEL_BUTTON         = 'button:has-text("Cancel")'

    # Inline errors — adjacent sibling p (same pattern as Profile module)
    _LEGAL_NAME_ERROR      = '[name="legalName"] ~ p[id$="-error"]'
    _DBA_NAME_ERROR        = '[name="dbaName"] ~ p[id$="-error"]'
    _MAIN_PHONE_ERROR      = '#phone ~ p[id$="-error"]'
    _EMERGENCY_PHONE_ERROR = '#emergencyPhone ~ p[id$="-error"]'
    _EMAIL_ERROR           = '[name="email"] ~ p[id$="-error"]'
    _WEBSITE_ERROR         = '[name="website"] ~ p[id$="-error"]'
    _STREET_ERROR          = '[name="address.street"] ~ p[id$="-error"]'
    _CITY_ERROR            = '[name="address.city"] ~ p[id$="-error"]'
    _ZIP_ERROR             = '[name="address.zipCode"] ~ p[id$="-error"]'
    _DESCRIPTION_ERROR     = '[name="description"] ~ p[id$="-error"]'

    # Success toast
    _SUCCESS_TOAST         = '[data-sonner-toast], text=Update in progress, text=updated, text=saved'

    # Description counter
    _DESCRIPTION_COUNTER   = 'span:has-text("/500")'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Inputs
        self.legal_name_input: Locator      = page.locator(self._LEGAL_NAME_INPUT)
        self.dba_name_input: Locator        = page.locator(self._DBA_NAME_INPUT)
        self.email_input: Locator           = page.locator(self._EMAIL_INPUT)
        self.website_input: Locator         = page.locator(self._WEBSITE_INPUT)
        self.street_input: Locator          = page.locator(self._STREET_INPUT)
        self.city_input: Locator            = page.locator(self._CITY_INPUT)
        self.zip_input: Locator             = page.locator(self._ZIP_INPUT)
        self.landmarks_input: Locator       = page.locator(self._LANDMARKS_INPUT)
        self.description_input: Locator     = page.locator(self._DESCRIPTION_INPUT)
        self.additional_notes: Locator      = page.locator(self._ADDITIONAL_NOTES)
        self.main_phone_input: Locator      = page.locator(self._MAIN_PHONE_INPUT)
        self.emergency_phone_input: Locator = page.locator(self._EMERGENCY_PHONE_INPUT)
        self.parking_toggle: Locator        = page.locator(self._PARKING_TOGGLE)

        # Selects — nth(0/1/2) confirmed from live DOM
        self.practice_type_select: Locator  = page.locator('select').nth(0)
        self.state_select: Locator          = page.locator('select').nth(1)
        self.timezone_select: Locator       = page.locator('select').nth(2)

        # Buttons
        self.save_button: Locator           = page.locator(self._SAVE_BUTTON)
        self.cancel_button: Locator         = page.locator(self._CANCEL_BUTTON)

        # Errors
        self.legal_name_error: Locator      = page.locator(self._LEGAL_NAME_ERROR).first
        self.dba_name_error: Locator        = page.locator(self._DBA_NAME_ERROR).first
        self.main_phone_error: Locator      = page.locator(self._MAIN_PHONE_ERROR).first
        self.emergency_phone_error: Locator = page.locator(self._EMERGENCY_PHONE_ERROR).first
        self.email_error: Locator           = page.locator(self._EMAIL_ERROR).first
        self.website_error: Locator         = page.locator(self._WEBSITE_ERROR).first
        self.street_error: Locator          = page.locator(self._STREET_ERROR).first
        self.city_error: Locator            = page.locator(self._CITY_ERROR).first
        self.zip_error: Locator             = page.locator(self._ZIP_ERROR).first
        self.description_error: Locator     = page.locator(self._DESCRIPTION_ERROR).first

        # Toast + counter
        self.success_toast: Locator         = page.locator(self._SUCCESS_TOAST)
        self.description_counter: Locator   = page.locator(self._DESCRIPTION_COUNTER)

    # ===================================================================
    # NAVIGATION
    # ===================================================================

    def navigate_to_practice_profile(self) -> None:
        """
        Navigate to /settings and click Practice Profile & Hours tab.

        With a valid saved session (admin.json), the page loads instantly
        with no spinner — same behaviour as Module 1 navigate_to_profile().
        The tab click takes <1s after the page loads.
        """
        import time
        self.page.goto(self._SETTINGS_URL, wait_until="commit", timeout=60_000)

        # Wait for any settings tab to appear — confirms page loaded
        end = time.time() + 30
        while time.time() < end:
            if self.page.get_by_role(
                "button", name="Practice Profile & Hours", exact=True
            ).is_visible():
                self.page.get_by_role(
                    "button", name="Practice Profile & Hours", exact=True
                ).click()
                self.page.wait_for_timeout(1000)
                return
            time.sleep(0.3)

        raise RuntimeError("Settings page did not load within 30s")

    def open_edit_form(self) -> None:
        # Get the first VISIBLE Edit button using get_by_role
        edit_btn = self.page.get_by_role("button", name="Edit").first
        edit_btn.scroll_into_view_if_needed()
        edit_btn.click()
        self.page.wait_for_selector(self._LEGAL_NAME_INPUT, timeout=10_000)

    # ===================================================================
    # FILL ACTIONS
    # ===================================================================

    def fill_and_blur(self, locator: Locator, value: str) -> None:
        locator.scroll_into_view_if_needed()
        locator.clear()
        locator.fill(value)
        locator.press("Tab")
        self.page.wait_for_timeout(300)

    def fill_legal_name(self, value: str) -> None:
        self.fill_and_blur(self.legal_name_input, value)

    def fill_dba_name(self, value: str) -> None:
        self.fill_and_blur(self.dba_name_input, value)

    def fill_main_phone(self, value: str) -> None:
        self.fill_and_blur(self.main_phone_input, value)

    def fill_emergency_phone(self, value: str) -> None:
        self.fill_and_blur(self.emergency_phone_input, value)

    def fill_email(self, value: str) -> None:
        self.fill_and_blur(self.email_input, value)

    def fill_website(self, value: str) -> None:
        self.fill_and_blur(self.website_input, value)

    def fill_street(self, value: str) -> None:
        self.fill_and_blur(self.street_input, value)

    def fill_city(self, value: str) -> None:
        self.fill_and_blur(self.city_input, value)

    def fill_zip(self, value: str) -> None:
        self.fill_and_blur(self.zip_input, value)

    def fill_description(self, value: str) -> None:
        self.fill_and_blur(self.description_input, value)

    # ===================================================================
    # SAVE / CANCEL
    # ===================================================================

    def save_and_assert_success(self) -> None:
        self.save_button.click()
        expect(self.success_toast).to_be_visible(timeout=10_000)

    def cancel(self) -> None:
        self.cancel_button.click()

    # ===================================================================
    # ASSERTIONS
    # ===================================================================

    def assert_legal_name_error(self, text: str) -> None:
        expect(self.legal_name_error).to_be_visible()
        expect(self.legal_name_error).to_contain_text(text)

    def assert_no_legal_name_error(self) -> None:
        expect(self.legal_name_error).to_be_hidden()

    def assert_dba_error(self, text: str) -> None:
        expect(self.dba_name_error).to_be_visible()
        expect(self.dba_name_error).to_contain_text(text)

    def assert_no_dba_error(self) -> None:
        expect(self.dba_name_error).to_be_hidden()

    def assert_main_phone_error(self, text: str) -> None:
        expect(self.main_phone_error).to_be_visible()
        expect(self.main_phone_error).to_contain_text(text)

    def assert_email_error(self, text: str) -> None:
        expect(self.email_error).to_be_visible()
        expect(self.email_error).to_contain_text(text)

    def assert_website_error(self, text: str) -> None:
        expect(self.website_error).to_be_visible()
        expect(self.website_error).to_contain_text(text)

    def assert_street_error(self, text: str) -> None:
        expect(self.street_error).to_be_visible()
        expect(self.street_error).to_contain_text(text)

    def assert_city_error(self, text: str) -> None:
        expect(self.city_error).to_be_visible()
        expect(self.city_error).to_contain_text(text)

    def assert_zip_error(self, text: str) -> None:
        expect(self.zip_error).to_be_visible()
        expect(self.zip_error).to_contain_text(text)
