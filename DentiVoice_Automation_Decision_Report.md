# Automation Strategy Decision Report
## Module: Settings → Tab 5 — DentiVoice™ Customization
**Prepared by:** Senior Automation Engineer
**Based on:** `qa-test-report-tab5-dentivoice-FINAL.md`
**Stack:** Python + Playwright
**Date:** 2026-07
**Version:** 1.0

---

## Executive Summary

| Category | Count | % |
|----------|-------|---|
| **Automate — High Priority** | **48 TCs** | **40%** |
| **Automate — Medium Priority** | **22 TCs** | **18%** |
| **Remain Manual** | **35 TCs** | **29%** |
| **Pending Confirmation** | **16 TCs** | **13%** |
| **Total** | **121 TCs** | 100% |

---

## Key Technical Notes

| Item | Detail |
|------|--------|
| Validation | Zod submit-only — no HTML maxlength, no live counters |
| Save pattern | Submit button triggers Zod validation on save |
| Required fields | All `required: false` in DOM (OBS-DV-01) — bug |
| Max lengths | No HTML maxlength anywhere (OBS-DV-02) |
| Cards | AI Identity · Language Support · Emergency Handling · Call Transfer · Terminology · SMS & Email Alerts |
| Save confirmation | Unknown — needs live verification |

---

## Section 1 — Automation Readiness Matrix

### 1A. HIGH PRIORITY ✅ — 48 TCs

#### AI Identity Panel — 12 TCs

| TC ID | Description | Rule |
|-------|-------------|------|
| TC-F-DV-01 | Valid assistant name saves | DV·R1 |
| TC-F-DV-02 | Personality dropdown all options | DV·R2 |
| TC-F-DV-03 | AI Disclosure toggle ON/OFF | DV·R4 |
| TC-N-DV-01 | Empty name → "Assistant name is required" | DV·R1 |
| TC-N-DV-02 | Whitespace name → trimmed → required error | DV·R1 |
| TC-N-DV-04 | Numbers in name → "can only contain letters and spaces" | DV·R1 |
| TC-N-DV-05 | XSS in name → rejected | DV·R1 |
| TC-N-DV-06 | Empty personality → "Please select a personality type" | DV·R2 |
| TC-B-DV-01 | Name = 2 chars (min valid) | DV·R1 |
| TC-B-DV-02 | Name = 1 char (below min — DEF-DV-03 xfail) | DV·R1 |
| TC-B-DV-03 | Name = 30 chars (max valid) | DV·R1 |
| TC-B-DV-04 | Name = 31 chars → "Name must be 30 characters or less" | DV·R1 |

#### Greeting Messages — 8 TCs

| TC ID | Description | Rule |
|-------|-------------|------|
| TC-F-DV-06 | Initial greeting valid text saves | DV·R5 |
| TC-F-DV-07 | Initial greeting empty (optional) | DV·R5 |
| TC-F-DV-08 | After-hours greeting valid text saves | DV·R6 |
| TC-F-DV-09 | After-hours greeting empty (optional) | DV·R6 |
| TC-N-DV-09 | Initial greeting 501 chars → error | DV·R5 |
| TC-N-DV-10 | After-hours greeting 501 chars → error | DV·R6 |
| TC-B-DV-05 | Initial greeting 500 chars (max valid) | DV·R5 |
| TC-B-DV-06 | After-hours greeting 500 chars (max valid) | DV·R6 |

#### Language Support — 4 TCs

| TC ID | Description | Rule |
|-------|-------------|------|
| TC-F-DV-04 | English + Spanish + Mandarin all selectable | DV·R3 |
| TC-F-DV-05 | English only (default) → accepted | DV·R3 |
| TC-N-DV-07 | Remove all languages → "At least one language is required" | DV·R3 |
| TC-R-DV-01 | Language selection persists after reload | DV·R3 |

#### Emergency Handling — 12 TCs

