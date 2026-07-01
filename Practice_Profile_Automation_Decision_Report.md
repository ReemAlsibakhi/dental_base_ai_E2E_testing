# Automation Strategy Decision Report
## Module: Settings → Tab 2 — Practice Profile & Hours
**Prepared by:** Senior Automation Engineer
**Based on:** `tab2-practice-profile-test-cases.md`
**Stack:** Python + Playwright
**Date:** 2026-06
**Version:** 2.0 — All pending items resolved from requirements

---

## Changelog v1.0 → v2.0

| # | Change | Reason |
|---|--------|--------|
| 1 | Phone max = **10 digits** (not 15) | Requirements PP·R4/R5 corrected |
| 2 | Phone max → **silent cap** → no test | Same pattern as Module 1 |
| 3 | ZIP = **format only** (NNNNN or NNNNN-NNNN) | PP·R11 — not a length rule |
| 4 | Street max 200 → **TC-B added** ✅ | Requirements PP·R8c |
| 5 | City max 100 → **TC-B added** ✅ | Requirements PP·R9c |
| 6 | Website max 2048 → **TC-B added** ✅ | Requirements PP·R7d |
| 7 | Email max 254 → **TC-B confirmed** ✅ | PP·R6c = RFC 5321 |
| 8 | Email trim → **pending product decision** | Not specified in requirements |
| 9 | Pending items: 9 → **2** | 7 resolved from requirements |

---

## Executive Summary

| Category | Count | % |
|----------|-------|---|
| **Automate — High Priority** | **79 TCs** | **65%** |
| **Automate — Medium Priority** | **18 TCs** | **15%** |
| **Remain Manual** | **16 TCs** | **13%** |
| **Pending Product Decision** | **8 TCs** | **7%** |
| **Total** | **121 TCs** | 100% |

> **BVA Golden Rule:** Boundary pairs always share the same priority.

---

## Section 1 — Automation Readiness Matrix

---

### 1A. HIGH PRIORITY ✅

---

#### Legal Name (PP·R1) — 15 TCs

| TC ID | Input | Expected | Rule |
|-------|-------|----------|------|
| TC-N-PP-01 | Empty | "Legal name is required" | R1a |
| TC-N-PP-15 | Whitespace-only | "Legal name is required" | R1a |
| TC-N-PP-19 | `<script>alert(1)</script>` | "Legal name contains invalid characters" | R1d XSS |
| TC-N-PP-31 | `Test😊Clinic` | "Legal name contains invalid characters" | R1d emoji |
| TC-N-PP-63 | `Clinic--Care` | "Legal name must not contain consecutive special characters" | R1f |
| TC-N-PP-64 | `Smith&&Jones` | "Legal name must not contain consecutive special characters" | R1f |
| TC-N-PP-65 | `Care.,Dental` | "Legal name must not contain consecutive special characters" | R1f |
| TC-N-PP-66 | `-Clinic Care` | "Legal name must start and end with a letter or number" | R1g leading |
| TC-N-PP-67 | `DentiVoice.` | "Legal name must start and end with a letter or number" | R1g trailing |
| TC-N-PP-68 | `'Care Dental` | "Legal name must start and end with a letter or number" | R1g leading |
| TC-B-PP-01 | `AB` (2 chars) | ✅ Accepted | R1b min valid |
| TC-B-PP-02 | `A` (1 char) | "Legal name must be at least 2 characters" | R1b min-1 |
| TC-B-PP-09 | 150-char string | ✅ Accepted | R1c max valid |
| TC-B-PP-10 | 151-char string | "Legal name cannot exceed 150 characters" | R1c max+1 |
| TC-F-PP-01 | `DentiVoice Clinic LLC` | ✅ Saved | R1 smoke |

---

#### DBA / Trade Name (PP·R2) — 14 TCs

> Identical rules to Legal Name → merged into one parametrised file.

