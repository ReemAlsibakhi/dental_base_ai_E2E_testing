import { test, expect, Browser } from '@playwright/test';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';
import { BasePage } from '../../src/pages/BasePage';

/**
 * Finance — IB-FIN-R1 to R9
 *
 * Truth source: tab6-insurance-billing.md
 * Reference: https://playwright.dev/docs/pom
 *
 * Uses module-scoped page — browser opens once for all tests in this file.
 *
 * NOT automated (per decision report):
 *   - IB-FIN-R6 Application Process (closed list)
 *   - IB-FIN-R7 Approval Time (options not fully enumerated)
 */

test.describe('Finance', () => {
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
    await ib.openEdit(InsuranceBillingPage.CARD.finance);
  });

  test.afterEach(async () => {
    await ib.cancel();
  });

  // -------------------------------------------------------------------------
  // TC-F-IB2-09 — Add from Quick Add list
  // -------------------------------------------------------------------------

  test('TC-F-IB2-09 add provider from Quick Add list', async () => {
    if (await ib.quickAddProviderAdded('CareCredit').isVisible()) {
      await ib.quickAddProviderAdded('CareCredit').click();
    }
    await ib.quickAddProvider('CareCredit').click();
    await ib.saveAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // TC-F-IB2-10 — Add Custom provider with full field set
  // -------------------------------------------------------------------------

  test('TC-F-IB2-10 add custom provider with full fields', async () => {
    await ib.addCustomProviderButton.click();

    await ib.providerNameInput.fill(BasePage.unique('LocalCreditUnion'));
    await ib.providerDescription.fill('In-house partnership financing');
    await ib.providerWebsite.fill('https://lcu.example.com');
    await ib.providerApr.fill('9.99');
    await ib.providerPaymentTerms.fill('12–24 months');
    await ib.providerLoanAmountRange.fill('$200–$5000');
    await ib.providerCreditRequirements.fill('Soft check only');
    await ib.providerKeyFeatures.fill('No prepayment penalty');

    await ib.addFinanceProviderAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // TC-F-IB2-11 — In-House Financing toggle
  // -------------------------------------------------------------------------

  test('TC-F-IB2-11 enable In-House Financing toggle', async () => {
    const toggle = ib.inHouseFinancingToggle;
    const initial = await toggle.getAttribute('aria-checked');
    await toggle.click();
    await ib.page.waitForTimeout(300);
    expect(await toggle.getAttribute('aria-checked')).not.toBe(initial);
    await ib.saveAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // TC-N-IB2-15 — Empty Provider Name blocked
  // -------------------------------------------------------------------------

  test('TC-N-IB2-15 empty provider name → blocked', async () => {
    await ib.addCustomProviderButton.click();
    await expect(ib.addFinanceProviderButton).toBeDisabled();
  });

  // -------------------------------------------------------------------------
  // TC-N-IB2-16 — APR outside 0–99.99
  // -------------------------------------------------------------------------

  test('TC-N-IB2-16 APR = 150 → error (outside 0–99.99)', async () => {
    await ib.addCustomProviderButton.click();
    await ib.providerApr.fill('150');
    await ib.providerApr.press('Tab');
    await expect(ib.error).toBeVisible();
  });

  // -------------------------------------------------------------------------
  // TC-B-IB2-11 — APR = 99.99 (upper boundary)
  // -------------------------------------------------------------------------

  test('TC-B-IB2-11 APR = 99.99 → maximum valid', async () => {
    await ib.addCustomProviderButton.click();
    await ib.providerApr.fill('99.99');
    await ib.providerApr.press('Tab');
    await expect(ib.error).not.toBeVisible();
  });

  // -------------------------------------------------------------------------
  // TC-B-IB2-12 — APR = 100 (one above ceiling)
  // -------------------------------------------------------------------------

  test('TC-B-IB2-12 APR = 100 → one above maximum → blocked', async () => {
    await ib.addCustomProviderButton.click();
    await ib.providerApr.fill('100');
    await ib.providerApr.press('Tab');
    await expect(ib.error).toBeVisible();
  });

  // -------------------------------------------------------------------------
  // TC-S-IB2-05 — XSS in Description and Key Features
  // -------------------------------------------------------------------------

  test('TC-S-IB2-05 XSS in description and key features → sanitized', async () => {
    await ib.addCustomProviderButton.click();

    let alertFired = false;
    ib.page.on('dialog', () => { alertFired = true; });

    await ib.providerDescription.fill("<script>alert('finance')</script>");
    await ib.providerKeyFeatures.fill("<script>alert('finance')</script>");

    await ib.page.waitForTimeout(1000);
    expect(alertFired).toBe(false);
  });
});
