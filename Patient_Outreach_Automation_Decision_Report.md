# Automation Strategy Decision Report
## Module: Settings → Tab 4 — Patient Outreach
**Prepared by:** Senior Automation Engineer
**Based on:** `tab4-patient-outreach-FINAL-v5.md`
**Stack:** Python + Playwright
**Date:** 2026-07
**Version:** 1.0

---

## Executive Summary

| Category | Count | % |
|----------|-------|---|
| **Automate — High Priority** | **38 TCs** | **42%** |
| **Automate — Medium Priority** | **16 TCs** | **18%** |
| **Remain Manual** | **24 TCs** | **27%** |
| **Pending Confirmation** | **12 TCs** | **13%** |
| **Total** | **90 TCs** | 100% |

---

## Key Differences from Previous Modules

| | Module 1-3 | Module 4 |
|--|--|--|
| Field types | Text/number inputs | Toggles + textarea + checkboxes + combobox |
| Sub-tabs | None | Global + Flows |
| Cards | Single form | 2 tabs × multiple panels |
| Save confirmation | Toast / panel close | Confirmed from live: needs verification |
| Known bugs | 15 | 8 (DEF-PO-03 to DEF-PO-11) |
| Discard dialog | No | Yes (when unsaved changes) |

---

## Section 1 — Automation Readiness Matrix

---

### 1A. HIGH PRIORITY ✅ — 38 TCs

#### Global Tab — Master Switch (PO·R1/R2/R3) — 8 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-F-PO-01 | Enable Master Switch → badge "Active" | Smoke gate |
| TC-F-PO-02 | Disable Master Switch → badge "Inactive" | Toggle state |
| TC-F-PO-03 | Enable Master + Appointment Reminders ON | Flow state |
| TC-F-PO-04 | Enable Master + Appointment Confirmation ON | Flow state |
| TC-F-PO-05 | All flows OFF with Master ON | Edge state |
| TC-R-PO-01 | Master state persists after reload | Regression |
| DEF-PO-10 | Sub-flow toggles not visually disabled when master OFF | Critical bug |
| TC-F-PO-13 | Reset to Defaults — confirm dialog behavior (DEF-PO-07) | Known bug |

#### Global Tab — Preferred Hours (PO·R4/R5) — 10 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-F-PO-06 | Enable Monday toggle → time inputs appear | Toggle reveals fields |
| TC-F-PO-07 | Disable active day (Tue) → time inputs hidden | Toggle hides fields |
| TC-F-PO-08 | Set valid hours Mon 9AM–5PM → save | Smoke gate |
| TC-F-PO-09 | End time after start time | Time range validation |
| TC-N-PO-01 | End time = start time → error | Boundary |
| TC-N-PO-02 | End time before start time → error | Negative |
| TC-B-PO-01 | Start 00:00 End 23:59 → accepted | BVA |
| TC-B-PO-02 | Same time start/end → error | BVA pair |
| TC-B-PO-03 | Start 23:00 End 23:01 → accepted | BVA |
| TC-R-PO-02 | Custom day hours persist after reload | Regression |

#### Flows — Appointment Reminders (FL·R1–R7) — 12 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-F-FL-01 | Enable Flow toggle → card shows "Active" | Smoke gate |
| TC-F-FL-02 | Disable Flow → card shows "Inactive" | Toggle state |
| TC-F-FL-03 | Select All operatories | Checkbox group |
| TC-F-FL-04 | Clear All operatories → hint text shown | Hint text |
| TC-F-FL-08 | Set Min Days Ahead to 7 | Number input |
| TC-N-FL-01 | Min Days Ahead = 0 → error | Range check |
| TC-N-FL-02 | Min Days Ahead negative → error | Range check |
| TC-B-FL-01 | Min Days Ahead = 1 (min valid) | BVA |
| TC-B-FL-02 | Min Days Ahead = 0 (below min) | BVA pair |
| TC-F-FL-09 | Set action timing to 24 hours | Number input |
| TC-N-FL-03 | Action timing = 0 → error (DEF-PO-05) | Known bug |
| TC-F-FL-13 | Message textarea accepts valid text | Textarea |

#### Flows — Appointment Confirmation (FL·R11/R12) — 8 TCs

| TC ID | Description | Why Automate |
|-------|-------------|--------------|
| TC-F-FL-21 | Enable Confirmation flow | Toggle |
| TC-F-FL-22 | Auto message section is read-only | FL·R11 |
| TC-F-FL-23 | No timing controls in Confirmation panel | FL·R12 |
| TC-F-FL-24 | No action sequence in Confirmation panel | FL·R12 |
| TC-F-FL-25 | Confirmation message textarea editable | Textarea |
| TC-F-FL-26 | Reset to default message | Reset button |
| TC-R-FL-07 | Confirmation custom message persists | Regression |
| TC-N-FL-08 | Cannot edit timing (read-only) | FL·R11 |

