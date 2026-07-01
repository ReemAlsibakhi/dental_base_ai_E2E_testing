# Automation Strategy Decision Report
## Module: Settings → Tab 2 — Practice Profile & Hours
**Prepared by:** Senior Automation Engineer
**Based on:** `tab2-practice-profile-test-cases.md`
**Stack:** Python + Playwright
**Date:** 2026-06
**Version:** 1.0

---

## Executive Summary

| Category | Count | % of Total |
|----------|-------|-----------|
| **Automate — High Priority** | **67 TCs** | **61%** |
| **Automate — Medium Priority** | **18 TCs** | **16%** |
| **Remain Manual** | **16 TCs** | **15%** |
| **Pending Confirmation** | **9 TCs** | **8%** |
| **Total** | **110 TCs** | 100% |

---

## Section 1 — Automation Readiness Matrix

---

### 1A. HIGH PRIORITY ✅

#### Legal Name (PP·R1) — 15 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-N-PP-01 | Empty Legal Name | Required field — core regression gate |
| TC-N-PP-15 | Whitespace-only | Trim logic — easy to regress |
| TC-N-PP-19 | XSS script tag | Security — 0 tolerance |
| TC-N-PP-31 | Emoji rejected | Char validation |
| TC-N-PP-63 | Consecutive hyphens | PP·R1f business rule |
| TC-N-PP-64 | Double ampersand | PP·R1f |
| TC-N-PP-65 | Period+comma | PP·R1f |
| TC-N-PP-66 | Leading hyphen | PP·R1g |
| TC-N-PP-67 | Trailing period | PP·R1g |
| TC-N-PP-68 | Leading apostrophe | PP·R1g |
| TC-B-PP-01 | Exact min 2 chars | BVA boundary |
| TC-B-PP-02 | 1 char (below min) | BVA pair |
| TC-B-PP-09 | Exact max 150 chars | BVA boundary |
| TC-B-PP-10 | 151 chars (above max) | BVA pair |
| TC-F-PP-01 | Valid name saves | Smoke gate |

#### DBA / Trade Name (PP·R2) — 14 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-N-PP-02 | Empty DBA | Required |
| TC-N-PP-20 | Whitespace-only | Trim logic |
| TC-N-PP-32 | XSS/emoji | Security |
| TC-N-PP-33 | Consecutive specials | PP·R2f |
| TC-N-PP-69 | Leading special | PP·R2g |
| TC-N-PP-70 | Trailing special | PP·R2g |
| TC-B-PP-11 | Exact min 2 chars | BVA |
| TC-B-PP-12 | 1 char (below min) | BVA pair |
| TC-B-PP-13 | Exact max 150 chars | BVA |
| TC-B-PP-14 | 151 chars (above max) | BVA pair |
| TC-N-PP-30 | Over max chars | Char limit |
| TC-F-PP-01 | Valid DBA saves | Smoke |
| TC-S-PP-05 | XSS in DBA | Security |
| TC-R-PP-05 | Fix DBA then save | Regression |

#### Phone Fields (PP·R4 + PP·R5) — 10 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-N-PP-03 | Empty Main Phone | Required |
| TC-N-PP-04 | Main Phone < 10 digits | Min length |
| TC-N-PP-35 | Main Phone alpha chars | Chars rule |
| TC-N-PP-16 | Empty Emergency Phone | Required |
| TC-N-PP-05 | Emergency Phone < 10 digits | Min length |
| TC-N-PP-36 | Emergency Phone XSS | Security |
| TC-B-PP-24 | Main Phone exactly 10 | BVA |
| TC-B-PP-25 | Main Phone 9 digits | BVA pair |
| TC-B-PP-26 | Emergency Phone exactly 10 | BVA |
| TC-B-PP-27 | Emergency Phone 9 digits | BVA pair |

