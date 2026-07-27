import { test as base } from '@playwright/test';
import { InsuranceBillingPage } from '../pages/InsuranceBillingPage';

/**
 * Extended test fixtures — typed, reusable across all spec files.
 */
type Fixtures = {
  insuranceBilling: InsuranceBillingPage;
};

export const test = base.extend<Fixtures>({
  insuranceBilling: async ({ page }, use) => {
    const ib = new InsuranceBillingPage(page);
    await ib.navigate();
    await use(ib);
  },
});

export { expect } from '@playwright/test';
