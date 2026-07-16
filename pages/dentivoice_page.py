"""
pages/dentivoice_page.py — Page Object for Settings → DentiVoice™ Customization tab.

All selectors confirmed from live DOM inspection (2026-07).

Edit button order (confirmed):
  nth(0) = AI Identity
  nth(1) = Terminology & Pronunciation
  nth(2) = Emergency Handling (Configure)
  nth(3) = Call Transfer
  nth(4) = SMS & Email Alerts

AI Identity panel fields (confirmed):
  Assistant Name:      input[name="aiName"]
  Personality:         select
  AI Disclosure:       button[role="switch"]
  Initial Greeting:    textarea[name="firstMessage"]
  After-Hours:         textarea[name="afterHoursGreeting"]

Terminology panel fields (confirmed):
  Additional Instructions: textarea[name="additionalInstructions"]
  Daily Email Report:      button[role="switch"] nth(0)
  Send Task Emails:        button[role="switch"] nth(1)
  Reveal Provider Details: button[role="switch"] nth(2)
  Additional Notes:        textarea[name="aiCustomizationAdditionalNotes"]

Save pattern (confirmed):
  - Save button activates on dirty state (real change only)
  - Toast: "Settings saved successfully!" (green, top-right)
  - Modal closes automatically after save
"""

import time
from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class DentiVoicePage(BasePage):

    _SETTINGS_URL     = "/settings"
    _TAB_NAME         = "DentiVoice™ Customization"

    # Common
    _SAVE_BUTTON      = 'button:has-text("Save Changes")'
    _CANCEL_BUTTON    = 'button:has-text("Cancel")'
    _SUCCESS_TOAST    = 'text=Settings saved successfully'
    _ERROR            = 'p[id$="-error"]'

    # AI Identity panel
    _AI_NAME_INPUT    = 'input[name="aiName"]'
    _PERSONALITY_SELECT = 'select'
    _TOGGLE_SWITCH    = 'button[role="switch"]'

    # Greetings
    _FIRST_MESSAGE    = 'textarea[name="firstMessage"]'
    _AFTER_HOURS      = 'textarea[name="afterHoursGreeting"]'

    # Terminology panel
    _ADDITIONAL_INSTRUCTIONS = 'textarea[name="additionalInstructions"]'
    _ADDITIONAL_NOTES        = 'textarea[name="aiCustomizationAdditionalNotes"]'

    # Card indices
    CARD = {
        "ai_identity":   0,
        "terminology":   1,
        "emergency":     2,
        "call_transfer": 3,
        "sms_email":     4,
    }

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.save_button:    Locator = page.locator(self._SAVE_BUTTON)
        self.cancel_button:  Locator = page.locator(self._CANCEL_BUTTON)
        self.success_toast:  Locator = page.locator(self._SUCCESS_TOAST)
        self.error:          Locator = page.locator(self._ERROR).first
        self.ai_name_input:  Locator = page.locator(self._AI_NAME_INPUT)
        self.personality:    Locator = page.locator(self._PERSONALITY_SELECT).first
        self.first_message:  Locator = page.locator(self._FIRST_MESSAGE)
        self.after_hours:    Locator = page.locator(self._AFTER_HOURS)
        self.add_instructions: Locator = page.locator(self._ADDITIONAL_INSTRUCTIONS)
        self.add_notes:      Locator = page.locator(self._ADDITIONAL_NOTES)

    # ===================================================================
    # NAVIGATION
    # ===================================================================

    def navigate_to_dentivoice(self) -> None:
        self.page.goto(self._SETTINGS_URL, wait_until="commit", timeout=60_000)
        end = time.time() + 120
        while time.time() < end:
            tab = self.page.get_by_role("button", name=self._TAB_NAME, exact=True)
            if tab.is_visible():
                tab.click()
                self.page.wait_for_timeout(1000)
                return
            time.sleep(0.5)
        raise RuntimeError("DentiVoice tab not found within 120s")

    def open_edit(self, index: int) -> None:
        """Open Edit/Configure panel by card index."""
        edit_btns = self.page.get_by_role("button", name="Edit")
        configure_btn = self.page.get_by_role("button", name="Configure")

        if index == self.CARD["emergency"]:
            configure_btn.scroll_into_view_if_needed()
            configure_btn.click()
        else:
            # Adjust index for non-emergency cards
            adj_index = index if index < self.CARD["emergency"] else index - 1
            edit_btns.nth(adj_index).scroll_into_view_if_needed()
            edit_btns.nth(adj_index).click()

        self.page.wait_for_timeout(500)

    # ===================================================================
    # TOGGLE
    # ===================================================================

    def is_toggle_on(self, index: int = 0) -> bool:
        return self.page.locator(self._TOGGLE_SWITCH).nth(index).get_attribute("aria-checked") == "true"

    def click_toggle(self, index: int = 0) -> None:
        self.page.locator(self._TOGGLE_SWITCH).nth(index).click()
        self.page.wait_for_timeout(300)

    # ===================================================================
    # FILL HELPERS
    # ===================================================================

    def fill_ai_name(self, value: str) -> None:
        """Fill Assistant Name — triple click to select all, then type via keyboard."""
        self.ai_name_input.scroll_into_view_if_needed()
        self.ai_name_input.click(click_count=3)
        self.page.wait_for_timeout(100)
        self.ai_name_input.press("Control+a")
        self.ai_name_input.press("Backspace")
        self.page.wait_for_timeout(100)
        if value:
            self.ai_name_input.press_sequentially(value, delay=50)
        self.page.wait_for_timeout(300)

    def fill_textarea(self, locator: Locator, value: str) -> None:
        """Fill a textarea using native setter to trigger React onChange."""
        escaped = value.replace("\\", "\\\\").replace("'", "\\'")
        js = f"""el => {{
            const setter = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, 'value').set;
            setter.call(el, '{escaped}');
            el.dispatchEvent(new Event('input', {{bubbles: true}}));
            el.dispatchEvent(new Event('change', {{bubbles: true}}));
        }}"""
        locator.evaluate(js)
        self.page.wait_for_timeout(300)

    # ===================================================================
    # SAVE / CANCEL
    # ===================================================================

    def save_and_assert_success(self) -> None:
        """Save and verify toast 'Settings saved successfully!'"""
        self.save_button.scroll_into_view_if_needed()
        self.save_button.click()
        expect(self.success_toast).to_be_visible(timeout=10_000)

    def cancel(self) -> None:
        try:
            self.cancel_button.click()
            self.page.wait_for_timeout(300)
        except Exception:
            pass
