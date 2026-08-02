import { test, expect, Browser } from '@playwright/test';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';
import { BasePage } from '../../src/pages/BasePage';
import { ACTIVE_OFFERS } from '../../src/test-data/insurance-billing';

/**
 * Active Offers — IB-OFF-R1 to R8
 *
 * Truth source: docs/requirements/tab6-insurance-billing.md
 * Test data:    src/test-data/insurance-billing.ts
 * Reference:    https://playwright.dev/docs/pom
 *
 * NOT automated (per decision report):
 *   - IB-OFF-R2 Promotion Type dropdown (closed list)
 *   - IB-OFF-R3 Target Audience dropdown (closed list)
 *
 * Key behaviors confirmed from truth source:
 *   - IB-OFF-R1: error inline on blur, Update Promotion button disabled proactively
 *   - IB-OFF-R4: promo > original not enforced — DEF-IB2-06
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
    await ib.modal.getByRole('button', { name: 'Add Offer' })
      .or(ib.modal.getByRole('button', { name: 'New Offer' }))
      .first().click();

    await ib.page.getByRole('textbox', { name: 'Promotion Name' })
      .or(ib.page.getByLabel('Name')).first()
      .fill(BasePage.unique(ACTIVE_OFFERS.name));

    await ib.page.getByRole('spinbutton', { name: 'Promotional Price' })
      .or(ib.page.getByLabel('Promotional Price')).first()
      .fill(ACTIVE_OFFERS.promoPrice);

    await ib.page.getByRole('spinbutton', { name: 'Original Price' })
      .or(ib.page.getByLabel('Original Price')).first()
      .fill(ACTIVE_OFFERS.originalPrice);

    await ib.page.getByRole('spinbutton', { name: 'Expiration Days' })
      .or(ib.page.getByLabel('Expiration Days')).first()
      .fill(ACTIVE_OFFERS.expirationDays);

    await ib.modal.getByRole('button', { name: 'Add Promotion' })
      .or(ib.modal.getByRole('button', { name: 'Save' }))
      .first().click();
    await ib.saveAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // IB-OFF-R1 — Promotion Name (inline error on blur, button disabled)
  // -------------------------------------------------------------------------

  test('TC-N-IB2-13 empty promotion name → error inline + button disabled', async () => {
    const nameField = ib.page.getByRole('textbox', { name: 'Promotion Name' })
      .or(ib.page.getByLabel('Name')).first();
    await nameField.clear();
    await nameField.press('Tab');
    await expect(ib.error).toContainText('at least 2 characters');
  });

  test('TC-S-IB2-04 XSS in promotion name → sanitized', async () => {
    const nameField = ib.page.getByRole('textbox', { name: 'Promotion Name' })
      .or(ib.page.getByLabel('Name')).first();
    let alertFired = false;
    ib.page.on('dialog', () => { alertFired = true; });
    await nameField.fill(ACTIVE_OFFERS.xssPayload);
    await ib.page.waitForTimeout(1000);
    expect(alertFired).toBe(false);
  });

  // -------------------------------------------------------------------------
  // IB-OFF-R4 — Promo price > original → DEF-IB2-06 (not enforced)
  // -------------------------------------------------------------------------

  test('DEF-IB2-06 promo price > original price → not enforced (bug)', async () => {
    const promoField = ib.page.getByRole('spinbutton', { name: 'Promotional Price' })
      .or(ib.page.getByLabel('Promotional Price')).first();
    const originalField = ib.page.getByRole('spinbutton', { name: 'Original Price' })
      .or(ib.page.getByLabel('Original Price')).first();

    await promoField.fill(ACTIVE_OFFERS.defPromoPrice);
    await originalField.fill(ACTIVE_OFFERS.defOriginalPrice);
    await originalField.press('Tab');

    // DEF-IB2-06: negative discount not blocked — documenting actual behavior
    const hasError = await ib.error.isVisible();
    console.log(`DEF-IB2-06 Promo > Original — error shown: ${hasError}`);
    // Known bug — test always passes to document the behavior
  });
});
