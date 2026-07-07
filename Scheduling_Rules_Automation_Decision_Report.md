# Automation Strategy Decision Report
## Module: Settings → Tab 3 — Scheduling Rules
**Prepared by:** Senior Automation Engineer
**Based on:** `tab3-scheduling-rules-test-cases.md`
**Stack:** Python + Playwright
**Date:** 2026-07
**Version:** 1.0

---

## Executive Summary

| Category | Count | % |
|----------|-------|---|
| **Automate — High Priority** | **52 TCs** | **46%** |
| **Automate — Medium Priority** | **20 TCs** | **18%** |
| **Remain Manual** | **28 TCs** | **25%** |
| **Pending Confirmation** | **12 TCs** | **11%** |
| **Total** | **112 TCs** | 100% |

---

## Key Differences from Module 1 & 2

| | Module 1 | Module 2 | Module 3 |
|--|--|--|--|
| Fields | Text inputs | Text inputs | Number inputs + toggles + time inputs |
| Toggles | Profile toggle | Radix Switch | Multiple Radix Switches per card |
| Validation | Text rules | Text rules | Numeric range (min/max) |
| Cards | 1 form | 1 form | 9 independent cards |
| Known bugs | 7 | 8 | 6 (DEF-SR-01 to 06) |
| Save confirmation | Toast | Panel closes | Toast: "Settings saved successfully!" |

---

## Section 1 — Automation Readiness Matrix

---

### 1A. HIGH PRIORITY ✅ — 52 TCs

#### Lead Time (SR·R1) — 10 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-F-SR-01 | Enable with 60 minutes | Smoke gate |
| TC-F-SR-03 | Disable toggle — field hidden | Toggle state |
| TC-N-SR-01 | Value 0 → min error | Known bug DEF-SR-01 |
| TC-N-SR-02 | Empty → required error | Required check |
| TC-N-SR-03 | Negative → error | Range check |
| TC-N-SR-04 | Decimal → error or floor | Type check |
| TC-B-SR-01 | Exactly 1 → accepted (min valid) | BVA |
| TC-B-SR-02 | 0 → error (min-1) | BVA pair |
| TC-B-SR-03 | Large value → accepted (no max) | No upper bound |
| TC-R-SR-01 | Fix invalid → save succeeds | Regression |

#### Advance Booking (SR·R2) — 8 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-F-SR-04 | Enable limit + same-day ON | Smoke gate |
| TC-F-SR-05 | Disable limit toggle | Toggle state |
| TC-F-SR-06 | Same-day OFF only | Independent toggle |
| TC-N-SR-06 | Value 0 → min error | Range check |
| TC-N-SR-07 | Negative → error | Range check |
| TC-B-SR-04 | Exactly 1 day → accepted | BVA |
| TC-B-SR-05 | 0 days → error | BVA pair |
| TC-R-SR-12 | Lead Time vs Advance Booking conflict | Cross-card regression |

#### Cancellation Policy (SR·R5) — 12 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-F-SR-18 | Enable + 24 hours → save | Smoke gate |
| TC-F-SR-19 | Disable toggle → field hidden | Toggle state |
| TC-N-SR-21 | Value 0 → min error | Range check |
| TC-N-SR-22 | Negative → error | Range check |
| TC-N-SR-23 | Empty → error | Required |
| TC-N-SR-24 | Decimal → error | Type check |
| TC-N-SR-25 | Exactly 720 → accepted (max valid) | BVA |
| TC-N-SR-26 | 721 → **no error (DEF-SR-03)** | Critical bug |
| TC-B-SR-11 | Exactly 1 → accepted | BVA |
| TC-B-SR-12 | 0 → error | BVA pair |
| TC-R-SR-02 | Fix invalid → save | Regression |
| TC-R-SR-05 | Card updates immediately after save | UI regression |

#### No-Show Policy (SR·R6) — 12 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-F-SR-20 | Enable + 30 minutes → save | Smoke gate |
| TC-F-SR-21 | Disable toggle → field hidden | Toggle state |
| TC-F-SR-22 | Switch unit Minutes → Hours | Unit toggle |
| TC-N-SR-27 | Value 0 → min error | Range check |
| TC-N-SR-28 | Negative → error | Range check |
| TC-N-SR-29 | Empty → error | Required |
| TC-N-SR-30 | Decimal → error | Type check |
| TC-N-SR-31 | Exactly 720 → accepted | BVA |
| TC-N-SR-32 | 721 → **no error (DEF-SR-04)** | Critical bug |
| TC-B-SR-13 | Exactly 1 → accepted | BVA |
| TC-B-SR-14 | 0 → error | BVA pair |
| TC-R-SR-03 | Fix invalid → save | Regression |

#### Cancellation Mode (SR·R7) — 2 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-F-SR-24 | Select Broken | Radio selection |
| TC-F-SR-25 | Select Unscheduled | Radio selection |

#### Override PMS (SR·R8) — 2 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-F-SR-26 | Enable Override PMS | Toggle state |
| TC-F-SR-27 | Disable Override PMS | Toggle state |

