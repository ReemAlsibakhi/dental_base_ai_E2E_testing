import { Page, Locator } from '@playwright/test';

/**
 * BasePage — foundation for all Page Objects.
 *
 * Provides:
 *  - smartFill: React-aware fill that guarantees dirty state
 *  - fillInput: for email/tel inputs (no execCommand support)
 *  - waitForApiSuccess: intercepts POST/PUT/PATCH 2xx responses
 *  - unique: short random string for test data isolation
 */
export abstract class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // -----------------------------------------------------------------------
  // Navigation
  // -----------------------------------------------------------------------

  abstract navigate(): Promise<void>;

  // -----------------------------------------------------------------------
  // React-aware fill
  //
  // execCommand('insertText') is the only method confirmed to trigger
  // React's synthetic onChange event in this app.
  //
  // NOTE: evaluate() callbacks run in browser context — no TypeScript types.
  // -----------------------------------------------------------------------

  async smartFill(locator: Locator, value: string, debounceMs = 500): Promise<void> {
    await locator.scrollIntoViewIfNeeded();
    await locator.click();
    await this.page.waitForTimeout(100);

    const current = await locator.inputValue().catch(() => '');

    // If same value → set temp first to guarantee React sees a change
    if (current === value) {
      const temp = value !== '__tmp__' ? '__tmp__' : '__tmp2__';
      await locator.evaluate((el, t) => {
        const input = el as HTMLInputElement | HTMLTextAreaElement;
        input.focus();
        input.setSelectionRange?.(0, input.value.length);
        document.execCommand('selectAll', false, undefined);
        document.execCommand('delete', false, undefined);
        document.execCommand('insertText', false, t);
      }, temp);
      await this.page.waitForTimeout(300);
    }

    // Set target value
    await locator.evaluate((el, v) => {
      const input = el as HTMLInputElement | HTMLTextAreaElement;
      input.focus();
      input.setSelectionRange?.(0, input.value.length);
      document.execCommand('selectAll', false, undefined);
      document.execCommand('delete', false, undefined);
      if (v) document.execCommand('insertText', false, v);
    }, value);

    await this.page.waitForTimeout(debounceMs);
  }

  /**
   * Fill input[type=email] or input[type=tel] — these don't support execCommand.
   * Uses Playwright's fill() which triggers React onChange directly.
   */
  async fillInput(locator: Locator, value: string): Promise<void> {
    await locator.scrollIntoViewIfNeeded();
    await locator.fill(value);
    await locator.press('Tab');
    await this.page.waitForTimeout(300);
  }

  // -----------------------------------------------------------------------
  // API response interception
  // -----------------------------------------------------------------------

  /**
   * Wait for a successful API mutation (POST/PUT/PATCH → 200/201/204).
   * More reliable than waiting for UI elements (toasts disappear too fast).
   */
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

  /** Generate a short unique string — prevents test data conflicts across runs. */
  static unique(prefix = 'Test'): string {
    return `${prefix}_${Math.random().toString(36).slice(2, 8)}`;
  }
}
