import { test, expect } from '../../src/fixtures';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';
import { BasePage } from '../../src/pages/BasePage';

/**
 * Finance — IB-FIN-R1 to R9
 *
 * Truth source: tab6-insurance-billing.md
 * Reference: https://playwright.dev/docs/pom
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

  // -------------------------------------------------------------------------
  // TC-F-IB2-09 — Add from Quick Add list
  // -------------------------------------------------------------------------

  test('TC-F-IB2-09 add provider from Quick Add list', async ({ insuranceBilling }) => {
    const alreadyAdded = insuranceBilling.modal.getByRole('button', { name: '✓ CareCredit' });
    if (await alreadyAdded.isVisible()) {
      await alreadyAdded.click();
    }
    await insuranceBilling.modal.getByRole('button', { name: '+ CareCredit' }).click();
    await insuranceBilling.saveAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // TC-F-IB2-10 — Add Custom provider with full field set
  // -------------------------------------------------------------------------

  test('TC-F-IB2-10 add custom provider with full fields', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();

    await insuranceBilling.providerNameInput.fill(BasePage.unique('LocalCreditUnion'));
    await insuranceBilling.providerDescription.fill('In-house partnership financing');
    await insuranceBilling.providerWebsite.fill('https://lcu.example.com');
    await insuranceBilling.providerApr.fill('9.99');
    await insuranceBilling.providerPaymentTerms.fill('12–24 months');
    await insuranceBilling.providerLoanAmountRange.fill('$200–$5000');
    await insuranceBilling.providerCreditRequirements.fill('Soft check only');
    await insuranceBilling.providerKeyFeatures.fill('No prepayment penalty');

    await insuranceBilling.addFinanceProviderAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // TC-F-IB2-11 — In-House Financing toggle
  // -------------------------------------------------------------------------

  test('TC-F-IB2-11 enable In-House Financing toggle', async ({ insuranceBilling }) => {
    const toggle = insuranceBilling.inHouseFinancingToggle;
    const initial = await toggle.getAttribute('aria-checked');
    await toggle.click();
    await insuranceBilling.page.waitForTimeout(300);
    expect(await toggle.getAttribute('aria-checked')).not.toBe(initial);
    await insuranceBilling.saveAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // TC-N-IB2-15 — Empty Provider Name blocked
  // -------------------------------------------------------------------------

  test('TC-N-IB2-15 empty provider name → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();
    await insuranceBilling.addFinanceProviderButton.click();
    const isDisabled = await insuranceBilling.addFinanceProviderButton.isDisabled();
    const hasError   = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });

  // -------------------------------------------------------------------------
  // TC-N-IB2-16 — APR outside 0–99.99
  // -------------------------------------------------------------------------

  test('TC-N-IB2-16 APR = 150 → error (outside 0–99.99)', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();
    await insuranceBilling.providerApr.fill('150');
    await insuranceBilling.providerApr.press('Tab');
    await expect(insuranceBilling.error).toBeVisible();
  });

  // -------------------------------------------------------------------------
  // TC-B-IB2-11 — APR = 99.99 (upper boundary)
  // -------------------------------------------------------------------------

  test('TC-B-IB2-11 APR = 99.99 → maximum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();
    await insuranceBilling.providerApr.fill('99.99');
    await insuranceBilling.providerApr.press('Tab');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  // -------------------------------------------------------------------------
  // TC-B-IB2-12 — APR = 100 (one above ceiling)
  // -------------------------------------------------------------------------

  test('TC-B-IB2-12 APR = 100 → one above maximum → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();
    await insuranceBilling.providerApr.fill('100');
    await insuranceBilling.providerApr.press('Tab');
    await expect(insuranceBilling.error).toBeVisible();
  });

  // -------------------------------------------------------------------------
  // TC-S-IB2-05 — XSS in Description and Key Features
  // -------------------------------------------------------------------------

  test('TC-S-IB2-05 XSS in description and key features → sanitized', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomProviderButton.click();

    let alertFired = false;
    insuranceBilling.page.on('dialog', () => { alertFired = true; });

    await insuranceBilling.providerDescription.fill("<script>alert('finance')</script>");
    await insuranceBilling.providerKeyFeatures.fill("<script>alert('finance')</script>");

    await insuranceBilling.page.waitForTimeout(1000);
    expect(alertFired).toBe(false);
  });
});
