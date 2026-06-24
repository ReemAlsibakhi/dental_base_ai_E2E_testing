# Automation Strategy Decision Report
## Module: Settings → Tab 1 — Profile
**Prepared by:** Senior Automation Engineer
**Based on:** `tab1-profile-test-cases.md`
**Stack:** Python + Playwright
**Date:** 2026-06
**Version:** 2.0 — Updated with boundary corrections + new gap analysis

---

## Changelog (v1.0 → v2.0)

| # | Correction | Impact |
|---|-----------|--------|
| 1 | TC-B-P-FN-03/04 (First Name max boundary) upgraded from Medium → **High Priority** | BVA pairs must always share the same priority |
| 2 | TC-B-P-LN-03/04 (Last Name max boundary) upgraded from Medium → **High Priority** | Same rule |
| 3 | **New rule R-PH-4** added: Phone maximum = 10 digits (exact-length field) | Max was missing from source document |
| 4 | **2 new TCs added**: TC-B-P-PH-03, TC-B-P-PH-04 (phone exceed-max boundary) | High Priority |
| 5 | **New rule R-AU-EM-4** added: Email maximum = 254 chars (RFC 5321 standard) | Max was flagged as a gap in source |
| 6 | **4 new TCs added**: TC-B-P-AU-EM-01 to AU-EM-04 (email boundary cases) | Pending dev confirmation |
| 7 | Total TC count updated: 106 → **118 TCs** | +12 new cases |

---

## Executive Summary

| Category | Count | % of Total |
|----------|-------|-----------|
| **Automate — High Priority** | **82 TCs** | **69%** |
| **Automate — Medium Priority** | **14 TCs** | **12%** |
| **Remain Manual** | **16 TCs** | **14%** |
| **Pending Confirmation** | **6 TCs** | **5%** |
| **Total** | **118 TCs** | 100% |

**Recommendation:** 96 test cases (81%) are suitable for automation.
6 cases are pending dev/business confirmation before they can be classified.
The remaining 16 (14%) have low ROI or require human judgment and should stay manual.

> **BVA Golden Rule applied throughout this report:**
> *"Boundary pairs are always the same priority. If below-min is High, above-max is High. Never split a boundary pair."*

---

## Section 1 — Automation Readiness Matrix

---

### 1A. HIGH PRIORITY FOR AUTOMATION ✅

> Deterministic, data-driven, regression-stable, directly protect core business logic.
> Every CI run must include these.

---

#### FIELD: First Name (Edit Profile)

| TC ID | Description | Boundary Type | Why Automate |
|-------|-------------|---------------|--------------|
| TC-F-P-FN-01 | Valid simple name + save | — | Smoke gate — if this fails, nothing else matters. |
| TC-N-P-FN-01 | Empty First Name | — | Required field — blocks save. Core regression gate. |
| TC-N-P-FN-02 | Whitespace-only | — | Trim logic — easy to regress silently. |
| TC-N-P-FN-03 | Digits in name | — | Char validation — data-driven, runs in <1s. |
| TC-N-P-FN-04 | @ symbol | — | Same rule, different char class — parameterisable. |
| TC-N-P-FN-05 | Underscore | — | Same rule — covers symbol rejection group. |
| TC-N-P-FN-07 | XSS script tag | — | Security — must never regress; 0 tolerance. |
| TC-N-P-FN-08 | Consecutive hyphens | — | Business rule R-FN-5 — unique to this app. |
| TC-N-P-FN-09 | Consecutive apostrophes | — | Same rule, different char — parameterisable. |
| TC-N-P-FN-10 | Mixed consecutive (hyphen+apostrophe) | — | Edge case of R-FN-5 — silently missed in PRs. |
| TC-N-P-FN-12 | Leading hyphen | — | R-FN-6 — start/end constraint. |
| TC-N-P-FN-13 | Trailing hyphen | — | R-FN-6 — symmetric to leading. |
| TC-N-P-FN-14 | Leading apostrophe | — | R-FN-6 — same rule, different char. |
| TC-N-P-FN-15 | Trailing apostrophe | — | R-FN-6 — closes the boundary on all 4 cases. |
| TC-B-P-FN-01 | Exact minimum (2 chars) | Min valid | Boundary — classic off-by-one regression. |
| TC-B-P-FN-02 | One below minimum (1 char) | Min invalid | Boundary pair — always pair with TC-B-FN-01. |
| TC-B-P-FN-03 | Exact maximum (50 chars) ⬆️ *upgraded* | Max valid | **BVA pair — must match TC-B-FN-04 priority.** Data integrity: does app accept exactly 50? |
| TC-B-P-FN-04 | One above maximum (51 chars) ⬆️ *upgraded* | Max invalid | **BVA pair — does app actually enforce the 50-char limit or silently save 200 chars?** |
| TC-B-P-FN-05 | Single space only | — | Trim + required combined — subtle edge case. |
| TC-R-P-FN-01 | Fix invalid → save succeeds | — | Regression: stale error state is a common bug. |
| TC-R-P-FN-02 | Card updates after save | — | Regression: UI sync without reload. |
| TC-U-P-FN-02 | Error clears on correction | — | UX regression — frequently broken after refactors. |

