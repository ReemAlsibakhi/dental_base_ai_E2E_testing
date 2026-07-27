import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

/**
 * InsuranceBillingPage
 *
 * URL: /settings?settingTab=Insurance+%26+Billing
 *
 * Save patterns (confirmed from live DOM):
 *   Toggle-only:  Save Changes → API response (200/204)
 *   New Plan:     fill fields → Save Plan (local) → Save Changes → API response
 *
 * IMPORTANT: Many cards share input[name="name"] and input[name="price"].
 * All locators are scoped to this.modal to avoid cross-card conflicts.
 * Use card-specific methods (addPlan, addMembershipPlan, etc.) when possible.
 */
export class InsuranceBillingPage extends BasePage {
  static readonly URL = '/settings?settingTab=Insurance+%26+Billing';

  static readonly CARD = {
    coverage:        'Coverage',
    membershipPlans: 'Membership Plans',
    finance:         'Finance',
    servicePricing:  'Service Pricing',
    activeOffers:    'Active Offers',
    pricingPolicy:   'Pricing Policy',
  } as const;

  constructor(page: Page) {
    super(page);
  }

  // -------------------------------------------------------------------------
  // Navigation
  // -------------------------------------------------------------------------

  override async navigate(): Promise<void> {
    await this.page.goto(InsuranceBillingPage.URL);
    await this.page.waitForLoadState('networkidle');
  }

  async openEdit(cardName: string): Promise<void> {
    const editBtn = this.page.locator(
      `//h3[contains(text(),'${cardName}')]` +
      `/ancestor::div[contains(@class,'flex')][2]` +
      `//button[normalize-space()='Edit']`
    ).first();
    await editBtn.scrollIntoViewIfNeeded();
    await editBtn.click();
    await this.page.waitForTimeout(500);
  }

  // -------------------------------------------------------------------------
  // Modal — shared helpers
  // -------------------------------------------------------------------------

  get modal(): Locator {
    return this.page.locator('[role="dialog"]');
  }

  get saveButton(): Locator {
    return this.modal.getByRole('button', { name: 'Save Changes' });
  }

  get cancelButton(): Locator {
    return this.modal.getByRole('button', { name: 'Cancel' });
  }

  get savePlanButton(): Locator {
    return this.modal.getByRole('button', { name: 'Save Plan' });
  }

  get error(): Locator {
    return this.modal.locator("p[id$='-error']").first();
  }

  async cancel(): Promise<void> {
    try {
      if (await this.cancelButton.isVisible()) {
        await this.cancelButton.click();
        await this.page.waitForTimeout(300);
        const discard = this.page.getByRole('button', { name: 'Discard' });
        if (await discard.isVisible()) await discard.click();
      }
    } catch { /* panel may already be closed */ }
  }

  async saveAndAssertSuccess(): Promise<void> {
    await this.saveButton.scrollIntoViewIfNeeded();
    await Promise.all([
      this.waitForApiSuccess(),
      this.saveButton.click(),
    ]);
  }

  async savePlanAndAssertSuccess(): Promise<void> {
    await this.savePlanButton.scrollIntoViewIfNeeded();
    await this.savePlanButton.click();
    await this.page.waitForTimeout(500);
    await this.saveAndAssertSuccess();
  }

  assertDeleteConfirmationShown(): Promise<void> {
    return expect(this.page.getByText('cannot be undone')).toBeVisible();
  }

  // -------------------------------------------------------------------------
  // Coverage — Accepted Insurance Plans
  // NOTE: 'input[name="name"]' is shared across cards — always scope to modal
  // -------------------------------------------------------------------------

  get acceptAllToggle(): Locator {
    return this.modal.locator('button[role="switch"]').first();
  }

  get addCustomButton(): Locator {
    return this.modal.getByRole('button', { name: 'Add Custom' });
  }

  // New Plan form fields
  get coverageNameInput(): Locator {
    return this.modal.locator('input[name="name"]');
  }

  get payerIdInput(): Locator {
    return this.modal.locator('input[name="payerId"]');
  }

  get preventiveInput(): Locator {
    return this.modal.locator('input[name="preventiveCoverage"]');
  }

  get basicInput(): Locator {
    return this.modal.locator('input[name="basicCoverage"]');
  }

  get majorInput(): Locator {
    return this.modal.locator('input[name="majorCoverage"]');
  }

