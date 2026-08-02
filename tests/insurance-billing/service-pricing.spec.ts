import { test, expect, Browser } from '@playwright/test';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';
import { BasePage } from '../../src/pages/BasePage';

/**
 * Service Pricing — IB-SVC-R1 to R4
 *
 * Truth source: tab6-insurance-billing.md
 * Reference: https://playwright.dev/docs/pom
 *
 * NOT automated (per decision report):
 *   - IB-SVC-R3 Category dropdown (closed list)
 */

test.describe('Service Pricing', () => {
  let ib: InsuranceBillingPage;

  test.beforeAll(async ({ browser }: { browser: Browser }) => {
    const context = await browser.newContext({ storageState: '.auth/admin.json' });
    const page = await context.newPage();
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

    await ib.page.getByRole('textbox', { name: 'Service Name' }).fill('Limited oral evaluation');
    await ib.page.getByRole('textbox', { name: 'CDT Code' }).fill('D0140');
    await ib.page.getByRole('spinbutton', { name: 'Price' }).fill('95');

    await ib.modal.getByRole('button', { name: 'Save Fee' }).click();
    await ib.saveAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // IB-SVC-R1 — Service Name validation
  // -------------------------------------------------------------------------

  test('TC-N-IB2-09 empty service name → error on submit', async () => {
    await ib.modal.getByRole('button', { name: 'Add Service' }).click();
    await ib.modal.getByRole('button', { name: 'Save Fee' }).click();
    await expect(ib.error).toContainText('at least 2 characters');
  });

  test('TC-N-IB2-10 1-char service name → error on submit', async () => {
    await ib.modal.getByRole('button', { name: 'Add Service' }).click();
    await ib.page.getByRole('textbox', { name: 'Service Name' }).fill('A');
    await ib.modal.getByRole('button', { name: 'Save Fee' }).click();
    await expect(ib.error).toContainText('at least 2 characters');
  });

  test('TC-B-IB2-08 2-char service name → minimum valid', async () => {
    await ib.modal.getByRole('button', { name: 'Add Service' }).click();
    await ib.page.getByRole('textbox', { name: 'Service Name' }).fill('AB');
    await ib.modal.getByRole('button', { name: 'Save Fee' }).click();
    await expect(ib.error).not.toBeVisible();
  });

  test('TC-S-IB2-03 XSS in service name → sanitized', async () => {
    await ib.modal.getByRole('button', { name: 'Add Service' }).click();
    let alertFired = false;
    ib.page.on('dialog', () => { alertFired = true; });
    await ib.page.getByRole('textbox', { name: 'Service Name' }).fill('<script>alert(1)</script>');
    await ib.page.waitForTimeout(1000);
    expect(alertFired).toBe(false);
  });

  // -------------------------------------------------------------------------
  // IB-SVC-R2 — CDT Code (optional)
  // -------------------------------------------------------------------------

  test('TC-F-IB2-07 CDT code D0150 accepted', async () => {
    await ib.modal.getByRole('button', { name: 'Add Service' }).click();
    await ib.page.getByRole('textbox', { name: 'CDT Code' }).fill('D0150');
    await expect(ib.error).not.toBeVisible();
  });

  // -------------------------------------------------------------------------
  // IB-SVC-R4 — Price (silent sanitization)
  // -------------------------------------------------------------------------

  test('TC-N-IB2-11 negative price → silently sanitized (DEF)', async () => {
    await ib.modal.getByRole('button', { name: 'Add Service' }).click();
    const priceField = ib.page.getByRole('spinbutton', { name: 'Price' });
    await priceField.fill('-50');
    await priceField.press('Tab');
    const value = await priceField.inputValue();
    // DEF: minus sign silently stripped — field shows 50 not -50
    expect(Number(value)).toBeGreaterThanOrEqual(0);
  });

  test('TC-B-IB2-09 valid price accepted', async () => {
    await ib.modal.getByRole('button', { name: 'Add Service' }).click();
    const priceField = ib.page.getByRole('spinbutton', { name: 'Price' });
    await priceField.fill('150');
    await expect(ib.error).not.toBeVisible();
  });
});