---

#### FIELD: Last Name (Edit Profile)

| TC ID | Description | Boundary Type | Why Automate |
|-------|-------------|---------------|--------------|
| TC-F-P-LN-01 | Valid simple last name + save | — | Smoke gate. |
| TC-N-P-LN-01 | Empty Last Name | — | Required field. |
| TC-N-P-LN-02 | Whitespace-only | — | Trim logic. |
| TC-N-P-LN-03 | Digits in last name | — | Char validation. |
| TC-N-P-LN-04 | @ symbol | — | Same rule. |
| TC-N-P-LN-05 | Underscore | — | Same rule. |
| TC-N-P-LN-07 | XSS injection (`<img onerror>`) | — | Security — different payload than FN-07. Must test both. |
| TC-N-P-LN-08 | Consecutive hyphens | — | R-LN-5 — business rule must not regress. |
| TC-N-P-LN-09 | Consecutive apostrophes | — | R-LN-5 — parameterisable. |
| TC-N-P-LN-10 | Mixed consecutive | — | R-LN-5. |
| TC-N-P-LN-12 | Leading hyphen | — | R-LN-6. |
| TC-N-P-LN-13 | Trailing hyphen | — | R-LN-6. |
| TC-N-P-LN-14 | Leading apostrophe | — | R-LN-6. |
| TC-N-P-LN-15 | Trailing apostrophe | — | R-LN-6. |
| TC-B-P-LN-01 | Exact minimum (2 chars) | Min valid | Boundary. |
| TC-B-P-LN-02 | One below minimum (1 char) | Min invalid | Boundary pair. |
| TC-B-P-LN-03 | Exact maximum (50 chars) ⬆️ *upgraded* | Max valid | **BVA pair — same justification as FN-03.** |
| TC-B-P-LN-04 | One above maximum (51 chars) ⬆️ *upgraded* | Max invalid | **BVA pair — same justification as FN-04.** |
| TC-B-P-LN-05 | Single space only | — | Trim + required. |
| TC-R-P-LN-01 | Fix invalid → save succeeds | — | Regression. |

---

#### FIELD: Phone Number (Edit Profile)

> ⚠️ **v2.0 Update:** Phone is an **exact-length field** — min AND max = 10 digits.
> Rule R-PH-4 (Maximum 10 digits) was missing from the source document and is added here.
> This requires 2 new boundary TCs (TC-B-P-PH-03, TC-B-P-PH-04).

**Updated rules:**

| Rule | Description |
|------|-------------|
| R-PH-1 | Optional — empty accepted |
| R-PH-2 | Minimum 10 digits if provided |
| R-PH-3 | Digits only — alpha stripped |
| R-PH-4 ✨ NEW | Maximum 10 digits — more than 10 digits rejected |

