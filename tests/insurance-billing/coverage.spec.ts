import { test, expect } from '../../src/fixtures';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';
import { BasePage } from '../../src/pages/BasePage';

/**
 * Coverage — Accepted Insurance Plans
 * IB-COV-R1 to R10
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
    await insuranceBilling.page.waitForTimeout(500);
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
    const after = await toggle.getAttribute('aria-checked');
    expect(after).not.toBe(initial);
    await insuranceBilling.saveAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // IB-COV-R2 — Insurance Name
  // -------------------------------------------------------------------------

  test('valid plan saves via Add Custom flow', async ({ insuranceBilling }) => {
    await insuranceBilling.addPlan({
      name: BasePage.unique('Delta'),
      payerId: '99001',
    });
  });

  test('empty name → Save Plan disabled or error', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await insuranceBilling.page.waitForTimeout(500);
    await insuranceBilling.insuranceNameInput.press('Tab');
    await insuranceBilling.page.waitForTimeout(500);

    const isDisabled = await insuranceBilling.savePlanButton.isDisabled();
    const hasError = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });

  test('1-char name → at least 2 characters error', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await insuranceBilling.page.waitForTimeout(500);
    await insuranceBilling.fill(insuranceBilling.insuranceNameInput, 'D');
    await insuranceBilling.insuranceNameInput.press('Tab');
    await insuranceBilling.page.waitForTimeout(500);
    await expect(insuranceBilling.error).toContainText('at least 2 characters');
  });

  test('2-char name — minimum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await insuranceBilling.page.waitForTimeout(500);
    await insuranceBilling.fill(insuranceBilling.insuranceNameInput, 'AB');
    await insuranceBilling.insuranceNameInput.press('Tab');
    await insuranceBilling.page.waitForTimeout(500);
    const nameError = insuranceBilling.modal
      .locator("p[id$='-error']")
      .filter({ hasText: 'characters' });
    await expect(nameError).not.toBeVisible();
  });

  test('XSS in name → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await insuranceBilling.page.waitForTimeout(500);
    await insuranceBilling.fill(
      insuranceBilling.insuranceNameInput,
      '<script>alert(1)</script>'
    );
    await insuranceBilling.insuranceNameInput.press('Tab');
    await insuranceBilling.page.waitForTimeout(500);
    const isDisabled = await insuranceBilling.savePlanButton.isDisabled();
    const hasError = await insuranceBilling.error.isVisible();
    expect(isDisabled || hasError).toBeTruthy();
  });

  test('error clears when name corrected', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await expect(insuranceBilling.insuranceNameInput).toBeVisible();

    // Error locator scoped to name field only — not modal-wide
    const nameError = insuranceBilling.insuranceNameInput.locator(
      'xpath=following-sibling::p[contains(@id, "-error")]'
    );

    // Invalid name → name error appears
    await insuranceBilling.fillAndBlur(insuranceBilling.insuranceNameInput, 'D');
    await expect(nameError).toBeVisible();

    // Correct name → name error disappears
    await insuranceBilling.fillAndBlur(insuranceBilling.insuranceNameInput, 'Delta Dental');
    await expect(nameError).not.toBeVisible();
  });

  // -------------------------------------------------------------------------
  // IB-COV-R8 — Coverage %
  // -------------------------------------------------------------------------

  test('coverage % > 100 → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await insuranceBilling.page.waitForTimeout(500);
    await insuranceBilling.fillAndBlur(insuranceBilling.preventiveInput, '101');
    const isDisabled = await insuranceBilling.savePlanButton.isDisabled();
    const errors = await insuranceBilling.modal.locator("p[id$='-error']").count();
    expect(isDisabled || errors > 0).toBeTruthy();
  });

  test('coverage % = 1 → minimum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await insuranceBilling.page.waitForTimeout(500);
    await insuranceBilling.fillAndBlur(insuranceBilling.preventiveInput, '1');
    const pctError = insuranceBilling.modal
      .locator("p[id$='-error']")
      .filter({ hasText: 'Preventive' });
    await expect(pctError).not.toBeVisible();
  });

  test('coverage % = 0 → blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await insuranceBilling.page.waitForTimeout(500);
    await insuranceBilling.fillAndBlur(insuranceBilling.preventiveInput, '0');
    const isDisabled = await insuranceBilling.savePlanButton.isDisabled();
    const errors = await insuranceBilling.modal.locator("p[id$='-error']").count();
    expect(isDisabled || errors > 0).toBeTruthy();
  });  

  test('coverage % = 100 → maximum valid', async ({ insuranceBilling }) => {
    await insuranceBilling.addCustomButton.click();
    await insuranceBilling.page.waitForTimeout(500);
    await insuranceBilling.fill(insuranceBilling.preventiveInput, '100');
    const pctError = insuranceBilling.modal
      .locator("p[id$='-error']")
      .filter({ hasText: 'Preventive' });
    await expect(pctError).not.toBeVisible();
  });

  test('plan with coverage % saves', async ({ insuranceBilling }) => {
    await insuranceBilling.addPlan({
      name: BasePage.unique('Coverage'),
      payerId: '55555',
      preventive: '75',
      basic: '80',
    });
  });

  // -------------------------------------------------------------------------
  // IB-COV-R10 — Additional Notes
  // -------------------------------------------------------------------------

  test('additional notes 500 chars accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.fillAndBlur(insuranceBilling.coverageNotes, 'A'.repeat(500));
    await insuranceBilling.page.waitForTimeout(500);
    const errors = await insuranceBilling.modal.locator("p[id$='-error']").count();
    expect(errors).toBe(0);
  });

  test('additional notes > 500 chars blocked', async ({ insuranceBilling }) => {
    await insuranceBilling.fill(insuranceBilling.coverageNotes, 'A'.repeat(501));
    await insuranceBilling.page.waitForTimeout(500);
    const value = await insuranceBilling.coverageNotes.inputValue();
    const errors = await insuranceBilling.modal.locator("p[id$='-error']").count();
    expect(errors > 0 || value.length <= 500).toBeTruthy();
  });

  // -------------------------------------------------------------------------
  // Delete
  // -------------------------------------------------------------------------

  test('delete plan shows confirmation', async ({ insuranceBilling }) => {
    const deleteBtn = insuranceBilling.modal
      .getByRole('button', { name: 'Remove' })
      .or(insuranceBilling.modal.getByRole('button', { name: 'Delete' }))
      .first();

    if (await deleteBtn.isVisible()) {
      await deleteBtn.click();
      await insuranceBilling.page.waitForTimeout(500);
      await insuranceBilling.assertDeleteConfirmationShown();
      await insuranceBilling.page.getByRole('button', { name: 'Cancel' }).last().click();
    } else {
      test.skip(true, 'No plan to delete');
    }
  });
});
