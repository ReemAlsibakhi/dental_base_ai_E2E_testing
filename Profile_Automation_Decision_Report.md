# Automation Strategy Decision Report
## Module: Settings → Tab 1 — Profile
**Prepared by:** Senior Automation Engineer
**Based on:** `tab1-profile-test-cases.md`
**Stack:** Python + Playwright
**Date:** 2026-06
**Version:** 2.1 — Final (all gaps resolved)

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-06 | Initial report — 106 TCs |
| v2.0 | 2026-06 | BVA corrections + new R-PH-4 + R-AU-EM-4 + 12 new TCs → 118 TCs |
| **v2.1** | **2026-06** | **Phone behaviour confirmed (silent truncation) → TC-B-P-PH-03/04 removed + R-PH-4 rewritten. Email 254 chars confirmed → 4 pending TCs promoted to Ready. Final count: 115 TCs** |

---

## Executive Summary

| Category | Count | % of Total |
|----------|-------|-----------|
| **Automate — High Priority** | **82 TCs** | **71%** |
| **Automate — Medium Priority** | **16 TCs** | **14%** |
| **Remain Manual** | **17 TCs** | **15%** |
| **Pending Confirmation** | **0 TCs** | **0% ✅ All resolved** |
| ~~Removed~~ | ~~2 TCs~~ | ~~TC-B-P-PH-03/04~~ |
| **Total** | **115 TCs** | 100% |

**Recommendation:** 98 test cases (85%) are suitable for automation.
17 cases (15%) have low ROI, require human judgment, or belong to the API test layer.
All previously pending items are now fully resolved.

> **BVA Golden Rule applied throughout:**
> *"Boundary pairs always share the same priority. Never split a boundary pair."*

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
| TC-N-P-FN-15 | Trailing apostrophe | — | R-FN-6 — closes all 4 leading/trailing cases. |
| TC-B-P-FN-01 | Exact minimum (2 chars) | Min valid | Boundary — classic off-by-one regression. |
| TC-B-P-FN-02 | One below minimum (1 char) | Min invalid | Boundary pair with FN-01. |
| TC-B-P-FN-03 | Exact maximum (50 chars) | Max valid | BVA pair — does app accept exactly 50? |
| TC-B-P-FN-04 | One above maximum (51 chars) | Max invalid | BVA pair — does app enforce the 50-char limit? |
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
| TC-B-P-LN-03 | Exact maximum (50 chars) | Max valid | BVA pair. |
| TC-B-P-LN-04 | One above maximum (51 chars) | Max invalid | BVA pair. |
| TC-B-P-LN-05 | Single space only | — | Trim + required. |
| TC-R-P-LN-01 | Fix invalid → save succeeds | — | Regression. |

---

#### FIELD: Phone Number (Edit Profile)

> **v2.1 — Behaviour confirmed:**
> The phone field uses a `maxlength` HTML attribute that **silently caps input at 10 digits**.
> No 11th character can be typed — the field physically blocks it.
> Therefore TC-B-P-PH-03 and TC-B-P-PH-04 are **removed** from this suite.
>
> ⚠️ API-level enforcement must be verified separately (see Manual section — TC-B-P-PH-API-01).

**Final rules:**

| Rule | Description | Enforcement |
|------|-------------|-------------|
| R-PH-1 | Optional — empty accepted | Frontend + Backend |
| R-PH-2 | Minimum 10 digits if provided | Inline error |
| R-PH-3 | Digits only — alpha stripped silently | Frontend strip |
| R-PH-4 | Maximum 10 digits — field caps via `maxlength` | **Silent UI cap — no error shown** |

| TC ID | Description | Boundary Type | Why Automate |
|-------|-------------|---------------|--------------|
| TC-F-P-PH-01 | Valid 10-digit phone + save | — | Positive path — verifies phone saves correctly. |
| TC-F-P-PH-02 | Empty phone (optional) | — | R-PH-1 — optional field must not block save. |
| TC-N-P-PH-01 | Short phone (5 digits) | — | R-PH-2 — min-digit constraint. |
| TC-N-P-PH-02 | Alpha input stripped | — | R-PH-3 — strip behaviour must not regress. |
| TC-B-P-PH-01 | Exactly 10 digits | Exact valid | Boundary — the only valid length. |
| TC-B-P-PH-02 | 9 digits (one below min) | Min invalid | Boundary pair for minimum. |
| ~~TC-B-P-PH-03~~ | ~~11 digits~~ | ~~Max invalid~~ | ❌ **Removed** — field physically blocks 11th digit; impossible to test via UI. |
| ~~TC-B-P-PH-04~~ | ~~15 digits~~ | ~~Max invalid~~ | ❌ **Removed** — same reason. |
| TC-R-P-PH-01 | Fix short phone → save | — | Regression: error recovery path. |

