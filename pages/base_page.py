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

    def smart_fill(self, locator: Locator, value: str, *, debounce_ms: int = 500) -> None:
        """
        Universal fill for React-controlled inputs and textareas.

        Strategy:
        1. Click to focus
        2. Read current value
        3. If same as target → set temp value first (guarantees dirty state)
        4. Set target value via execCommand (triggers React onChange)
        5. Wait for debounce

        Works for: input[type=text], textarea
        Does NOT work for: input[type=email], input[type=tel] → use fill() instead
        """
        locator.scroll_into_view_if_needed()
        locator.click()
        self.page.wait_for_timeout(100)

        try:
            current = locator.input_value()
        except Exception:
            current = ""

        # If same value → set temp first to guarantee React sees a change
        if current == value:
            temp = "__tmp__" if value != "__tmp__" else "__tmp2__"
            locator.evaluate(f"""el => {{
                el.focus();
                if (el.setSelectionRange) el.setSelectionRange(0, el.value.length);
                document.execCommand('selectAll', false, null);
                document.execCommand('delete', false, null);
                document.execCommand('insertText', false, {repr(temp)});
            }}""")
            self.page.wait_for_timeout(300)

        # Clear and set target value
        locator.evaluate(f"""el => {{
            el.focus();
            if (el.setSelectionRange) el.setSelectionRange(0, el.value.length);
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);
            {f"document.execCommand('insertText', false, {repr(value)});" if value else ""}
        }}""")
        self.page.wait_for_timeout(debounce_ms)

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
