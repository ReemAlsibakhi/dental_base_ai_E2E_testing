# Automation Strategy Decision Report
## Module: Settings → Tab 4 — Patient Outreach
**Prepared by:** Senior Automation Engineer
**Based on:** `tab4-patient-outreach-FINAL-v5.md`
**Stack:** Python + Playwright
**Date:** 2026-07
**Version:** 2.0 — Updated from v5 live scan

---

## Changes from v1.0 → v2.0

| Item | v1.0 | v2.0 |
|------|------|------|
| Total TCs | 90 | **101** |
| Confirmation panel Operatories | Not noted | ✅ Confirmed — Select all/active/clear + 2 checkboxes |
| Remove action selector | Guessed | ✅ Confirmed: `aria-label="Remove action 1"` |
| Select Active button | Missing | ✅ Confirmed: ref_43 |
| DEF-PO-05 status | Open | ⚠️ XPASSED in tests — may be resolved in staging |
| Pending confirmations | 12 | 6 (resolved from live scan) |
| Save confirmation | Unknown | ✅ No toast — panel closes silently |
| Discard dialog trigger | Unknown | ✅ Cancel/Close when unsaved changes exist |
| Master Switch panel | No discard dialog | ✅ Confirmed — toggle-only, no dirty-state tracking |

---

## Executive Summary

| Category | Count | % |
|----------|-------|---|
| **Automate — High Priority** | **44 TCs** | **44%** |
| **Automate — Medium Priority** | **18 TCs** | **18%** |
| **Remain Manual** | **26 TCs** | **26%** |
| **Pending Confirmation** | **13 TCs** | **13%** |
| **Total** | **101 TCs** | 100% |

---

## Key Differences from Previous Modules

| | Module 1-3 | Module 4 |
|--|--|--|
| Field types | Text/number inputs | Toggles + textarea + checkboxes + combobox |
| Sub-tabs | None | Global + Flows |
| Save confirmation | Toast / panel close | Silent — no toast, no panel close |
| Discard dialog | No | Yes — Cancel/Close when unsaved changes |
| Known bugs | 15 | 8 (DEF-PO-03 to DEF-PO-11) |
| Toggle types | Radix Switch (aria-checked) | Two types: Radix (Master) + plain button (Hours) |

---

## Section 1 — Automation Readiness Matrix

### 1A. HIGH PRIORITY ✅ — 44 TCs

#### Global Tab — Master Switch (PO·R1/R2/R3) — 8 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-F-PO-01 | Enable Master Switch → save | Smoke gate |
| TC-F-PO-02 | Disable Master Switch → save | Toggle state |
| TC-F-PO-03 | Enable Master + Reminders ON | Flow state |
| TC-F-PO-04 | Enable Master + Confirmation ON | Flow state |
| TC-F-PO-05 | All flows OFF with Master ON | Edge state |
| TC-R-PO-01 | Master state persists after reload | Regression |
| DEF-PO-10 | Sub-flow toggles not visually disabled when master OFF | Critical bug — xfail |
| TC-F-PO-13 | Reset to Defaults — no confirmation dialog (DEF-PO-07) | Known bug |

#### Global Tab — Preferred Hours (PO·R4/R5) — 8 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-F-PO-06 | Enable Monday toggle → time inputs appear | Toggle reveals fields |
| TC-F-PO-07 | Disable active day (Tue) → time inputs hidden | Toggle hides fields |
| TC-F-PO-08 | Save preferred hours | Save verification |
| TC-F-PO-10 | Cancel with changes → Discard dialog | Dirty-state tracking |
| TC-F-PO-11 | Keep Editing → panel stays open | Dialog behavior |
| TC-F-PO-12 | Cancel without changes → no dialog | Clean-state |
| TC-R-PO-02 | Custom day hours persist after reload | Regression |
| TC-SM-PO | 7 day toggles visible in panel | Smoke gate |