| TC ID | Description | Boundary Type | Why Automate |
|-------|-------------|---------------|--------------|
| TC-F-P-PH-01 | Valid 10-digit phone + save | — | Positive path — verifies phone saves correctly. |
| TC-F-P-PH-02 | Empty phone (optional) | — | R-PH-1 — optional field must not block save. |
| TC-N-P-PH-01 | Short phone (5 digits) | — | R-PH-2 — min-digit constraint. |
| TC-N-P-PH-02 | Alpha input stripped | — | R-PH-3 — strip behaviour must not regress. |
| TC-B-P-PH-01 | Exactly 10 digits | Exact valid | Boundary — the only valid length. |
| TC-B-P-PH-02 | 9 digits (one below) | Min invalid | Boundary pair for minimum. |
| TC-B-P-PH-03 ✨ NEW | 11 digits (one above max) | Max invalid | **R-PH-4 — does app reject 11 digits?** |
| TC-B-P-PH-04 ✨ NEW | 15 digits (well above max) | Max invalid | **R-PH-4 — stress test for max enforcement.** |
| TC-R-P-PH-01 | Fix short phone → save | — | Regression: error recovery path. |

---

#### FEATURE: Add User — Email

> ⚠️ **v2.0 Update:** Email follows RFC 5321 standard — max 254 chars total.
> Rule R-AU-EM-4 added. 4 new boundary TCs added (pending dev confirmation on whether
> the app enforces RFC limit or has a custom shorter limit).

**Updated rules:**

| Rule | Description |
|------|-------------|
| R-AU-EM-1 | Required |
| R-AU-EM-2 | Valid format |
| R-AU-EM-3 | Not already a member |
| R-AU-EM-4 ✨ NEW | Maximum 254 characters (RFC 5321) |

| TC ID | Description | Boundary Type | Why Automate |
|-------|-------------|---------------|--------------|
| TC-F-P-AU-01 | Valid email → invite sent | — | Core happy path — business-critical. |
| TC-N-P-AU-01 | Empty email | — | Required field. |
| TC-N-P-AU-02 | No domain (`notanemail`) | — | Format validation. |
| TC-N-P-AU-03 | Missing domain (`user@`) | — | Format validation. |
| TC-N-P-AU-04 | Missing local (`@domain.com`) | — | Format validation. |
| TC-N-P-AU-05 | Duplicate email | — | R-AU-EM-3 — business rule, backend call. |
| TC-U-P-AU-02 | Count increments after add | — | UI sync regression — common bug pattern. |
| TC-S-P-AU-01 | Non-admin cannot see Add User | — | RBAC — security regression must be automated. |
| TC-R-P-AU-01 | Added user in View All immediately | — | UI sync without reload — regression gate. |

---

#### FEATURE: Add User — Username

| TC ID | Description | Boundary Type | Why Automate |
|-------|-------------|---------------|--------------|
| TC-F-P-UN-01 | Valid username accepted | — | Smoke. |
| TC-N-P-UN-01 | Empty username | — | Required. |
| TC-N-P-UN-02 | Uppercase letters | — | R-UN-3 — lowercase-only rule. |
| TC-N-P-UN-03 | Space in username | — | R-UN-3 — spaces rejected. |
| TC-N-P-UN-04 | @ symbol | — | R-UN-3. |
| TC-N-P-UN-05 | Consecutive dots | — | R-UN-4. |
| TC-N-P-UN-06 | Consecutive hyphens | — | R-UN-4. |
| TC-N-P-UN-09 | Leading underscore | — | R-UN-5. |
| TC-N-P-UN-10 | Trailing underscore | — | R-UN-5. |
| TC-N-P-UN-13 | Duplicate username | — | R-UN-6 — uniqueness check. |
| TC-N-P-UN-14 | Case-insensitive duplicate | — | R-UN-6 — subtle uniqueness rule. |
| TC-B-P-UN-01 | Exact minimum (3 chars) | Min valid | Boundary. |
| TC-B-P-UN-02 | One below minimum (2 chars) | Min invalid | Boundary pair. |
| TC-B-P-UN-04 | Exact maximum (30 chars) | Max valid | Boundary. |
| TC-B-P-UN-05 | One above maximum (31 chars) | Max invalid | Boundary pair. |
| TC-S-P-UN-01 | XSS in username | — | Security. |