| TC ID | Description | Rule |
|-------|-------------|------|
| TC-F-DV-10 | Book Earliest selected → saves | DV·R12 |
| TC-F-DV-11 | Connect to On-Call + valid phone → saves | DV·R12/13 |
| TC-F-DV-12 | Refer to ER selected → saves | DV·R12 |
| TC-N-DV-11 | No handling method selected → "Select at least one" | DV·R12 |
| TC-N-DV-12 | On-Call selected + empty phone → "On-call contact required" | DV·R13 |
| TC-N-DV-13 | On-Call + invalid phone format → "valid phone number" | DV·R13 |
| TC-N-DV-14 | First-aid toggle ON + empty advice → "required when enabled" | DV·R17 |
| TC-N-DV-15 | First-aid advice 3,001 chars → error | DV·R18 |
| TC-B-DV-10 | First-aid advice 3,000 chars (max valid) | DV·R18 |
| TC-B-DV-11 | Triage script 5,000 chars (max valid) | DV·R16 |
| TC-B-DV-12 | Triage script 5,001 chars → error | DV·R16 |
| TC-R-DV-03 | Emergency config persists after reload | DV·R12 |

#### Call Transfer — 8 TCs

| TC ID | Description | Rule |
|-------|-------------|------|
| TC-F-DV-15 | Enable transfer + valid rule → saves | DV·R19/20/21 |
| TC-F-DV-16 | Disable transfer → saves | DV·R19 |
| TC-N-DV-18 | Rule name empty → "Name is required" | DV·R20 |
| TC-N-DV-19 | Rule name 101 chars → "100 characters or less" | DV·R20 |
| TC-N-DV-20 | Rule phone empty → "Phone number is required" | DV·R21 |
| TC-N-DV-21 | Rule phone invalid → "valid phone number" | DV·R21 |
| TC-N-DV-22 | Rule condition empty → blocked | DV·R22 |
| TC-B-DV-13 | Rule condition 500 chars (max valid) | DV·R22 |

#### Daily Email Report — 4 TCs

| TC ID | Description | Rule |
|-------|-------------|------|
| TC-F-DV-17 | Toggle ON + valid email → saves | DV·R9 |
| TC-F-DV-18 | Toggle OFF → saves | DV·R9 |
| TC-N-DV-23 | Toggle ON + empty email → "Email required" | DV·R9 |
| TC-N-DV-24 | Toggle ON + invalid email → "valid email" | DV·R9 |

---

### 1B. MEDIUM PRIORITY ✅ — 22 TCs

| TC ID | Description | Justification |
|-------|-------------|---------------|
| TC-F-DV-19 | Quick Setup Template applies preset | DV·R7 |
| TC-F-DV-20 | Additional Instructions saves (max 2000) | DV·R8 |
| TC-N-DV-25 | Instructions 2,001 chars → error | DV·R8 |
| TC-B-DV-14 | Instructions 2,000 chars (max valid) | DV·R8 |
| TC-F-DV-21 | Enable SMS Alerts + rule → saves | DV·R26 |
| TC-F-DV-22 | Disable SMS Alerts → saves | DV·R26 |
| TC-N-DV-29 | SMS enabled + no rules → error | DV·R26 |
| TC-N-DV-30 | SMS rule name empty → error | DV·R27 |
| TC-N-DV-32 | SMS rule condition empty → error | DV·R28 |
| TC-N-DV-34 | SMS rule no recipients → error | DV·R29 |
| TC-N-DV-35 | SMS invalid phone recipient → error | DV·R29 |
| TC-B-DV-17 | SMS condition 1,000 chars (max valid) | DV·R28 |
| TC-B-DV-18 | SMS condition 1,001 chars → error | DV·R28 |
| TC-F-DV-23 | Enable Email Alerts + rule → saves | DV·R30 |
| TC-N-DV-39 | Email enabled + no rules → error | DV·R30 |
| TC-N-DV-40 | Email invalid recipient → error | DV·R33 |
| TC-B-DV-19 | Email condition 1,000 chars (max valid) | DV·R32 |
| TC-R-DV-08 | Disable SMS preserves existing rules | DV·R26 |
| TC-R-DV-09 | Send Task Emails toggle persists | DV·R34 |
| TC-F-DV-28 | Toggle Send Task Emails Immediately ON | DV·R34 |
| TC-F-DV-29 | Deactivate SMS rule (Inactive status) | DV·R26 |
| TC-F-DV-30 | Disable SMS Alerts toggle OFF | DV·R26 |

