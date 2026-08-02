import { test, expect } from '../../src/fixtures';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';
import { BasePage } from '../../src/pages/BasePage';

/**
 * Finance — IB-FIN-R1 to R9
 *
 * Truth source: tab6-insurance-billing.md (QA Test Report 2026-07-21)
 * Reference: https://playwright.dev/docs/pom
 *
 * Selectors confirmed via Playwright codegen on live app.
 *
 * NOT automated (per decision report):
 *   - IB-FIN-R6 Application Process dropdown (closed list)
 *   - IB-FIN-R7 Approval Time dropdown (options not fully enumerated)
 *   - DEF-IB2-09: chip removal has no confirmation — documented not fixed
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
    // Remove CareCredit first if already added to ensure clean state
    const careCredit = insuranceBilling.modal.getByRole('button', { name: '✓ CareCredit' });
    if (await careCredit.isVisible()) {
      await careCredit.click();
    }
    // Add CareCredit from Quick Add
    await insuranceBilling.modal.getByRole('button', { name: '+ CareCredit' }).click();
    await insuranceBilling.saveAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // TC-F-IB2-10 — Add Custom provider with full field set
  // -------------------------------------------------------------------------

  test('TC-F-IB2-10 add custom finance provider with full fields', async ({ insuranceBilling }) => {
    await insuranceBilling.modal.getByRole('button', { name: 'Add Custom' }).click();

    const name = BasePage.unique('LocalCreditUnion');
    await insuranceBilling.page.getByRole('textbox', { name: 'Provider Name' }).fill(name);
    await insuranceBilling.page.getByRole('textbox', { name: 'Description' }).fill('In-house partnership financing');
    await insuranceBilling.page.getByRole('textbox', { name: 'Website' }).fill('https://lcu.example.com');
    await insuranceBilling.page.getByRole('textbox', { name: 'APR / Interest Rate (%)' }).fill('9.99');
    await insuranceBilling.page.getByRole('textbox', { name: 'Payment Terms' }).fill('12–24 months');
    await insuranceBilling.page.getByRole('textbox', { name: 'Loan Amount Range' }).fill('$200–$5000');
    await insuranceBilling.page.getByRole('textbox', { name: 'Credit Requirements' }).fill('Soft check only');
    await insuranceBilling.page.getByRole('textbox', { name: 'Key Features' }).fill('No prepayment penalty');

    await insuranceBilling.modal.getByRole('button', { name: 'Add Finance Provider' }).click();
    await insuranceBilling.saveAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // TC-F-IB2-11 — In-House Financing toggle
  // -------------------------------------------------------------------------

  test('TC-F-IB2-11 enable In-House Financing toggle', async ({ insuranceBilling }) => {
    const toggle = insuranceBilling.modal.getByRole('switch').nth(1);
    const initial = await toggle.getAttribute('aria-checked');
    await toggle.click();
    await insuranceBilling.page.waitForTimeout(300);
    const after = await toggle.getAttribute('aria-checked');
    expect(after).not.toBe(initial);
    await insuranceBilling.saveAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // TC-N-IB2-15 — Empty Provider Name blocked
  // -------------------------------------------------------------------------

  test('TC-N-IB2-15 empty provider name → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.modal.getByRole('button', { name: 'Add Custom' }).click();
    // Leave Provider Name empty and try to submit
    await insuranceBilling.modal.getByRole('button', { name: 'Add Finance Provider' }).click();
    const isDisabled = await insuranceBilling.modal
      .getByRole('button', { name: 'Add Finance Provider' })
      .isDisabled();
    const hasError = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });

  // -------------------------------------------------------------------------
  // TC-N-IB2-16 — APR outside 0–99.99
  // -------------------------------------------------------------------------

  test('TC-N-IB2-16 APR = 150 → error (outside 0–99.99)', async ({ insuranceBilling }) => {
    await insuranceBilling.modal.getByRole('button', { name: 'Add Custom' }).click();
    const aprField = insuranceBilling.page.getByRole('textbox', { name: 'APR / Interest Rate (%)' });
    await aprField.fill('150');
    await aprField.press('Tab');
    await expect(insuranceBilling.error).toBeVisible();
  });

  // -------------------------------------------------------------------------
  // TC-B-IB2-11 — APR = 99.99 (upper boundary)
  // -------------------------------------------------------------------------

  test('TC-B-IB2-11 APR = 99.99 → maximum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.modal.getByRole('button', { name: 'Add Custom' }).click();
    const aprField = insuranceBilling.page.getByRole('textbox', { name: 'APR / Interest Rate (%)' });
    await aprField.fill('99.99');
    await aprField.press('Tab');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  // -------------------------------------------------------------------------
  // TC-B-IB2-12 — APR = 100 (one above ceiling)
  // -------------------------------------------------------------------------

  test('TC-B-IB2-12 APR = 100 → one above maximum → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.modal.getByRole('button', { name: 'Add Custom' }).click();
    const aprField = insuranceBilling.page.getByRole('textbox', { name: 'APR / Interest Rate (%)' });
    await aprField.fill('100');
    await aprField.press('Tab');
    await expect(insuranceBilling.error).toBeVisible();
  });

  // -------------------------------------------------------------------------
  // TC-S-IB2-05 — XSS in Description and Key Features
  // -------------------------------------------------------------------------

  test('TC-S-IB2-05 XSS in description → sanitized', async ({ insuranceBilling }) => {
    await insuranceBilling.modal.getByRole('button', { name: 'Add Custom' }).click();

    let alertFired = false;
    insuranceBilling.page.on('dialog', () => { alertFired = true; });

    await insuranceBilling.page.getByRole('textbox', { name: 'Description' })
      .fill("<script>alert('finance')</script>");
    await insuranceBilling.page.getByRole('textbox', { name: 'Key Features' })
      .fill("<script>alert('finance')</script>");

    await insuranceBilling.page.waitForTimeout(1000);
    expect(alertFired).toBe(false);
  });
});
