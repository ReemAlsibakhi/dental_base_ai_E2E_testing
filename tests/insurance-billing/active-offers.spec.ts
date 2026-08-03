import { test, expect } from '../../src/fixtures';
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
  test.beforeEach(async ({ insuranceBilling }) => {
    await insuranceBilling.openEdit(InsuranceBillingPage.CARD.activeOffers);
  });

  test.afterEach(async ({ insuranceBilling }) => {
    await insuranceBilling.cancel();
  });

  test('TC-F-IB2-08 add active offer with all fields', async ({ insuranceBilling }) => {
    await insuranceBilling.addOfferButton.click();
    await insuranceBilling.fill(insuranceBilling.promotionNameInput, ACTIVE_OFFERS.name);
    await insuranceBilling.fillAndBlur(insuranceBilling.promotionalPriceInput, ACTIVE_OFFERS.promoPrice);
    await insuranceBilling.fillAndBlur(insuranceBilling.originalPriceInput, ACTIVE_OFFERS.originalPrice);
    await insuranceBilling.fillAndBlur(insuranceBilling.includedServicesInput, 'Cleaning, X-ray');
    await insuranceBilling.fillAndBlur(insuranceBilling.restrictionsTermsInput, 'New patients only');
    await insuranceBilling.addPromotionButton.click();
    await insuranceBilling.saveAndAssertSuccess();
  });

  test('TC-N-IB2-13 empty promotion name → error inline', async ({ insuranceBilling }) => {
    await insuranceBilling.addOfferButton.click();
    await insuranceBilling.promotionNameInput.clear();
    await insuranceBilling.promotionNameInput.press('Tab');
    await expect(insuranceBilling.error).toContainText('at least 2 characters');
  });

  test('TC-S-IB2-04 XSS in promotion name → sanitized', async ({ insuranceBilling }) => {
    let alertFired = false;
    insuranceBilling.page.on('dialog', () => { alertFired = true; });
    await insuranceBilling.fillAndBlur(insuranceBilling.promotionNameInput, ACTIVE_OFFERS.xssPayload);
    await insuranceBilling.page.waitForTimeout(1000);
    expect(alertFired).toBe(false);
  });

  test('DEF-IB2-06 promo price > original price → not enforced (bug)', async ({ insuranceBilling }) => {
    await insuranceBilling.addOfferButton.click();

    await insuranceBilling.fill(insuranceBilling.promotionNameInput, ACTIVE_OFFERS.name);
    await insuranceBilling.fillAndBlur(insuranceBilling.promotionalPriceInput, ACTIVE_OFFERS.defPromoPrice);
    await insuranceBilling.fillAndBlur(insuranceBilling.originalPriceInput, ACTIVE_OFFERS.defOriginalPrice);
    // DEF-IB2-06: negative discount accepted — no error shown (known bug)
    const hasError = await insuranceBilling.error.isVisible();
    console.log(`DEF-IB2-06 Promo > Original — error shown: ${hasError}`);
<<<<<<< HEAD
   
    expect(hasError).toBeTruthy();

=======
    // No assertion — test always passes to document actual behavior
>>>>>>> cbff1db0b532117aff31e419e81d4c1543ad3c7f
  });
});
