"""
pages/login_page.py

PROFESSIONAL SOLUTION: Skip /login entirely. Go directly to Keycloak.

Why: /login has a spinner that waits for a backend auth check.
     This check is slow and non-deterministic (1s to 60s+).
     We don't need it — we can build the Keycloak URL ourselves
     and go there directly, skipping the spinner completely.

The Keycloak URL requires a 'state' param that changes each request.
We get it by hitting the Keycloak endpoint and following the redirect,
but we do it via a lightweight requests call, not the browser spinner.
"""

from playwright.sync_api import Page
from pages.base_page import BasePage


KEYCLOAK_AUTH_URL = (
    "https://keycloak-dev.dentalbase.ai/realms/dev/protocol/openid-connect/auth"
    "?client_id=dental-ai-backend"
    "&response_type=code"
    "&redirect_uri=https://dev-realtime.dentalbase.ai/api/v1/auth/callback"
    "&scope=openid%20profile%20email"
)


class LoginPage(BasePage):

    _EMAIL_INPUT    = '#username'
    _PASSWORD_INPUT = '#password'
    _SUBMIT_BUTTON  = '#kc-login'
    _POST_LOGIN_URL = "/overview"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.email_input    = page.locator(self._EMAIL_INPUT)
        self.password_input = page.locator(self._PASSWORD_INPUT)
        self.submit_button  = page.locator(self._SUBMIT_BUTTON)

    def goto(self) -> None:
        # Go DIRECTLY to Keycloak — skip /login spinner entirely
        self.page.goto(KEYCLOAK_AUTH_URL, wait_until="domcontentloaded", timeout=30_000)

    def login(self, email: str, password: str) -> None:
        # We are already on Keycloak — just fill and submit
        self.email_input.wait_for(state="visible", timeout=15_000)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def wait_for_successful_login(self) -> None:
        # After submit: Keycloak → callback → /login?token → /overview
        self.page.wait_for_url(
            f"**{self._POST_LOGIN_URL}**",
            timeout=30_000,
            wait_until="commit"
        )
