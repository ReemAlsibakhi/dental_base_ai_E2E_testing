"""pages/base_page.py — Abstract base class for all Page Objects."""

from playwright.sync_api import Page, Locator, expect


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def goto(self, path: str = "") -> None:
        self.page.goto(path)

    def wait_for_network_idle(self) -> None:
        self.page.wait_for_load_state("networkidle")

    # ------------------------------------------------------------------
    # Field interactions
    # ------------------------------------------------------------------

    def fill_and_blur(self, locator: Locator, value: str) -> None:
        """Fill a field and immediately tab away to trigger inline validation."""
        locator.fill(value)
        locator.press("Tab")

    def clear_and_blur(self, locator: Locator) -> None:
        """Clear a field and blur it."""
        locator.clear()
        locator.press("Tab")

    # ------------------------------------------------------------------
    # Assertions helpers
    # ------------------------------------------------------------------

    def assert_visible(self, locator: Locator) -> None:
        expect(locator).to_be_visible()

    def assert_hidden(self, locator: Locator) -> None:
        expect(locator).to_be_hidden()

    def assert_error_message(self, error_locator: Locator, message: str) -> None:
        expect(error_locator).to_be_visible()
        expect(error_locator).to_contain_text(message)

    def assert_no_error(self, error_locator: Locator) -> None:
        expect(error_locator).to_be_hidden()

    def assert_field_value(self, locator: Locator, value: str) -> None:
        expect(locator).to_have_value(value)
