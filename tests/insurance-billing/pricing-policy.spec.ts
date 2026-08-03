import { test, expect } from '../../src/fixtures';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';
import { PRICING_POLICY } from '../../src/test-data/insurance-billing';

/**
 * Pricing Policy — IB-PP-R1 to R3
 *
 * Truth source: docs/requirements/tab6-insurance-billing.md
 * Test data:    src/test-data/insurance-billing.ts
 * Selectors:    confirmed via Playwright codegen on live app
 */

test.describe('Pricing Policy', () => {
  test.beforeEach(async ({ insuranceBilling }) => {
    await insuranceBilling.openEdit(InsuranceBillingPage.CARD.pricingPolicy);
  });

  test.afterEach(async ({ insuranceBilling }) => {
    await insuranceBilling.cancel();
  });

  test('TC-F-IB2-12 panel shows all 4 pricing policy options', async ({ insuranceBilling }) => {
    for (const option of PRICING_POLICY.options) {
      await expect(insuranceBilling.modal.getByRole('radio', { name: option })).toBeVisible();
    }
  });

  test('TC-F-IB2-12 select Always Provide Exact Pricing → saves', async ({ insuranceBilling }) => {
    await insuranceBilling.page.getByRole('radio', { name: 'Always Provide Exact Pricing' }).click();
    await insuranceBilling.saveAndAssertSuccess();
  });

  test('IB-PP-R2 Good Faith Estimate toggle changes state and saves', async ({ insuranceBilling }) => {
    const toggle  = insuranceBilling.goodFaithToggle;
    const initial = await toggle.getAttribute('aria-checked');
    await toggle.click();
    await insuranceBilling.page.waitForTimeout(300);
    expect(await toggle.getAttribute('aria-checked')).not.toBe(initial);
    await insuranceBilling.saveAndAssertSuccess();
  });

  test('IB-PP-R3 custom AI script = 2000 chars → accepted', async ({ insuranceBilling }) => {
    await insuranceBilling.customAiScriptTextarea.fill('A'.repeat(PRICING_POLICY.maxScriptLength));
    await expect(insuranceBilling.error).not.toBeVisible();
  });

  test('IB-PP-R3 custom AI script = 2001 chars → blocked or truncated', async ({ insuranceBilling }) => {
    await insuranceBilling.customAiScriptTextarea.fill('A'.repeat(PRICING_POLICY.maxScriptLength + 1));
    await insuranceBilling.page.waitForTimeout(500);
    const value  = await insuranceBilling.customAiScriptTextarea.inputValue();
    const errors = await insuranceBilling.modal.locator("p[id$='-error']").count();
    expect(errors > 0 || value.length <= PRICING_POLICY.maxScriptLength).toBeTruthy();
  });

  test('DEF-IB2-04 injection text stored as-is — security gap (High)', async ({ insuranceBilling }) => {
    await insuranceBilling.customAiScriptTextarea.fill(PRICING_POLICY.injectionText);
    const value = await insuranceBilling.customAiScriptTextarea.inputValue();
    expect(value).toBe(PRICING_POLICY.injectionText);
  });
});