---

### 1B. MEDIUM PRIORITY ✅ — 16 TCs

| TC ID | Description | Justification |
|-------|-------------|---------------|
| TC-F-FL-10 | Add second action row | Action sequence |
| TC-F-FL-11 | Remove action row | Action sequence |
| TC-F-FL-12 | Row numbers auto-increment | Sequence numbering |
| TC-F-FL-14 | Insert {first_name} chip at cursor | Chip insertion |
| TC-F-FL-15 | Insert {office_name} chip at cursor | Chip insertion |
| TC-F-FL-16 | Reset message to factory default | Reset button |
| TC-N-FL-04 | Remove last action → min 1 warning | FL·R6 |
| TC-N-FL-05 | Message > 500 chars → error | Max length |
| TC-B-FL-07 | Message exactly 500 chars | BVA max valid |
| TC-B-FL-08 | Message 501 chars → rejected | BVA max+1 |
| TC-F-FL-17 | Cancel with changes → Discard dialog | Discard dialog |
| TC-F-FL-18 | Discard Changes → panel closes | Discard dialog |
| TC-F-FL-19 | Keep Editing → panel stays open | Discard dialog |
| TC-F-FL-20 | Cancel without changes → no dialog | Discard dialog |
| TC-R-FL-02 | Min Days Ahead persists after reload | Regression |
| TC-R-FL-06 | Action timing persists after reload | Regression |

---

### 1C. REMAIN MANUAL 🛑 — 24 TCs

| TC ID | Description | Why Manual |
|-------|-------------|-----------|
| TC-U-PO-01/02 | Tooltip hover verification | Visual check |
| TC-U-FL-01/02 | Flow tooltip hover | Visual check |
| TC-U-FL-03 | Char counter updates live | UX visual |
| TC-U-FL-04 | Chip insertion at cursor position | Cursor position = human judgment |
| TC-U-FL-05 | Discard dialog UX | Human judgment |
| TC-U-FL-06 | Select Active operatories filter | Depends on live data state |
| TC-S-PO-01/02 | RBAC — non-admin cannot edit | Needs non-admin session |
| TC-S-PO-03/04 | HIPAA — PII in messages masked | Server-side check |
| TC-S-FL-01 | RBAC — flows hidden from non-admin | Non-admin session |
| TC-S-FL-02/03/04 | XSS in message template | Needs live verification |
| TC-B-FL-03/04/05/06/09/10 | Complex BVA pairs | Timing + cursor interaction |
| TC-N-FL-06/07 | Message special chars behavior | Live verification needed |
| TC-R-PO-03 | Reset restores hours (pending DEF-PO-07) | Bug not yet fixed |
| TC-R-FL-03/04/05 | Complex persistence tests | Multi-step state |

---

### 1D. PENDING CONFIRMATION 🔶 — 12 TCs

| Item | Blocking Question |
|------|-------------------|
| Save toast text | What text appears after Save in Patient Outreach? |
| DEF-PO-07 | Does Reset to Defaults now show confirmation dialog? |
| Min Days Ahead max | Is there a max value enforced? |
| Action timing max | Is max enforced (DEF-PO-05 related)? |
| Operatories count | How many operatories exist in staging? |
| Discard dialog trigger | Exact conditions for dirty-state tracking? |

---

## Section 2 — Known Bugs

| ID | Severity | Description |
|----|----------|-------------|
| DEF-PO-03 | 🟡 Medium | Office name repeats ~12× in header |
| DEF-PO-05 | 🔴 High | Action timing defaults to 0 hours (invalid) |
| DEF-PO-06 | 🟡 Medium | Both operatories labeled "new operatory" |
| DEF-PO-07 | 🔴 High | Reset to Defaults fires without confirmation |
| DEF-PO-08 | 🟡 Medium | Reset tooltip mentions "retry settings" (non-existent) |
| DEF-PO-09 | 🟡 Medium | Help text says "confirm" instead of "remind" |
| DEF-PO-10 | 🔴 High | Sub-flow toggles not disabled when master OFF |
| DEF-PO-11 | 🟡 Medium | Only SMS channel available (Call option absent) |

---

## Section 3 — Execution Roadmap

### Phase 1 — Foundation + Smoke (Week 1)
- Confirm selectors via live DOM (Global + Flows tabs)
- Build `patient_outreach_page.py` POM
- 4 smoke tests

### Phase 2 — Global Tab: Master Switch + Preferred Hours (Week 2)
- 18 TCs covering PO·R1–R6

### Phase 3 — Flows: Reminders + Confirmation (Week 3)
- 20 TCs covering FL·R1–R12

### Phase 4 — Medium Priority + CI Update (Week 4)
- 16 TCs + CI update

---

*Ready to proceed to Phase 1 upon approval.*
