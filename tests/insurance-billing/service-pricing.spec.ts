import { test, expect } from '../../src/fixtures';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';
import { BasePage } from '../../src/pages/BasePage';
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

  // -------------------------------------------------------------------------
  // TC-F-IB2-07 — Add Service (happy path)
  // -------------------------------------------------------------------------

  test('TC-F-IB2-07 add service with all fields', async ({ insuranceBilling }) => {
    await insuranceBilling.addServiceButton.click();
    await insuranceBilling.fillAndBlur(insuranceBilling.serviceNameInput, SERVICE_PRICING.validName);
    // Use unique CDT code to avoid "already exists" error
    await insuranceBilling.fillAndBlur(insuranceBilling.cdtCodeInput, BasePage.unique(SERVICE_PRICING.uniqueCdtPrefix));
    await insuranceBilling.fillAndBlur(insuranceBilling.servicePriceInput, SERVICE_PRICING.validPrice);
    await insuranceBilling.saveFeeButton.click();
    await insuranceBilling.saveAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // IB-SVC-R1 — Service Name (error fires on submit)
  // -------------------------------------------------------------------------

  test('TC-N-IB2-09 empty service name → Save Fee disabled', async ({ insuranceBilling }) => {
    await insuranceBilling.addServiceButton.click();
    await expect(insuranceBilling.saveFeeButton).toBeDisabled();
  });

  test('TC-N-IB2-10 1-char service name → error on submit', async ({ insuranceBilling }) => {
    await insuranceBilling.addServiceButton.click();
    await insuranceBilling.fillAndBlur(insuranceBilling.serviceNameInput, SERVICE_PRICING.invalidName);
    await insuranceBilling.saveFeeButton.click();
    await expect(insuranceBilling.error).toContainText('at least 2 characters');
  });

  test('TC-B-IB2-08 2-char service name → minimum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.addServiceButton.click();
    await insuranceBilling.fillAndBlur(insuranceBilling.serviceNameInput, SERVICE_PRICING.minName);
    await insuranceBilling.saveFeeButton.click();
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('TC-S-IB2-03 XSS in service name → sanitized', async ({ insuranceBilling }) => {
    await insuranceBilling.addServiceButton.click();
    let alertFired = false;
    insuranceBilling.page.on('dialog', () => { alertFired = true; });
    await insuranceBilling.serviceNameInput.fill(SERVICE_PRICING.xssPayload);
    await insuranceBilling.page.waitForTimeout(1000);
    expect(alertFired).toBe(false);
  });

  // -------------------------------------------------------------------------
  // IB-SVC-R2 — CDT Code (optional)
  // -------------------------------------------------------------------------

  test('TC-F CDT code accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.addServiceButton.click();
    await insuranceBilling.fillAndBlur(insuranceBilling.cdtCodeInput, SERVICE_PRICING.cdtCode);
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  // -------------------------------------------------------------------------
  // IB-SVC-R4 — Price
  // -------------------------------------------------------------------------

  test('TC-N-IB2-11 negative price → error (min is 1)', async ({ insuranceBilling }) => {
    await insuranceBilling.addServiceButton.click();
    await insuranceBilling.fillAndBlur(insuranceBilling.servicePriceInput, SERVICE_PRICING.negPrice);
    await expect(insuranceBilling.error).toContainText('must be 1 or greater');
  });

  test('TC-B price = 0 → blocked (min is 1)', async ({ insuranceBilling }) => {
    await insuranceBilling.addServiceButton.click();
    await insuranceBilling.fillAndBlur(insuranceBilling.servicePriceInput, '0');
    await expect(insuranceBilling.error).toContainText('must be 1 or greater');
  });

  test('TC-B price = 1 → minimum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.addServiceButton.click();
    await insuranceBilling.fillAndBlur(insuranceBilling.servicePriceInput, '1');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('TC-B-IB2-09 valid price accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.addServiceButton.click();
    await insuranceBilling.fillAndBlur(insuranceBilling.servicePriceInput, SERVICE_PRICING.validPrice);
    await expect(insuranceBilling.error).not.toBeVisible();
  });
});
