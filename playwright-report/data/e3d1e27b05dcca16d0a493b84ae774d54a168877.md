# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: insurance-billing/membership-plans.spec.ts >> Membership Plans >> TC-F-IB2-15 delete plan shows confirmation
- Location: tests/insurance-billing/membership-plans.spec.ts:196:7

# Error details

```
Error: locator.click: Error: strict mode violation: getByRole('button', { name: 'Cancel' }) resolved to 2 elements:
    1) <button type="button" class="↵        inline-flex items-center justify-center font-medium rounded-md↵        transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-600↵        disabled:opacity-50 disabled:cursor-not-allowed↵        cursor-pointer↵        border border-gray-200 bg-white hover:bg-gray-50 text-gray-700 dark:border-gray-600 dark:bg-gray-800/50 dark:hover:bg-gray-800 dark:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600↵        px-4 py-2 text-…>Cancel</button> aka getByRole('button', { name: 'Cancel' }).first()
    2) <button type="button" class="↵        inline-flex items-center justify-center font-medium rounded-md↵        transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-600↵        disabled:opacity-50 disabled:cursor-not-allowed↵        cursor-pointer↵        bg-gray-200 hover:bg-gray-300 text-gray-800 dark:bg-gray-700 dark:hover:bg-gray-600 dark:text-gray-200↵        px-4 py-2 text-sm↵        ↵      ">Cancel</button> aka getByLabel('Delete All Plans').getByRole('button', { name: 'Cancel' })

Call log:
  - waiting for getByRole('button', { name: 'Cancel' })

```

# Page snapshot

