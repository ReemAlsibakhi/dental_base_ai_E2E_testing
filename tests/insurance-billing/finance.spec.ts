import { test, expect } from '../../src/fixtures';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';
import { BasePage } from '../../src/pages/BasePage';
import { FINANCE } from '../../src/test-data/insurance-billing';

/**
 * Finance — IB-FIN-R1 to R9
 *
 * Truth source: docs/requirements/tab6-insurance-billing.md
 * Test data:    src/test-data/insurance-billing.ts
 * Selectors:    confirmed via Playwright codegen on live app
 *
 * NOT automated (per decision report):
 *   - IB-FIN-R6 Application Process (closed list)
 *   - IB-FIN-R7 Approval Time (options not fully enumerated)
 */

test.describe('Finance', () => {
  test.beforeEach(async ({ insuranceBilling }) => {
    await insuranceBilling.openEdit(InsuranceBillingPage.CARD.finance);
  });

  test.afterEach(async ({ insuranceBilling }) => {
    await insuranceBilling.cancel();
  });

  test('TC-F-IB2-09 add provider from Quick Add list', async ({ insuranceBilling }) => {
    if (await insuranceBilling.quickAddProviderAdded('CareCredit').isVisible()) {
      await insuranceBilling.quickAddProviderAdded('CareCredit').click();
    }
    await insuranceBilling.quickAddProvider('CareCredit').click();
    await insuranceBilling.saveAndAssertSuccess();
  });

  test('TC-F-IB2-10 add custom provider with full fields', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();
    await insuranceBilling.providerNameInput.fill(BasePage.unique(FINANCE.providerName));
    await insuranceBilling.providerDescription.fill(FINANCE.description);
    await insuranceBilling.providerWebsite.fill(FINANCE.website);
    await insuranceBilling.providerApr.fill(FINANCE.validApr);
    await insuranceBilling.providerPaymentTerms.fill(FINANCE.paymentTerms);
    await insuranceBilling.providerLoanAmountRange.fill(FINANCE.loanRange);
    await insuranceBilling.providerCreditRequirements.fill(FINANCE.creditReqs);
    await insuranceBilling.providerKeyFeatures.fill(FINANCE.keyFeatures);
    await insuranceBilling.addFinanceProviderAndAssertSuccess();
  });

  test('TC-F-IB2-11 enable In-House Financing toggle', async ({ insuranceBilling }) => {
    const toggle = insuranceBilling.inHouseFinancingToggle;
    const initial = await toggle.getAttribute('aria-checked');
    await toggle.click();
    expect(await toggle.getAttribute('aria-checked')).not.toBe(initial);
    await insuranceBilling.saveAndAssertSuccess();
  });

  test('TC-N-IB2-15 empty provider name → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();
    await expect(insuranceBilling.addFinanceProviderButton).toBeDisabled();
  });

  test('TC-N-IB2-16 APR = 150 → error (outside 0–99.99)', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();
    await insuranceBilling.providerApr.fill(FINANCE.invalidApr);
    await insuranceBilling.providerApr.press('Tab');
    await expect(insuranceBilling.error).toBeVisible();
  });

  test('TC-B-IB2-11 APR = 99.99 → maximum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();
    await insuranceBilling.providerApr.fill(FINANCE.maxApr);
    await insuranceBilling.providerApr.press('Tab');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('TC-B-IB2-12 APR = 100 → one above maximum → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();
    await insuranceBilling.providerApr.fill(FINANCE.overApr);
    await insuranceBilling.providerApr.press('Tab');
    await expect(insuranceBilling.error).toBeVisible();
  });

  test('TC-S-IB2-05 XSS in description and key features → sanitized', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();
    let alertFired = false;
    insuranceBilling.page.on('dialog', () => { alertFired = true; });
    await insuranceBilling.providerDescription.fill(FINANCE.xssPayload);
    await insuranceBilling.providerKeyFeatures.fill(FINANCE.xssPayload);
    await insuranceBilling.page.waitForTimeout(1000);
    expect(alertFired).toBe(false);
  });

  // -------------------------------------------------------------------------
  // IB-FIN-R2 — Description (max 500 chars)
  // -------------------------------------------------------------------------

  test('IB-FIN-R2 description = 500 chars → accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();
    await insuranceBilling.providerDescription.fill(FINANCE.maxDescription);
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('IB-FIN-R2 description > 500 chars → blocked or truncated', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();
    await insuranceBilling.providerDescription.fill(FINANCE.overDescription);
    const value  = await insuranceBilling.providerDescription.inputValue();
    const errors = await insuranceBilling.fieldErrorCount();
    expect(errors > 0 || value.length <= 500).toBeTruthy();
  });

  // -------------------------------------------------------------------------
  // IB-FIN-R3 — Website (free text, no enforced format)
  // -------------------------------------------------------------------------

  test('IB-FIN-R3 valid URL accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();
    await insuranceBilling.providerWebsite.fill(FINANCE.website);
    await insuranceBilling.providerWebsite.press('Tab');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  // -------------------------------------------------------------------------
  // IB-FIN-R4 — APR negative value
  // -------------------------------------------------------------------------

  test('IB-FIN-R4 APR negative → blocked or sanitized', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();
    await insuranceBilling.providerApr.fill(FINANCE.negativeApr);
    await insuranceBilling.providerApr.press('Tab');
    const value  = await insuranceBilling.providerApr.inputValue();
    const errors = await insuranceBilling.fieldErrorCount();
    expect(errors > 0 || Number(value) >= 0).toBeTruthy();
  });

  // -------------------------------------------------------------------------
  // IB-FIN-R5 — Key Features (max 1000 chars)
  // -------------------------------------------------------------------------

  test('IB-FIN-R5 key features = 1000 chars → accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();
    await insuranceBilling.providerKeyFeatures.fill(FINANCE.maxKeyFeatures);
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('IB-FIN-R5 key features > 1000 chars → blocked or truncated', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();
    await insuranceBilling.providerKeyFeatures.fill(FINANCE.overKeyFeatures);
    const value  = await insuranceBilling.providerKeyFeatures.inputValue();
    const errors = await insuranceBilling.fieldErrorCount();
    expect(errors > 0 || value.length <= 1000).toBeTruthy();
  });

  // -------------------------------------------------------------------------
  // IB-FIN-R8 — Active Status toggle (defaults ON for new providers)
  // -------------------------------------------------------------------------

  test('IB-FIN-R8 active status toggle changes state', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();
    const toggle  = insuranceBilling.modal.getByRole('switch').first();
    const initial = await toggle.getAttribute('aria-checked');
    await toggle.click();
    expect(await toggle.getAttribute('aria-checked')).not.toBe(initial);
  });
});
