import { Page, Locator } from '@playwright/test';

/**
 * BasePage — shared utilities for all Page Objects.
 *
 * Responsibilities:
 *  - Navigation helpers
 *  - React-aware fill (triggers onChange via execCommand)
 *  - Unique value generation for test isolation
 */
export abstract class BasePage {
  constructor(protected readonly page: Page) {}

  // -----------------------------------------------------------------------
  // Navigation
  // -----------------------------------------------------------------------

  async navigate(path: string): Promise<void> {
    await this.page.goto(path);
    await this.page.waitForLoadState('networkidle');
  }

  // -----------------------------------------------------------------------
  // React-aware fill
  //
  // Standard fill() triggers React onChange via Playwright's InputEvent.
  // For complex React-controlled inputs that need execCommand, use smartFill().
  // -----------------------------------------------------------------------

  /**
   * Fill a React-controlled input/textarea.
   * Guarantees dirty state even when value === current value.
   */
  async smartFill(locator: Locator, value: string, debounceMs = 500): Promise<void> {
    await locator.scrollIntoViewIfNeeded();
    await locator.click();
    await this.page.waitForTimeout(100);

    const current = await locator.inputValue().catch(() => '');

    // If same value → set temp first to guarantee React sees a change
    if (current === value) {
      const temp = value !== '__tmp__' ? '__tmp__' : '__tmp2__';
      await locator.evaluate((el, t) => {
        el.focus();
        if (el.setSelectionRange) el.setSelectionRange(0, (el as HTMLInputElement).value.length);
        document.execCommand('selectAll', false);
        document.execCommand('delete', false);
        document.execCommand('insertText', false, t);
      }, temp);
      await this.page.waitForTimeout(300);
    }

    // Set target value
    await locator.evaluate((el, v) => {
      el.focus();
      if (el.setSelectionRange) el.setSelectionRange(0, (el as HTMLInputElement).value.length);
      document.execCommand('selectAll', false);
      document.execCommand('delete', false);
      if (v) document.execCommand('insertText', false, v);
    }, value);

    await this.page.waitForTimeout(debounceMs);
  }

  /**
   * Fill input[type=email] or input[type=tel] — these don't support execCommand.
   */
  async fillInput(locator: Locator, value: string): Promise<void> {
    await locator.scrollIntoViewIfNeeded();
    await locator.fill(value);
    await locator.press('Tab');
    await this.page.waitForTimeout(300);
  }

  // -----------------------------------------------------------------------
  // Test data helpers
  // -----------------------------------------------------------------------

  static unique(prefix = 'Test'): string {
    const hex = Math.random().toString(16).slice(2, 8);
    return `${prefix}_${hex}`;
  }

  // -----------------------------------------------------------------------
  // Wait helpers
  // -----------------------------------------------------------------------

  async waitForApiSuccess(): Promise<void> {
    await this.page.waitForResponse(
      (r) => ['POST', 'PUT', 'PATCH'].includes(r.request().method())
            && [200, 201, 204].includes(r.status()),
      { timeout: 10_000 }
    );
  }
}