---

#### FEATURE: Add User — Email

> **v2.1 — Email max confirmed: 254 characters (RFC 5321).**
> All 4 previously pending TCs are now promoted to Ready.

**Final rules:**

| Rule | Description |
|------|-------------|
| R-AU-EM-1 | Required |
| R-AU-EM-2 | Valid format |
| R-AU-EM-3 | Not already a member |
| R-AU-EM-4 ✅ Confirmed | Maximum 254 characters (RFC 5321) |

| TC ID | Description | Boundary Type | Why Automate |
|-------|-------------|---------------|--------------|
| TC-F-P-AU-01 | Valid email → invite sent | — | Core happy path — business-critical. |
| TC-N-P-AU-01 | Empty email | — | Required field. |
| TC-N-P-AU-02 | No domain (`notanemail`) | — | Format validation. |
| TC-N-P-AU-03 | Missing domain (`user@`) | — | Format validation. |
| TC-N-P-AU-04 | Missing local (`@domain.com`) | — | Format validation. |
| TC-N-P-AU-05 | Duplicate email | — | R-AU-EM-3 — business rule, backend call. |
| TC-B-P-AU-EM-01 ✅ *promoted* | Email exactly 254 chars | Max valid | BVA pair — RFC 5321 max confirmed. |
| TC-B-P-AU-EM-02 ✅ *promoted* | Email 255 chars (one above) | Max invalid | BVA pair — does app reject 255-char email? |
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

> Automate in Phase 2 after high-priority suite is stable.

| TC ID | Description | Justification |
|-------|-------------|---------------|
| TC-F-P-FN-02 | Hyphen in middle of First Name | Valid char rule — parameterise with TC-F-FN-01. |
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
| TC-N-P-FN-06 | Emoji in First Name | Emoji handling can silently break on library upgrades. |
| TC-N-P-LN-06 | Emoji in Last Name | Same. |
| TC-B-P-AU-EM-03 | Email local part exactly 64 chars | Max local part — RFC boundary, medium regression risk. |
| TC-B-P-AU-EM-04 | Email local part 65 chars (one above) | BVA pair with EM-03. |
| TC-F-P-VA-01 | View All opens with correct columns | UI structure — moderate regression risk. |

---

### 1C. SHOULD REMAIN MANUAL 🛑

> Low ROI, subjective judgment, flaky by nature, or belong to the API test layer.

| TC ID | Description | Why Manual |
|-------|-------------|-----------|
| TC-B-P-PH-API-01 ✨ NEW | API accepts max 10 digits (server-side) | Frontend silently caps via `maxlength` — but a dev can bypass the UI and POST 11 digits directly to the API. **This is an API test, not an E2E test.** Must be verified via Postman or a dedicated API test layer. |
| TC-F-P-FN-07 | Mixed Latin + Arabic | Low priority (P-Low in source). Rare real-world data. ROI too low. |
| TC-N-P-FN-11 | Mixed consecutive (apostrophe+hyphen) | Near-duplicate of FN-10. One covers the rule; second adds cost with minimal signal. |
| TC-N-P-LN-11 | Mixed consecutive (Last Name) | Same reason as FN-11. |
| TC-U-P-FN-01 | Cancel discards First Name change | Tests user intent — requires human judgment on perceived behaviour. |
| TC-U-P-LN-01 | Error clears when Last Name corrected | Structurally covered by TC-U-P-FN-02 pattern. Duplicate maintenance. |
| TC-U-P-AU-01 | Cancel Add User sends no invite | Needs inbox/API mock to verify no email sent — infrastructure overhead unjustified. |
| DEF-P-01 | "No phone" shows no add-phone prompt | UX/discoverability defect — subjective, not a pass/fail rule. |
| DEF-P-02 | Email field not visually marked read-only | Visual design defect — requires human eye. |
| TC-F-P-VA-01 (layout) | Column layout correct in View All | Visual alignment needs human verification. |
| R-EM-1 gap | Email field has no edit cursor in modal | "No cursor appears" is flaky headless. Better confirmed visually. |
| TC-N-P-UN-15 | XSS in username | Username field existence unconfirmed — manual check required first. |
| TC-B-P-UN-06 | Boundary for consecutive specials (username) | Same — blocked by unconfirmed field. |
| TC-S-P-SES-01 | Back button after logout | Browser history behaviour varies by OS/browser — flaky in CI. |
| Server-side R-FN-3/R-LN-3 | API-level max-50 name enforcement | Requires API test layer, not E2E UI. |
| TC-F-P-PH-MAX-VISUAL | Verify field physically blocks 11th digit | Manual observation — cannot assert "a keypress was ignored" reliably in Playwright. |

