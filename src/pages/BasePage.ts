import { Page, Locator } from '@playwright/test';

/**
 * BasePage — foundation for all Page Objects.
 *
 * Provides:
 *  - smartFill: React-aware fill that guarantees dirty state
 *  - fillInput: for email/tel inputs (no execCommand support)
 *  - waitForApiSuccess: intercepts POST/PUT/PATCH 2xx
 *  - unique: UUID-based test data generator
 */
export abstract class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // -----------------------------------------------------------------------
  // React-aware fill
  // -----------------------------------------------------------------------

  async smartFill(locator: Locator, value: string, debounceMs = 500): Promise<void> {
    await locator.scrollIntoViewIfNeeded();
    await locator.click();
    await this.page.waitForTimeout(100);

    const current = await locator.inputValue().catch(() => '');

    if (current === value) {
      const temp = value !== '__tmp__' ? '__tmp__' : '__tmp2__';
      await locator.evaluate((el: HTMLInputElement, t: string) => {
        el.focus();
        el.setSelectionRange?.(0, el.value.length);
        document.execCommand('selectAll', false);
        document.execCommand('delete', false);
        document.execCommand('insertText', false, t);
      }, temp);
      await this.page.waitForTimeout(300);
    }

    await locator.evaluate((el: HTMLInputElement, v: string) => {
      el.focus();
      el.setSelectionRange?.(0, el.value.length);
      document.execCommand('selectAll', false);
      document.execCommand('delete', false);
      if (v) document.execCommand('insertText', false, v);
    }, value);

    await this.page.waitForTimeout(debounceMs);
  }

  async fillInput(locator: Locator, value: string): Promise<void> {
    await locator.scrollIntoViewIfNeeded();
    await locator.fill(value);
    await locator.press('Tab');
    await this.page.waitForTimeout(300);
  }

  // -----------------------------------------------------------------------
  // Wait helpers
  // -----------------------------------------------------------------------

  async waitForApiSuccess(): Promise<void> {
    await this.page.waitForResponse(
      (r) =>
        ['POST', 'PUT', 'PATCH'].includes(r.request().method()) &&
        [200, 201, 204].includes(r.status()),
      { timeout: 15_000 }
    );
  }

  // -----------------------------------------------------------------------
  // Test data
  // -----------------------------------------------------------------------

  static unique(prefix = 'Test'): string {
    return `${prefix}_${Math.random().toString(16).slice(2, 8)}`;
  }
}
