import { test, expect, Browser } from '@playwright/test';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';
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
    await ib.addOfferButton.click();
    await ib.promotionalPriceInput.fill(ACTIVE_OFFERS.promoPrice);
    await ib.originalPriceInput.fill(ACTIVE_OFFERS.originalPrice);
    await ib.includedServicesInput.fill('Cleaning, X-ray');
    await ib.restrictionsTermsInput.fill('New patients only');
    await ib.addPromotionButton.click();
    await ib.saveAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // IB-OFF-R1 — Promotion Name
  // -------------------------------------------------------------------------

  test('TC-N-IB2-13 empty promotion name → error inline', async () => {
    await ib.promotionNameInput.clear();
    await ib.promotionNameInput.press('Tab');
    await expect(ib.error).toContainText('at least 2 characters');
  });

  test('TC-S-IB2-04 XSS in promotion name → sanitized', async () => {
    let alertFired = false;
    ib.page.on('dialog', () => { alertFired = true; });
    await ib.promotionNameInput.fill(ACTIVE_OFFERS.xssPayload);
    await ib.page.waitForTimeout(1000);
    expect(alertFired).toBe(false);
  });

  // -------------------------------------------------------------------------
  // IB-OFF-R4 — Promo price > original → DEF-IB2-06 (not enforced)
  // -------------------------------------------------------------------------

  test('DEF-IB2-06 promo price > original price → not enforced (bug)', async () => {
    await ib.promotionalPriceInput.fill(ACTIVE_OFFERS.defPromoPrice);
    await ib.originalPriceInput.fill(ACTIVE_OFFERS.defOriginalPrice);
    await ib.originalPriceInput.press('Tab');
    // DEF-IB2-06: negative discount not blocked — documenting actual behavior
    const hasError = await ib.error.isVisible();
    console.log(`DEF-IB2-06 Promo > Original — error shown: ${hasError}`);
  });
});