---

## Section 2 — Boundary Value Analysis — Complete Final Reference

> All boundary pairs resolved. Zero pending items.

| Field | Rule | Min | Max | Min valid TC | Min−1 invalid TC | Max valid TC | Max+1 invalid TC | How max enforced |
|-------|------|-----|-----|-------------|-----------------|-------------|-----------------|-----------------|
| First Name | R-FN-2/3 | 2 | 50 | TC-B-P-FN-01 ✅ | TC-B-P-FN-02 ✅ | TC-B-P-FN-03 ✅ | TC-B-P-FN-04 ✅ | Inline error |
| Last Name | R-LN-2/3 | 2 | 50 | TC-B-P-LN-01 ✅ | TC-B-P-LN-02 ✅ | TC-B-P-LN-03 ✅ | TC-B-P-LN-04 ✅ | Inline error |
| Phone | R-PH-2/4 | 10 | 10 | TC-B-P-PH-01 ✅ | TC-B-P-PH-02 ✅ | TC-B-P-PH-01 ✅ | ❌ **Removed** | **Silent `maxlength` cap** |
| Username | R-UN-2 | 3 | 30 | TC-B-P-UN-01 ✅ | TC-B-P-UN-02 ✅ | TC-B-P-UN-04 ✅ | TC-B-P-UN-05 ✅ | Inline error |
| Email total | R-AU-EM-4 | format | 254 | — | — | TC-B-P-AU-EM-01 ✅ | TC-B-P-AU-EM-02 ✅ | Inline error |
| Email local | R-AU-EM-4 | — | 64 | — | — | TC-B-P-AU-EM-03 ✅ | TC-B-P-AU-EM-04 ✅ | Inline error |

---

## Section 3 — Final Rules Reference

### R-PH-4 — Phone: Maximum 10 digits (UI cap)

```
Rule:        Phone field accepts maximum 10 digits.
Enforcement: HTML maxlength attribute — the 11th keypress is silently ignored.
             No inline error is shown for exceeding max (field just stops accepting input).
E2E test:    Not possible — Playwright cannot assert "a keypress was ignored."
             TC-B-P-PH-03 and TC-B-P-PH-04 are REMOVED from this suite.
API test:    TC-B-P-PH-API-01 — POST /profile with 11-digit phone.
             Expected: 400 Bad Request. Must be in API test layer (Postman/pytest+requests).
```

### R-AU-EM-4 — Email: Maximum 254 characters (RFC 5321) ✅ Confirmed

```
Rule:         Email must not exceed 254 characters total (RFC 5321).
              Local part (before @): max 64 characters.
              Domain part (after @): max 255 characters.
Enforcement:  Inline validation error (confirmed by app team).
E2E test:     TC-B-P-AU-EM-01 (254 chars valid) + TC-B-P-AU-EM-02 (255 chars invalid).
              TC-B-P-AU-EM-03 (64-char local valid) + TC-B-P-AU-EM-04 (65-char local invalid).
Test data:    254-char email = 64-char local + "@" + 189-char domain
              Example: "a"*64 + "@" + "b"*185 + ".com"  (total = 254 chars)
```

---

## Section 4 — Execution Roadmap (Final)

### Phase 1 — Foundation & Smoke (Week 1)
**Goal:** Auth, navigation, Edit modal working end-to-end.