  get orthodonticInput(): Locator {
    return this.modal.locator('input[name="orthodonticCoverage"]');
  }

  get coverageNotes(): Locator {
    return this.modal.locator('textarea').first();
  }

  async fillCoveragePercentage(locator: Locator, value: string): Promise<void> {
    await locator.scrollIntoViewIfNeeded();
    await locator.fill(value);
    await locator.press('Tab');
    await this.page.waitForTimeout(300);
  }

  async addPlan(options: {
    name?: string;
    payerId?: string;
    preventive?: string;
    basic?: string;
    major?: string;
    orthodontic?: string;
  } = {}): Promise<{ name: string; payerId: string }> {
    const name    = options.name    ?? BasePage.unique('Plan');
    const payerId = options.payerId ?? '12345';

    await this.addCustomButton.click();
    await this.page.waitForTimeout(500);

    await this.smartFill(this.coverageNameInput, name);
    await this.coverageNameInput.press('Tab');
    await this.page.waitForTimeout(300);

    await this.smartFill(this.payerIdInput, payerId);
    await this.payerIdInput.press('Tab');
    await this.page.waitForTimeout(300);

    if (options.preventive) await this.fillCoveragePercentage(this.preventiveInput, options.preventive);
    if (options.basic)      await this.fillCoveragePercentage(this.basicInput,      options.basic);
    if (options.major)      await this.fillCoveragePercentage(this.majorInput,      options.major);
    if (options.orthodontic) await this.fillCoveragePercentage(this.orthodonticInput, options.orthodontic);

    await this.savePlanAndAssertSuccess();
    return { name, payerId };
  }

  // -------------------------------------------------------------------------
  // Membership Plans
  // -------------------------------------------------------------------------

  get membershipNameInput(): Locator {
    return this.modal.locator('input[name="name"]');
  }

  get annualFeeInput(): Locator {
    return this.modal.locator('input[name="annualFee"]');
  }

  get discountPercentageInput(): Locator {
    return this.modal.locator('input[name="discountPercentage"]');
  }

  // -------------------------------------------------------------------------
  // Finance
  // -------------------------------------------------------------------------

  get providerNameInput(): Locator {
    return this.modal.locator('input[placeholder*="CareCredit"]');
  }

  get providerDescription(): Locator {
    return this.modal.locator('textarea[placeholder*="Most popular"]');
  }

  get providerApr(): Locator {
    return this.modal.locator('input[placeholder="26.99"]');
  }

  get providerKeyFeatures(): Locator {
    return this.modal.locator('textarea[placeholder*="No prepayment"]');
  }

  get inHouseFinancingToggle(): Locator {
    return this.modal.locator('button[role="switch"]').last();
  }

  // -------------------------------------------------------------------------
  // Service Pricing
  // -------------------------------------------------------------------------

  get cdtCodeInput(): Locator {
    return this.modal.locator('input[name="cdtCode"]');
  }

  get serviceNameInput(): Locator {
    return this.modal.locator('input[name="serviceName"]');
  }

  get servicePriceInput(): Locator {
    return this.modal.locator('input[name="price"]');
  }

  // -------------------------------------------------------------------------
  // Active Offers
  // NOTE: input[name="price"] is shared with servicePriceInput
  //       Safe here because modals don't overlap
  // -------------------------------------------------------------------------

  get offerNameInput(): Locator {
    return this.modal.locator('input[name="name"]');
  }

  get promotionalPriceInput(): Locator {
    return this.modal.locator('input[name="price"]');
  }

  get originalPriceInput(): Locator {
    return this.modal.locator('input[name="originalPrice"]');
  }

  get includedServicesTextarea(): Locator {
    return this.modal.locator('textarea[placeholder*="services separated"]');
  }

  get restrictionsTextarea(): Locator {
    return this.modal.locator('textarea[name="restrictions"]');
  }

  get expirationDaysInput(): Locator {
    return this.modal.locator('input[name="expirationDays"]');
  }

  // -------------------------------------------------------------------------
  // Pricing Policy
  // -------------------------------------------------------------------------

  get goodFaithToggle(): Locator {
    return this.modal.locator('button[role="switch"]').first();
  }

  get customAiScriptTextarea(): Locator {
    return this.modal.locator('textarea').first();
  }

  async selectPricingOption(text: string): Promise<void> {
    await this.modal.getByText(text, { exact: false }).first().click();
    await this.page.waitForTimeout(300);
  }
}
