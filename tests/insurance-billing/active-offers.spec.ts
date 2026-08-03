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
    await insuranceBilling.fillAndBlur(insuranceBilling.includedServicesInput, ACTIVE_OFFERS.includedServices);
    await insuranceBilling.fillAndBlur(insuranceBilling.restrictionsTermsInput, ACTIVE_OFFERS.restrictions);
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

  // -------------------------------------------------------------------------
  // IB-OFF-R4 — Price boundaries (confirmed from live DOM)
  // -------------------------------------------------------------------------

  test('IB-OFF-R4 promotional price = 0 → blocked (min is 1)', async ({ insuranceBilling }) => {
     await insuranceBilling.addOfferButton.click();

    await insuranceBilling.fillAndBlur(insuranceBilling.promotionalPriceInput, ACTIVE_OFFERS.zeroPriceBlocked);
    await expect(insuranceBilling.error).toContainText('must be 1 or greater');
  });

  test('IB-OFF-R4 original price = 0 → blocked (min is 1)', async ({ insuranceBilling }) => {
    await insuranceBilling.addOfferButton.click();

    await insuranceBilling.fillAndBlur(insuranceBilling.originalPriceInput, ACTIVE_OFFERS.zeroPriceBlocked);
    await expect(insuranceBilling.error).toContainText('must be 1 or greater');
  });

  test('IB-OFF-R4 promotional price = 1 → minimum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.addOfferButton.click();

    await insuranceBilling.fillAndBlur(insuranceBilling.promotionalPriceInput, ACTIVE_OFFERS.minPromoPrice);
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('IB-OFF-R4 original price = 1 → minimum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.addOfferButton.click();

    await insuranceBilling.fillAndBlur(insuranceBilling.originalPriceInput, ACTIVE_OFFERS.minOriginalPrice);
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('IB-OFF-R4 negative promotional price → blocked or sanitized', async ({ insuranceBilling }) => {
    await insuranceBilling.addOfferButton.click();

    await insuranceBilling.fillAndBlur(insuranceBilling.promotionalPriceInput, '-10');
    await insuranceBilling.page.waitForTimeout(500);
    const value  = await insuranceBilling.promotionalPriceInput.inputValue();
    const errors = await insuranceBilling.modal.locator("p[id$='-error']").count();
    expect(errors > 0 || Number(value) >= 0).toBeTruthy();
  });

  test('IB-OFF-R4 negative original price → blocked or sanitized', async ({ insuranceBilling }) => {
    await insuranceBilling.addOfferButton.click();

    await insuranceBilling.fillAndBlur(insuranceBilling.originalPriceInput, '-10');
    await insuranceBilling.page.waitForTimeout(500);
    const value  = await insuranceBilling.originalPriceInput.inputValue();
    const errors = await insuranceBilling.modal.locator("p[id$='-error']").count();
    expect(errors > 0 || Number(value) >= 0).toBeTruthy();
  });

  test('DEF-IB2-06 promo price > original price → not enforced (bug)', async ({ insuranceBilling }) => {
    await insuranceBilling.addOfferButton.click();

    await insuranceBilling.fill(insuranceBilling.promotionNameInput, ACTIVE_OFFERS.name);
    await insuranceBilling.fillAndBlur(insuranceBilling.promotionalPriceInput, ACTIVE_OFFERS.defPromoPrice);
    await insuranceBilling.fillAndBlur(insuranceBilling.originalPriceInput, ACTIVE_OFFERS.defOriginalPrice);
    // DEF-IB2-06: negative discount accepted — no error shown (known bug)
    const hasError = await insuranceBilling.error.isVisible();
    console.log(`DEF-IB2-06 Promo > Original — error shown: ${hasError}`);   
    expect(hasError).toBeTruthy();


  });

  // -------------------------------------------------------------------------
  // IB-OFF-R5 — Included Services (max 500 chars)
  // -------------------------------------------------------------------------

  test('IB-OFF-R5 included services 500 chars → accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.addOfferButton.click();
    await insuranceBilling.fill(insuranceBilling.promotionNameInput, ACTIVE_OFFERS.name);  
    await insuranceBilling.fillAndBlur(insuranceBilling.includedServicesInput, 'A'.repeat(500));
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('IB-OFF-R5 included services > 500 chars → blocked or truncated', async ({ insuranceBilling }) => {
    await insuranceBilling.addOfferButton.click();

    await insuranceBilling.fillAndBlur(insuranceBilling.includedServicesInput, 'A'.repeat(501));
    await insuranceBilling.page.waitForTimeout(500);
    const value  = await insuranceBilling.includedServicesInput.inputValue();
    const errors = await insuranceBilling.modal.locator("p[id$='-error']").count();
    expect(errors > 0 || value.length <= 500).toBeTruthy();
  });

  // -------------------------------------------------------------------------
  // IB-OFF-R6 — Restrictions/Terms (max 500 chars)
  // -------------------------------------------------------------------------

  test('IB-OFF-R6 restrictions 500 chars → accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.addOfferButton.click();
    await insuranceBilling.fill(insuranceBilling.promotionNameInput, ACTIVE_OFFERS.name);  
    await insuranceBilling.fillAndBlur(insuranceBilling.restrictionsTermsInput, 'A'.repeat(500));
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('IB-OFF-R6 restrictions > 500 chars → blocked or truncated', async ({ insuranceBilling }) => {
    await insuranceBilling.addOfferButton.click();

    await insuranceBilling.fillAndBlur(insuranceBilling.restrictionsTermsInput, 'A'.repeat(501));
    await insuranceBilling.page.waitForTimeout(500);
    const value  = await insuranceBilling.restrictionsTermsInput.inputValue();
    const errors = await insuranceBilling.modal.locator("p[id$='-error']").count();
    expect(errors > 0 || value.length <= 500).toBeTruthy();
  });

  // -------------------------------------------------------------------------
  // IB-OFF-R7 — Expiration Days (numeric, default 90)
  // -------------------------------------------------------------------------

  test('IB-OFF-R7 negative expiration days → error or sanitized', async ({ insuranceBilling }) => {
    await insuranceBilling.addOfferButton.click();

    await insuranceBilling.fillAndBlur(insuranceBilling.expirationDaysInput, '-10');
    await insuranceBilling.page.waitForTimeout(500);
    const value  = await insuranceBilling.expirationDaysInput.inputValue();
    const errors = await insuranceBilling.modal.locator("p[id$='-error']").count();
    // Expected: error shown OR value silently sanitized to positive
    expect(errors > 0 || Number(value) >= 0).toBeTruthy();
  });

  test('IB-OFF-R7 valid expiration days → accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.addOfferButton.click();
    await insuranceBilling.fill(insuranceBilling.promotionNameInput, ACTIVE_OFFERS.name);  
    await insuranceBilling.fillAndBlur(insuranceBilling.expirationDaysInput, ACTIVE_OFFERS.expirationDays);
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  // -------------------------------------------------------------------------
  // IB-OFF-R8 — Active toggle
  // -------------------------------------------------------------------------

  test('IB-OFF-R8 active promotion toggle changes state', async ({ insuranceBilling }) => {
    await insuranceBilling.addOfferButton.click();

    const toggle  = insuranceBilling.modal.getByRole('switch').first();
    const initial = await toggle.getAttribute('aria-checked');
    await toggle.click();
    await insuranceBilling.page.waitForTimeout(300);
    expect(await toggle.getAttribute('aria-checked')).not.toBe(initial);
  });
});
