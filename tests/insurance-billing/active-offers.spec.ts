import { test, expect, Browser } from '@playwright/test';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';
import { BasePage } from '../../src/pages/BasePage';
import { ACTIVE_OFFERS } from '../../src/test-data/insurance-billing';

/**
 * Active Offers — IB-OFF-R1 to R8
 *
 * Truth source: docs/requirements/tab6-insurance-billing.md
 * Test data:    src/test-data/insurance-billing.ts
 * Selectors:    confirmed via Playwright codegen on live app
 *
 * NOT automated (per decision report):
 *   - IB-OFF-R2 Promotion Type dropdown (closed list)
 *   - IB-OFF-R3 Target Audience dropdown (closed list)
 */

test.describe('Active Offers', () => {
  let ib: InsuranceBillingPage;

  test.beforeAll(async ({ browser }: { browser: Browser }) => {
    const context = await browser.newContext({ storageState: '.auth/admin.json' });
    const page    = await context.newPage();
    ib = new InsuranceBillingPage(page);
    await ib.navigate();
  });

  test.afterAll(async () => {
    await ib.page.close();
  });

  test.beforeEach(async () => {
    await ib.openEdit(InsuranceBillingPage.CARD.activeOffers);
  });

  test.afterEach(async () => {
    await ib.cancel();
  });

  // -------------------------------------------------------------------------
  // TC-F-IB2-08 — Add Offer (happy path)
  // -------------------------------------------------------------------------

  test('TC-F-IB2-08 add active offer with all fields', async () => {
    await ib.page.getByText('New PromotionPromotion Name*').click();

    await ib.page.getByRole('spinbutton', { name: 'Promotional Price ($)' }).fill(ACTIVE_OFFERS.promoPrice);
    await ib.page.getByRole('spinbutton', { name: 'Original Price ($)' }).fill(ACTIVE_OFFERS.originalPrice);
    await ib.page.getByRole('textbox', { name: 'Included Services' }).fill('Cleaning, X-ray');
    await ib.page.getByRole('textbox', { name: 'Restrictions/Terms' }).fill('New patients only');

    await ib.page.getByRole('button', { name: 'Add Promotion' }).click();
    await ib.saveAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // IB-OFF-R1 — Promotion Name (inline error on blur, button disabled)
  // -------------------------------------------------------------------------

  test('TC-N-IB2-13 empty promotion name → error inline', async () => {
    const nameField = ib.page.getByText('New PromotionPromotion Name*');
    await nameField.click();
    // Clear the name field in the existing offer
    const existingName = ib.page.getByRole('textbox', { name: 'Promotion Name' });
    if (await existingName.isVisible()) {
      await existingName.clear();
      await existingName.press('Tab');
      await expect(ib.error).toContainText('at least 2 characters');
    }
  });

  test('TC-S-IB2-04 XSS in promotion name → sanitized', async () => {
    const nameField = ib.page.getByRole('textbox', { name: 'Promotion Name' });
    if (await nameField.isVisible()) {
      let alertFired = false;
      ib.page.on('dialog', () => { alertFired = true; });
      await nameField.fill(ACTIVE_OFFERS.xssPayload);
      await ib.page.waitForTimeout(1000);
      expect(alertFired).toBe(false);
    }
  });

  // -------------------------------------------------------------------------
  // IB-OFF-R4 — Promo price > original → DEF-IB2-06 (not enforced)
  // -------------------------------------------------------------------------

  test('DEF-IB2-06 promo price > original price → not enforced (bug)', async () => {
    const promoField    = ib.page.getByRole('spinbutton', { name: 'Promotional Price ($)' });
    const originalField = ib.page.getByRole('spinbutton', { name: 'Original Price ($)' });

    await promoField.fill(ACTIVE_OFFERS.defPromoPrice);
    await originalField.fill(ACTIVE_OFFERS.defOriginalPrice);
    await originalField.press('Tab');

    const hasError = await ib.error.isVisible();
    console.log(`DEF-IB2-06 Promo > Original — error shown: ${hasError}`);
  });
});