| Step | Task |
|------|------|
| 1.1 | Confirm live selectors (done via browser inspection) |
| 1.2 | Implement `LoginPage` with Keycloak SSO + auth state reuse |
| 1.3 | Implement `ProfilePage` POM |
| 1.4 | Smoke suite: TC-F-P-FN-01, TC-F-P-LN-01, TC-F-P-PH-01, TC-F-P-AU-01 |
| 1.5 | Confirm runs green headed + headless |
| 1.6 | Set up `pytest.ini` markers + HTML report |

**Exit criterion:** 4 smoke tests pass in CI.

---

### Phase 2 — Core Validation + All Boundaries (Week 2)
**Goal:** Full First Name, Last Name, Phone coverage including all BVA pairs.

| Step | Task |
|------|------|
| 2.1 | Centralise all test data + error strings in `test_data/profile_data.py` |
| 2.2 | `test_edit_profile_first_name.py` — TC-N + TC-B-FN-01/02/03/04/05 |
| 2.3 | `test_edit_profile_last_name.py` — TC-N + TC-B-LN-01/02/03/04/05 |
| 2.4 | `test_edit_profile_phone.py` — TC-F/N/B (PH-01/02 only) + TC-R |
| 2.5 | Cross-form regression TCs |

**Exit criterion:** 45+ tests pass. All boundary pairs green.

---

### Phase 3 — Add User, Username & Security (Week 3)
**Goal:** Complete Add User (email + username) + RBAC.

| Step | Task |
|------|------|
| 3.1 | Confirm Username field exists in live Add User form (manual check) |
| 3.2 | `test_add_user_email.py` — TC-N/B including TC-B-P-AU-EM-01/02 |
| 3.3 | `test_add_user_username.py` (if field confirmed) |
| 3.4 | `test_profile_security.py` — RBAC tests with non-admin account |

**Exit criterion:** 70+ tests pass. Security suite green.

---

### Phase 4 — View All, Medium Priority & CI Pipeline (Week 4)
**Goal:** Full coverage + production-ready CI.

| Step | Task |
|------|------|
| 4.1 | `test_account_users_view_all.py` |
| 4.2 | Medium-priority: Unicode, accented, emoji cases |
| 4.3 | Medium-priority: TC-B-P-AU-EM-03/04 (email local part boundary) |
| 4.4 | CI config: `smoke` on every PR, `regression` nightly |
| 4.5 | Screenshot-on-failure + video recording in CI |
| 4.6 | Selector maintenance guide for team |

**Exit criterion:** 98 tests pass. CI pipeline green. Report delivered.

---

## Section 5 — Risk Register (Final)

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Buttons have no `id`/`data-testid` | **Confirmed** | High | Request `data-testid` from devs for Edit, Save, Cancel, Add User, View All |
| Radix UI dynamic error ids | **Confirmed** | Medium | Use `#input_id + p.text-red-500` adjacent sibling selector (implemented) |
| Phone max not enforced at API level | Unknown | High | TC-B-P-PH-API-01 must be run via API test layer (Postman) |
| Username field may not exist in Add User | Flagged in source | Medium | Manual live check before Phase 3 |
| Keycloak session expiry mid-suite | Low | High | Auth state saved to disk; re-login fixture resets if 401 detected |
| Error message text changes in release | Medium | Medium | Centralise all strings in `test_data/profile_data.py` |
| `networkidle` SPA timeout | **Confirmed + Fixed** | High | Using `domcontentloaded` (already implemented) |

---

## Section 6 — Sign-off Checklist (Final)

**Before Phase 1 starts:**
- [ ] Dev team adds `data-testid` to: Edit, Save Changes, Cancel, Add User, View All buttons
- [ ] Non-admin test account credentials provided for RBAC tests
- [ ] CI environment configured with Python + Playwright

**Before Phase 3 starts:**
- [ ] Username field confirmed to exist separately in live Add User form

**API test layer (separate from this E2E suite):**
- [ ] TC-B-P-PH-API-01 — POST /profile with 11-digit phone → expect 400
- [ ] Server-side max-50 enforcement for First Name and Last Name

---

*All gaps resolved. All boundary pairs classified. Ready to proceed to code generation.*