#### Address Fields (PP·R8 + PP·R9 + PP·R10 + PP·R11 + PP·R12) — 16 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-N-PP-08 | Empty Street | Required |
| TC-N-PP-22 | Whitespace-only Street | Trim |
| TC-N-PP-40 | XSS in Street | Security |
| TC-B-PP-17 | Street exact min 5 chars | BVA |
| TC-B-PP-18 | Street 4 chars (below min) | BVA pair |
| TC-N-PP-09 | Empty City | Required |
| TC-N-PP-27 | Whitespace-only City | Trim |
| TC-N-PP-41 | XSS in City | Security |
| TC-B-PP-19 | City exact min 2 chars | BVA |
| TC-B-PP-20 | City 1 char (below min) | BVA pair |
| TC-N-PP-17 | Empty State | Required dropdown |
| TC-N-PP-10 | Empty ZIP | Required |
| TC-N-PP-11 | ZIP letters rejected | Format rule |
| TC-B-PP-05 | ZIP exactly 5 digits | BVA |
| TC-B-PP-06 | ZIP 4 digits (below min) | BVA pair |
| TC-N-PP-18 | Empty Timezone | Required dropdown |

#### Email (PP·R6) — 6 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-F-PP-02 | Valid email accepted | Functional |
| TC-F-PP-03 | Empty email (optional) | R6a optional |
| TC-N-PP-06 | Invalid email format | Format rule |
| TC-N-PP-37 | Missing @ | Format |
| TC-N-PP-38 | Missing domain | Format |
| TC-B-PP-21 | Email 254 chars (max valid) | RFC 5321 BVA |
| TC-B-PP-22 | Email 255 chars (above max) | BVA pair |
| TC-S-PP-13 | XSS in email | Security |

#### Website (PP·R7) — 3 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-N-PP-07 | Invalid URL (no http/https) | Format rule |
| TC-N-PP-21 | javascript: URL blocked | Security |
| TC-S-PP-08 | javascript: XSS | Security |

#### Description (PP·R13) — 3 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-B-PP-03 | Description exactly 500 chars | BVA max |
| TC-B-PP-04 | Description 501 chars | BVA pair |
| TC-N-PP-26 | XSS in description | Security |

---

### 1B. MEDIUM PRIORITY ✅

| TC ID | Description | Justification |
|-------|-------------|---------------|
| TC-F-PP-05 | Practice Type dropdown saves | Valid selection |
| TC-N-PP-34 | Practice Type empty | Required dropdown |
| TC-B-PP-15 | ZIP+4 format (9 digits) | Extended ZIP format |
| TC-B-PP-16 | ZIP+4 below min | BVA pair |
| TC-B-PP-03/04 | Description counter updates | UX counter |
| TC-U-PP-04 | Description counter at 500 | Counter boundary |
| TC-F-PP-06 | Parking toggle ON | Toggle state |
| TC-U-PP-05 | Parking toggle shows/hides details | UX conditional |
| TC-N-PP-28 | Parking Details > 300 chars | Max length |
| TC-B-PP-30 | Parking Details exactly 300 | BVA |
| TC-B-PP-31 | Parking Details 301 chars | BVA pair |
| TC-N-PP-29 | Additional Notes > 500 | Max length |
| TC-B-PP-32 | Additional Notes exactly 500 | BVA |
| TC-B-PP-33 | Additional Notes 501 chars | BVA pair |
| TC-N-PP-44 | Landmarks > 500 | Max length |
| TC-B-PP-28 | Landmarks exactly 500 | BVA |
| TC-B-PP-29 | Landmarks 501 chars | BVA pair |
| TC-S-PP-04 | HTTPS enforced | Security |

---

### 1C. REMAIN MANUAL 🛑

