import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

/**
 * InsuranceBillingPage
 *
 * URL: /settings?settingTab=Insurance+%26+Billing
 *
 * Inherits from BasePage:
 *   openEdit(), modal, saveButton, cancelButton, error,
 *   cancel(), saveAndAssertSuccess(), fill(), fillAndBlur(),
 *   waitForApiSuccess(), unique()
 *
 * Save patterns (confirmed from live DOM):
 *   Toggle-only:  saveAndAssertSuccess()
 *   New Plan:     addPlan() → Save Plan (local) → saveAndAssertSuccess()
 *
 * NOTE: input[name="name"] and input[name="price"] are shared across cards.
 * All locators scoped to this.modal — safe because modals never overlap.
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

  override async navigate(): Promise<void> {
    await this.page.goto(InsuranceBillingPage.URL);
    await this.page.waitForLoadState('domcontentloaded');
  }

  // -------------------------------------------------------------------------
  // Coverage — Save Plan button (unique to this card's Add Custom flow)
  // -------------------------------------------------------------------------

  get savePlanButton(): Locator {
    return this.modal.getByRole('button', { name: 'Save Plan' });
  }

  async savePlanAndAssertSuccess(): Promise<void> {
    await this.savePlanButton.scrollIntoViewIfNeeded();
    await this.savePlanButton.click();
    await expect(this.savePlanButton).not.toBeVisible();
    await this.saveAndAssertSuccess();
  }

  assertDeleteConfirmationShown(): Promise<void> {
    return expect(this.page.getByText('cannot be undone')).toBeVisible();
  }

  // -------------------------------------------------------------------------
  // Coverage — Accepted Insurance Plans
  // -------------------------------------------------------------------------

  get acceptAllToggle(): Locator {
    return this.modal.locator('button[role="switch"]').first();
  }

  get addCustomButton(): Locator {
    return this.modal.getByRole('button', { name: 'Add Custom' });
  }

  get insuranceNameInput(): Locator {
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
    await expect(this.insuranceNameInput).toBeVisible();

    await this.fillAndBlur(this.insuranceNameInput, name);
    await this.fillAndBlur(this.payerIdInput, payerId);

    if (options.preventive)  await this.fillAndBlur(this.preventiveInput,  options.preventive);
    if (options.basic)       await this.fillAndBlur(this.basicInput,       options.basic);
    if (options.major)       await this.fillAndBlur(this.majorInput,       options.major);
    if (options.orthodontic) await this.fillAndBlur(this.orthodonticInput, options.orthodontic);

    await this.savePlanAndAssertSuccess();
    return { name, payerId };
  }

  // -------------------------------------------------------------------------
  // Membership Plans
  // -------------------------------------------------------------------------

  get membershipNameInput(): Locator {
    return this.modal.getByRole('textbox', { name: 'Plan Name' });
  }

  get annualFeeInput(): Locator {
    return this.modal.getByRole('spinbutton', { name: 'Annual Fee' });
  }

  get discountPercentageInput(): Locator {
    return this.modal.getByRole('spinbutton', { name: 'Discount (%)' });
  }

  get updatePlanButton(): Locator {
    return this.modal.getByRole('button', { name: 'Update Plan' });
  }

  get addMembershipPlanButton(): Locator {
    return this.modal.getByRole('button', { name: 'Add Plan' });
  }

  get deletePlanButton(): Locator {
    return this.modal.getByRole('dialog').getByRole('button', { name: 'Delete' })
  }

  /** Open the edit form for the first plan in the list */
  async openFirstPlanEdit(): Promise<void> {
    // The edit icon is an empty-text button — nth(5) targets first plan's edit
    await this.modal.getByRole('button').filter({ hasText: /^$/ }).nth(5).click();
    await expect(this.updatePlanButton).toBeVisible();
  }

  async updatePlanAndAssertSuccess(): Promise<void> {
    await this.updatePlanButton.click();
    await this.saveAndAssertSuccess();
  }

  async addMembershipPlanAndAssertSuccess(): Promise<void> {
    await this.addMembershipPlanButton.click();
    await this.saveAndAssertSuccess();
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
  }
}
