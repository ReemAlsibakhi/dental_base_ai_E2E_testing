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
  //
  // Problem: React ignores DOM mutations — it only responds to its own
  // synthetic events. Playwright's fill() doesn't trigger React's onChange
  // in complex controlled inputs.
  //
  // Solution: execCommand('insertText') dispatches a real InputEvent that
  // React intercepts. Confirmed working in Chromium for this app.
  //
  // Dirty state guarantee: if current === target, React sees no change.
  // We set a temp value first to force a state transition.
  // -----------------------------------------------------------------------

  async smartFill(locator: Locator, value: string, debounceMs = 500): Promise<void> {
    await locator.scrollIntoViewIfNeeded();
    await locator.focus();
    await this.page.waitForTimeout(BasePage.FOCUS_DELAY_MS);

    const current = await locator.inputValue().catch(() => '');

    // Dirty state guarantee: temp → target forces React to see two changes
    if (current === value) {
      const temp = value !== '__tmp__' ? '__tmp__' : '__tmp2__';
      await this._execFill(locator, temp);
      await this.page.waitForTimeout(BasePage.TEMP_DELAY_MS);
    }

    await this._execFill(locator, value);
    await this.page.waitForTimeout(debounceMs);
  }

  /** Internal: clear and insert value via execCommand */
  private async _execFill(locator: Locator, value: string): Promise<void> {
    await locator.evaluate((el, v) => {
      const input = el as HTMLInputElement | HTMLTextAreaElement;
      input.focus();
      // Select all existing text then replace with insertText in one operation
      // Avoids deprecated execCommand('selectAll') and execCommand('delete')
      const len = input.value.length;
      input.setSelectionRange(0, len);
      document.execCommand('insertText', false, v);
    }, value);
  }

  /**
   * Fill input[type=email] or input[type=tel].
   * These don't support setSelectionRange — use Playwright's fill() instead.
   * Includes dirty state guarantee via clear → fill pattern.
   */
  async fillInput(locator: Locator, value: string): Promise<void> {
    await locator.scrollIntoViewIfNeeded();
    await locator.clear();
    await locator.fill(value);
    await locator.press('Tab');
    await this.page.waitForTimeout(BasePage.TEMP_DELAY_MS);
  }

  // -----------------------------------------------------------------------
  // API response interception
  //
  // Toasts disappear in ~1s — too fast for Playwright to catch reliably.
  // Network responses are slower and guaranteed to exist on success.
  // -----------------------------------------------------------------------

  async waitForApiSuccess(timeout = 15_000): Promise<void> {
    await this.page.waitForResponse(
      (response) =>
        ['POST', 'PUT', 'PATCH'].includes(response.request().method()) &&
        [200, 201, 204].includes(response.status()),
      { timeout }
    );
  }

  // -----------------------------------------------------------------------
  // Test data isolation
  // -----------------------------------------------------------------------

  /**
   * Generate a unique string per test run.
   * Prevents conflicts when tests create persistent data (plans, providers).
   * Example: BasePage.unique('Plan') → 'Plan_3a7f2c'
   */
  static unique(prefix = 'Test'): string {
    return `${prefix}_${Math.random().toString(36).slice(2, 8)}`;
  }
}
