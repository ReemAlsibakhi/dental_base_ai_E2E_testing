import { Page, Locator, expect } from '@playwright/test';

/**
 * BasePage — foundation for all Page Objects.
 *
 * Contains shared functionality used across ALL modules:
 *  - Navigation helpers
 *  - Modal interactions (save, cancel, error)
 *  - API response interception
 *  - Test data isolation
 */
export abstract class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // -----------------------------------------------------------------------
  // Navigation — must be implemented by every POM
  // -----------------------------------------------------------------------

  abstract navigate(): Promise<void>;

  /**
   * Open Edit panel by card heading text.
   * Works for all settings modules — finds Edit button next to h3 heading.
   */
  async openEdit(cardName: string): Promise<void> {
    const editBtn = this.page
      .locator('h3')
      .filter({ hasText: cardName })
      .locator('..')
      .locator('..')
      .getByRole('button', { name: 'Edit' })
      .first();
    await editBtn.scrollIntoViewIfNeeded();
    await editBtn.click();
    await expect(this.modal).toBeVisible();
  }

  // -----------------------------------------------------------------------
  // Modal — shared across all modules
  // -----------------------------------------------------------------------

  get modal(): Locator {
    return this.page.locator('[role="dialog"]');
  }

  get saveButton(): Locator {
    return this.modal.getByRole('button', { name: 'Save Changes' });
  }

  get cancelButton(): Locator {
    return this.modal.getByRole('button', { name: 'Cancel' });
  }

  get error(): Locator {
    return this.modal.locator("p[id$='-error']").first();
  }

  async cancel(): Promise<void> {
    try {
      if (await this.cancelButton.isVisible()) {
        await this.cancelButton.click();
        const discard = this.page.getByRole('button', { name: 'Discard' });
        if (await discard.isVisible()) await discard.click();
      }
    } catch { /* panel may already be closed */ }
  }

  async saveAndAssertSuccess(): Promise<void> {
    await this.saveButton.scrollIntoViewIfNeeded();
    // Start listening before click — avoids race condition with fast responses
    await Promise.all([
      this.waitForApiSuccess(),
      this.saveButton.click(),
    ]);
  }

  // -----------------------------------------------------------------------
  // Fill methods
  //
  // Playwright's fill() dispatches real InputEvents internally.
  // React intercepts these correctly in all modern versions.
  // Dirty state is solved by unique() test data — not fill() workarounds.
  // -----------------------------------------------------------------------

  async fill(locator: Locator, value: string): Promise<void> {
    await locator.scrollIntoViewIfNeeded();
    await locator.fill(value);
  }

  async fillAndBlur(locator: Locator, value: string): Promise<void> {
    await locator.scrollIntoViewIfNeeded();
    await locator.fill(value);
    await locator.press('Tab');
  }

  // -----------------------------------------------------------------------
  // API response interception
  //
  // Toasts disappear in ~1s — too fast for Playwright to catch reliably.
  // Network response interception is the correct, reliable approach.
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
  //
  // Unique values prevent dirty state — no fill() workarounds needed.
  // -----------------------------------------------------------------------

  static unique(prefix = 'Test'): string {
    return `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 5)}`;
  }
}
