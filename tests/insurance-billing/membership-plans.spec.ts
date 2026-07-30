import { test, expect } from '../../src/fixtures';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';
import { BasePage } from '../../src/pages/BasePage';

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
  });

  test.afterEach(async ({ insuranceBilling }) => {
    await insuranceBilling.cancel();
  });

  // -------------------------------------------------------------------------
  // Smoke
  // -------------------------------------------------------------------------

  test('plan edit form opens with required fields', async ({ insuranceBilling }) => {
    await insuranceBilling.openFirstPlanEdit();
    await expect(insuranceBilling.membershipNameInput).toBeVisible();
    await expect(insuranceBilling.annualFeeInput).toBeVisible();
    await expect(insuranceBilling.discountPercentageInput).toBeVisible();
  });

  // -------------------------------------------------------------------------
  // IB-MEM-R1 — Plan Name
  // -------------------------------------------------------------------------

  test('valid plan name saves', async ({ insuranceBilling }) => {
    await insuranceBilling.openFirstPlanEdit();
    await insuranceBilling.fillAndBlur(insuranceBilling.membershipNameInput, BasePage.unique('Delta'));
    await insuranceBilling.updatePlanAndAssertSuccess();
  });

  test('empty plan name → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.openFirstPlanEdit();
    await insuranceBilling.membershipNameInput.clear();
    await insuranceBilling.membershipNameInput.press('Tab');
    const isDisabled = await insuranceBilling.updatePlanButton.isDisabled();
    const hasError   = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });

  test('XSS in plan name → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.openFirstPlanEdit();

    await insuranceBilling.fillAndBlur(
      insuranceBilling.membershipNameInput,
      '<script>alert(1)</script>'
    );
    const isDisabled = await insuranceBilling.updatePlanButton.isDisabled();
    const hasError   = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });

  test('plan name error clears when corrected', async ({ insuranceBilling }) => {
    await insuranceBilling.openFirstPlanEdit();

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
    await insuranceBilling.openFirstPlanEdit();

    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '20');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('discount % > 100 → Save disabled', async ({ insuranceBilling }) => {
     await insuranceBilling.openFirstPlanEdit();

    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '101');
    await expect(insuranceBilling.updatePlanButton).toBeDisabled();
  });

  test('discount % negative → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.openFirstPlanEdit();

    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '-1');
    const isDisabled = await insuranceBilling.updatePlanButton.isDisabled();
    const hasError   = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });

  test('discount % = 1 → minimum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.openFirstPlanEdit();

    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '1');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('discount % = 100 → maximum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.openFirstPlanEdit();
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '100');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('discount % decimal → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.openFirstPlanEdit();  
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '10.5');
    const isDisabled = await insuranceBilling.updatePlanButton.isDisabled();
    const hasError   = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });
  

  // -------------------------------------------------------------------------
  // IB-MEM-R3 — Annual Fee
  // -------------------------------------------------------------------------

  test('valid annual fee accepted', async ({ insuranceBilling }) => {
     await insuranceBilling.openFirstPlanEdit();

    await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '299');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('negative annual fee → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.openFirstPlanEdit();

    await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '-1');
    const isDisabled = await insuranceBilling.updatePlanButton.isDisabled();
    const hasError   = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });


test('annual fee = 1 → minimum valid', async ({ insuranceBilling }) => {
  await insuranceBilling.openFirstPlanEdit();

  await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '1');
  await expect(insuranceBilling.error).not.toBeVisible();
});

test('annual fee = 0 → blocked', async ({ insuranceBilling }) => {
  await insuranceBilling.openFirstPlanEdit();

  await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '0');
  const isDisabled = await insuranceBilling.updatePlanButton.isDisabled();
  const hasError   = await insuranceBilling.error.isVisible();
  expect(isDisabled || hasError).toBeTruthy();
});



test('delete plan shows confirmation', async ({ insuranceBilling }) => {
  const deleteBtn = insuranceBilling.modal.getByRole('button').filter({ hasText: /^$/ }).nth(6);
  await deleteBtn.click();
  
  console.log('test delete plan ');

  await expect(insuranceBilling.deletePlanButton).toBeVisible();
  // await insuranceBilling.cancelButton.click();
});

test('cancel delete keeps plan', async ({ insuranceBilling }) => {
  const planName = await insuranceBilling.membershipNameInput.inputValue();
  const deleteBtn = insuranceBilling.modal.getByRole('button').filter({ hasText: /^$/ }).nth(6);
  await deleteBtn.click();
  await insuranceBilling.page.getByRole('button', { name: 'Cancel' }).click();
  await expect(insuranceBilling.page.getByText(planName)).toBeVisible();
});


});