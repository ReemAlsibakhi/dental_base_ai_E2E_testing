"""pages/login_page.py — Page Object for the Login page (Keycloak SSO)."""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):

    # Landing page CTA (on dentalbase-dev-v2.vercel.app/login)
    _GET_STARTED_BUTTON = 'button:has-text("Get started")'

    # Keycloak form (keycloak-dev.dentalbase.ai)
    _EMAIL_INPUT    = '#username'
    _PASSWORD_INPUT = '#password'
    _SUBMIT_BUTTON  = '#kc-login'

    # URL fragment that confirms successful login
    _POST_LOGIN_URL_FRAGMENT = "/overview"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.get_started_button = page.locator(self._GET_STARTED_BUTTON)
        self.email_input        = page.locator(self._EMAIL_INPUT)
        self.password_input     = page.locator(self._PASSWORD_INPUT)
        self.submit_button      = page.locator(self._SUBMIT_BUTTON)

    def goto(self) -> None:
        self.page.goto("/login")

    def login(self, email: str, password: str) -> None:
        # Step 1: click "Get started" to open Keycloak SSO
        self.get_started_button.click()
        self.page.wait_for_load_state("networkidle")
        # Step 2: fill Keycloak credentials
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def wait_for_successful_login(self) -> None:
        self.page.wait_for_url(f"**{self._POST_LOGIN_URL_FRAGMENT}**")