---

#### FEATURE: View All Users

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-F-P-VA-02 | Row count matches card count | Data integrity — count mismatch is a real bug. |
| TC-S-P-VA-01 | Non-admin cannot access View All | RBAC — security regression. |
| TC-R-P-VA-01 | Name updates in View All after edit | Cross-feature sync regression. |

---

#### CROSS-FIELD: Security & Session

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-S-P-SES-02 | Non-admin cannot access Edit Profile | RBAC — security gate. |

---

#### CROSS-FORM: Regression

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-R-P-FN-CROSS-01 | First Name validates same in Add User | Cross-form parity — silently diverges in refactors. |
| TC-R-P-LN-CROSS-01 | Last Name validates same in Add User | Same reason. |

---

### 1B. MEDIUM PRIORITY FOR AUTOMATION ✅

> Valid but lower regression risk. Automate in Phase 2 after high-priority suite is stable.

| TC ID | Description | Justification |
|-------|-------------|---------------|
| TC-F-P-FN-02 | Hyphen in middle of First Name | Valid char rule — parameterise with TC-F-01. |
| TC-F-P-FN-03 | Apostrophe in First Name | Same rule, different char. |
| TC-F-P-FN-04 | Internal space in First Name | Same rule. |
| TC-F-P-FN-05 | Arabic Unicode First Name | Unicode support — medium risk of regression. |
| TC-F-P-FN-06 | Accented Latin First Name | Same as above. |
| TC-B-P-FN-06 | Min valid name with hyphen (A-B) | Boundary for R-FN-5/6 combined. |
| TC-F-P-LN-02 | Hyphen in Last Name | Same as FN-02. |
| TC-F-P-LN-03 | Apostrophe in Last Name | Same as FN-03. |
| TC-F-P-LN-04 | Spaces in Last Name | Same as FN-04. |
| TC-F-P-LN-05 | Arabic Unicode Last Name | Same as FN-05. |
| TC-F-P-LN-06 | Accented Latin Last Name | Same as FN-06. |
| TC-N-P-FN-06 | Emoji in First Name | Medium risk — emoji handling can silently break. |
| TC-N-P-LN-06 | Emoji in Last Name | Same. |
| TC-F-P-VA-01 | View All opens with correct columns | UI structure — moderate regression risk. |

---

### 1C. PENDING CONFIRMATION 🔶

> Cannot be classified until dev/business confirms the behaviour.
> **Do not automate until confirmed.**

| TC ID | Description | Blocking Question | Action |
|-------|-------------|-------------------|--------|
| TC-B-P-AU-EM-01 ✨ NEW | Email exactly 254 chars (RFC max valid) | Does the app enforce RFC 5321 or a custom limit? | Ask dev team |
| TC-B-P-AU-EM-02 ✨ NEW | Email 255 chars (one above RFC max) | Same | Ask dev team |
| TC-B-P-AU-EM-03 ✨ NEW | Local part exactly 64 chars | Does app validate local part length separately? | Ask dev team |
| TC-B-P-AU-EM-04 ✨ NEW | Local part 65 chars (one above) | Same | Ask dev team |
| TC-N-P-UN-15 | XSS in username | Username field existence unconfirmed | Manual live check first |
| TC-B-P-UN-06 | Boundary for consecutive specials (username) | Same | Manual live check first |

---

### 1D. SHOULD REMAIN MANUAL 🛑

> Low ROI, subjective judgment, flaky by nature, or infrastructure-dependent.

