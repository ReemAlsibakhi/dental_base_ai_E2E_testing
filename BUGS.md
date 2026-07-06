# Bug Report — Profile Module
**Reported by:** QA Automation Suite
**Environment:** https://dentalbase-dev-v2.vercel.app
**Date:** 2026-06
**Discovered via:** Automated E2E tests (Playwright + Python)

---

## Summary

| ID | Severity | Feature | Status |
|----|----------|---------|--------|
| BUG-001 | 🔴 High | Username — dot not allowed | Open |
| BUG-002 | 🔴 High | Username — wrong error message for consecutive specials | Open |
| BUG-003 | 🔴 High | Username — no error for leading/trailing special chars | Open |
| BUG-004 | 🔴 High | Username — no error for max length exceeded | Open |
| BUG-005 | 🟡 Medium | Email — 254-char email rejected (RFC 5321 violation) | Open |
| BUG-006 | 🟡 Medium | Save Changes — stays enabled when field has validation error | Open |
| BUG-007 | 🟡 Medium | Username — uppercase not rejected immediately | Open |

---

## BUG-001 — Username: Dot character not allowed (violates R-UN-3)

**Severity:** 🔴 High
**Discovered by:** `test_username_valid_no_error[with_dot-reem.test]`
**Rule violated:** R-UN-3

**Expected (per requirements):**
`reem.test` → ✅ Accepted — dots are valid in usernames

**Actual:**
`reem.test` → ❌ Error: "Username can only contain letters, numbers, hyphens, and underscores"

**Impact:**
Users cannot create usernames with dots (e.g. `john.doe`, `reem.s`).
This is a common username format and is explicitly allowed in R-UN-3.

**Steps to reproduce:**
1. Open Settings → Add User
2. Fill Username field with `reem.test`
3. Press Tab
4. Observe: error appears — should not

---

## BUG-002 — Username: Wrong error message for consecutive special characters

**Severity:** 🔴 High
**Discovered by:** `test_username_invalid_shows_error[consec_dots/consec_hyphens/...]`
**Rule violated:** R-UN-4

**Expected (per requirements):**
`reem..test`, `reem--test` → ❌ "Username cannot contain consecutive special characters"

**Actual:**
`reem..test`, `reem--test` → ❌ "Username can only contain letters, numbers, hyphens, and underscores"

**Impact:**
Wrong error message misleads users. They get told the characters
are invalid when actually the issue is consecutive repetition.
Also suggests R-UN-4 is not implemented as a separate rule.

**Steps to reproduce:**
1. Open Settings → Add User
2. Fill Username with `reem..test`
3. Press Tab
4. Observe: wrong error message shown

---

## BUG-003 — Username: No validation error for leading/trailing special characters

**Severity:** 🔴 High
**Discovered by:** `test_username_invalid_shows_error[leading_underscore/_reem]`
**Rule violated:** R-UN-5

**Expected (per requirements):**
`_reem`, `-reem`, `reem_`, `reem-` → ❌ "Username must start and end with a letter or number"

**Actual:**
`_reem`, `reem_` → ✅ No error shown — field accepted silently

**Impact:**
Users can create usernames starting/ending with special characters.
This violates R-UN-5 and may cause issues in downstream systems.

**Steps to reproduce:**
1. Open Settings → Add User
2. Fill Username with `_reem`
3. Press Tab
4. Observe: no error appears — should show "must start and end with a letter or number"

---

## BUG-004 — Username: No validation error when exceeding 30-character maximum

**Severity:** 🔴 High
**Discovered by:** `test_username_31_chars_triggers_max_error`
**Rule violated:** R-UN-2 (max 30 chars)

**Expected (per requirements):**
31-character username → ❌ "Username cannot exceed 30 characters"

**Actual:**
31-character username → ✅ No error shown — field accepts input silently

**Impact:**
Users can submit usernames longer than 30 characters.
This may cause database truncation, API errors, or security issues.

**Steps to reproduce:**
1. Open Settings → Add User
2. Fill Username with 31 characters (e.g. `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`)
3. Press Tab
4. Observe: no error appears

---

## BUG-005 — Email: 254-character email rejected (RFC 5321 violation)

