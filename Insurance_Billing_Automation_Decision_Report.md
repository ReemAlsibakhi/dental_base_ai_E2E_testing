# Insurance & Billing — Automation Decision Report

**Module:** `/settings?settingTab=Insurance+%26+Billing`
**Source:** QA Test Report Tab 6 (2026-07-21)
**Date:** 2026-07-29

---

## Automation Approach

### Framework
TypeScript + Playwright — matches the app's React-first architecture.

### Page Object
`InsuranceBillingPage` extends `BasePage`:
- `openEdit(cardName)` — opens Edit panel by card heading
- `saveAndAssertSuccess()` — waits for API response (POST/PUT/PATCH 200/201/204)
- `fill()` / `fillAndBlur()` — standard Playwright fill
- `unique()` — timestamp+random to prevent data conflicts

### Test Data Strategy
- Edit **existing records** where possible (5 membership plans, existing coverage plan, etc.)
- Use `BasePage.unique()` only when creating new records is unavoidable
- Never hardcode values that may already exist in DB

---

## Cards & Automation Decisions

### 1. Coverage (IB-COV-R1 to R10)
**Automate:** Yes
- Toggle, Insurance Name validation, Coverage % validation, Additional Notes
- **Not automate:** Plan Type / Network Status dropdowns (custom components, low risk)
- **Known bugs to document:** DEF-IB2-01 (1-char name saved), DEF-IB2-02 (% out of range), DEF-IB2-03 (5000 chars in notes)

### 2. Membership Plans (IB-MEM-R1 to R4)
**Automate:** Yes
- Edit existing plans (5 plans available in live data)
- Plan Name, Annual Fee, Discount % validation
- Delete confirmation (per-item delete button on each row)
- **Not automate:** Plan Type dropdown (closed list, low risk)

### 3. Finance (IB-FIN-R1 to R9)
**Automate:** Yes — Add Custom Provider flow
- Provider Name, APR, Key Features
- In-House Financing toggle
- **Bug to document:** DEF-IB2-09 (chip removal has no confirmation)
- **Not automate:** Application Process / Approval Time dropdowns

### 4. Service Pricing (IB-SVC-R1 to R4)
**Automate:** Yes — edit existing services + Add Service
- Service Name, CDT Code, Price validation
- Quick Setup button visibility
- **Bug to document:** DEF-IB2-11 (Quick Setup shows duplicates)

### 5. Active Offers (IB-OFF-R1 to R8)
**Automate:** Yes — edit existing offer + Add Offer
- Promotion Name, Price pair logic (promo > original = DEF-IB2-06), Expiration Days
- **Bug to document:** DEF-IB2-06 (negative discount accepted)

### 6. Pricing Policy (IB-PP-R1 to R3)
**Automate:** Yes
- 4 radio options, Good Faith toggle, Custom AI Script (2000 char limit)
- **Bug to document:** DEF-IB2-04 (AI Script contains injection text)

---

## What NOT to Automate

| Item | Reason |
|------|--------|
| Plan Type / Network Status dropdowns | Closed lists, low risk, custom components |
| Delete All confirmation | Risk of destroying live data |
| Quick Setup / Use Template commit | Risk of adding duplicates to live data |
| RBAC (non-admin access) | Needs separate non-admin session |
| Monthly price computation (Membership) | Needs engineering confirmation of rounding rule |

---

## Test File Structure

```
tests/insurance-billing/
  coverage.spec.ts          ← IB-COV-R1 to R10
  membership-plans.spec.ts  ← IB-MEM-R1 to R4
  finance.spec.ts           ← IB-FIN-R1 to R9
  service-pricing.spec.ts   ← IB-SVC-R1 to R4
  active-offers.spec.ts     ← IB-OFF-R1 to R8
  pricing-policy.spec.ts    ← IB-PP-R1 to R3
```

---

## Known Bugs (Documented as Tests)

| Bug ID | Description | Severity |
|--------|-------------|----------|
| DEF-IB2-01 | 1-char name saved in DB | High |
| DEF-IB2-02 | Coverage % accepts out-of-range (99999) | High |
| DEF-IB2-03 | Additional Notes holds 5000 chars (limit 500) | High |
| DEF-IB2-04 | Custom AI Script unsanitized injection text | High |
| DEF-IB2-06 | Promo price > original accepted (negative discount) | Medium |
| DEF-IB2-09 | Finance chip removal has no confirmation | Medium |
| DEF-IB2-10 | Cancel silently discards edits (4 of 5 cards) | Low |
| DEF-IB2-11 | Quick Setup shows already-added items | Medium |
