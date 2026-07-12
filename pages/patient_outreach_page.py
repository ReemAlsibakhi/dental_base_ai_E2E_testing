"""
pages/patient_outreach_page.py — Page Object for Settings → Patient Outreach tab.

Confirmed selectors (2026-07):
  Sub-tabs: button[role="tab"] — Global / Flows
  Edit buttons: get_by_role("button", name="Edit").nth(0/1)

  Master Switch panel toggles: button[role="switch"] + aria-checked="true/false"
  Preferred Hours panel toggles: button[type="button"] with class containing h-5 w-10
    State: bg-indigo-600 = ON, bg-gray-300 = OFF (no role/aria-checked)

  Save: button:has-text("Save Changes") — use force=True (enabled after toggle click)
"""

import time
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class PatientOutreachPage(BasePage):

    _SETTINGS_URL         = "/settings"
    _GLOBAL_TAB           = 'button[role="tab"]:has-text("Global")'
    _FLOWS_TAB            = 'button[role="tab"]:has-text("Flows")'
    _TOGGLE_SWITCH        = 'button[role="switch"]'
    _HOURS_TOGGLE         = 'button[type="button"]'
    _SAVE_BUTTON          = 'button:has-text("Save Changes")'
    _CANCEL_BUTTON        = 'button:has-text("Cancel")'
    _DISCARD_BUTTON       = 'button:has-text("Discard Changes")'
    _KEEP_EDITING_BUTTON  = 'button:has-text("Keep Editing")'
    _ERROR                = 'p[id$="-error"]'
    _MIN_DAYS_INPUT       = 'input[type="number"]'
    _MESSAGE_TEXTAREA     = 'textarea'
    _ADD_ACTION_BUTTON    = 'button:has-text("Add Action")'
    _RESET_DEFAULT_BTN    = 'button:has-text("Reset to default")'
    _SELECT_ALL_BTN       = 'button:has-text("Select all")'
    _CLEAR_ALL_BTN        = 'button:has-text("Clear all")'

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.save_button:     Locator = page.locator(self._SAVE_BUTTON)
        self.cancel_button:   Locator = page.locator(self._CANCEL_BUTTON)
        self.discard_button:  Locator = page.locator(self._DISCARD_BUTTON)
        self.keep_editing:    Locator = page.locator(self._KEEP_EDITING_BUTTON)
        self.toggle:          Locator = page.locator(self._TOGGLE_SWITCH).first
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
        edit_btns = self.page.get_by_role("button", name="Edit")
        edit_btns.nth(index).scroll_into_view_if_needed()
        edit_btns.nth(index).click()
        self.page.wait_for_timeout(500)

    # ===================================================================
    # MASTER SWITCH PANEL TOGGLES (button[role="switch"] + aria-checked)
    # ===================================================================

    def is_toggle_on(self, index: int = 0) -> bool:
        return self.page.locator(self._TOGGLE_SWITCH).nth(index).get_attribute("aria-checked") == "true"

    def turn_toggle_on(self, index: int = 0) -> None:
        toggle = self.page.locator(self._TOGGLE_SWITCH).nth(index)
        if toggle.get_attribute("aria-checked") != "true":
            toggle.click()
            self.page.wait_for_timeout(300)

    def turn_toggle_off(self, index: int = 0) -> None:
        toggle = self.page.locator(self._TOGGLE_SWITCH).nth(index)
        if toggle.get_attribute("aria-checked") == "true":
            toggle.click()
            self.page.wait_for_timeout(300)

    # ===================================================================
    # PREFERRED HOURS PANEL TOGGLES (plain button + bg class)
    # bg-indigo-600 = ON, bg-gray-300 = OFF
    # Day order: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    # ===================================================================

    def _get_hours_toggles(self):
        """Get all day toggles in Preferred Hours panel."""
        return self.page.locator(
            'button[type="button"]'
        ).filter(has=self.page.locator('[class*="h-5"][class*="w-10"]'))

    def is_hours_toggle_on(self, day_index: int) -> bool:
        """Check day toggle state via bg class."""
        toggles = self.page.locator('button').filter(
            has=self.page.locator('[class*="h-5 w-10"]')
        )
        btn = toggles.nth(day_index)
        classes = btn.evaluate("el => el.className")
        return "bg-indigo" in classes

    def click_hours_toggle(self, day_index: int) -> None:
        """Click a day toggle in Preferred Hours panel."""
        # Find toggles by their visual size (h-5 w-10 = small toggle buttons)
        all_btns = self.page.locator('button[type="button"]').all()
        hours_toggles = [
            b for b in all_btns
            if "h-5" in (b.get_attribute("class") or "") and
               "w-10" in (b.get_attribute("class") or "") and
               b.bounding_box() is not None
        ]
        if day_index < len(hours_toggles):
            hours_toggles[day_index].click()
            self.page.wait_for_timeout(300)

    def get_hours_toggle_count(self) -> int:
        """Count day toggles in Preferred Hours panel."""
        all_btns = self.page.locator('button[type="button"]').all()
        return len([
            b for b in all_btns
            if "h-5" in (b.get_attribute("class") or "") and
               "w-10" in (b.get_attribute("class") or "") and
               b.bounding_box() is not None
        ])

    # ===================================================================
    # SAVE / CANCEL / DISCARD
    # ===================================================================

    def save(self) -> None:
        """Save — force=True since button is enabled after toggle click."""
        self.save_button.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)
        self.save_button.click(force=True)
        self.page.wait_for_timeout(2000)

    def cancel(self) -> None:
        try:
            self.cancel_button.click()
            self.page.wait_for_timeout(300)
            if self.discard_button.is_visible(timeout=1000):
                self.discard_button.click()
        except Exception:
            pass
