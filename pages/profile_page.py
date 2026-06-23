"""
pages/profile_page.py — Page Object for Settings → Profile tab.

Every selector marked # TODO must be confirmed against the live DOM before
the suite can run.  See README.md for the full locator requirements table.

Recommended approach to discover selectors:
  1. Run: playwright codegen https://dentalbase-staging-v2.vercel.app
  2. Interact with each element; copy the generated locator
  3. Replace the TODO strings below
"""

from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class ProfilePage(BasePage):

    # ===================================================================
    # LOCATOR CONSTANTS — ALL TODO VALUES MUST BE REPLACED
    # ===================================================================

    # --- Navigation ---
    _SETTINGS_NAV_LINK = '[data-testid="nav-settings"]'          # TODO
    _PROFILE_TAB = '[data-testid="tab-profile"]'                  # TODO

    # --- Profile Information card (read view) ---
    _FULL_NAME_DISPLAY = '[data-testid="profile-full-name"]'      # TODO
    _PHONE_DISPLAY = '[data-testid="profile-phone"]'              # TODO
    _EMAIL_DISPLAY = '[data-testid="profile-email"]'              # TODO
    _EDIT_PROFILE_BUTTON = '[data-testid="edit-profile-btn"]'     # TODO

    # --- Edit Profile Modal ---
    _EDIT_MODAL = '[data-testid="edit-profile-modal"]'            # TODO
    _FIRST_NAME_INPUT = '[data-testid="first-name-input"]'        # TODO
    _LAST_NAME_INPUT = '[data-testid="last-name-input"]'          # TODO
    _PHONE_INPUT = '[data-testid="phone-input"]'                  # TODO
    _MODAL_SAVE_BUTTON = '[data-testid="modal-save-btn"]'         # TODO
    _MODAL_CANCEL_BUTTON = '[data-testid="modal-cancel-btn"]'     # TODO

    # --- Edit Profile Modal — Inline Errors ---
    _FIRST_NAME_ERROR = '[data-testid="first-name-error"]'        # TODO
    _LAST_NAME_ERROR = '[data-testid="last-name-error"]'          # TODO
    _PHONE_ERROR = '[data-testid="phone-error"]'                  # TODO

    # --- Toast / Notification ---
    _SUCCESS_TOAST = '[data-testid="success-toast"]'              # TODO

    # --- Account Users card ---
    _USER_COUNT_TEXT = '[data-testid="user-count"]'               # TODO
    _ADD_USER_BUTTON = '[data-testid="add-user-btn"]'             # TODO
    _VIEW_ALL_BUTTON = '[data-testid="view-all-btn"]'             # TODO

    # --- Add User Form / Modal ---
    _ADD_USER_MODAL = '[data-testid="add-user-modal"]'            # TODO
    _ADD_USER_EMAIL_INPUT = '[data-testid="add-user-email"]'      # TODO
    _ADD_USER_FIRST_NAME_INPUT = '[data-testid="add-user-first-name"]'  # TODO (confirm exists)
    _ADD_USER_LAST_NAME_INPUT = '[data-testid="add-user-last-name"]'    # TODO (confirm exists)
    _ADD_USER_SUBMIT_BUTTON = '[data-testid="add-user-submit"]'   # TODO
    _ADD_USER_CANCEL_BUTTON = '[data-testid="add-user-cancel"]'   # TODO
    _ADD_USER_EMAIL_ERROR = '[data-testid="add-user-email-error"]'  # TODO

    # --- View All Modal ---
    _VIEW_ALL_MODAL = '[data-testid="view-all-modal"]'            # TODO
    _VIEW_ALL_USER_ROWS = '[data-testid="view-all-user-row"]'     # TODO

    # ===================================================================
    # CONSTRUCTOR
    # ===================================================================

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Profile card
        self.full_name_display: Locator = page.locator(self._FULL_NAME_DISPLAY)
        self.phone_display: Locator = page.locator(self._PHONE_DISPLAY)
        self.email_display: Locator = page.locator(self._EMAIL_DISPLAY)
        self.edit_profile_button: Locator = page.locator(self._EDIT_PROFILE_BUTTON)

        # Edit modal
        self.edit_modal: Locator = page.locator(self._EDIT_MODAL)
        self.first_name_input: Locator = page.locator(self._FIRST_NAME_INPUT)
        self.last_name_input: Locator = page.locator(self._LAST_NAME_INPUT)
        self.phone_input: Locator = page.locator(self._PHONE_INPUT)
        self.modal_save_button: Locator = page.locator(self._MODAL_SAVE_BUTTON)
        self.modal_cancel_button: Locator = page.locator(self._MODAL_CANCEL_BUTTON)

        # Edit modal errors
        self.first_name_error: Locator = page.locator(self._FIRST_NAME_ERROR)
        self.last_name_error: Locator = page.locator(self._LAST_NAME_ERROR)
        self.phone_error: Locator = page.locator(self._PHONE_ERROR)

        # Toast
        self.success_toast: Locator = page.locator(self._SUCCESS_TOAST)

        # Account Users card
        self.user_count_text: Locator = page.locator(self._USER_COUNT_TEXT)
        self.add_user_button: Locator = page.locator(self._ADD_USER_BUTTON)
        self.view_all_button: Locator = page.locator(self._VIEW_ALL_BUTTON)

        # Add User form
        self.add_user_modal: Locator = page.locator(self._ADD_USER_MODAL)
        self.add_user_email_input: Locator = page.locator(self._ADD_USER_EMAIL_INPUT)
        self.add_user_first_name_input: Locator = page.locator(self._ADD_USER_FIRST_NAME_INPUT)
        self.add_user_last_name_input: Locator = page.locator(self._ADD_USER_LAST_NAME_INPUT)
        self.add_user_submit_button: Locator = page.locator(self._ADD_USER_SUBMIT_BUTTON)
        self.add_user_cancel_button: Locator = page.locator(self._ADD_USER_CANCEL_BUTTON)
        self.add_user_email_error: Locator = page.locator(self._ADD_USER_EMAIL_ERROR)

        # View All
        self.view_all_modal: Locator = page.locator(self._VIEW_ALL_MODAL)
        self.view_all_user_rows: Locator = page.locator(self._VIEW_ALL_USER_ROWS)

    # ===================================================================
    # NAVIGATION ACTIONS
    # ===================================================================

    def navigate_to_profile(self) -> None:
        """Navigate to Settings → Profile tab."""
        self.page.goto("/settings")
        self.page.wait_for_load_state("networkidle")
        # Click the Profile tab if the settings page has multiple tabs
        # TODO: adjust if /settings lands directly on the profile tab
        self.page.locator(self._PROFILE_TAB).click()
        self.page.wait_for_load_state("networkidle")

    # ===================================================================
    # EDIT PROFILE MODAL — HIGH-LEVEL ACTIONS
    # ===================================================================

    def open_edit_modal(self) -> None:
        self.edit_profile_button.click()
        expect(self.edit_modal).to_be_visible()

    def save_profile(self) -> None:
        self.modal_save_button.click()

    def cancel_edit(self) -> None:
        self.modal_cancel_button.click()

    def edit_first_name(self, value: str, *, blur: bool = True) -> None:
        """Fill First Name; optionally blur to trigger inline validation."""
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
        """Click save and wait for the success toast."""
        self.save_profile()
        expect(self.success_toast).to_be_visible()

    # ===================================================================
    # ACCOUNT USERS — HIGH-LEVEL ACTIONS
    # ===================================================================

    def open_add_user_form(self) -> None:
        self.add_user_button.click()
        expect(self.add_user_modal).to_be_visible()

    def submit_add_user(self, email: str) -> None:
        """Fill email in Add User form and submit."""
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
        # e.g. "3 users with access" → 3
        return int(text.split()[0])

    def get_view_all_row_count(self) -> int:
        return self.view_all_user_rows.count()

    # ===================================================================
    # ASSERTION HELPERS (profile-specific)
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

    def assert_full_name_on_card(self, expected: str) -> None:
        expect(self.full_name_display).to_contain_text(expected)

    def assert_modal_is_closed(self) -> None:
        expect(self.edit_modal).to_be_hidden()

    def assert_add_user_modal_closed(self) -> None:
        expect(self.add_user_modal).to_be_hidden()

    def assert_save_blocked(self) -> None:
        """Assert that clicking Save does not dismiss the modal (form is still open)."""
        self.save_profile()
        expect(self.edit_modal).to_be_visible()