| TC ID | Input | Expected | Rule |
|-------|-------|----------|------|
| TC-N-PP-02 | Empty | "DBA name is required" | R2a |
| TC-N-PP-20 | Whitespace-only | "DBA name is required" | R2a |
| TC-N-PP-32 | `Clinic🦷` | "DBA name contains invalid characters" | R2d |
| TC-N-PP-33 | `Smile--Care` | "DBA name must not contain consecutive special characters" | R2f |
| TC-N-PP-69 | `-Smile Dental` | "DBA name must start and end with a letter or number" | R2g leading |
| TC-N-PP-70 | `Smile Dental,` | "DBA name must start and end with a letter or number" | R2g trailing |
| TC-N-PP-30 | 151-char string | "DBA name cannot exceed 150 characters" | R2c |
| TC-B-PP-11 | `AB` (2 chars) | ✅ Accepted | R2b min valid |
| TC-B-PP-12 | `A` (1 char) | "DBA name must be at least 2 characters" | R2b min-1 |
| TC-B-PP-13 | 150-char string | ✅ Accepted | R2c max valid |
| TC-B-PP-14 | 151-char string | "DBA name cannot exceed 150 characters" | R2c max+1 |
| TC-S-PP-05 | `<img onerror=1>` | Rejected, no execution | R2d XSS |
| TC-F-PP-01 | `Smile Dental Center` | ✅ Saved | R2 smoke |
| TC-R-PP-05 | Fix invalid → save | ✅ Succeeds | Regression |

---

#### Phone Fields (PP·R4 + PP·R5) — 10 TCs

> Phone max = 10 digits enforced via HTML maxlength (silent cap).
> No test for max — same pattern as Module 1.

| TC ID | Field | Input | Expected | Rule |
|-------|-------|-------|----------|------|
| TC-N-PP-03 | Main Phone | Empty | "Main phone is required" | R4a |
| TC-N-PP-04 | Main Phone | 9 digits | "Phone must be at least 10 digits" | R4b |
| TC-N-PP-35 | Main Phone | Alpha chars | Stripped silently | R4d |
| TC-N-PP-16 | Emergency | Empty | "Emergency phone is required" | R5a |
| TC-N-PP-05 | Emergency | 9 digits | "Phone must be at least 10 digits" | R5b |
| TC-N-PP-36 | Emergency | XSS payload | Rejected | R5d |
| TC-B-PP-24 | Main Phone | 10 digits exactly | ✅ Accepted | R4b min valid |
| TC-B-PP-25 | Main Phone | 9 digits | ❌ Error | R4b min-1 |
| TC-B-PP-26 | Emergency | 10 digits exactly | ✅ Accepted | R5b min valid |
| TC-B-PP-27 | Emergency | 9 digits | ❌ Error | R5b min-1 |

---

#### Address Fields — 22 TCs

**Street Address (PP·R8):**

| TC ID | Input | Expected | Rule |
|-------|-------|----------|------|
| TC-N-PP-08 | Empty | "Street address is required" | R8a |
| TC-N-PP-22 | Whitespace-only | "Street address is required" | R8a |
| TC-N-PP-40 | XSS payload | Rejected | R8d |
| TC-B-PP-17 | `123 A` (5 chars) | ✅ Accepted | R8b min valid |
| TC-B-PP-18 | `123` (4 chars) | ❌ Error | R8b min-1 |
| TC-B-PP-NEW-01 | 200-char string | ✅ Accepted | R8c max valid |
| TC-B-PP-NEW-02 | 201-char string | ❌ Error | R8c max+1 |

**City (PP·R9):**

| TC ID | Input | Expected | Rule |
|-------|-------|----------|------|
| TC-N-PP-09 | Empty | "City is required" | R9a |
| TC-N-PP-27 | Whitespace-only | "City is required" | R9a |
| TC-N-PP-41 | XSS payload | Rejected | R9d |
| TC-B-PP-19 | `AB` (2 chars) | ✅ Accepted | R9b min valid |
| TC-B-PP-20 | `A` (1 char) | ❌ Error | R9b min-1 |
| TC-B-PP-NEW-03 | 100-char string | ✅ Accepted | R9c max valid |
| TC-B-PP-NEW-04 | 101-char string | ❌ Error | R9c max+1 |

**State + ZIP + Timezone:**

