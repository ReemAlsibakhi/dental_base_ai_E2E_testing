import { test, expect } from '../../src/fixtures';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';
import { BasePage } from '../../src/pages/BasePage';

/**
 * Membership Plans — IB-MEM-R1 to R4
 *
 * Fields:
 *   membershipNameInput  — Plan Name
 *   annualFeeInput       — Annual Fee
 *   discountPercentageInput — Discount %
 */

test.describe('Membership Plans', () => {
  test.beforeEach(async ({ insuranceBilling }) => {
    await insuranceBilling.openEdit(InsuranceBillingPage.CARD.membershipPlans);
  });

  test.afterEach(async ({ insuranceBilling }) => {
    await insuranceBilling.cancel();
  });

  // -------------------------------------------------------------------------

  test('panel opens with required elements', async ({ insuranceBilling }) => {
    await expect(insuranceBilling.modal).toBeVisible();
    await expect(insuranceBilling.cancelButton).toBeVisible();
    await expect(insuranceBilling.saveButton).toBeVisible();
  });
  // IB-MEM-R1 — Plan Name
  // -------------------------------------------------------------------------
  test('valid plan name saves', async ({ insuranceBilling }) => {
    const name = BasePage.unique('Plan');
    await insuranceBilling.fillAndBlur(insuranceBilling.membershipNameInput, name);
    await insuranceBilling.saveAndAssertSuccess();
  });

  test('empty plan name → Save disabled or error', async ({ insuranceBilling }) => {
    await insuranceBilling.membershipNameInput.clear();
    await insuranceBilling.membershipNameInput.press('Tab');
    const isDisabled = await insuranceBilling.saveButton.isDisabled();
    const hasError   = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });

  test('XSS in plan name → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(
      insuranceBilling.membershipNameInput,
      '<script>alert(1)</script>'
    );
    const isDisabled = await insuranceBilling.saveButton.isDisabled();
    const hasError   = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });

  test('plan name error clears when corrected', async ({ insuranceBilling }) => {
    await insuranceBilling.membershipNameInput.clear();
    await insuranceBilling.membershipNameInput.press('Tab');
    await expect(insuranceBilling.error).toBeVisible();

    await insuranceBilling.fillAndBlur(insuranceBilling.membershipNameInput, 'Basic Plan');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('plan name persists after save', async ({ insuranceBilling }) => {
    const name = BasePage.unique('Persist');
    await insuranceBilling.fillAndBlur(insuranceBilling.membershipNameInput, name);
    await insuranceBilling.saveAndAssertSuccess();

    await insuranceBilling.openEdit(InsuranceBillingPage.CARD.membershipPlans);
    await expect(insuranceBilling.membershipNameInput).toHaveValue(name);
  });

  // -------------------------------------------------------------------------
  // IB-MEM-R4 — Discount %
  // -------------------------------------------------------------------------

  test('valid discount % accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '20');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('discount % > 100 → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '101');
    const isDisabled = await insuranceBilling.saveButton.isDisabled();
    const hasError   = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });

  test('discount % negative → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '-1');
    const isDisabled = await insuranceBilling.saveButton.isDisabled();
    const hasError   = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });

  test('discount % = 0 → minimum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '0');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('discount % = 100 → maximum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '100');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('Save disabled when discount % invalid', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '150');
    await expect(insuranceBilling.saveButton).toBeDisabled();
  });

  // -------------------------------------------------------------------------
  // IB-MEM-R3 — Annual Fee
  // -------------------------------------------------------------------------

  test('valid annual fee accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '299');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('negative annual fee → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '-1');
    const isDisabled = await insuranceBilling.saveButton.isDisabled();
    const hasError   = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });

  test('annual fee = 0 → minimum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '0');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('annual fee large value accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '9999');
    await expect(insuranceBilling.error).not.toBeVisible();
  });
});
