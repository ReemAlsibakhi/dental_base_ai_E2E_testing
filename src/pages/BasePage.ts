import { Page, Locator } from '@playwright/test';

/**
 * BasePage — foundation for all Page Objects.
 *
 * Philosophy:
 *  - Use Playwright's built-in methods — they are well-tested and maintained
 *  - Solve problems at the root, not with workarounds
 *  - Dirty state is a test data problem, not a fill() problem
 *  - unique() ensures every test uses fresh data → no dirty state possible
 */
export abstract class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // -----------------------------------------------------------------------
  // Navigation — enforced contract for every POM
  // -----------------------------------------------------------------------

  abstract navigate(): Promise<void>;

  // -----------------------------------------------------------------------
  // Fill methods
  //
  // Playwright's fill() dispatches real InputEvents internally.
  // React intercepts these correctly in all modern versions.
  //
  // The only fill "problem" we ever faced was dirty state — which is
  // a test data problem, solved by unique() below, not by fill() wrappers.
  // -----------------------------------------------------------------------

  /**
   * Fill any input or textarea.
   * Uses Playwright's fill() — the standard, recommended approach.
   */
  async fill(locator: Locator, value: string): Promise<void> {
    await locator.scrollIntoViewIfNeeded();
    await locator.fill(value);
  }

  /**
   * Fill input[type=email] or input[type=tel] and blur.
   * Tab press triggers validation on fields that validate on blur.
   */
  async fillAndBlur(locator: Locator, value: string): Promise<void> {
    await locator.scrollIntoViewIfNeeded();
    await locator.fill(value);
    await locator.press('Tab');
  }

  // -----------------------------------------------------------------------
  // API response interception
  //
  // Toasts disappear in ~1s — too fast for Playwright to catch reliably.
  // Intercepting the network response is the correct, reliable approach.
  // -----------------------------------------------------------------------

  /**
   * Wait for a successful API mutation response.
   * @param urlPattern - optional filter to avoid catching unrelated requests
   */
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
  // The correct solution to dirty state is unique test data.
  // If every test uses a value that never existed before,
  // React will always see a change — no workarounds needed.
  // -----------------------------------------------------------------------

  /**
   * Generate a unique value for test data isolation.
   * Combines timestamp + random → collision-proof across parallel runs.
   *
   * @example
   * BasePage.unique('Plan')  → 'Plan_lf3k2_4x7'
   */
  static unique(prefix = 'Test'): string {
    return `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 5)}`;
  }
}
