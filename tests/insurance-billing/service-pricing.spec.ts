import { test, expect, Browser } from '@playwright/test';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';
import { SERVICE_PRICING } from '../../src/test-data/insurance-billing';

/**
 * Service Pricing — IB-SVC-R1 to R4
 *
 * Truth source: docs/requirements/tab6-insurance-billing.md
 * Test data:    src/test-data/insurance-billing.ts
 * Selectors:    confirmed via Playwright codegen on live app
 *
 * NOT automated (per decision report):
 *   - IB-SVC-R3 Category dropdown (closed list)
 */

test.describe('Service Pricing', () => {
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
    await ib.openEdit(InsuranceBillingPage.CARD.servicePricing);
  });

  test.afterEach(async () => {
    await ib.cancel();
  });

  // -------------------------------------------------------------------------
  // TC-F-IB2-07 — Add Service (happy path)
  // -------------------------------------------------------------------------

  test('TC-F-IB2-07 add service with all fields', async () => {
    await ib.modal.getByRole('button', { name: 'Add Service' }).click();
    await ib.page.getByRole('textbox', { name: 'Service Name' }).fill(SERVICE_PRICING.validName);
    await ib.page.getByRole('textbox', { name: 'CDT Code' }).fill(SERVICE_PRICING.cdtCode);
    await ib.page.getByRole('spinbutton', { name: 'Price ($)' }).fill(SERVICE_PRICING.validPrice);
    await ib.page.getByRole('button', { name: 'Save Fee' }).click();
    await ib.saveAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // IB-SVC-R1 — Service Name (error fires on submit, not on blur)
  // -------------------------------------------------------------------------

  test('TC-N-IB2-09 empty service name → error on submit', async () => {
    await ib.modal.getByRole('button', { name: 'Add Service' }).click();
    await ib.page.getByRole('button', { name: 'Save Fee' }).click();
    await expect(ib.error).toContainText('at least 2 characters');
  });

  test('TC-N-IB2-10 1-char service name → error on submit', async () => {
    await ib.modal.getByRole('button', { name: 'Add Service' }).click();
    await ib.page.getByRole('textbox', { name: 'Service Name' }).fill(SERVICE_PRICING.invalidName);
    await ib.page.getByRole('button', { name: 'Save Fee' }).click();
    await expect(ib.error).toContainText('at least 2 characters');
  });

  test('TC-B-IB2-08 2-char service name → minimum valid', async () => {
    await ib.modal.getByRole('button', { name: 'Add Service' }).click();
    await ib.page.getByRole('textbox', { name: 'Service Name' }).fill(SERVICE_PRICING.minName);
    await ib.page.getByRole('button', { name: 'Save Fee' }).click();
    await expect(ib.error).not.toBeVisible();
  });

  test('TC-S-IB2-03 XSS in service name → sanitized', async () => {
    await ib.modal.getByRole('button', { name: 'Add Service' }).click();
    let alertFired = false;
    ib.page.on('dialog', () => { alertFired = true; });
    await ib.page.getByRole('textbox', { name: 'Service Name' }).fill(SERVICE_PRICING.xssPayload);
    await ib.page.waitForTimeout(1000);
    expect(alertFired).toBe(false);
  });

  // -------------------------------------------------------------------------
  // IB-SVC-R2 — CDT Code (optional)
  // -------------------------------------------------------------------------

  test('TC-F CDT code accepted', async () => {
    await ib.modal.getByRole('button', { name: 'Add Service' }).click();
    await ib.page.getByRole('textbox', { name: 'CDT Code' }).fill(SERVICE_PRICING.cdtCode);
    await expect(ib.error).not.toBeVisible();
  });

  // -------------------------------------------------------------------------
  // IB-SVC-R4 — Price (silent sanitization — DEF)
  // -------------------------------------------------------------------------

  test('TC-N-IB2-11 negative price → silently sanitized (DEF)', async () => {
    await ib.modal.getByRole('button', { name: 'Add Service' }).click();
    const priceField = ib.page.getByRole('spinbutton', { name: 'Price ($)' });
    await priceField.fill(SERVICE_PRICING.negPrice);
    await priceField.press('Tab');
    const value = await priceField.inputValue();
    expect(Number(value)).toBeGreaterThanOrEqual(0);
  });

  test('TC-B-IB2-09 valid price accepted', async () => {
    await ib.modal.getByRole('button', { name: 'Add Service' }).click();
    const priceField = ib.page.getByRole('spinbutton', { name: 'Price ($)' });
    await priceField.fill(SERVICE_PRICING.validPrice);
    await expect(ib.error).not.toBeVisible();
  });
});