**Severity:** 🟡 Medium
**Discovered by:** `test_add_user_email_254_chars_accepted`
**Rule violated:** R-AU-EM-4 (max 254 chars per RFC 5321)

**Expected (per requirements):**
Email of exactly 254 chars → ✅ Accepted (RFC 5321 standard)

**Actual:**
Email of 254 chars → ❌ "Please enter a valid email address"

**Test data used:**
```
"a" * 64 + "@" + "b" * 185 + ".com"  = 254 characters total
```

**Impact:**
Valid email addresses (per internet standard) are incorrectly rejected.
Users with long email addresses cannot be invited.

**Note:** The app may intentionally use a shorter limit than RFC 5321.
If so, R-AU-EM-4 must be updated to reflect the actual limit.
**Action required:** Confirm with dev team what the actual max email length is.

---

## BUG-006 — Save Changes button stays enabled when validation error is shown

**Severity:** 🟡 Medium
**Discovered by:** `test_name_invalid_blocks_save` (removed — see note)
**Rule violated:** General UX / form validation best practice

**Expected:**
When any field has an inline validation error → Save Changes button is disabled

**Actual:**
Save Changes button remains enabled even when First Name or Last Name
has an active validation error (e.g. contains digits, consecutive specials)

**Impact:**
Users can attempt to submit invalid data. The server likely rejects it,
but the UX is confusing — the button should be disabled to prevent
the attempt and signal that the form is not ready.

**Note:**
The automated tests for this behaviour were removed (Option 1 decision)
because they would fail on every run. This bug should be fixed and
the tests re-added once resolved.

---

## BUG-007 — Username error message is incorrect / incomplete

**Severity:** 🟡 Medium
**Discovered by:** Multiple username tests
**Rule violated:** R-UN-3

**Expected error message (per requirements):**
`"Username can only contain lowercase letters, numbers, hyphens, underscores, and dots"`

**Actual error message:**
`"Username can only contain letters, numbers, hyphens, and underscores"`

**Differences:**
- Missing "lowercase" qualifier
- Missing "dots" as an allowed character
- Inconsistent with R-UN-3 which explicitly allows dots

**Impact:**
The error message does not accurately describe the validation rule,
leading to user confusion.

---

## Recommendations

1. **BUG-001, 007:** Update username validation to allow dots — align with R-UN-3
2. **BUG-002:** Implement R-UN-4 as a separate rule with its own error message
3. **BUG-003:** Implement R-UN-5 start/end validation
4. **BUG-004:** Implement R-UN-2 max-length validation for username
5. **BUG-005:** Confirm actual email max length with backend team
6. **BUG-006:** Disable Save Changes button when any field has an error

Once bugs are fixed, all automated tests are expected to pass without modification.
The tests reflect the correct requirements — not the current implementation.

---

## Module 2 — Practice Profile & Hours Bugs

| ID | Severity | Feature | Status |
|----|----------|---------|--------|
| DEF-PP-03 | 🟡 Medium | Website max length < 2048 chars | Open |
| DEF-PP-04 | 🟡 Medium | trailing period in Legal Name not rejected | Open |

---

## DEF-PP-03 — Website: max length less than 2048 chars

**Severity:** 🟡 Medium
**Discovered by:** `test_website_max_2048_chars_accepted`
**Rule violated:** PP·R7d (max 2048 chars)

**Expected:** URL of exactly 2048 chars → ✅ Accepted
**Actual:** URL of 2048 chars → ❌ "Website URL cannot exceed 2048 characters"

**Impact:** Valid long URLs rejected. Max is enforced at a lower limit than specified.
**Action:** Confirm actual max with dev team and update PP·R7d accordingly.

---

## DEF-PP-04 — Legal Name: trailing period not rejected

**Severity:** 🟡 Medium
**Discovered by:** `test_practice_name_invalid_shows_error[ln-trailing_period]`
**Rule violated:** PP·R1g (must start and end with letter or number)

**Expected:** `DentiVoice.` → ❌ Error (trailing period)
**Actual:** No error shown — trailing period accepted silently

**Impact:** Legal names can end with special characters, violating PP·R1g.