| TC ID | Field | Input | Expected | Rule |
|-------|-------|-------|----------|------|
| TC-N-PP-17 | State | None selected | "State is required" | R10a |
| TC-N-PP-10 | ZIP | Empty | "ZIP code is required" | R11a |
| TC-N-PP-11 | ZIP | `ABCDE` | "ZIP must contain only digits" | R11c |
| TC-B-PP-05 | ZIP | `12345` | ✅ Accepted (5-digit) | R11b |
| TC-B-PP-06 | ZIP | `1234` | ❌ Error | R11b below min |
| TC-B-PP-15 | ZIP | `12345-6789` | ✅ Accepted (ZIP+4) | R11d |
| TC-B-PP-16 | ZIP | `12345-678` | ❌ Error (ZIP+4 incomplete) | R11d |
| TC-N-PP-18 | Timezone | None selected | "Timezone is required" | R12a |

---

#### Email (PP·R6) — 8 TCs

| TC ID | Input | Expected | Rule |
|-------|-------|----------|------|
| TC-F-PP-02 | `admin@clinic.com` | ✅ Accepted | R6b valid |
| TC-F-PP-03 | Empty | ✅ Accepted (optional) | R6a |
| TC-N-PP-06 | `notanemail` | ❌ Error | R6b format |
| TC-N-PP-37 | `user@` | ❌ Error | R6b format |
| TC-N-PP-38 | `@domain.com` | ❌ Error | R6b format |
| TC-S-PP-13 | XSS in email | Rejected | R6e |
| TC-B-PP-21 | 254-char email | ✅ Accepted | R6c max valid |
| TC-B-PP-22 | 255-char email | ❌ Error | R6c max+1 |

---

#### Website (PP·R7) — 5 TCs

| TC ID | Input | Expected | Rule |
|-------|-------|----------|------|
| TC-F-PP-03 | `https://clinic.com` | ✅ Accepted | R7a valid |
| TC-N-PP-07 | `clinic.com` (no scheme) | ❌ Error | R7b scheme |
| TC-N-PP-39 | `ftp://clinic.com` | ❌ Error | R7b scheme |
| TC-N-PP-21 | `javascript:alert(1)` | ❌ Blocked | R7c |
| TC-B-PP-NEW-05 | 2048-char URL | ✅ Accepted | R7d max valid |
| TC-B-PP-NEW-06 | 2049-char URL | ❌ Error | R7d max+1 |

---

#### Description (PP·R13) — 3 TCs

| TC ID | Input | Expected | Rule |
|-------|-------|----------|------|
| TC-B-PP-03 | 500-char text | ✅ Accepted, counter = 500/500 | R13b max |
| TC-B-PP-04 | 501-char text | ❌ Blocked or error | R13b max+1 |
| TC-N-PP-26 | XSS in description | Rejected | R13d |

---

#### Security (Cross-field) — 2 TCs

| TC ID | Description | Rule |
|-------|-------------|------|
| TC-S-PP-04 | Page served over HTTPS | Security |
| TC-S-PP-08 | javascript: in Website blocked | R7c |

---

### 1B. MEDIUM PRIORITY ✅

| TC ID | Description | Justification |
|-------|-------------|---------------|
| TC-F-PP-05 | Practice Type dropdown saves | Valid selection |
| TC-N-PP-34 | Practice Type empty/unselected | Required dropdown |
| TC-U-PP-04 | Description counter updates live | UX counter |
| TC-F-PP-06 | Parking toggle ON → details shown | Toggle state |
| TC-N-PP-28 | Parking Details > 300 chars | Max length |
| TC-B-PP-30 | Parking Details exactly 300 | BVA max valid |
| TC-B-PP-31 | Parking Details 301 chars | BVA max+1 |
| TC-N-PP-29 | Additional Notes > 500 | Max length |
| TC-B-PP-32 | Additional Notes exactly 500 | BVA max valid |
| TC-B-PP-33 | Additional Notes 501 chars | BVA max+1 |
| TC-N-PP-44 | Landmarks > 500 | Max length |
| TC-B-PP-28 | Landmarks exactly 500 | BVA max valid |
| TC-B-PP-29 | Landmarks 501 chars | BVA max+1 |
| TC-U-PP-05 | Parking toggle hides details when OFF | UX conditional |
| TC-S-PP-09 | XSS in Landmarks | Security |
| TC-S-PP-10 | XSS in Additional Notes | Security |
| TC-S-PP-12 | XSS in Parking Details | Security |
| TC-R-PP-04 | Multi-field error regression | Regression |

---

### 1C. REMAIN MANUAL 🛑

