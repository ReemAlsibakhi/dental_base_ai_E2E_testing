# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: insurance-billing/coverage.spec.ts >> Coverage — Accepted Insurance Plans >> additional notes 500 chars accepted
- Location: tests/insurance-billing/coverage.spec.ts:180:7

# Error details

```
TimeoutError: locator.scrollIntoViewIfNeeded: Timeout 20000ms exceeded.
Call log:
  - waiting for locator('h3').filter({ hasText: 'Coverage' }).locator('..').locator('..').getByRole('button', { name: 'Edit' }).first()

```

# Page snapshot

```yaml
- generic [ref=f2e15]:
  - generic [ref=f2e16]: D
  - generic [ref=f2e17]: e
  - generic [ref=f2e18]: "n"
  - generic [ref=f2e19]: t
  - generic [ref=f2e20]: a
  - generic [ref=f2e21]: l
  - generic [ref=f2e22]: B
  - generic [ref=f2e23]: a
  - generic [ref=f2e24]: s
  - generic [ref=f2e25]: e
```

# Test source

```ts
  1   | import { Page, Locator, expect } from '@playwright/test';
  2   | 
  3   | /**
  4   |  * BasePage — foundation for all Page Objects.
  5   |  *
  6   |  * Contains shared functionality used across ALL modules:
  7   |  *  - Navigation helpers
  8   |  *  - Modal interactions (save, cancel, error)
  9   |  *  - API response interception
  10  |  *  - Test data isolation
  11  |  */
  12  | export abstract class BasePage {
  13  |   readonly page: Page;
  14  | 
  15  |   constructor(page: Page) {
  16  |     this.page = page;
  17  |   }
  18  | 
  19  |   // -----------------------------------------------------------------------
  20  |   // Navigation — must be implemented by every POM
  21  |   // -----------------------------------------------------------------------
  22  | 
  23  |   abstract navigate(): Promise<void>;
  24  | 
  25  |   /**
  26  |    * Open Edit panel by card heading text.
  27  |    * Works for all settings modules — finds Edit button next to h3 heading.
  28  |    */
  29  |   async openEdit(cardName: string): Promise<void> {
  30  |     const editBtn = this.page
  31  |       .locator('h3')
  32  |       .filter({ hasText: cardName })
  33  |       .locator('..')
  34  |       .locator('..')
  35  |       .getByRole('button', { name: 'Edit' })
  36  |       .first();
> 37  |     await editBtn.scrollIntoViewIfNeeded();
      |                   ^ TimeoutError: locator.scrollIntoViewIfNeeded: Timeout 20000ms exceeded.
  38  |     await editBtn.click();
  39  |     await expect(this.modal).toBeVisible();
  40  |   }
  41  | 
  42  |   // -----------------------------------------------------------------------
  43  |   // Modal — shared across all modules
  44  |   // -----------------------------------------------------------------------
  45  | 
  46  |   get modal(): Locator {
  47  |     return this.page.locator('[role="dialog"]');
  48  |   }
  49  | 
  50  |   get saveButton(): Locator {
  51  |     return this.modal.getByRole('button', { name: 'Save Changes' });
  52  |   }
  53  | 
  54  |   get cancelButton(): Locator {
  55  |     return this.modal.getByRole('button', { name: 'Cancel' });
  56  |   }
  57  | 
  58  |   get error(): Locator {
  59  |     return this.modal.locator("p[id$='-error']").first();
  60  |   }
  61  | 
  62  |   async cancel(): Promise<void> {
  63  |     try {
  64  |       if (await this.cancelButton.isVisible()) {
  65  |         await this.cancelButton.click();
  66  |         const discard = this.page.getByRole('button', { name: 'Discard' });
  67  |         if (await discard.isVisible()) await discard.click();
  68  |       }
  69  |     } catch { /* panel may already be closed */ }
  70  |   }
  71  | 
  72  |   async saveAndAssertSuccess(): Promise<void> {
  73  |     await this.saveButton.scrollIntoViewIfNeeded();
  74  |     // Start listening before click — avoids race condition with fast responses
  75  |     await Promise.all([
  76  |       this.waitForApiSuccess(),
  77  |       this.saveButton.click(),
  78  |     ]);
  79  |   }
  80  | 
  81  |   // -----------------------------------------------------------------------
  82  |   // Fill methods
  83  |   //
  84  |   // Playwright's fill() dispatches real InputEvents internally.
  85  |   // React intercepts these correctly in all modern versions.
  86  |   // Dirty state is solved by unique() test data — not fill() workarounds.
  87  |   // -----------------------------------------------------------------------
  88  | 
  89  |   async fill(locator: Locator, value: string): Promise<void> {
  90  |     await locator.scrollIntoViewIfNeeded();
  91  |     await locator.fill(value);
  92  |   }
  93  | 
  94  |   async fillAndBlur(locator: Locator, value: string): Promise<void> {
  95  |     await locator.scrollIntoViewIfNeeded();
  96  |     await locator.fill(value);
  97  |     await locator.press('Tab');
  98  |   }
  99  | 
  100 |   // -----------------------------------------------------------------------
  101 |   // API response interception
  102 |   //
  103 |   // Toasts disappear in ~1s — too fast for Playwright to catch reliably.
  104 |   // Network response interception is the correct, reliable approach.
  105 |   // -----------------------------------------------------------------------
  106 | 
  107 |   async waitForApiSuccess(
  108 |     urlPattern?: string | RegExp,
  109 |     timeout = 15_000
  110 |   ): Promise<void> {
  111 |     await this.page.waitForResponse(
  112 |       (response) => {
  113 |         const urlMatch = urlPattern
  114 |           ? response.url().match(urlPattern) !== null
  115 |           : true;
  116 |         return (
  117 |           urlMatch &&
  118 |           ['POST', 'PUT', 'PATCH'].includes(response.request().method()) &&
  119 |           [200, 201, 204].includes(response.status())
  120 |         );
  121 |       },
  122 |       { timeout }
  123 |     );
  124 |   }
  125 | 
  126 |   // -----------------------------------------------------------------------
  127 |   // Test data isolation
  128 |   //
  129 |   // Unique values prevent dirty state — no fill() workarounds needed.
  130 |   // -----------------------------------------------------------------------
  131 | 
  132 |   static unique(prefix = 'Test'): string {
  133 |     return `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 5)}`;
  134 |   }
  135 | }
  136 | 
```