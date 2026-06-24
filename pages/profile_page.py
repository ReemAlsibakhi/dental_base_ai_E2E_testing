"""
pages/profile_page.py — Page Object for Settings → Profile tab.

All selectors extracted from the live DOM at:
  https://dentalbase-dev-v2.vercel.app
  (Keycloak SSO: keycloak-dev.dentalbase.ai)

No data-testid attributes exist on this app; selectors use stable
id attributes, aria-label, placeholder, and role-based locators.
"""

from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class ProfilePage(BasePage):

    # ===================================================================
    # LOCATOR CONSTANTS  — extracted from live DOM
    # ===================================================================

    # --- Navigation ---
    _SETTINGS_NAV_LINK = 'a[href="/settings"]'
    _PROFILE_TAB       = 'button:has-text("Profile")'   # first tab in Settings

    # --- Profile Information card (read view) ---
    # Username display: <span class="text-base text-gray-900...">@reem_user</span>
    _USERNAME_DISPLAY  = 'span.text-base.text-gray-900:has-text("@")'
    # Email display
    _EMAIL_DISPLAY     = 'span.text-base.text-gray-900:nth-of-type(2)'
    # Phone display: shows "No phone" when empty
    _PHONE_DISPLAY     = 'span.text-base.text-gray-900:has-text("No phone"), span.text-base.text-gray-900:has-text("(")'
    # Edit button (first "Edit" button on the page — Profile card)
    _EDIT_PROFILE_BUTTON = 'button[type="button"]:has-text("Edit")'

    # --- Edit Profile Panel (slide-in, role=dialog, aria-label="Edit Profile") ---
    _EDIT_MODAL        = '[role="dialog"][aria-label="Edit Profile"]'
    _FIRST_NAME_INPUT  = '#first_name'
    _LAST_NAME_INPUT   = '#last_name'
    _PHONE_INPUT       = '#phone_number'
    _MODAL_SAVE_BUTTON   = '[role="dialog"][aria-label="Edit Profile"] button:has-text("Save Changes")'
    _MODAL_CANCEL_BUTTON = '[role="dialog"][aria-label="Edit Profile"] button:has-text("Cancel")'
    _CLOSE_PANEL_BUTTON  = 'button[aria-label="Close panel"]'

    # --- Inline validation errors (dynamic id pattern: _r_N_-error) ---
    # Errors are <p class="text-sm text-red-500 mt-1"> siblings of their inputs.
    # We locate them relative to their labelled input for robustness.
    _FIRST_NAME_ERROR  = '#first_name ~ p.text-red-500, p:has-text("First name")'
    _LAST_NAME_ERROR   = '#last_name ~ p.text-red-500,  p:has-text("Last name")'
    _PHONE_ERROR       = '#phone_number ~ p.text-red-500, p:has-text("Phone number")'

    # --- Success toast ---
    # <p class="flex-1 text-sm font-medium ...">Profile updated successfully!</p>
    _SUCCESS_TOAST = 'p.text-sm.font-medium:has-text("Profile updated successfully")'

    # --- Account Users card ---
    _USER_COUNT_TEXT   = 'p.text-sm.text-gray-500:has-text("users with access")'
    _VIEW_ALL_BUTTON   = 'button[type="button"]:has-text("View all")'
    _ADD_USER_BUTTON   = 'button[type="button"]:has-text("Add User")'

    # --- Add User panel (role=dialog, aria-label="Add New User") ---
    _ADD_USER_MODAL            = '[role="dialog"][aria-label="Add New User"]'
    _ADD_USER_EMAIL_INPUT      = '#email'                   # type="email", aria-label="Email address"
    _ADD_USER_FIRST_NAME_INPUT = '[role="dialog"][aria-label="Add New User"] #first_name'
    _ADD_USER_LAST_NAME_INPUT  = '[role="dialog"][aria-label="Add New User"] #last_name'
    _ADD_USER_USERNAME_INPUT   = '[role="dialog"][aria-label="Add New User"] #username'
    _ADD_USER_SUBMIT_BUTTON    = '[role="dialog"][aria-label="Add New User"] button:has-text("Add User")'
    _ADD_USER_CANCEL_BUTTON    = '[role="dialog"][aria-label="Add New User"] button:has-text("Cancel")'
    _ADD_USER_EMAIL_ERROR      = '#email ~ p.text-red-500, [role="dialog"][aria-label="Add New User"] p.text-red-500'

    # --- View All panel (role=dialog, aria-label="All Users") ---
    _VIEW_ALL_MODAL     = '[role="dialog"][aria-label="All Users"]'
    # Each user row: div containing name + email + role badge
    _VIEW_ALL_USER_ROWS = '[role="dialog"][aria-label="All Users"] .space-y-1 > div.flex.items-center'

    # ===================================================================
    # CONSTRUCTOR
    # ===================================================================

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Profile card
        self.username_display: Locator    = page.locator(self._USERNAME_DISPLAY)
        self.email_display: Locator       = page.locator(self._EMAIL_DISPLAY)
        self.phone_display: Locator       = page.locator(self._PHONE_DISPLAY)
        self.edit_profile_button: Locator = page.locator(self._EDIT_PROFILE_BUTTON)

        # Edit modal
        self.edit_modal: Locator          = page.locator(self._EDIT_MODAL)
        self.first_name_input: Locator    = page.locator(self._FIRST_NAME_INPUT)
        self.last_name_input: Locator     = page.locator(self._LAST_NAME_INPUT)
        self.phone_input: Locator         = page.locator(self._PHONE_INPUT)
        self.modal_save_button: Locator   = page.locator(self._MODAL_SAVE_BUTTON)
        self.modal_cancel_button: Locator = page.locator(self._MODAL_CANCEL_BUTTON)
        self.close_panel_button: Locator  = page.locator(self._CLOSE_PANEL_BUTTON)

        # Inline errors
        self.first_name_error: Locator    = page.locator(self._FIRST_NAME_ERROR)
        self.last_name_error: Locator     = page.locator(self._LAST_NAME_ERROR)
        self.phone_error: Locator         = page.locator(self._PHONE_ERROR)

        # Toast
        self.success_toast: Locator       = page.locator(self._SUCCESS_TOAST)

        # Account Users card
        self.user_count_text: Locator     = page.locator(self._USER_COUNT_TEXT)
        self.add_user_button: Locator     = page.locator(self._ADD_USER_BUTTON)
        self.view_all_button: Locator     = page.locator(self._VIEW_ALL_BUTTON)

        # Add User panel
        self.add_user_modal: Locator            = page.locator(self._ADD_USER_MODAL)
        self.add_user_email_input: Locator      = page.locator(self._ADD_USER_EMAIL_INPUT)
        self.add_user_first_name_input: Locator = page.locator(self._ADD_USER_FIRST_NAME_INPUT)
        self.add_user_last_name_input: Locator  = page.locator(self._ADD_USER_LAST_NAME_INPUT)
        self.add_user_username_input: Locator   = page.locator(self._ADD_USER_USERNAME_INPUT)
        self.add_user_submit_button: Locator    = page.locator(self._ADD_USER_SUBMIT_BUTTON)
        self.add_user_cancel_button: Locator    = page.locator(self._ADD_USER_CANCEL_BUTTON)
        self.add_user_email_error: Locator      = page.locator(self._ADD_USER_EMAIL_ERROR)

        # View All panel
        self.view_all_modal: Locator      = page.locator(self._VIEW_ALL_MODAL)
        self.view_all_user_rows: Locator  = page.locator(self._VIEW_ALL_USER_ROWS)

    # ===================================================================
    # NAVIGATION
    # ===================================================================

    def navigate_to_profile(self) -> None:
        """Navigate to /settings and ensure the Profile tab is active."""
        self.page.goto("/settings")
        self.page.wait_for_load_state("networkidle")
        # Profile tab is active by default; click it to be explicit
        profile_tab = self.page.locator(self._PROFILE_TAB).first
        profile_tab.click()
        self.page.wait_for_load_state("networkidle")

    # ===================================================================
    # EDIT PROFILE PANEL
    # ===================================================================

    def open_edit_modal(self) -> None:
        self.edit_profile_button.first.click()
        expect(self.edit_modal).to_be_visible()

    def save_profile(self) -> None:
        self.modal_save_button.click()

    def cancel_edit(self) -> None:
        self.modal_cancel_button.click()

    def close_panel(self) -> None:
        self.close_panel_button.click()

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

    def save_and_assert_success(self) -> None:
        self.save_profile()
        expect(self.success_toast).to_be_visible(timeout=8_000)

    # ===================================================================
    # ACCOUNT USERS
    # ===================================================================

    def open_add_user_form(self) -> None:
        self.add_user_button.click()
        expect(self.add_user_modal).to_be_visible()

    def submit_add_user(self, email: str) -> None:
        self.add_user_email_input.fill(email)
        self.add_user_submit_button.click()

    def cancel_add_user(self) -> None:
        self.add_user_cancel_button.click()

    def open_view_all(self) -> None:
        self.view_all_button.click()
        expect(self.view_all_modal).to_be_visible()

    def get_user_count_number(self) -> int:
        """Parse the integer from 'N users with access'."""
        text = self.user_count_text.inner_text()
        return int(text.split()[0])

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

    def assert_name_on_card(self, expected: str) -> None:
        """Assert expected text appears anywhere in the profile card area."""
        expect(self.page.locator(f'span.text-base.text-gray-900:has-text("{expected}")')).to_be_visible()

    def assert_modal_is_closed(self) -> None:
        expect(self.edit_modal).to_be_hidden()

    def assert_add_user_modal_closed(self) -> None:
        expect(self.add_user_modal).to_be_hidden()

    def assert_save_blocked(self) -> None:
        """Click Save and verify the panel stays open (validation blocked submit)."""
        self.save_profile()
        expect(self.edit_modal).to_be_visible()