| TC ID | Description | Why Manual |
|-------|-------------|-----------|
| TC-F-P-FN-07 | Mixed Latin + Arabic | Low priority (P-Low in source). Rare real-world data. ROI too low. |
| TC-N-P-FN-11 | Mixed consecutive (apostrophe+hyphen) | Near-duplicate of FN-10. One covers the rule; second adds cost with minimal signal. |
| TC-N-P-LN-11 | Mixed consecutive (Last Name) | Same reason as FN-11. |
| TC-U-P-FN-01 | Cancel discards First Name change | Tests user intent — requires human judgment on perceived behaviour. |
| TC-U-P-LN-01 | Error clears when Last Name corrected | Structurally covered by TC-U-P-FN-02 pattern. Duplicate maintenance cost. |
| TC-U-P-AU-01 | Cancel Add User sends no invite | Needs inbox/API mock to verify no email sent — infrastructure overhead unjustified. |
| DEF-P-01 | "No phone" shows no add-phone prompt | UX/discoverability defect — subjective, not a pass/fail rule. |
| DEF-P-02 | Email field not visually marked read-only | Visual design defect — requires human eye. |
| TC-F-P-VA-01 (layout) | Column layout correct in View All | Column existence automatable; visual alignment needs human verification. |
| R-EM-1 gap | Email field has no edit cursor in modal | "No cursor appears" assertion is flaky headless. Better confirmed visually. |
| TC-S-P-SES-01 | Back button after logout shows no settings | Browser history behaviour varies by browser/OS — flaky in CI. |
| Server-side R-FN-3/R-LN-3 | API-level max-50 enforcement | Requires separate API test layer, not E2E UI automation. |
| Max phone custom behaviour | If app truncates vs. rejects 11 digits | Cannot know without manual test or API spec — classify after confirmation. |

---

## Section 2 — Boundary Value Analysis — Complete Reference

> This section documents every boundary pair in the module for traceability.
> **Rule: Pairs always share the same priority.**

| Field | Rule | Min | Max | Min valid | Min-1 invalid | Max valid | Max+1 invalid | All High? |
|-------|------|-----|-----|-----------|---------------|-----------|---------------|-----------|
| First Name | R-FN-2/3 | 2 | 50 | `Jo` (2) | `J` (1) | 50-char string | 51-char string | ✅ Yes |
| Last Name | R-LN-2/3 | 2 | 50 | `Li` (2) | `L` (1) | 50-char string | 51-char string | ✅ Yes |
| Phone | R-PH-2/4 | 10 | **10** | `6035551234` | `603555123` (9) | `6035551234` | `60355512345` (11) | ✅ Yes |
| Username | R-UN-2 | 3 | 30 | `abc` (3) | `ab` (2) | 30-char string | 31-char string | ✅ Yes |
| Email (Add User) | R-AU-EM-4 | format | **254** | — | — | 254-char email | 255-char email | 🔶 Pending |

---

## Section 3 — New Rules Added in v2.0

### R-PH-4 — Phone Number: Maximum 10 digits

```
Rule:    Phone number must not exceed 10 digits.
Valid:   6035551234  (10 digits) → accepted
Invalid: 60355512345 (11 digits) → "Phone number cannot exceed 10 digits"
Invalid: 123456789012345 (15 digits) → same error
Error:   "Phone number cannot exceed 10 digits"
Note:    This makes Phone an exact-length field (min = max = 10 digits).
         Empty remains valid (R-PH-1 — optional).
Action:  Confirm error message text with dev team before automating.
```

### R-AU-EM-4 — Add User Email: Maximum 254 characters (RFC 5321)

```
Rule:    Email must not exceed 254 characters total (RFC 5321 standard).
         Local part (before @): max 64 characters.
         Domain part (after @): max 255 characters.
         Total: max 254 characters.
Valid:   Any valid email ≤ 254 chars → accepted
Invalid: 255-char email → error (message TBD — confirm with dev team)
Note:    Some apps enforce a shorter custom limit (e.g. 100 chars).
         MUST verify against live app or API spec before automating.
Action:  Ask dev team: "What is the maximum email length accepted by the API?"
```

---

## Section 4 — Execution Roadmap (Updated)

### Phase 1 — Foundation & Smoke (Week 1)
**Goal:** Auth, navigation, Edit modal working end-to-end.

| Step | Task |
|------|------|
| 1.1 | Confirm live selectors (done via browser inspection) |
| 1.2 | Implement `LoginPage` with Keycloak SSO + auth state reuse |
| 1.3 | Implement `ProfilePage` POM |
| 1.4 | Write smoke suite: TC-F-P-FN-01, TC-F-P-LN-01, TC-F-P-PH-01, TC-F-P-AU-01 |
| 1.5 | Confirm suite runs green headed + headless |
| 1.6 | Set up `pytest.ini` markers + HTML report |

