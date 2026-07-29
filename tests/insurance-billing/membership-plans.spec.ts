import { test, expect } from '../../src/fixtures';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';

/**
 * Membership Plans — IB-MEM-R1 to R4
 *
 * Flow (confirmed via Playwright codegen):
 *   openEdit(membershipPlans) → openFirstPlanEdit() → fill fields → updatePlanAndAssertSuccess()
 *
 * Live data: 5 plans exist — we edit the first one.
 */

test.describe('Membership Plans', () => {
  test.beforeEach(async ({ insuranceBilling }) => {
    await insuranceBilling.openEdit(InsuranceBillingPage.CARD.membershipPlans);
    await insuranceBilling.openFirstPlanEdit();
  });

  test.afterEach(async ({ insuranceBilling }) => {
    await insuranceBilling.cancel();
  });

  // -------------------------------------------------------------------------
  // Smoke
  // -------------------------------------------------------------------------

  test('plan edit form opens with required fields', async ({ insuranceBilling }) => {
    await expect(insuranceBilling.membershipNameInput).toBeVisible();
    await expect(insuranceBilling.annualFeeInput).toBeVisible();
    await expect(insuranceBilling.discountPercentageInput).toBeVisible();
    await expect(insuranceBilling.updatePlanButton).toBeVisible();
  });

  // -------------------------------------------------------------------------
  // IB-MEM-R1 — Plan Name
  // -------------------------------------------------------------------------

  test('valid plan name saves', async ({ insuranceBilling }) => {
    const current = await insuranceBilling.membershipNameInput.inputValue();
    const newName = current !== 'Premium Plan' ? 'Premium Plan' : 'Family Plan';
    await insuranceBilling.fillAndBlur(insuranceBilling.membershipNameInput, newName);
    await insuranceBilling.updatePlanAndAssertSuccess();
  });

  test('empty plan name → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.membershipNameInput.clear();
    await insuranceBilling.membershipNameInput.press('Tab');
    const isDisabled = await insuranceBilling.updatePlanButton.isDisabled();
    const hasError   = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });

  test('XSS in plan name → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(
      insuranceBilling.membershipNameInput,
      '<script>alert(1)</script>'
    );
    const isDisabled = await insuranceBilling.updatePlanButton.isDisabled();
    const hasError   = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });

  test('plan name error clears when corrected', async ({ insuranceBilling }) => {
    await insuranceBilling.membershipNameInput.clear();
    await insuranceBilling.membershipNameInput.press('Tab');
    await expect(insuranceBilling.error).toBeVisible();

    await insuranceBilling.fillAndBlur(insuranceBilling.membershipNameInput, 'Family Plan');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  // -------------------------------------------------------------------------
  // IB-MEM-R4 — Discount %
  // -------------------------------------------------------------------------

  test('valid discount % accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '20');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('discount % > 100 → Save disabled', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '101');
    await expect(insuranceBilling.updatePlanButton).toBeDisabled();
  });

  test('discount % negative → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '-1');
    const isDisabled = await insuranceBilling.updatePlanButton.isDisabled();
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

  // -------------------------------------------------------------------------
  // IB-MEM-R3 — Annual Fee
  // -------------------------------------------------------------------------

  test('valid annual fee accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '299');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('negative annual fee → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '-1');
    const isDisabled = await insuranceBilling.updatePlanButton.isDisabled();
    const hasError   = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });

  test('annual fee = 0 → minimum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '0');
    await expect(insuranceBilling.error).not.toBeVisible();
  });
});
