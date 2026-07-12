"""
pages/patient_outreach_page.py — Page Object for Settings → Patient Outreach tab.

All selectors confirmed from live DOM inspection (2026-07).

Sub-tabs: button[role="tab"] with text "Global" or "Flows"

Edit buttons (Global tab):
  nth(0) → Master Switch      (top: 309px)
  nth(1) → Preferred Hours    (top: 426px)

Edit buttons (Flows tab):
  nth(0) → Appointment Reminders
  nth(1) → Appointment Confirmation

Confirmed patterns:
  Toggle:   button[role="switch"] (Radix UI — same as Module 2/3)
  Save:     button:has-text("Save Changes")
  Cancel:   button:has-text("Cancel")
  Discard:  button:has-text("Discard Changes")
  Keep:     button:has-text("Keep Editing")
"""

import time
from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class PatientOutreachPage(BasePage):

    _SETTINGS_URL        = "/settings"
    _PATIENT_OUTREACH_TAB = 'button:has-text("Patient Outreach")'

    # Sub-tabs
    _GLOBAL_TAB          = 'button[role="tab"]:has-text("Global")'
    _FLOWS_TAB           = 'button[role="tab"]:has-text("Flows")'

    # Common panel selectors
    _TOGGLE              = 'button[role="switch"]'
    _SAVE_BUTTON         = 'button:has-text("Save Changes")'
    _CANCEL_BUTTON       = 'button:has-text("Cancel")'
    _DISCARD_BUTTON      = 'button:has-text("Discard Changes")'
    _KEEP_EDITING_BUTTON = 'button:has-text("Keep Editing")'

    # Error pattern
    _ERROR               = 'p[id$="-error"]'

    # Flows — Reminders panel
    _ENABLE_FLOW_TOGGLE  = 'button[role="switch"]'
    _MIN_DAYS_INPUT      = 'input[type="number"]'
    _TIMING_INPUT        = 'input[type="number"]'
    _MESSAGE_TEXTAREA    = 'textarea'
    _ADD_ACTION_BUTTON   = 'button:has-text("Add Action")'
    _RESET_DEFAULT_BTN   = 'button:has-text("Reset to default")'

    # Operatories
    _SELECT_ALL_BTN      = 'button:has-text("Select all")'
    _CLEAR_ALL_BTN       = 'button:has-text("Clear all")'

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.save_button:     Locator = page.locator(self._SAVE_BUTTON)
        self.cancel_button:   Locator = page.locator(self._CANCEL_BUTTON)
        self.discard_button:  Locator = page.locator(self._DISCARD_BUTTON)
        self.keep_editing:    Locator = page.locator(self._KEEP_EDITING_BUTTON)
        self.toggle:          Locator = page.locator(self._TOGGLE).first
        self.error:           Locator = page.locator(self._ERROR).first
        self.message_textarea:Locator = page.locator(self._MESSAGE_TEXTAREA).first
        self.min_days_input:  Locator = page.locator(self._MIN_DAYS_INPUT).first
        self.add_action_btn:  Locator = page.locator(self._ADD_ACTION_BUTTON)
        self.select_all_btn:  Locator = page.locator(self._SELECT_ALL_BTN)
        self.clear_all_btn:   Locator = page.locator(self._CLEAR_ALL_BTN)
        self.reset_default:   Locator = page.locator(self._RESET_DEFAULT_BTN)

    # ===================================================================
    # NAVIGATION
    # ===================================================================

    def navigate_to_patient_outreach(self) -> None:
        self.page.goto(self._SETTINGS_URL, wait_until="commit", timeout=60_000)
        end = time.time() + 120
        while time.time() < end:
            tab = self.page.get_by_role("button", name="Patient Outreach", exact=True)
            if tab.is_visible():
                tab.click()
                self.page.wait_for_timeout(1000)
                return
            time.sleep(0.5)
        raise RuntimeError("Patient Outreach tab not found within 120s")

    def click_global_tab(self) -> None:
        self.page.locator(self._GLOBAL_TAB).click()
        self.page.wait_for_timeout(500)

    def click_flows_tab(self) -> None:
        self.page.locator(self._FLOWS_TAB).click()
        self.page.wait_for_timeout(500)

    def open_edit(self, index: int) -> None:
        """Open Edit panel by index (0=Master Switch/Reminders, 1=Preferred Hours/Confirmation)."""
        edit_btns = self.page.get_by_role("button", name="Edit")
        edit_btns.nth(index).scroll_into_view_if_needed()
        edit_btns.nth(index).click()
        self.page.wait_for_timeout(500)

    # ===================================================================
    # TOGGLE
    # ===================================================================

    def is_toggle_on(self, index: int = 0) -> bool:
        return self.page.locator(self._TOGGLE).nth(index).get_attribute("data-state") == "checked"

    def turn_toggle_on(self, index: int = 0) -> None:
        toggle = self.page.locator(self._TOGGLE).nth(index)
        if toggle.get_attribute("data-state") != "checked":
            toggle.click()
            self.page.wait_for_timeout(300)

    def turn_toggle_off(self, index: int = 0) -> None:
        toggle = self.page.locator(self._TOGGLE).nth(index)
        if toggle.get_attribute("data-state") == "checked":
            toggle.click()
            self.page.wait_for_timeout(300)

    # ===================================================================
    # SAVE / CANCEL / DISCARD
    # ===================================================================

    def save(self) -> None:
        self.save_button.scroll_into_view_if_needed()
        self.save_button.click()
        self.page.wait_for_timeout(2000)

    def cancel(self) -> None:
        try:
            self.cancel_button.click()
            self.page.wait_for_timeout(300)
            # Handle discard dialog if it appears
            if self.discard_button.is_visible(timeout=1000):
                self.discard_button.click()
        except Exception:
            pass

    def cancel_without_discard(self) -> None:
        """Cancel when no changes made — no discard dialog expected."""
        try:
            self.cancel_button.click()
            self.page.wait_for_timeout(300)
        except Exception:
            pass