| TC ID | Description | Why Manual |
|-------|-------------|-----------|
| TC-F-PP-04 | Logo upload PNG/JPG/SVG | File upload — flaky in headless |
| TC-N-PP-12 | Logo wrong file type | File upload |
| TC-N-PP-13 | Logo > 2MB | File upload — needs real file |
| TC-B-PP-07 | Logo exactly 2MB | File upload boundary |
| TC-B-PP-08 | Logo 2MB+1 byte | File upload boundary |
| TC-B-PP-23 | Logo MIME mismatch | Server MIME validation |
| TC-S-PP-03 | Logo malicious filename | Security + file upload |
| TC-S-PP-11 | Logo MIME validation | Security + server |
| TC-N-PP-24 | GIF rejected | File upload |
| TC-N-PP-42 | BMP rejected | File upload |
| TC-N-PP-43 | WEBP rejected | File upload |
| TC-N-PP-25 | Zero-byte logo | File upload |
| TC-R-PP-06 | Logo delete regression | File state management |
| TC-U-PP-07 | Keyboard navigation | Accessibility — needs human judgment |
| TC-U-PP-01 | Cancel discards changes | User intent judgment |
| DEF-PP-01 | required:false on all fields | DevTools inspection — not automatable via UI |

---

### 1D. PENDING CONFIRMATION 🔶

| TC ID | Description | Blocking Question |
|-------|-------------|-------------------|
| TC-B (PP·R4c) | Main Phone max 15 digits | Does field cap at 15? Silent or error? |
| TC-B (PP·R5c) | Emergency Phone max 15 digits | Same |
| TC-B (PP·R7d) | Website max 2048 chars | Does field enforce max? |
| TC-B (PP·R8c) | Street max 200 chars | Does field enforce max? |
| TC-B (PP·R9c) | City max 100 chars | Does field enforce max? |
| TC-U (PP·R6d) | Email trim behaviour | Does field trim silently? |
| TC-B (PP·R11e) | ZIP trim | Same |
| TC-B (PP·R11f) | ZIP max length | What is the max? |
| TC-R-PP-03 | Email format regression | Needs live confirmation |

---

## Section 2 — Key Differences from Module 1

| | Module 1 (Profile) | Module 2 (Practice Profile) |
|--|--|--|
| Fields | 3 (name, phone, email) | 17+ fields |
| Char rules | Letters + specials | + periods, ampersands, commas |
| File upload | ❌ | ✅ Logo (manual only) |
| Dropdowns | ❌ | ✅ Practice Type, State, Timezone |
| Toggles | ❌ | ✅ Parking toggle |
| Max lengths | 50 chars | Up to 500 chars |
| Known bugs | 7 | 2 (DEF-PP-01, DEF-PP-02) |

---

## Section 3 — Execution Roadmap

### Phase 1 — Foundation (Week 1)
- Confirm selectors for Practice Profile form via live browser
- Add `practice_profile_page.py` POM
- Write 4 smoke tests (valid save for each required field group)

### Phase 2 — Core Validation (Week 2)
- Legal Name (15 TCs) + DBA (14 TCs) — merge into one file (identical rules)
- Phone fields (10 TCs)
- Address fields (16 TCs)

### Phase 3 — Email, Website, Description (Week 3)
- Email (8 TCs) + Website (3 TCs)
- Description counter + XSS (3 TCs)
- Security suite

### Phase 4 — Medium Priority + CI Update (Week 4)
- Dropdowns, toggles, text areas
- Confirm pending items with dev team
- Update CI pipeline

---

## Section 4 — Risk Register

| Risk | Impact | Mitigation |
|------|--------|-----------|
| File upload tests flaky | High | Keep manual — not worth the infrastructure |
| 9 pending items unconfirmed | Medium | Manual check on live site before Phase 3 |
| DEF-PP-01 (required:false) | Critical | Reported — tests validate via inline errors not browser required |
| Legal Name + DBA share rules | Low | Merge into one parametrised file (same as FN+LN in Module 1) |
| State/Timezone server injection | Medium | Manual only — requires DevTools DOM manipulation |

---

*Ready to proceed to code generation upon approval.*
