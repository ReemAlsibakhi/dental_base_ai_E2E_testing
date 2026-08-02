import { test, expect } from '../../src/fixtures';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';

/**
 * Membership Plans — IB-MEM-R1 to R4
 *
 * Truth source: tab6-insurance-billing.md (QA Test Report 2026-07-21)
 * Reference: https://playwright.dev/docs/pom
 *
 * Flow (confirmed via Playwright codegen on live app):
 *   openEdit → openFirstPlanEdit → fill → updatePlanAndAssertSuccess
 *
 * NOT automated (per decision report):
 *   - Plan Type dropdown (IB-MEM-R2) — closed list, low risk
 *   - Delete All — risk of destroying live data
 *   - Monthly price computation — rounding rule unconfirmed with engineering
 */

test.describe('Membership Plans', () => {
  test.beforeEach(async ({ insuranceBilling }) => {
    await insuranceBilling.openEdit(InsuranceBillingPage.CARD.membershipPlans);
    // await insuranceBilling.openFirstPlanEdit();
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
  // TC-F-IB2-04, TC-N-IB2-06, TC-S-IB2-02, TC-U-IB2-01, TC-R-IB2-01
  // -------------------------------------------------------------------------

  test('TC-F-IB2-04 valid plan name saves', async ({ insuranceBilling }) => {
    const current = await insuranceBilling.membershipNameInput.inputValue();
    const newName = current !== 'Premium Plan' ? 'Premium Plan' : 'Family Plan';
    await insuranceBilling.fillAndBlur(insuranceBilling.membershipNameInput, newName);
    await insuranceBilling.updatePlanAndAssertSuccess();
  });

  test('TC-N-IB2-06 empty plan name → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.membershipNameInput.clear();
    await insuranceBilling.membershipNameInput.press('Tab');
    const isDisabled = await insuranceBilling.updatePlanButton.isDisabled();
    const hasError   = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });

  test('TC-S-IB2-02 XSS in plan name → sanitized on render', async ({ insuranceBilling }) => {
    // Truth source test data: <img src=x onerror=alert(1)>
    await insuranceBilling.fillAndBlur(
      insuranceBilling.membershipNameInput,
      '<img src=x onerror=alert(1)>'
    );
    // Expected: sanitized/escaped on render — no alert fires
    // Verify no JS dialog appeared
    let alertFired = false;
    insuranceBilling.page.on('dialog', () => { alertFired = true; });
    await insuranceBilling.page.waitForTimeout(1000);
    expect(alertFired).toBe(false);
  });

  test('TC-U-IB2-01 plan name error clears when corrected', async ({ insuranceBilling }) => {
    await insuranceBilling.membershipNameInput.clear();
    await insuranceBilling.membershipNameInput.press('Tab');
    await expect(insuranceBilling.error).toBeVisible();
    await insuranceBilling.fillAndBlur(insuranceBilling.membershipNameInput, 'Family Plan');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('TC-R-IB2-01 plan name persists after save', async ({ insuranceBilling }) => {
    const current = await insuranceBilling.membershipNameInput.inputValue();
    const newName = current !== 'Premium Plan' ? 'Premium Plan' : 'Family Plan';
    await insuranceBilling.fillAndBlur(insuranceBilling.membershipNameInput, newName);
    await insuranceBilling.updatePlanAndAssertSuccess();
    await insuranceBilling.openFirstPlanEdit();
    await expect(insuranceBilling.membershipNameInput).toHaveValue(newName);
  });

  // -------------------------------------------------------------------------
  // IB-MEM-R4 — Discount %
  // TC-F-IB2-04, TC-N-IB2-07, TC-B-IB2-04, TC-B-IB2-05, TC-U-IB2-05
  // -------------------------------------------------------------------------

  test('TC-F-IB2-04 add new membership plan (happy path)', async ({ insuranceBilling }) => {
    // Close current plan edit first
    await insuranceBilling.cancel();

    // Open panel and click "+ New Membership Plan"
    await insuranceBilling.openEdit(InsuranceBillingPage.CARD.membershipPlans);
    const newPlanBtn = insuranceBilling.modal.getByRole('button', { name: '+ New Membership Plan' })
      .or(insuranceBilling.modal.getByText('New Membership Plan'));
    await newPlanBtn.click();

    await insuranceBilling.fillAndBlur(insuranceBilling.membershipNameInput, 'Ortho Care Plan');
    await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '599');
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '25');
    await insuranceBilling.addMembershipPlanAndAssertSuccess();
  });

  test('EXPLORE negative discount % → behavior', async ({ insuranceBilling }) => {
    // IB-MEM-R4 states range 0–100 — negative is out of range
    // Not an explicit TC in truth source but logically invalid
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '-1');
    const isDisabled = await insuranceBilling.updatePlanButton.isDisabled();
    const hasError   = await insuranceBilling.error.isVisible();
    const value      = await insuranceBilling.discountPercentageInput.inputValue();
    // Document actual behavior — negative may be silently sanitized like annual fee
    console.log(`Negative discount: value=${value}, error=${hasError}, disabled=${isDisabled}`);
    // expect(Number(value)).toBeGreaterThanOrEqual(0);
    await expect(insuranceBilling.updatePlanButton).toBeDisabled();

  });

  test('valid discount % accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '20');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('TC-N-IB2-07 discount % > 100 → error + Save disabled', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '150');
    await expect(insuranceBilling.error).toContainText('cannot exceed 100%');
    await expect(insuranceBilling.updatePlanButton).toBeDisabled();
  });

  test('TC-B-IB2-04 discount % = 100 → maximum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '100');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('TC-B-IB2-05 discount % = 101 → one above maximum → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '101');
    await expect(insuranceBilling.error).toBeVisible();
    await expect(insuranceBilling.updatePlanButton).toBeDisabled();
  });

  test('TC-U-IB2-05 save disabled proactively when discount invalid', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '150');
    await expect(insuranceBilling.updatePlanButton).toBeDisabled();
  });

  // -------------------------------------------------------------------------
  // IB-MEM-R3 — Annual Fee
  // TC-F-IB2-05, TC-N-IB2-08, TC-B-IB2-06, TC-B-IB2-07
  // -------------------------------------------------------------------------

  test('TC-F-IB2-05 valid annual fee accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '299');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('TC-N-IB2-08 negative annual fee → silently corrected (DEF)', async ({ insuranceBilling }) => {
    // DEF: minus sign is silently dropped — field shows 50 instead of -50
    // No error message shown — flagged as missing feedback issue
    await insuranceBilling.annualFeeInput.fill('-50');
    await insuranceBilling.annualFeeInput.press('Tab');
    // const value = await insuranceBilling.annualFeeInput.inputValue();
    // expect(Number(value)).toBeGreaterThanOrEqual(0);
    await expect(insuranceBilling.error).toBeVisible();
    await expect(insuranceBilling.updatePlanButton).toBeDisabled();
  });

  test('TC-N annual fee = 0.01 → blocked (min is 1)', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '0.01');
    await expect(insuranceBilling.error).toBeVisible();
    await expect(insuranceBilling.updatePlanButton).toBeDisabled();
  });

  test('TC-B-IB2-07 annual fee = 0 → blocked (min is 1)', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '0');
    await expect(insuranceBilling.error).toBeVisible();
    await expect(insuranceBilling.updatePlanButton).toBeDisabled();
  });

  test('TC-B-IB2-06 annual fee = 1 → minimum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '1');
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  // -------------------------------------------------------------------------
  // IB-DEL-R1 — Delete confirmation
  // TC-F-IB2-15, TC-N-IB2-17
  // -------------------------------------------------------------------------

test('TC-F-IB2-15 delete plan shows confirmation', async ({ insuranceBilling }) => {
  await expect(insuranceBilling.deletePlanButton).toBeVisible();
  await insuranceBilling.deletePlanButton.click();
  await insuranceBilling.assertDeleteConfirmationShown();
  await insuranceBilling.cancelDelete();
});

test('TC-N-IB2-17 cancel delete keeps plan', async ({ insuranceBilling }) => {
  // await insuranceBilling.modal.getByRole('button', { name: 'Cancel' }).first().click();
  
  await insuranceBilling.deletePlanButton.click();
  await insuranceBilling.assertDeleteConfirmationShown();
  await insuranceBilling.cancelDelete();
  
  // Verify "Family Plan" still exists in the list
  await expect(insuranceBilling.modal.getByText('Family Plan').first()).toBeVisible();
});
});