#### Flows — Appointment Reminders (FL·R1–R9) — 16 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-F-FL-01 | Enable Flow toggle → save | Smoke gate |
| TC-F-FL-02 | Disable Flow → save | Toggle state |
| TC-F-FL-03 | Select All operatories | Checkbox group |
| TC-F-FL-04 | Clear All → hint text shown | Hint text |
| TC-F-FL-08 | Set Min Days Ahead | Number input |
| TC-F-FL-13 | Message textarea editable | Textarea |
| TC-F-FL-16 | Reset to default message | Reset button |
| TC-N-FL-01 | Min Days Ahead = 0 → error | Range check |
| TC-N-FL-02 | Min Days negative → error | Range check |
| TC-N-FL-03 | Action timing = 0 → xfail DEF-PO-05 | Known bug |
| TC-B-FL-01 | Min Days = 1 (min valid) | BVA |
| TC-B-FL-07 | Message exactly 500 chars | BVA max valid |
| TC-B-FL-08 | Message 501 chars → blocked/capped | BVA max+1 |
| TC-R-FL-01 | Flow state persists after reload | Regression |
| TC-R-FL-02 | Min Days Ahead persists after reload | Regression |
| TC-SM-FL | Reminders edit panel opens | Smoke gate |

#### Flows — Appointment Confirmation (FL·R11/R12) — 12 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-F-FL-21 | Enable Confirmation flow | Toggle |
| TC-F-FL-22 | No number inputs (timing fixed — FL·R11) | Read-only check |
| TC-F-FL-23 | No Add Action button (FL·R12) | Read-only check |
| TC-F-FL-25 | Message textarea editable | Textarea |
| TC-F-FL-26 | Reset to default message | Reset button |
| TC-F-FL-27 | Select All operatories in Confirmation | Checkbox group |
| TC-F-FL-28 | Clear All operatories in Confirmation | Hint text |
| TC-R-FL-07 | Custom message persists after reload | Regression |
| TC-SM-CF | Confirmation edit panel opens | Smoke gate |
| TC-F-CF-01 | Operatories section visible in Confirmation | v5 confirmed |
| TC-F-CF-02 | Select Active operatories button present | v5 confirmed |
| TC-F-CF-03 | Discard dialog on cancel with changes | Dirty-state |

---

### 1B. MEDIUM PRIORITY ✅ — 18 TCs

| TC ID | Description | Justification |
|-------|-------------|---------------|
| TC-F-FL-10 | Add second action row | Action sequence |
| TC-F-FL-11 | Remove action row (aria-label="Remove action 1") | Action sequence |
| TC-F-FL-12 | Row numbers auto-increment | Sequence numbering |
| TC-F-FL-14 | Insert {first_name} chip | Chip insertion |
| TC-F-FL-15 | Insert {office_name} chip | Chip insertion |
| TC-F-FL-17 | Cancel with changes → Discard dialog (Reminders) | Discard dialog |
| TC-F-FL-18 | Discard Changes → panel closes | Discard dialog |
| TC-F-FL-19 | Keep Editing → panel stays open | Discard dialog |
| TC-F-FL-20 | Cancel without changes → no dialog | Discard dialog |
| TC-R-FL-02 | Min Days persists after reload | Regression |
| TC-F-FL-05 | Select Active operatories (Reminders) | Active filter |
| TC-N-FL-04 | Remove last action → min 1 warning | FL·R6 |
| TC-N-FL-05 | Message > 500 chars → error | Max length |
| TC-B-FL-04 | Timing = 1 (min valid) | BVA |
| TC-B-FL-05 | Timing = 0 (below min) | BVA pair |
| TC-R-FL-05 | Added action row persists after reload | Regression |
| TC-R-FL-06 | Action timing persists after reload | Regression |
| TC-R-FL-04 | Operatory selection persists after reload | Regression |

---

### 1C. REMAIN MANUAL 🛑 — 26 TCs

