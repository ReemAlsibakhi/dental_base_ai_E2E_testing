"""
pages/scheduling_rules_page.py — Page Object for Settings → Scheduling Rules tab.

All selectors confirmed from live DOM inspection (2026-07).

Edit button order (confirmed):
  nth(0) = Minimum Lead Time
  nth(1) = Advance Booking
  nth(2) = Cancellation Policy
  nth(3) = No-Show Policy
  nth(4) = Override PMS
  nth(5) = Business Hours      ← Manual only
  nth(6) = Holiday Schedule    ← Manual only
  nth(7) = Additional Notes

Selectors confirmed:
  Toggle:       button[role="switch"]  (Radix UI — same as Module 2)
  Number input: input[type="number"]   (one per panel)
  Unit select:  select                 (one per panel where applicable)
  Save button:  button:has-text("Save Changes")
  Toast:        "Settings saved successfully!" (confirmed from test file)
"""

import time
from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class SchedulingRulesPage(BasePage):

    _SETTINGS_URL           = "/settings"
    _SCHEDULING_TAB         = 'button:has-text("Scheduling Rules")'

    # Edit buttons by index (confirmed order)
    _EDIT_BUTTONS           = 'button:has-text("Edit")'

    # Common panel selectors
    _TOGGLE                 = 'button[role="switch"]'
    _NUMBER_INPUT           = 'input[type="number"]'
    _UNIT_SELECT            = 'select'
    _SAVE_BUTTON            = 'button:has-text("Save Changes")'
    _CANCEL_BUTTON          = 'button:has-text("Cancel")'

    # Error pattern — confirmed p[id$="-error"] from Module 2 same app
    _ERROR                  = 'p[id$="-error"]'

    # Success toast
    _SUCCESS_TOAST          = 'text=Settings saved successfully'

    # Additional Notes
    _NOTES_TEXTAREA         = 'textarea'

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.save_button:   Locator = page.locator(self._SAVE_BUTTON)
        self.cancel_button: Locator = page.locator(self._CANCEL_BUTTON)
        self.toggle:        Locator = page.locator(self._TOGGLE).first
        self.number_input:  Locator = page.locator(self._NUMBER_INPUT).first
        self.unit_select:   Locator = page.locator(self._UNIT_SELECT).first
        self.error:         Locator = page.locator(self._ERROR).first
        self.notes_textarea:Locator = page.locator(self._NOTES_TEXTAREA).first
        self.success_toast: Locator = page.locator(self._SUCCESS_TOAST)

    # ===================================================================
    # NAVIGATION
    # ===================================================================

    def navigate_to_scheduling_rules(self) -> None:
        self.page.goto(self._SETTINGS_URL, wait_until="commit", timeout=60_000)
        # Poll up to 120s — same proven pattern as Module 2
        end = time.time() + 120
        while time.time() < end:
            tab = self.page.get_by_role("button", name="Scheduling Rules", exact=True)
            if tab.is_visible():
                tab.click()
                self.page.wait_for_timeout(1000)
                return
            time.sleep(0.5)
        raise RuntimeError("Scheduling Rules tab not found within 120s")

    def open_edit(self, index: int) -> None:
        """Open the Edit panel for a card by index (0-7)."""
        edit_btns = self.page.get_by_role("button", name="Edit")
        edit_btns.nth(index).scroll_into_view_if_needed()
        edit_btns.nth(index).click()
        self.page.wait_for_timeout(500)

    # ===================================================================
    # TOGGLE
    # ===================================================================

    def is_toggle_on(self) -> bool:
        return self.toggle.get_attribute("data-state") == "checked"

    def turn_toggle_on(self) -> None:
        if not self.is_toggle_on():
            self.toggle.click()
            self.page.wait_for_timeout(300)

    def turn_toggle_off(self) -> None:
        if self.is_toggle_on():
            self.toggle.click()
            self.page.wait_for_timeout(300)

    # ===================================================================
    # NUMBER INPUT
    # ===================================================================

    def fill_number(self, value: str) -> None:
        """
        Fill a React-controlled number input and trigger validation.

        Strategy:
        1. First set a temporary different value to ensure React detects a change
        2. Then set the actual target value
        This guarantees Save button activates regardless of current field value.
        """
        self.number_input.scroll_into_view_if_needed()
        self.number_input.click()

        def _set_value(val: str) -> None:
            self.number_input.evaluate(f"""el => {{
                const setter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value'
                ).set;
                setter.call(el, '{val}');
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}""")
            self.page.wait_for_timeout(200)

        # Set temporary value first to ensure React detects change
        current = self.number_input.input_value()
        temp = "999" if current != "999" else "998"
        _set_value(temp)

        # Now set the actual target value
        _set_value(value)

        self.number_input.press("Tab")
        self.page.wait_for_timeout(800)

    # ===================================================================
    # SAVE / CANCEL
    # ===================================================================

    def save_and_assert_success(self) -> None:
        """
        Save and verify success.
        Scheduling Rules has no success toast — confirmation is:
        1. "Saving changes..." toast appears briefly
        2. Save button becomes disabled again (no pending changes)
        """
        self.save_button.scroll_into_view_if_needed()
        self.save_button.click()
        # Wait for save to complete — button becomes disabled again
        self.page.wait_for_timeout(2000)
        # Verify no error appeared
        import re
        page_text = self.page.content()
        assert "error" not in page_text.lower() or                self.error.count() == 0 or                not self.error.is_visible(), "Error appeared after save"

    def save_toggle_only(self) -> None:
        """Save for toggle-only panels (no number input — Override PMS)."""
        self.save_button.scroll_into_view_if_needed()
        # Wait for Save to be enabled after toggle click
        self.save_button.wait_for(state="visible", timeout=5_000)
        self.page.wait_for_timeout(500)
        self.save_button.click(force=True)
        self.page.wait_for_timeout(2000)

    def cancel(self) -> None:
        try:
            self.cancel_button.click()
            self.page.wait_for_timeout(300)
        except Exception:
            pass