---

### 1C. REMAIN MANUAL 🛑 — 35 TCs

| TC ID | Description | Why Manual |
|-------|-------------|-----------|
| TC-U-DV-* (7) | Tooltip hover, UX flow | Visual/UX check |
| TC-S-DV-* (11) | RBAC, HIPAA, audio preview | Non-admin session / server-side |
| TC-N-DV-03 | Reserved/unpronounceable name | Dynamic word list — unpredictable |
| TC-F-DV-13/14 | Emergency keywords add/remove tags | Complex tag interaction |
| TC-N-DV-16/17 | On-Call eligibility options | Multi-select state |
| TC-F-DV-24/25/26 | Transfer rule schedule dropdown | Complex date/time UI |
| TC-N-DV-36/37/38 | SMS max rules, duplicate detection | State-dependent |
| TC-N-DV-41 | Email duplicate detection | State-dependent |
| TC-N-DV-42/43 | XSS in SMS/Email condition | Needs server-side check |
| TC-B-DV-21/22 | Max 10 recipients | Complex UI state |
| TC-B-DV-15/16 | Transfer rule condition boundary | Complex form state |
| TC-R-DV-04/05/06/07 | Complex persistence with reload | Multi-step state |

---

### 1D. PENDING CONFIRMATION 🔶 — 16 TCs

| Item | Blocking Question |
|------|-------------------|
| Save confirmation | Toast text or panel close? |
| DEF-DV-03 | Min 2 chars not enforced — xfail or test app behavior? |
| DEF-DV-05 | No max on Additional Notes — skip test or document? |
| Quick Setup Template | Does it overwrite without confirm? (DEF-DV-02) |
| Terminology panel | What fields are inside? Selectors unknown |
| SMS & Email Alert panels | Are they inside same Edit panel as AI Identity? |
| TC-N-DV-31/33 | SMS name/condition max — needs live verify |
| TC-B-DV-20 | Email condition 1,001 chars — needs live verify |

---

## Section 2 — Known Bugs

| ID | Severity | Description |
|----|----------|-------------|
| DEF-DV-01 | 🟡 Medium | Quick Setup Template: no undo after applying |
| DEF-DV-02 | 🔴 High | Quick Setup Template overwrites custom config without confirmation |
| DEF-DV-03 | 🟡 Medium | Min 2 chars for assistant name not enforced (1-char accepted) |
| DEF-DV-04 | 🟡 Medium | Variable syntax mismatch: UI uses `{agent_name}` not `${aiName}` |
| DEF-DV-05 | 🟡 Medium | Additional Notes has no max limit (9,537 chars observed) |
| DEF-DV-06 | 🟡 Medium | Call Transfer accepts 1-char rule names ("s", "mmm") |

---

## Section 3 — Execution Roadmap

### Phase 1 — Foundation + Smoke (Week 1)
- Confirm selectors for all panels via live DOM
- Build `dentivoice_page.py` POM
- 4 smoke tests

### Phase 2 — AI Identity + Greetings + Language (Week 2)
- 24 TCs covering DV·R1–R6

### Phase 3 — Emergency Handling + Call Transfer + Daily Email (Week 3)
- 24 TCs covering DV·R9, R12–R22

### Phase 4 — Medium Priority + SMS/Email Alerts + CI Update (Week 4)
- 22 TCs + CI update

---

*Ready to proceed to Phase 1 upon approval.*
