import { test as base, expect } from '@playwright/test';
import { InsuranceBillingPage } from '../pages/InsuranceBillingPage';

type AppFixtures = {
  insuranceBilling: InsuranceBillingPage;
};

export const test = base.extend<AppFixtures>({
  insuranceBilling: async ({ page }, use) => {
    const ib = new InsuranceBillingPage(page);
    await ib.navigate();
    await use(ib);
  },
});

export { expect };