| TC ID | Description | Why Manual |
|-------|-------------|-----------|
| TC-F-PP-04 | Logo upload PNG/JPG/SVG | File upload — flaky headless |
| TC-N-PP-12 | Logo wrong file type | File upload |
| TC-N-PP-13 | Logo > 2MB | Needs real file at exact size |
| TC-B-PP-07 | Logo exactly 2MB | File boundary — needs real file |
| TC-B-PP-08 | Logo 2MB+1 byte | File boundary — needs real file |
| TC-B-PP-23 | Logo MIME mismatch | Server MIME — not testable via UI |
| TC-S-PP-03 | Logo malicious filename | Security + file upload |
| TC-S-PP-11 | Logo MIME validation | Security + server |
| TC-N-PP-24 | GIF rejected | File upload |
| TC-N-PP-42 | BMP rejected | File upload |
| TC-N-PP-43 | WEBP rejected | File upload |
| TC-N-PP-25 | Zero-byte logo | File upload |
| TC-R-PP-06 | Logo delete regression | File state management |
| TC-U-PP-07 | Keyboard navigation | Accessibility — human judgment |
| TC-U-PP-01 | Cancel discards changes | User intent — human judgment |
| DEF-PP-01 | required:false on all fields | DevTools inspection only |

---

### 1D. PENDING PRODUCT DECISION 🔶

| Item | Question |
|------|----------|
| Email trim (PP·R6d) | Is leading/trailing whitespace trimmed silently? |
| ZIP trim (PP·R11e) | Same question for ZIP field |

> All other previously pending items resolved from requirements document.

---

## Section 2 — BVA Complete Reference

| Field | Min | Max | Min valid | Min-1 | Max valid | Max+1 |
|-------|-----|-----|-----------|-------|-----------|-------|
| Legal Name | 2 | 150 | `AB` | `A` | 150-char | 151-char |
| DBA Name | 2 | 150 | `AB` | `A` | 150-char | 151-char |
| Main Phone | 10 | 10 | 10 digits | 9 digits | 10 digits | silent cap |
| Emergency Phone | 10 | 10 | 10 digits | 9 digits | 10 digits | silent cap |
| Street Address | 5 | 200 | 5 chars | 4 chars | 200 chars | 201 chars |
| City | 2 | 100 | 2 chars | 1 char | 100 chars | 101 chars |
| ZIP (5-digit) | 5 | 5 | `12345` | `1234` | `12345` | N/A (format) |
| ZIP+4 | 10 | 10 | `12345-6789` | `12345-678` | `12345-6789` | N/A |
| Email | format | 254 | valid format | invalid | 254-char | 255-char |
| Website | scheme | 2048 | `https://x.com` | no scheme | 2048-char | 2049-char |
| Description | 0 | 500 | empty | N/A | 500-char | 501-char |
| Parking Details | 0 | 300 | empty | N/A | 300-char | 301-char |
| Landmarks | 0 | 500 | empty | N/A | 500-char | 501-char |
| Additional Notes | 0 | 500 | empty | N/A | 500-char | 501-char |

---

## Section 3 — Execution Roadmap

### Phase 1 — Foundation (Week 1)
- Confirm selectors via live browser inspection
- Build `practice_profile_page.py` POM
- 4 smoke tests (valid save)

### Phase 2 — Core Text Fields (Week 2)
- Legal Name + DBA merged (identical rules) — 29 TCs
- Phone fields — 10 TCs

### Phase 3 — Address + Email + Website (Week 3)
- Address group — 22 TCs
- Email — 8 TCs
- Website — 6 TCs
- Description — 3 TCs
- Security XSS suite

### Phase 4 — Medium Priority + CI Update (Week 4)
- Dropdowns, toggles, text areas — 18 TCs
- Confirm email/ZIP trim with product team
- Update GitHub Actions CI

---

## Section 4 — Risk Register

| Risk | Impact | Mitigation |
|------|--------|-----------|
| File upload tests | High | All manual — no automation ROI |
| DEF-PP-01 (required:false) | Critical | Already reported — tests use inline errors |
| Legal Name + DBA share rules | Low | Merge into one file (same as FN+LN Module 1) |
| Phone silent cap | Low | Confirmed 10-digit cap — no max test needed |
| Email/ZIP trim unconfirmed | Low | 2 items pending product decision |

---

*All pending items from v1.0 resolved. Ready to proceed to Phase 1.*