#### Additional Notes (SR·R4) — 4 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-F-SR-16 | Enter valid notes → save | Smoke |
| TC-F-SR-17 | Clear notes → save | Empty state |
| TC-N-SR-18 | XSS payload → check behavior | Security |
| TC-R-SR-04 | Notes triplicated (DEF-SR-02) | Known bug |

#### Smoke (Cross-card) — 2 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-SM-SR-01 | All 9 cards visible on page load | Smoke gate |
| TC-SM-SR-02 | All Edit buttons clickable | Smoke gate |

---

### 1B. MEDIUM PRIORITY ✅ — 20 TCs

| TC ID | Description | Justification |
|-------|-------------|---------------|
| TC-F-SR-02 | Lead Time with Hours unit | Unit variation |
| TC-F-SR-07 | Both Advance Booking toggles OFF | Edge state |
| TC-N-SR-03/04/05 | Lead Time: negative, decimal, text | Type validation |
| TC-N-SR-08/09/10 | Advance Booking: negative, decimal, text | Type validation |
| TC-R-SR-06/07/08 | Persist after reload (Lead/Cancel/NoShow) | Persistence |
| TC-R-SR-13 | Re-enable clears prior value | State management |
| TC-F-SR-28/29/30 | Holiday: Standard/Minimal/Clear All | Preset buttons |
| TC-F-SR-31/32/33 | Holiday: checkbox toggle × 3 | Checkbox behavior |
| TC-N-SR-33/34/35 | Holiday: invalid custom holiday | Validation |

---

### 1C. REMAIN MANUAL 🛑 — 28 TCs

| TC ID | Description | Why Manual |
|-------|-------------|-----------|
| TC-F-SR-08 to 15 | Business Hours full suite | time inputs complex + cross-field validation |
| TC-B-SR-06/07/08 | Business Hours boundary | time input BVA |
| TC-U-SR-06/07/08 | Apply to All button | Copies hours to multiple days — visual check |
| TC-U-SR-01 to 05 | Discard dialog (UX) | Human judgment |
| TC-S-SR-03/04 | RBAC + HIPAA/URL | DevTools + server-side |
| TC-R-SR-09/10/11 | Break/PMS/Holiday persist | Compound state |
| TC-U-SR-09/10 | Holiday schedule UX | Visual check |
| TC-F-SR-09/10/11 | Enable/disable business days | time input state |

---

### 1D. PENDING CONFIRMATION 🔶 — 12 TCs

| Item | Blocking Question |
|------|-------------------|
| TC-B-SR-09/10 | Additional Notes: is 1000-char limit enforced by JS? |
| TC-S-SR-01/02 | XSS: does app sanitize or just display raw HTML? |
| TC-N-SR-05 | Lead Time: text input rejected or silently NaN'd? |
| TC-F-SR-12 to 15 | Business Hours break add/delete/apply — DOM selectors unconfirmed |
| TC-U-SR-10 | Holiday UX — custom holiday form fields unconfirmed |

---

## Section 2 — Known Bugs (from test cases file)

| ID | Severity | Description |
|----|----------|-------------|
| DEF-SR-01 | 🟡 Medium | Lead Time defaults to 0 on enable (min=1 violated) |
| DEF-SR-02 | 🟡 Medium | Additional Notes triplicated in DOM when panel opens |
| DEF-SR-03 | 🔴 Critical | Cancellation Policy max=720 not enforced — 721+ saves |
| DEF-SR-04 | 🔴 Critical | No-Show Policy max=720 not enforced — 43260 persisted |
| DEF-SR-05 | 🟡 Medium | Advance Booking unit mismatch: form=Days, card=Months |
| DEF-SR-06 | 🟡 Medium | Additional Notes maxLength=-1, 1000-char limit unverified |

---

## Section 3 — Execution Roadmap

### Phase 1 — Foundation + Smoke (Week 1)
- Confirm selectors via live DOM for all 9 cards
- Build `scheduling_rules_page.py` POM
- 4 smoke tests

### Phase 2 — Numeric Fields: Lead Time + Cancellation + No-Show (Week 2)
- 34 TCs covering SR·R1, SR·R5, SR·R6

### Phase 3 — Advance Booking + Mode + Override + Notes (Week 3)
- 18 TCs covering SR·R2, SR·R7, SR·R8, SR·R4

### Phase 4 — Medium Priority + Holiday + CI Update (Week 4)
- 20 TCs + CI update

---

## Section 4 — Risk Register

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Business Hours time inputs | High | Manual only — complex cross-field validation |
| DEF-SR-03/04 max not enforced | Critical | Tests marked @xfail — document bugs |
| DEF-SR-01 defaults to 0 | Medium | Test verifies bug behavior |
| Radix toggles (same pattern) | Low | Use button[role="switch"] — proven in Module 2 |
| 9 separate Edit panels | Medium | Separate fixture per card group |
| Save toast different from Module 2 | Low | Confirmed: "Settings saved successfully!" |

---

*Ready to proceed to Phase 1 upon approval.*
