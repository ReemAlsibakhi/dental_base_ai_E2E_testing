import { test, expect } from '../../src/fixtures';
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
  test.beforeEach(async ({ insuranceBilling }) => {
    await insuranceBilling.openEdit(InsuranceBillingPage.CARD.servicePricing);
  });

  test.afterEach(async ({ insuranceBilling }) => {
    await insuranceBilling.cancel();
  });

  test('TC-F-IB2-07 add service with all fields', async ({ insuranceBilling }) => {
    await insuranceBilling.modal.getByRole('button', { name: 'Add Service' }).click();
    await insuranceBilling.page.getByRole('textbox', { name: 'Service Name' }).fill(SERVICE_PRICING.validName);
    await insuranceBilling.page.getByRole('textbox', { name: 'CDT Code' }).fill(SERVICE_PRICING.cdtCode);
    await insuranceBilling.page.getByRole('spinbutton', { name: 'Price ($)' }).fill(SERVICE_PRICING.validPrice);
    await insuranceBilling.page.getByRole('button', { name: 'Save Fee' }).click();
    await insuranceBilling.saveAndAssertSuccess();
  });

  test('TC-N-IB2-09 empty service name → error on submit', async ({ insuranceBilling }) => {
    await insuranceBilling.modal.getByRole('button', { name: 'Add Service' }).click();
    await insuranceBilling.page.getByRole('button', { name: 'Save Fee' }).click();
    await expect(insuranceBilling.error).toContainText('at least 2 characters');
  });

  test('TC-N-IB2-10 1-char service name → error on submit', async ({ insuranceBilling }) => {
    await insuranceBilling.modal.getByRole('button', { name: 'Add Service' }).click();
    await insuranceBilling.page.getByRole('textbox', { name: 'Service Name' }).fill(SERVICE_PRICING.invalidName);
    await insuranceBilling.page.getByRole('button', { name: 'Save Fee' }).click();
    await expect(insuranceBilling.error).toContainText('at least 2 characters');
  });

  test('TC-B-IB2-08 2-char service name → minimum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.modal.getByRole('button', { name: 'Add Service' }).click();
    await insuranceBilling.page.getByRole('textbox', { name: 'Service Name' }).fill(SERVICE_PRICING.minName);
    await insuranceBilling.page.getByRole('button', { name: 'Save Fee' }).click();
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('TC-S-IB2-03 XSS in service name → sanitized', async ({ insuranceBilling }) => {
    await insuranceBilling.modal.getByRole('button', { name: 'Add Service' }).click();
    let alertFired = false;
    insuranceBilling.page.on('dialog', () => { alertFired = true; });
    await insuranceBilling.page.getByRole('textbox', { name: 'Service Name' }).fill(SERVICE_PRICING.xssPayload);
    await insuranceBilling.page.waitForTimeout(1000);
    expect(alertFired).toBe(false);
  });

  test('TC-F CDT code accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.modal.getByRole('button', { name: 'Add Service' }).click();
    await insuranceBilling.page.getByRole('textbox', { name: 'CDT Code' }).fill(SERVICE_PRICING.cdtCode);
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('TC-N-IB2-11 negative price → silently sanitized (DEF)', async ({ insuranceBilling }) => {
    await insuranceBilling.modal.getByRole('button', { name: 'Add Service' }).click();
    const priceField = insuranceBilling.page.getByRole('spinbutton', { name: 'Price ($)' });
    await priceField.fill(SERVICE_PRICING.negPrice);
    await priceField.press('Tab');
    const value = await priceField.inputValue();
    expect(Number(value)).toBeGreaterThanOrEqual(0);
  });

  test('TC-B-IB2-09 valid price accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.modal.getByRole('button', { name: 'Add Service' }).click();
    const priceField = insuranceBilling.page.getByRole('spinbutton', { name: 'Price ($)' });
    await priceField.fill(SERVICE_PRICING.validPrice);
    await expect(insuranceBilling.error).not.toBeVisible();
  });
});
