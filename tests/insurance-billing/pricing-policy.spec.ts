import { test, expect, Browser } from '@playwright/test';
import { InsuranceBillingPage } from '../../src/pages/InsuranceBillingPage';
import { PRICING_POLICY } from '../../src/test-data/insurance-billing';

/**
 * Pricing Policy — IB-PP-R1 to R3
 *
 * Truth source: docs/requirements/tab6-insurance-billing.md
 * Test data:    src/test-data/insurance-billing.ts
 * Reference:    https://playwright.dev/docs/pom
 *
 * Key behaviors confirmed from truth source:
 *   - IB-PP-R1: 4 radio options (3 original + "Do Not Discuss Pricing" added in live UI)
 *   - IB-PP-R2: compliance-relevant toggle (No Surprises Act)
 *   - IB-PP-R3: max 2000 chars; security surface (fed to DentiVoice AI)
 */

test.describe('Pricing Policy', () => {
  let ib: InsuranceBillingPage;

  test.beforeAll(async ({ browser }: { browser: Browser }) => {
    const context = await browser.newContext({ storageState: '.auth/admin.json' });
    const page    = await context.newPage();
    ib = new InsuranceBillingPage(page);
    await ib.navigate();
  });

  test.afterAll(async () => {
    await ib.page.close();
  });

  test.beforeEach(async () => {
    await ib.openEdit(InsuranceBillingPage.CARD.pricingPolicy);
  });

  test.afterEach(async () => {
    await ib.cancel();
  });

  // -------------------------------------------------------------------------
  // IB-PP-R1 — Pricing Policy radio options (4 options confirmed from live UI)
  // -------------------------------------------------------------------------

  test('TC-F-IB2-12 panel shows all 4 pricing policy options', async () => {
    for (const option of PRICING_POLICY.options) {
      await expect(ib.modal.getByText(option)).toBeVisible();
    }
  });

  test('TC-F-IB2-12 select Do Not Discuss Pricing → saves', async () => {
    await ib.selectPricingOption('Do Not Discuss Pricing');
    await ib.saveAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // IB-PP-R2 — Good Faith Estimate toggle (compliance — No Surprises Act)
  // -------------------------------------------------------------------------

  test('IB-PP-R2 Good Faith Estimate toggle changes state and saves', async () => {
    const toggle  = ib.goodFaithToggle;
    const initial = await toggle.getAttribute('aria-checked');
    await toggle.click();
    await ib.page.waitForTimeout(300);
    expect(await toggle.getAttribute('aria-checked')).not.toBe(initial);
    await ib.saveAndAssertSuccess();
  });

  // -------------------------------------------------------------------------
  // IB-PP-R3 — Custom AI Script (max 2000 chars, security surface)
  // -------------------------------------------------------------------------

  test('IB-PP-R3 custom AI script = 2000 chars → accepted', async () => {
    await ib.customAiScriptTextarea.fill('A'.repeat(PRICING_POLICY.maxScriptLength));
    await expect(ib.error).not.toBeVisible();
  });

  test('IB-PP-R3 custom AI script = 2001 chars → blocked or truncated', async () => {
    await ib.customAiScriptTextarea.fill('A'.repeat(PRICING_POLICY.maxScriptLength + 1));
    await ib.page.waitForTimeout(500);
    const value  = await ib.customAiScriptTextarea.inputValue();
    const errors = await ib.modal.locator("p[id$='-error']").count();
    expect(errors > 0 || value.length <= PRICING_POLICY.maxScriptLength).toBeTruthy();
  });

  test('DEF-IB2-04 injection text stored as-is — security gap (High)', async () => {
    // Security: script fed directly to DentiVoice AI agent on live calls
    // Expected: stored as inert text, not interpreted as a system command
    await ib.customAiScriptTextarea.fill(PRICING_POLICY.injectionText);
    const value = await ib.customAiScriptTextarea.inputValue();
    expect(value).toBe(PRICING_POLICY.injectionText);
    // DEF-IB2-04: no input-layer sanitization detected — flagged as High priority
  });
});