**Exit criterion:** 4 smoke tests pass in CI.

---

### Phase 2 — Core Validation (Week 2)
**Goal:** Full First Name, Last Name, and Phone coverage including all boundary pairs.

| Step | Task |
|------|------|
| 2.1 | Add R-PH-4 max rule to `test_data/profile_data.py` |
| 2.2 | Write `test_edit_profile_first_name.py` — TC-N + TC-B including upgraded FN-03/04 |
| 2.3 | Write `test_edit_profile_last_name.py` — TC-N + TC-B including upgraded LN-03/04 |
| 2.4 | Write `test_edit_profile_phone.py` — including new TC-B-P-PH-03 and PH-04 |
| 2.5 | Write cross-form regression TCs |
| 2.6 | Verify error messages for phone max against live app |

**Exit criterion:** 45+ tests pass. All boundary pairs covered.

---

### Phase 3 — Add User, Username & Security (Week 3)
**Goal:** Complete Add User + RBAC.

| Step | Task |
|------|------|
| 3.1 | Confirm Username field exists in live Add User form |
| 3.2 | Confirm email max length with dev team |
| 3.3 | Write `test_add_user.py` — email validation TCs |
| 3.4 | Write `test_add_user_username.py` (if field confirmed) |
| 3.5 | Write `test_profile_security.py` — RBAC tests |
| 3.6 | If email max confirmed: add TC-B-P-AU-EM-01/02 |

**Exit criterion:** 65+ tests pass. Security suite runs with non-admin credentials.

---

### Phase 4 — View All, Medium Priority & CI (Week 4)
**Goal:** Full coverage + pipeline.

| Step | Task |
|------|------|
| 4.1 | Write `test_account_users_view_all.py` |
| 4.2 | Add medium-priority Unicode + accented name cases |
| 4.3 | Add emoji rejection cases |
| 4.4 | Configure CI: `smoke` on PR, `regression` nightly |
| 4.5 | Add screenshot-on-failure + video recording |
| 4.6 | Document selector maintenance guide |

**Exit criterion:** 96 tests pass. CI pipeline green.

---

## Section 5 — Risk Register (Updated)

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Buttons have no `id`/`data-testid` | **Confirmed** | High | Request `data-testid` from devs for Edit, Save, Cancel, Add User, View All |
| Radix UI dynamic error ids | **Confirmed** | Medium | Use `#input_id + p.text-red-500` adjacent sibling selector |
| R-PH-4 error message text unknown | High | Medium | Confirm exact error message with dev before writing assertions |
| Email max limit may differ from RFC | Medium | Medium | Ask dev team before automating email boundary TCs |
| Username field may not exist | **Flagged in source** | Medium | Manual live check before Phase 3 |
| Keycloak session expiry mid-suite | Low | High | Auth state saved to disk; re-login if 401 detected |
| Error message text changes in release | Medium | Medium | Centralise all strings in `test_data/profile_data.py` |
| `networkidle` SPA timeout | **Confirmed + Fixed** | High | Using `domcontentloaded` (already implemented) |

---

## Section 6 — Sign-off Checklist

**Before Phase 1:**
- [ ] Dev team adds `data-testid` to: Edit, Save Changes, Cancel, Add User, View All buttons
- [ ] Non-admin test account credentials provided for RBAC tests
- [ ] CI environment configured with Python + Playwright

**Before Phase 2:**
- [ ] Confirm exact error message for phone > 10 digits (R-PH-4)
- [ ] Confirm phone field rejects 11+ digits vs. silently truncates

**Before Phase 3:**
- [ ] Confirm Username field exists separately in Add User form (manual check)
- [ ] Confirm email maximum length: RFC 5321 (254) or custom app limit?
- [ ] Agree on which branch triggers smoke vs. full regression in CI

---

*Ready to proceed to code generation upon your approval.*
