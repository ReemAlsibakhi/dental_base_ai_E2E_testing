import { Page, Locator } from '@playwright/test';

/**
 * BasePage — foundation for all Page Objects.
 *
 * Design decisions:
 *  - abstract: no standalone "base page" exists in the app
 *  - abstract navigate(): every POM must declare its URL
 *  - smartFill: React requires execCommand to trigger synthetic onChange
 *  - waitForApiSuccess: network interception is more reliable than toasts
 *  - static unique(): no instance needed — pure utility
 */
export abstract class BasePage {
  readonly page: Page;

  // Timing constants — named to avoid magic numbers
  private static readonly FOCUS_DELAY_MS = 100;
  private static readonly TEMP_DELAY_MS  = 300;

  constructor(page: Page) {
    this.page = page;
  }

  // -----------------------------------------------------------------------
  // Navigation — must be implemented by every POM
  // -----------------------------------------------------------------------

  abstract navigate(): Promise<void>;

  // -----------------------------------------------------------------------
  // React-aware fill
  // -----------------------------------------------------------------------

  async smartFill(locator: Locator, value: string, debounceMs = 500): Promise<void> {
    await locator.scrollIntoViewIfNeeded();
    await locator.focus();
    await this.page.waitForTimeout(BasePage.FOCUS_DELAY_MS);

    const current = await locator.inputValue().catch(() => {
      // inputValue() fails on non-input elements (e.g. contenteditable)
      return '';
    });

    // Dirty state guarantee: temp → target forces React to see two changes
    if (current === value) {
      const temp = value !== '__tmp__' ? '__tmp__' : '__tmp2__';
      await this._execFill(locator, temp);
      await this.page.waitForTimeout(BasePage.TEMP_DELAY_MS);
    }

    await this._execFill(locator, value);
    await this.page.waitForTimeout(debounceMs);
  }

  /** Internal: select all + insertText via execCommand (only non-deprecated way to trigger React onChange) */
  private async _execFill(locator: Locator, value: string): Promise<void> {
    await locator.evaluate((el, v) => {
      const input = el as HTMLInputElement | HTMLTextAreaElement;
      input.focus();
      // setSelectionRange replaces deprecated execCommand('selectAll') + execCommand('delete')
      input.setSelectionRange(0, input.value.length);
      // insertText with selected text replaces it — only method that triggers React's synthetic onChange
      document.execCommand('insertText', false, v);
    }, value);
  }

  /**
   * Fill input[type=email] or input[type=tel].
   * These don't support setSelectionRange — use Playwright's fill() instead.
   * Includes dirty state guarantee.
   */
  async fillInput(locator: Locator, value: string): Promise<void> {
    await locator.scrollIntoViewIfNeeded();
    const current = await locator.inputValue().catch(() => '');
    // Dirty state guarantee — same value means no React change without this
    if (current === value) {
      await locator.fill('__tmp__');
    }
    await locator.fill(value);
    await locator.press('Tab');
    await this.page.waitForTimeout(BasePage.TEMP_DELAY_MS);
  }

  // -----------------------------------------------------------------------
  // API response interception
  //
  // Toasts disappear in ~1s — too fast for Playwright to catch reliably.
  // Network responses are slower and guaranteed to exist on success.
  // Optional urlPattern to avoid catching unrelated background requests.
  // -----------------------------------------------------------------------

  async waitForApiSuccess(
    urlPattern?: string | RegExp,
    timeout = 15_000
  ): Promise<void> {
    await this.page.waitForResponse(
      (response) => {
        const urlMatch = urlPattern
          ? response.url().match(urlPattern) !== null
          : true;
        return (
          urlMatch &&
          ['POST', 'PUT', 'PATCH'].includes(response.request().method()) &&
          [200, 201, 204].includes(response.status())
        );
      },
      { timeout }
    );
  }

  // -----------------------------------------------------------------------
  // Test data isolation
  // -----------------------------------------------------------------------

  /**
   * Generate a unique string per test run.
   * Combines timestamp + random to make collisions practically impossible.
   * Example: BasePage.unique('Plan') → 'Plan_lf3k2_4x7'
   */
  static unique(prefix = 'Test'): string {
    return `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 5)}`;
  }
}