```yaml
- generic [ref=e4]:
  - complementary [ref=e5]:
    - img "DentalBase Logo" [ref=e7]
    - navigation [ref=e8]:
      - link "Overview" [ref=e9] [cursor=pointer]:
        - /url: /overview
      - link "Calls" [ref=e15] [cursor=pointer]:
        - /url: /calls
      - link "Patients" [ref=e20] [cursor=pointer]:
        - /url: /patients
      - link "Messages" [ref=e26] [cursor=pointer]:
        - /url: /messages
      - link "Tasks" [ref=e29] [cursor=pointer]:
        - /url: /tasks
      - link "Schedule" [ref=e33] [cursor=pointer]:
        - /url: /schedule
      - link "Forms" [ref=e36] [cursor=pointer]:
        - /url: /forms
      - link "Reviews" [ref=e40] [cursor=pointer]:
        - /url: /reviews
      - link "Patient Outreach" [ref=e43] [cursor=pointer]:
        - /url: /patient-outreach
      - link "Settings" [ref=e48] [cursor=pointer]:
        - /url: /settings
      - button "Phone System" [ref=e52] [cursor=pointer]
    - generic [ref=e55]:
      - button "Collapse" [ref=e56] [cursor=pointer]
      - generic [ref=e60]:
        - img "User" [ref=e61]
        - generic:
          - generic [ref=e62]:
            - paragraph [ref=e63]: Reem Sibakhi
            - paragraph [ref=e64]: User
          - button "Logout" [ref=e65]
  - generic [ref=e69]:
    - banner [ref=e70]:
      - textbox "Search patients..." [ref=e75]
      - generic [ref=e76]:
        - button [ref=e77] [cursor=pointer]
        - button "Softphone" [ref=e81] [cursor=pointer]
        - button "100+" [ref=e87] [cursor=pointer]
        - button "Logout" [ref=e92] [cursor=pointer]
    - main [ref=e96]:
      - generic [ref=e98]:
        - generic [ref=e99]:
          - heading "Settings" [level=3] [ref=e100]
          - generic [ref=e104]: "Office: Smile Dental"
        - generic [ref=e105]:
          - navigation [ref=e107]:
            - button "Profile" [ref=e108] [cursor=pointer]
            - button "Practice Profile & Hours" [ref=e109] [cursor=pointer]
            - button "Scheduling Rules" [ref=e110] [cursor=pointer]
            - button "Patient Outreach" [ref=e111] [cursor=pointer]
            - button "DentiVoice™ Customization" [ref=e112] [cursor=pointer]
            - button "Insurance & Billing" [ref=e113] [cursor=pointer]
            - button "Office Setup" [ref=e114] [cursor=pointer]
          - generic [ref=e117]:
            - generic [ref=e119]:
              - generic [ref=e120]:
                - generic [ref=e121]:
                  - heading "Coverage" [level=3] [ref=e122]
                  - paragraph [ref=e123]: Insurance acceptance policy
                - generic [ref=e125]:
                  - generic [ref=e126]: Delta_ms4npfaj_lhj
                  - generic [ref=e127]: Coverage_ms4ntcw5_upz
                  - generic [ref=e128]: Coverage_ms4qnodr_yb8
                - button "Edit" [ref=e130] [cursor=pointer]
              - generic [ref=e134]:
                - generic [ref=e135]:
                  - heading "Membership Plans" [level=3] [ref=e136]
                  - paragraph [ref=e137]: 6 membership plans
                - generic [ref=e139]:
                  - generic [ref=e140]:
                    - generic [ref=e141]:
                      - paragraph [ref=e142]: Individual Adult Plan
                      - paragraph [ref=e143]: custom • 22% discount
                    - generic [ref=e144]:
                      - paragraph [ref=e145]: $399/yr
                      - paragraph [ref=e146]: $35/mo
                  - generic [ref=e147]:
                    - generic [ref=e148]:
                      - paragraph [ref=e149]: Family Plan
                      - paragraph [ref=e150]: individual • 20% discount
                    - generic [ref=e151]:
                      - paragraph [ref=e152]: $899/yr
                      - paragraph [ref=e153]: $80/mo
                  - generic [ref=e154]:
                    - generic [ref=e155]:
                      - paragraph [ref=e156]: Family Plan
                      - paragraph [ref=e157]: senior • 15% discount
                    - generic [ref=e158]:
                      - paragraph [ref=e159]: $279/yr
                      - paragraph [ref=e160]: $25/mo
                  - button "+3 more" [ref=e161] [cursor=pointer]
                - button "Edit" [ref=e163] [cursor=pointer]
              - generic [ref=e167]:
                - generic [ref=e168]:
                  - heading "Finance" [level=3] [ref=e169]
                  - paragraph [ref=e170]: Payment financing options
                - generic [ref=e171]: 0 providers
                - button "Edit" [ref=e175] [cursor=pointer]
              - generic [ref=e179]:
                - generic [ref=e180]:
                  - heading "Service Pricing" [level=3] [ref=e181]
                  - paragraph [ref=e182]: Service pricing
                - generic [ref=e185]:
                  - generic [ref=e186]: preventive
                  - generic [ref=e187]: "2"
                - button "Edit" [ref=e189] [cursor=pointer]
              - generic [ref=e193]:
                - generic [ref=e194]:
                  - heading "Active Offers" [level=3] [ref=e195]
                  - paragraph [ref=e196]: 1 promotions
                - generic [ref=e199]:
                  - generic [ref=e200]:
                    - paragraph [ref=e201]: ds
                    - paragraph [ref=e202]: all patients
                  - generic [ref=e203]: $1
                - button "Edit" [ref=e205] [cursor=pointer]
              - generic [ref=e209]:
                - generic [ref=e210]:
                  - heading "Pricing Policy" [level=3] [ref=e211]
                  - paragraph [ref=e212]: Disclosure and discounts
                - generic [ref=e213]: Always provide exact pricing
                - button "Edit" [ref=e215] [cursor=pointer]
            - dialog "Membership Plans" [ref=e220]:
              - generic [ref=e221]:
                - generic [ref=e223]:
                  - generic [ref=e230]:
                    - heading "Membership Plans" [level=2] [ref=e231]
                    - paragraph [ref=e232]: Set up in-house membership plans for patients without insurance
                  - button "Close panel" [ref=e233] [cursor=pointer]
                - generic [ref=e237]:
                  - generic [ref=e239]:
                    - heading "Membership Plans" [level=3] [ref=e240]
                    - paragraph [ref=e241]: Manage your membership plan offerings
                  - generic [ref=e242]:
                    - button "Delete All" [ref=e243] [cursor=pointer]
                    - button "Quick Setup" [ref=e247] [cursor=pointer]
                  - generic [ref=e252]:
                    - generic [ref=e253]:
                      - paragraph [ref=e254]: Individual Adult Plan
                      - paragraph [ref=e255]: custom • $399/yr • 22% discount
                    - generic [ref=e256]:
                      - button [ref=e257] [cursor=pointer]
                      - button [ref=e261] [cursor=pointer]
                  - generic [ref=e266]:
                    - generic [ref=e267]:
                      - paragraph [ref=e268]: Family Plan
                      - paragraph [ref=e269]: individual • $899/yr • 20% discount
                    - generic [ref=e270]:
                      - button [ref=e271] [cursor=pointer]
                      - button [ref=e275] [cursor=pointer]
                  - generic [ref=e280]:
                    - generic [ref=e281]:
                      - paragraph [ref=e282]: Edit Membership Plan
                      - button [ref=e283]
                    - generic [ref=e287]:
                      - generic [ref=e289]:
                        - text: Plan Name
                        - generic [ref=e290]: "*"
                      - textbox "Plan Name" [ref=e292]: Family Plan
                    - generic [ref=e293]:
                      - generic [ref=e294]: Plan Type
                      - combobox "Plan Type" [ref=e297] [cursor=pointer]:
                        - generic: Senior
                    - generic [ref=e300]:
                      - generic [ref=e301]:
                        - generic [ref=e302]: Annual Fee ($)
                        - spinbutton "Annual Fee ($)" [ref=e305]: "279"
                      - generic [ref=e306]:
                        - generic [ref=e307]: Discount (%)
                        - spinbutton "Discount (%)" [ref=e310]: "15"
                    - button "Update Plan" [disabled] [ref=e311]
                  - generic [ref=e313]:
                    - generic [ref=e314]:
                      - paragraph [ref=e315]: Periodontal Maintenance
                      - paragraph [ref=e316]: periodontal • $499/yr • 30% discount
                    - generic [ref=e317]:
                      - button [ref=e318] [cursor=pointer]
                      - button [ref=e322] [cursor=pointer]
                  - generic [ref=e327]:
                    - generic [ref=e328]:
                      - paragraph [ref=e329]: Child/Teen Plan
                      - paragraph [ref=e330]: child • $229/yr • 25% discount
                    - generic [ref=e331]:
                      - button [ref=e332] [cursor=pointer]
                      - button [ref=e336] [cursor=pointer]
                  - generic [ref=e341]:
                    - generic [ref=e342]:
                      - paragraph [ref=e343]: Ortho Care Plan
                      - paragraph [ref=e344]: individual • $599/yr • 25% discount
                    - generic [ref=e345]:
                      - button [ref=e346] [cursor=pointer]
                      - button [ref=e350] [cursor=pointer]
                - generic [ref=e354]:
                  - button "Cancel" [ref=e355] [cursor=pointer]
                  - button "Save Changes" [disabled] [ref=e356]
                - dialog [ref=e359]:
                  - generic [ref=e360]:
                    - heading "Delete All Plans" [level=2] [ref=e361]
                    - button "Close modal" [active] [ref=e362] [cursor=pointer]
                  - paragraph [ref=e372]: Are you sure you want to delete all membership plans? This action cannot be undone.
                  - generic [ref=e373]:
                    - button "Cancel" [ref=e374] [cursor=pointer]
                    - button "Delete" [ref=e375] [cursor=pointer]
```

