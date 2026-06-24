"""
pages/profile_page.py — Page Object for Settings → Profile tab.

SELECTORS VERIFIED LIVE via browser automation on:
  https://dentalbase-dev-v2.vercel.app  (2024-06)

Key findings from live DOM inspection:
  ✅ Inputs: have stable `id` AND `name` attributes
  ✅ Modals: have stable `role="dialog"` + `aria-label`
  ✅ Close button: has `aria-label="Close panel"`
  ⚠️  Buttons (Edit/Save/Cancel/Add User/View all): NO id, NO data-testid
       → use :has-text() scoped inside their modal to minimise risk
  ⚠️  Error messages: Radix UI generates dynamic id (_r_9_-error)
       → id changes per session; use `#input_id + p` sibling selector instead
  ⚠️  Profile card text (name, email, phone): NO id, NO data-testid
       → use text-based span selector scoped to card container
"""

from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class ProfilePage(BasePage):

    # ===================================================================
    # LOCATOR CONSTANTS — ALL VERIFIED ON LIVE SITE
    # ===================================================================

    # --- Navigation ---
    # <a href="/settings"> in the left sidebar
    _SETTINGS_NAV_LINK   = 'a[href="/settings"]'
    # Settings tab bar — first button with active border
    _PROFILE_TAB         = 'button.border-indigo-500'          # active tab has this class

    # --- Edit Profile button ---
    # Only button with text "Edit" in the profile card area (top-right of card)
    # Scoped to avoid collision with other "Edit" buttons in future
    _EDIT_PROFILE_BUTTON = 'button[type="button"]:has-text("Edit")'

    # --- Edit Profile Panel ---
    # role=dialog aria-label="Edit Profile" — VERIFIED STABLE
    _EDIT_MODAL          = '[role="dialog"][aria-label="Edit Profile"]'

    # Inputs inside Edit Profile panel — id VERIFIED STABLE
    _FIRST_NAME_INPUT    = '#first_name'          # id="first_name"   ✅
    _LAST_NAME_INPUT     = '#last_name'           # id="last_name"    ✅
    _PHONE_INPUT         = '#phone_number'        # id="phone_number" ✅

    # Buttons inside Edit Profile panel — scoped to modal, text-based
    _MODAL_SAVE_BUTTON   = '[role="dialog"][aria-label="Edit Profile"] button:has-text("Save Changes")'
    _MODAL_CANCEL_BUTTON = '[role="dialog"][aria-label="Edit Profile"] button:has-text("Cancel")'
    # Close X button — aria-label VERIFIED STABLE
    _CLOSE_PANEL_BUTTON  = 'button[aria-label="Close panel"]'

    # --- Inline validation errors ---
    # ⚠️  Radix UI generates dynamic id like _r_9_-error — DO NOT USE id
    # Use CSS adjacent sibling: input#id + p  (p tag immediately after input)
    # class "text-sm text-red-500 mt-1" VERIFIED on live site
    _FIRST_NAME_ERROR    = '#first_name + p.text-red-500'
    _LAST_NAME_ERROR     = '#last_name + p.text-red-500'
    _PHONE_ERROR         = '#phone_number + p.text-red-500'

    # --- Success toast ---
    # <p class="flex-1 text-sm font-medium whitespace-pre-line">Profile updated successfully!</p>
    # VERIFIED on live site after save
    _SUCCESS_TOAST       = 'p.text-sm.font-medium:has-text("Profile updated successfully")'

    # --- Profile card display values (read-only) ---
    # All <span class="text-base text-gray-900"> — no id/data-testid on any
    # We scope by text content which is the user's own data
    _FULL_NAME_DISPLAY   = 'span.text-base.text-gray-900:not(:has-text("@"))'  # "Reem Sibakhi"
    _USERNAME_DISPLAY    = 'span.text-base.text-gray-900:has-text("@")'        # "@reem_user"
    _EMAIL_DISPLAY       = 'span.text-base.text-gray-900:has-text("@gmail")'   # email address
    _PHONE_DISPLAY       = 'span.text-base.text-gray-900:has-text("No phone"), span.text-base.text-gray-900:has-text("(")'

    # --- Account Users card ---
    # <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">47 users with access</p>
    _USER_COUNT_TEXT     = 'p.text-sm.text-gray-500:has-text("users with access")'
    _VIEW_ALL_BUTTON     = 'button[type="button"]:has-text("View all")'
    _ADD_USER_BUTTON     = 'button[type="button"]:has-text("Add User")'

    # --- Add New User panel ---
    # role=dialog aria-label="Add New User" — VERIFIED STABLE
    _ADD_USER_MODAL      = '[role="dialog"][aria-label="Add New User"]'

    # Inputs — id AND name BOTH verified stable
    _ADD_USER_EMAIL_INPUT      = '#email'         # id="email"      name="email"      ariaLabel="Email address" ✅
    _ADD_USER_FIRST_NAME_INPUT = '[aria-label="Add New User"] #first_name'   # id="first_name" name="first_name" ✅
    _ADD_USER_LAST_NAME_INPUT  = '[aria-label="Add New User"] #last_name'    # id="last_name"  name="last_name"  ✅
    _ADD_USER_USERNAME_INPUT   = '[aria-label="Add New User"] #username'     # id="username"   name="username"   ✅

    # Buttons — scoped to modal
    _ADD_USER_SUBMIT_BUTTON    = '[aria-label="Add New User"] button:has-text("Add User")'
    _ADD_USER_CANCEL_BUTTON    = '[aria-label="Add New User"] button:has-text("Cancel")'

    # Error — same Radix pattern; use sibling selector
    _ADD_USER_EMAIL_ERROR      = '#email + p.text-red-500'

    # --- View All Users panel ---
    # role=dialog aria-label="All Users" — VERIFIED STABLE
    _VIEW_ALL_MODAL      = '[role="dialog"][aria-label="All Users"]'
    # Each user row is a flex div inside .space-y-1
    _VIEW_ALL_USER_ROWS  = '[aria-label="All Users"] .space-y-1 > div.flex.items-center'

    # ===================================================================
    # CONSTRUCTOR
    # ===================================================================

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Profile card (read view)
        self.full_name_display: Locator    = page.locator(self._FULL_NAME_DISPLAY).first
        self.username_display: Locator     = page.locator(self._USERNAME_DISPLAY)
        self.email_display: Locator        = page.locator(self._EMAIL_DISPLAY)
        self.phone_display: Locator        = page.locator(self._PHONE_DISPLAY)
        self.edit_profile_button: Locator  = page.locator(self._EDIT_PROFILE_BUTTON)

        # Edit Profile panel
        self.edit_modal: Locator           = page.locator(self._EDIT_MODAL)
        self.first_name_input: Locator     = page.locator(self._FIRST_NAME_INPUT)
        self.last_name_input: Locator      = page.locator(self._LAST_NAME_INPUT)
        self.phone_input: Locator          = page.locator(self._PHONE_INPUT)
        self.modal_save_button: Locator    = page.locator(self._MODAL_SAVE_BUTTON)
        self.modal_cancel_button: Locator  = page.locator(self._MODAL_CANCEL_BUTTON)
        self.close_panel_button: Locator   = page.locator(self._CLOSE_PANEL_BUTTON)

        # Inline errors — adjacent sibling selectors (stable, not Radix dynamic id)
        self.first_name_error: Locator     = page.locator(self._FIRST_NAME_ERROR)
        self.last_name_error: Locator      = page.locator(self._LAST_NAME_ERROR)
        self.phone_error: Locator          = page.locator(self._PHONE_ERROR)

        # Toast
        self.success_toast: Locator        = page.locator(self._SUCCESS_TOAST)

        # Account Users card
        self.user_count_text: Locator      = page.locator(self._USER_COUNT_TEXT)
        self.add_user_button: Locator      = page.locator(self._ADD_USER_BUTTON)
        self.view_all_button: Locator      = page.locator(self._VIEW_ALL_BUTTON)

        # Add New User panel
        self.add_user_modal: Locator             = page.locator(self._ADD_USER_MODAL)
        self.add_user_email_input: Locator       = page.locator(self._ADD_USER_EMAIL_INPUT)
        self.add_user_first_name_input: Locator  = page.locator(self._ADD_USER_FIRST_NAME_INPUT)
        self.add_user_last_name_input: Locator   = page.locator(self._ADD_USER_LAST_NAME_INPUT)
        self.add_user_username_input: Locator    = page.locator(self._ADD_USER_USERNAME_INPUT)
        self.add_user_submit_button: Locator     = page.locator(self._ADD_USER_SUBMIT_BUTTON)
        self.add_user_cancel_button: Locator     = page.locator(self._ADD_USER_CANCEL_BUTTON)
        self.add_user_email_error: Locator       = page.locator(self._ADD_USER_EMAIL_ERROR)

        # View All panel
        self.view_all_modal: Locator       = page.locator(self._VIEW_ALL_MODAL)
        self.view_all_user_rows: Locator   = page.locator(self._VIEW_ALL_USER_ROWS)

    # ===================================================================
    # NAVIGATION
    # ===================================================================

    def navigate_to_profile(self) -> None:
        self.page.goto("/settings")
        self.page.wait_for_load_state("networkidle")
        # Profile is the default active tab — click to be explicit
        self.page.locator(self._PROFILE_TAB).first.click()
        self.page.wait_for_load_state("networkidle")

    # ===================================================================
    # EDIT PROFILE ACTIONS
    # ===================================================================

    def open_edit_modal(self) -> None:
        self.edit_profile_button.first.click()
        expect(self.edit_modal).to_be_visible()

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
        expect(self.success_toast).to_be_visible(timeout=8_000)

    def assert_save_blocked(self) -> None:
        """Click Save — modal must stay open (validation blocked submit)."""
        self.save_profile()
        expect(self.edit_modal).to_be_visible()

    # ===================================================================
    # ACCOUNT USERS ACTIONS
    # ===================================================================

    def open_add_user_form(self) -> None:
        self.add_user_button.click()
        expect(self.add_user_modal).to_be_visible()

    def cancel_add_user(self) -> None:
        self.add_user_cancel_button.click()

    def open_view_all(self) -> None:
        self.view_all_button.click()
        expect(self.view_all_modal).to_be_visible()

    def get_user_count_number(self) -> int:
        """Parse integer from '47 users with access'."""
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
        expect(self.edit_modal).to_be_hidden()

    def assert_add_user_modal_closed(self) -> None:
        expect(self.add_user_modal).to_be_hidden()

    def assert_name_on_card(self, expected: str) -> None:
        expect(self.page.locator(
            f'span.text-base.text-gray-900:has-text("{expected}")'
        )).to_be_visible()
