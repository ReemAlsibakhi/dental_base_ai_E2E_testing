"""
pages/profile_page.py — Page Object for Settings → Profile tab.
All selectors verified from live DOM.
"""

from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class ProfilePage(BasePage):

    # Navigation
    _SETTINGS_URL        = "/settings"
    _PROFILE_TAB         = 'button.border-indigo-500'

    # Profile card
    _EDIT_PROFILE_BUTTON = 'button[type="button"]:has-text("Edit")'

    # Edit Profile panel
    _EDIT_MODAL          = '[role="dialog"][aria-label="Edit Profile"]'
    _FIRST_NAME_INPUT    = '#first_name'
    _LAST_NAME_INPUT     = '#last_name'
    _PHONE_INPUT         = '#phone_number'
    _MODAL_SAVE_BUTTON   = '[role="dialog"][aria-label="Edit Profile"] button:has-text("Save Changes")'
    _MODAL_CANCEL_BUTTON = '[role="dialog"][aria-label="Edit Profile"] button:has-text("Cancel")'
    _CLOSE_PANEL_BUTTON  = 'button[aria-label="Close panel"]'

    # Inline errors — adjacent sibling (stable, not Radix dynamic id)
    _FIRST_NAME_ERROR    = '#first_name + p.text-red-500'
    _LAST_NAME_ERROR     = '#last_name + p.text-red-500'
    _PHONE_ERROR         = '#phone_number + p.text-red-500'

    # Success toast
    _SUCCESS_TOAST       = 'p.text-sm.font-medium:has-text("Profile updated successfully")'

    # Account Users card
    _USER_COUNT_TEXT     = 'p.text-sm.text-gray-500:has-text("users with access")'
    _ADD_USER_BUTTON     = 'button[type="button"]:has-text("Add User")'
    _VIEW_ALL_BUTTON     = 'button[type="button"]:has-text("View all")'

    # Add User panel
    _ADD_USER_MODAL            = '[role="dialog"][aria-label="Add New User"]'
    _ADD_USER_EMAIL_INPUT      = '#email'
    _ADD_USER_FIRST_NAME_INPUT = '[aria-label="Add New User"] #first_name'
    _ADD_USER_LAST_NAME_INPUT  = '[aria-label="Add New User"] #last_name'
    _ADD_USER_USERNAME_INPUT   = '[aria-label="Add New User"] #username'
    _ADD_USER_SUBMIT_BUTTON    = '[aria-label="Add New User"] button:has-text("Add User")'
    _ADD_USER_CANCEL_BUTTON    = '[aria-label="Add New User"] button:has-text("Cancel")'
    _ADD_USER_EMAIL_ERROR      = '#email + p.text-red-500'

    # View All panel
    _VIEW_ALL_MODAL      = '[role="dialog"][aria-label="All Users"]'
    _VIEW_ALL_USER_ROWS  = '[aria-label="All Users"] .space-y-1 > div.flex.items-center'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.edit_profile_button: Locator  = page.locator(self._EDIT_PROFILE_BUTTON)
        self.edit_modal: Locator           = page.locator(self._EDIT_MODAL)
        self.first_name_input: Locator     = page.locator(self._FIRST_NAME_INPUT)
        self.last_name_input: Locator      = page.locator(self._LAST_NAME_INPUT)
        self.phone_input: Locator          = page.locator(self._PHONE_INPUT)
        self.modal_save_button: Locator    = page.locator(self._MODAL_SAVE_BUTTON)
        self.modal_cancel_button: Locator  = page.locator(self._MODAL_CANCEL_BUTTON)
        self.close_panel_button: Locator   = page.locator(self._CLOSE_PANEL_BUTTON)
        self.first_name_error: Locator     = page.locator(self._FIRST_NAME_ERROR)
        self.last_name_error: Locator      = page.locator(self._LAST_NAME_ERROR)
        self.phone_error: Locator          = page.locator(self._PHONE_ERROR)
        self.success_toast: Locator        = page.locator(self._SUCCESS_TOAST)
        self.user_count_text: Locator      = page.locator(self._USER_COUNT_TEXT)
        self.add_user_button: Locator      = page.locator(self._ADD_USER_BUTTON)
        self.view_all_button: Locator      = page.locator(self._VIEW_ALL_BUTTON)
        self.add_user_modal: Locator             = page.locator(self._ADD_USER_MODAL)
        self.add_user_email_input: Locator       = page.locator(self._ADD_USER_EMAIL_INPUT)
        self.add_user_first_name_input: Locator  = page.locator(self._ADD_USER_FIRST_NAME_INPUT)
        self.add_user_last_name_input: Locator   = page.locator(self._ADD_USER_LAST_NAME_INPUT)
        self.add_user_username_input: Locator    = page.locator(self._ADD_USER_USERNAME_INPUT)
        self.add_user_submit_button: Locator     = page.locator(self._ADD_USER_SUBMIT_BUTTON)
        self.add_user_cancel_button: Locator     = page.locator(self._ADD_USER_CANCEL_BUTTON)
        self.add_user_email_error: Locator       = page.locator(self._ADD_USER_EMAIL_ERROR)
        self.view_all_modal: Locator       = page.locator(self._VIEW_ALL_MODAL)
        self.view_all_user_rows: Locator   = page.locator(self._VIEW_ALL_USER_ROWS)

    # ===================================================================
    # NAVIGATION
    # ===================================================================

    def navigate_to_profile(self) -> None:
        self.page.goto(self._SETTINGS_URL, wait_until="commit", timeout=60_000)
        # Wait for Profile Information card — confirms settings loaded
        self.page.locator("text=Profile Information").wait_for(
            state="visible", timeout=30_000
        )
        # Ensure any leftover modals from previous tests are closed
        try:
            if self.page.locator('[role="dialog"]').count() > 0:
                close_btn = self.page.locator('button[aria-label="Close panel"]')
                if close_btn.count() > 0 and close_btn.is_visible():
                    close_btn.click()
        except Exception:
            pass

    # ===================================================================
    # EDIT PROFILE ACTIONS
    # ===================================================================

    def open_edit_modal(self) -> None:
        self.edit_profile_button.first.click()
        expect(self.edit_modal).to_be_visible(timeout=10_000)

    def edit_first_name(self, value: str, *, blur: bool = True) -> None:
        self.first_name_input.clear()
        self.first_name_input.fill(value)
        if blur:
            self.first_name_input.press("Tab")

    def edit_last_name(self, value: str, *, blur: bool = True) -> None:
        self.last_name_input.clear()
        self.last_name_input.fill(value)
        if blur:
            self.last_name_input.press("Tab")

    def edit_phone(self, value: str, *, blur: bool = True) -> None:
        self.phone_input.clear()
        self.phone_input.fill(value)
        if blur:
            self.phone_input.press("Tab")

    def save_profile(self) -> None:
        self.modal_save_button.click()

    def cancel_edit(self) -> None:
        self.modal_cancel_button.click()

    def close_panel(self) -> None:
        self.close_panel_button.click()

    def save_and_assert_success(self) -> None:
        self.save_profile()
        expect(self.success_toast).to_be_visible(timeout=10_000)

    def assert_save_blocked(self) -> None:
        self.save_profile()
        expect(self.edit_modal).to_be_visible()

    # ===================================================================
    # ACCOUNT USERS ACTIONS
    # ===================================================================

    def open_add_user_form(self) -> None:
        self.add_user_button.click()
        expect(self.add_user_modal).to_be_visible(timeout=10_000)

    def cancel_add_user(self) -> None:
        self.add_user_cancel_button.click()

    def open_view_all(self) -> None:
        self.view_all_button.click()
        expect(self.view_all_modal).to_be_visible(timeout=10_000)

    def get_user_count_number(self) -> int:
        return int(self.user_count_text.inner_text().split()[0])

    def get_view_all_row_count(self) -> int:
        return self.view_all_user_rows.count()

    # ===================================================================
    # ASSERTION HELPERS
    # ===================================================================

    def assert_first_name_error(self, message: str) -> None:
        self.assert_error_message(self.first_name_error, message)

    def assert_no_first_name_error(self) -> None:
        self.assert_no_error(self.first_name_error)

    def assert_last_name_error(self, message: str) -> None:
        self.assert_error_message(self.last_name_error, message)

    def assert_no_last_name_error(self) -> None:
        self.assert_no_error(self.last_name_error)

    def assert_phone_error(self, message: str) -> None:
        self.assert_error_message(self.phone_error, message)

    def assert_no_phone_error(self) -> None:
        self.assert_no_error(self.phone_error)

    def assert_add_user_email_error(self, message: str) -> None:
        self.assert_error_message(self.add_user_email_error, message)

    def assert_modal_is_closed(self) -> None:
        expect(self.edit_modal).to_be_hidden(timeout=10_000)

    def assert_add_user_modal_closed(self) -> None:
        expect(self.add_user_modal).to_be_hidden(timeout=10_000)

    def assert_name_on_card(self, expected: str) -> None:
        expect(self.page.locator(
            f'span.text-base.text-gray-900:has-text("{expected}")'
        )).to_be_visible()