# Test source

```ts
  105 | 
  106 |     await insuranceBilling.fillAndBlur(insuranceBilling.membershipNameInput, 'Ortho Care Plan');
  107 |     await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '599');
  108 |     await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '25');
  109 |     await insuranceBilling.addMembershipPlanAndAssertSuccess();
  110 |   });
  111 | 
  112 |   test('EXPLORE negative discount % → behavior', async ({ insuranceBilling }) => {
  113 |     // IB-MEM-R4 states range 0–100 — negative is out of range
  114 |     // Not an explicit TC in truth source but logically invalid
  115 |     await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '-1');
  116 |     const isDisabled = await insuranceBilling.updatePlanButton.isDisabled();
  117 |     const hasError   = await insuranceBilling.error.isVisible();
  118 |     const value      = await insuranceBilling.discountPercentageInput.inputValue();
  119 |     // Document actual behavior — negative may be silently sanitized like annual fee
  120 |     console.log(`Negative discount: value=${value}, error=${hasError}, disabled=${isDisabled}`);
  121 |     // expect(Number(value)).toBeGreaterThanOrEqual(0);
  122 |     await expect(insuranceBilling.updatePlanButton).toBeDisabled();
  123 | 
  124 |   });
  125 | 
  126 |   test('valid discount % accepted', async ({ insuranceBilling }) => {
  127 |     await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '20');
  128 |     await expect(insuranceBilling.error).not.toBeVisible();
  129 |   });
  130 | 
  131 |   test('TC-N-IB2-07 discount % > 100 → error + Save disabled', async ({ insuranceBilling }) => {
  132 |     await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '150');
  133 |     await expect(insuranceBilling.error).toContainText('cannot exceed 100%');
  134 |     await expect(insuranceBilling.updatePlanButton).toBeDisabled();
  135 |   });
  136 | 
  137 |   test('TC-B-IB2-04 discount % = 100 → maximum valid', async ({ insuranceBilling }) => {
  138 |     await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '100');
  139 |     await expect(insuranceBilling.error).not.toBeVisible();
  140 |   });
  141 | 
  142 |   test('TC-B-IB2-05 discount % = 101 → one above maximum → blocked', async ({ insuranceBilling }) => {
  143 |     await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '101');
  144 |     await expect(insuranceBilling.error).toBeVisible();
  145 |     await expect(insuranceBilling.updatePlanButton).toBeDisabled();
  146 |   });
  147 | 
  148 |   test('TC-U-IB2-05 save disabled proactively when discount invalid', async ({ insuranceBilling }) => {
  149 |     await insuranceBilling.fillAndBlur(insuranceBilling.discountPercentageInput, '150');
  150 |     await expect(insuranceBilling.updatePlanButton).toBeDisabled();
  151 |   });
  152 | 
  153 |   // -------------------------------------------------------------------------
  154 |   // IB-MEM-R3 — Annual Fee
  155 |   // TC-F-IB2-05, TC-N-IB2-08, TC-B-IB2-06, TC-B-IB2-07
  156 |   // -------------------------------------------------------------------------
  157 | 
  158 |   test('TC-F-IB2-05 valid annual fee accepted', async ({ insuranceBilling }) => {
  159 |     await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '299');
  160 |     await expect(insuranceBilling.error).not.toBeVisible();
  161 |   });
  162 | 
  163 |   test('TC-N-IB2-08 negative annual fee → silently corrected (DEF)', async ({ insuranceBilling }) => {
  164 |     // DEF: minus sign is silently dropped — field shows 50 instead of -50
  165 |     // No error message shown — flagged as missing feedback issue
  166 |     await insuranceBilling.annualFeeInput.fill('-50');
  167 |     await insuranceBilling.annualFeeInput.press('Tab');
  168 |     // const value = await insuranceBilling.annualFeeInput.inputValue();
  169 |     // expect(Number(value)).toBeGreaterThanOrEqual(0);
  170 |     await expect(insuranceBilling.error).toBeVisible();
  171 |     await expect(insuranceBilling.updatePlanButton).toBeDisabled();
  172 |   });
  173 | 
  174 |   test('TC-N annual fee = 0.01 → blocked (min is 1)', async ({ insuranceBilling }) => {
  175 |     await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '0.01');
  176 |     await expect(insuranceBilling.error).toBeVisible();
  177 |     await expect(insuranceBilling.updatePlanButton).toBeDisabled();
  178 |   });
  179 | 
  180 |   test('TC-B-IB2-07 annual fee = 0 → blocked (min is 1)', async ({ insuranceBilling }) => {
  181 |     await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '0');
  182 |     await expect(insuranceBilling.error).toBeVisible();
  183 |     await expect(insuranceBilling.updatePlanButton).toBeDisabled();
  184 |   });
  185 | 
  186 |   test('TC-B-IB2-06 annual fee = 1 → minimum valid', async ({ insuranceBilling }) => {
  187 |     await insuranceBilling.fillAndBlur(insuranceBilling.annualFeeInput, '1');
  188 |     await expect(insuranceBilling.error).not.toBeVisible();
  189 |   });
  190 | 
  191 |   // -------------------------------------------------------------------------
  192 |   // IB-DEL-R1 — Delete confirmation
  193 |   // TC-F-IB2-15, TC-N-IB2-17
  194 |   // -------------------------------------------------------------------------
  195 | 
  196 |   test('TC-F-IB2-15 delete plan shows confirmation', async ({ insuranceBilling }) => {
  197 |     const deleteBtn = insuranceBilling.page
  198 |       .getByRole('dialog')
  199 |       .getByRole('button', { name: 'Delete' })
  200 |       .first();
  201 | 
  202 |     if (await deleteBtn.isVisible()) {
  203 |       await deleteBtn.click();
  204 |       await expect(insuranceBilling.page.getByText('cannot be undone')).toBeVisible();
> 205 |       await insuranceBilling.page.getByRole('button', { name: 'Cancel' }).click();
      |                                                                           ^ Error: locator.click: Error: strict mode violation: getByRole('button', { name: 'Cancel' }) resolved to 2 elements:
  206 |     } else {
  207 |       test.skip(true, 'No per-row delete button visible');
  208 |     }
  209 |   });
  210 | 
  211 |   test('TC-N-IB2-17 cancel delete keeps plan', async ({ insuranceBilling }) => {
  212 |     const planName  = await insuranceBilling.membershipNameInput.inputValue();
  213 |     const deleteBtn = insuranceBilling.page
  214 |       .getByRole('dialog')
  215 |       .getByRole('button', { name: 'Delete' })
  216 |       .first();
  217 | 
  218 |     if (await deleteBtn.isVisible()) {
  219 |       await deleteBtn.click();
  220 |       await insuranceBilling.page.getByRole('button', { name: 'Cancel' }).click();
  221 |       await expect(insuranceBilling.page.getByText(planName)).toBeVisible();
  222 |     } else {
  223 |       test.skip(true, 'No per-row delete button visible');
  224 |     }
  225 |   });
  226 | });
  227 | 
```