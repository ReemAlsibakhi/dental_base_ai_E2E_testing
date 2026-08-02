import { test, expect } from '../../src/fixtures';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';
import { BasePage } from '../../src/pages/BasePage';
import { COVERAGE } from '../../src/test-data/insurance-billing';

/**
 * Coverage — Accepted Insurance Plans
 * IB-COV-R1 to R10
 *
 * Truth source: docs/requirements/tab6-insurance-billing.md
 * Test data:    src/test-data/insurance-billing.ts
 */

test.describe('Coverage — Accepted Insurance Plans', () => {
  test.beforeEach(async ({ insuranceBilling }) => {
    await insuranceBilling.openEdit(InsuranceBillingPage.CARD.coverage);
  });

  test.afterEach(async ({ insuranceBilling }) => {
    await insuranceBilling.cancel();
  });

  // -------------------------------------------------------------------------
  // Smoke
  // -------------------------------------------------------------------------

  test('panel opens with required elements', async ({ insuranceBilling }) => {
    await expect(insuranceBilling.modal).toBeVisible();
    await expect(insuranceBilling.cancelButton).toBeVisible();
    await expect(insuranceBilling.addCustomButton).toBeVisible();
  });

  test('Add Custom reveals New Plan form', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await expect(insuranceBilling.insuranceNameInput).toBeVisible();
    await expect(insuranceBilling.payerIdInput).toBeVisible();
  });

  // -------------------------------------------------------------------------
  // IB-COV-R1 — Accept All Toggle
  // -------------------------------------------------------------------------

  test('Accept All toggle changes state and saves', async ({ insuranceBilling }) => {
    const toggle = insuranceBilling.acceptAllToggle;
    const initial = await toggle.getAttribute('aria-checked');
    await toggle.click();
    await insuranceBilling.page.waitForTimeout(800);
    expect(await toggle.getAttribute('aria-checked')).not.toBe(initial);
    await insuranceBilling.saveAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // IB-COV-R2 — Insurance Name
  // -------------------------------------------------------------------------

  test('valid plan saves via Add Custom flow', async ({ insuranceBilling }) => {
    await insuranceBilling.addPlan({
      name: BasePage.unique('Delta'),
      payerId: COVERAGE.validPayerId,
    });
  });

  test('empty name → Save Plan disabled or error', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await insuranceBilling.insuranceNameInput.press('Tab');
    const isDisabled = await insuranceBilling.savePlanButton.isDisabled();
    const hasError   = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });

  test('1-char name → at least 2 characters error', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await insuranceBilling.fillAndBlur(insuranceBilling.insuranceNameInput, COVERAGE.invalidName);
    await expect(insuranceBilling.error).toContainText('at least 2 characters');
  });

  test('2-char name — minimum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await insuranceBilling.fillAndBlur(insuranceBilling.insuranceNameInput, 'AB');
    const nameError = insuranceBilling.modal
      .locator("p[id$='-error']")
      .filter({ hasText: 'characters' });
    await expect(nameError).not.toBeVisible();
  });

  test('XSS in name → sanitized', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    let alertFired = false;
    insuranceBilling.page.on('dialog', () => { alertFired = true; });
    await insuranceBilling.fillAndBlur(insuranceBilling.insuranceNameInput, COVERAGE.xssPayload);
    await insuranceBilling.page.waitForTimeout(1000);
    expect(alertFired).toBe(false);
  });

  test('error clears when name corrected', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await expect(insuranceBilling.insuranceNameInput).toBeVisible();

    const nameError = insuranceBilling.insuranceNameInput.locator(
      'xpath=following-sibling::p[contains(@id, "-error")]'
    );

    await insuranceBilling.fillAndBlur(insuranceBilling.insuranceNameInput, COVERAGE.invalidName);
    await expect(nameError).toBeVisible();

    await insuranceBilling.fillAndBlur(insuranceBilling.insuranceNameInput, COVERAGE.validName);
    await expect(nameError).not.toBeVisible();
  });

  // -------------------------------------------------------------------------
  // IB-COV-R8 — Coverage %
  // -------------------------------------------------------------------------

  test('coverage % > 100 → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await insuranceBilling.fillAndBlur(insuranceBilling.preventiveInput, COVERAGE.overPercent);
    const isDisabled = await insuranceBilling.savePlanButton.isDisabled();
    const errors     = await insuranceBilling.modal.locator("p[id$='-error']").count();
    expect(isDisabled || errors > 0).toBeTruthy();
  });

  test('coverage % = 1 → minimum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await insuranceBilling.fillAndBlur(insuranceBilling.preventiveInput, '1');
    const pctError = insuranceBilling.modal
      .locator("p[id$='-error']")
      .filter({ hasText: 'Preventive' });
    await expect(pctError).not.toBeVisible();
  });

  test('coverage % = 0 → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await insuranceBilling.fillAndBlur(insuranceBilling.preventiveInput, '0');
    const isDisabled = await insuranceBilling.savePlanButton.isDisabled();
    const errors     = await insuranceBilling.modal.locator("p[id$='-error']").count();
    expect(isDisabled || errors > 0).toBeTruthy();
  });

  test('coverage % = 100 → maximum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await insuranceBilling.fillAndBlur(insuranceBilling.preventiveInput, COVERAGE.validPercent);
    const pctError = insuranceBilling.modal
      .locator("p[id$='-error']")
      .filter({ hasText: 'Preventive' });
    await expect(pctError).not.toBeVisible();
  });

  test('plan with coverage % saves', async ({ insuranceBilling }) => {
    await insuranceBilling.addPlan({
      name:      BasePage.unique('Coverage'),
      payerId:   COVERAGE.validPayerId,
      preventive: '75',
      basic:      '80',
    });
  });

  // -------------------------------------------------------------------------
  // IB-COV-R10 — Additional Notes
  // -------------------------------------------------------------------------

  test('additional notes 500 chars accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.coverageNotes, COVERAGE.maxNotes);
    const errors = await insuranceBilling.modal.locator("p[id$='-error']").count();
    expect(errors).toBe(0);
  });

  test('additional notes > 500 chars blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.fill(insuranceBilling.coverageNotes, COVERAGE.overNotes);
    await insuranceBilling.page.waitForTimeout(500);
    const value  = await insuranceBilling.coverageNotes.inputValue();
    const errors = await insuranceBilling.modal.locator("p[id$='-error']").count();
    expect(errors > 0 || value.length <= 500).toBeTruthy();
  });

  test('disable plan via toggle', async ({ insuranceBilling }) => {
    const firstPlan = insuranceBilling.modal.locator('[role="switch"]').first();
    const initial   = await firstPlan.getAttribute('aria-checked');
    await firstPlan.click();
    await expect(firstPlan).not.toHaveAttribute('aria-checked', initial!);
  });
});