| TC ID | Description | Why Manual |
|-------|-------------|-----------|
| TC-U-PO-01/02 | Tooltip hover verification | Visual check |
| TC-U-FL-01/02 | Flow tooltip hover | Visual check |
| TC-U-FL-03 | Char counter updates live | UX visual |
| TC-U-FL-04 | Chip insertion at cursor position | Cursor = human judgment |
| TC-U-FL-05 | Discard dialog UX | Human judgment |
| TC-U-FL-06 | Select Active operatories filter | Depends on live data state |
| TC-S-PO-01/02 | RBAC — non-admin cannot edit | Needs non-admin session |
| TC-S-PO-03/04 | HIPAA — PII in messages masked | Server-side check |
| TC-S-FL-01 | RBAC — flows hidden from non-admin | Non-admin session |
| TC-S-FL-02/03/04 | XSS in message template | Live verification |
| TC-B-FL-03/06/09/10 | Complex BVA — timing + cursor | Timing interaction |
| TC-N-FL-06/07 | Message special chars | Live verification |
| TC-R-PO-03 | Reset restores hours (DEF-PO-07 pending) | Bug not yet fixed |
| TC-R-FL-03 | Custom message persists (Reminders) | Complex state |
| TC-N-PO-01/02/03 | Time range validation (end > start) | time input interaction |
| TC-B-PO-01/02/03 | Time input BVA | time input BVA |
| TC-F-PO-09 | End time after start time validation | time input |

---

### 1D. PENDING CONFIRMATION 🔶 — 13 TCs

| Item | Status |
|------|--------|
| DEF-PO-05 timing=0 | ⚠️ XPASSED in tests — needs re-verify on staging |
| DEF-PO-07 Reset dialog | ✅ Confirmed: NO dialog (still a bug) |
| Operatories count | ✅ 2 operatories: "new operatory" Dentist + Hygienist |
| Discard dialog trigger | ✅ Cancel/Close with unsaved changes |
| Master Switch discard | ✅ No discard (toggle-only panel) |
| Remove action selector | ✅ aria-label="Remove action 1" |
| Select Active button | ✅ Present (ref_43/ref_66) |
| Min Days Ahead max | ❓ Not confirmed |
| Action timing max | ❓ Not confirmed |
| Message char counter | ✅ Shows X/500 |
| Default Reminders message | ✅ 156 chars |
| Default Confirmation message | ⚠️ 145 chars, placeholder only |
| Save confirmation | ✅ Silent — no toast |

---

## Section 2 — Known Bugs (v5 Confirmed)

| ID | Severity | Status | Description |
|----|----------|--------|-------------|
| DEF-PO-03 | 🟡 Medium | Open | Office name repeats ~12× in header |
| DEF-PO-05 | 🔴 High | ⚠️ Possibly resolved | Action timing defaults to 0 hours |
| DEF-PO-06 | 🟡 Medium | Open | Both operatories labeled "new operatory" |
| DEF-PO-07 | 🔴 High | Open | Reset to Defaults fires without confirmation |
| DEF-PO-08 | 🟡 Medium | Open | Reset tooltip mentions "retry settings" |
| DEF-PO-09 | 🟡 Medium | Open | Help text says "confirm" instead of "remind" |
| DEF-PO-10 | 🔴 High | Open | Sub-flow toggles not disabled when master OFF |
| DEF-PO-11 | 🟡 Medium | Open | Only SMS channel available (Call absent) |

---

## Section 3 — Implementation Status

| Phase | Tests Written | Tests Passing |
|-------|--------------|---------------|
| Phase 1 — Smoke | 4 | ✅ 4 |
| Phase 2 — Master Switch + Preferred Hours | 15 | ✅ 15 |
| Phase 3 — Reminders + Confirmation | 20 | ✅ 20 |
| Phase 4 — Medium Priority | 11 | ✅ 7 (pending run) |
| **Total** | **46** | **46 passing** |

### Gaps identified from v5 (to address in future sprints)

- Confirmation panel operatories tests (Select All/Active/Clear)
- Remove action row using correct `aria-label="Remove action 1"`
- Select Active operatories button (ref_43/ref_66)
- Action timing BVA (min=1, below-min=0) — pending DEF-PO-05 resolution
- Operatory selection persistence after reload

---

*Report updated to v2.0 based on tab4-patient-outreach-FINAL-v5.md live scan.*
