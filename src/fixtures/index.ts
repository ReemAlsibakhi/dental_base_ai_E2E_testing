import { test as base, expect, Page } from '@playwright/test';
import { InsuranceBillingPage } from '../pages/InsuranceBillingPage';

/**
 * App-wide typed fixtures.
 *
 * Usage in spec files:
 *   import { test, expect } from '../../src/fixtures';
 *
 * Each fixture creates a fresh page, navigates to the module,
 * and tears down automatically after each test.
 */
type AppFixtures = {
  insuranceBilling: InsuranceBillingPage;
};

export const test = base.extend<AppFixtures>({

  insuranceBilling: async ({ page }: { page: Page }, use) => {
    const ib = new InsuranceBillingPage(page);
    await ib.navigate();
    await use(ib);
    // Teardown: close any open modal
    try {
      const cancel = page.getByRole('button', { name: 'Cancel' });
      if (await cancel.isVisible()) {
        await cancel.click();
        const discard = page.getByRole('button', { name: 'Discard' });
        if (await discard.isVisible()) await discard.click();
      }
    } catch { /* panel may already be closed */ }
  },

});

export { expect };
