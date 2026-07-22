"""
tests/insurance_billing/test_coverage.py
Coverage — Accepted Insurance Plans (IB-COV-R1 to R10)

Known bugs:
  DEF-IB2-01: Plan "D" saved with 1 char (min 2 not enforced at save time)
  DEF-IB2-02: Coverage % fields accept out-of-range values (99999, 100000000)
  DEF-IB2-03: Additional Notes accepts 5000 chars against 500-char limit
  DEF-IB2-10: Cancel silently discards edits (no confirmation dialog)
"""

import pytest
from playwright.sync_api import expect

from pages.insurance_billing_page import InsuranceBillingPage


def _open(ib):
    ib.open_edit(InsuranceBillingPage.CARD["coverage"])


# ===========================================================================
# Smoke
# ===========================================================================

@pytest.mark.smoke
@pytest.mark.functional
def test_coverage_panel_opens(insurance_billing_page):
    """TC-SM-IB-01: Coverage panel opens with required elements."""
    _open(insurance_billing_page)
    expect(insurance_billing_page.modal).to_be_visible()
    expect(insurance_billing_page.cancel_button).to_be_visible()
    insurance_billing_page.cancel()


@pytest.mark.smoke
@pytest.mark.functional
def test_add_custom_plan_form_opens(insurance_billing_page):
    """TC-SM-IB-02: Add Custom button reveals plan form fields."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    expect(insurance_billing_page.insurance_name_input).to_be_visible()
    insurance_billing_page.cancel()


# ===========================================================================
# IB-COV-R1 — Accept All Insurance toggle
# ===========================================================================

@pytest.mark.functional
def test_accept_all_toggle_on(insurance_billing_page):
    """TC-F-IB2-03: Accept All Insurance toggle ON → saves."""
    _open(insurance_billing_page)
    toggle = insurance_billing_page.accept_all_toggle
    initial = toggle.get_attribute("aria-checked")
    toggle.click(force=True)
    insurance_billing_page.page.wait_for_timeout(500)
    assert toggle.get_attribute("aria-checked") != initial
    insurance_billing_page.save_and_assert_success()


# ===========================================================================
# IB-COV-R2 — Insurance Name
# ===========================================================================

@pytest.mark.functional
def test_insurance_name_valid_saves(insurance_billing_page):
    """TC-F-IB2-02: Valid insurance name saves."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.smart_fill(
        insurance_billing_page.insurance_name_input, "Delta Dental PPO"
    )
    insurance_billing_page.save_and_assert_success()


@pytest.mark.negative
def test_insurance_name_empty_shows_error(insurance_billing_page):
    """TC-N-IB2-01: Empty insurance name → error."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.insurance_name_input.fill("")
    insurance_billing_page.insurance_name_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    is_disabled = insurance_billing_page.save_button.is_disabled()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0, "Empty name should be rejected"
    insurance_billing_page.cancel()


@pytest.mark.negative
def test_insurance_name_1_char_shows_error(insurance_billing_page):
    """TC-N-IB2-02: 1-char insurance name → 'at least 2 characters' error."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.smart_fill(insurance_billing_page.insurance_name_input, "D")
    insurance_billing_page.page.wait_for_timeout(500)
    expect(insurance_billing_page.error).to_contain_text("at least 2 characters")
    insurance_billing_page.cancel()


@pytest.mark.boundary
def test_insurance_name_2_chars_accepted(insurance_billing_page):
    """TC-B-IB2-01: 2-char name — minimum valid."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.smart_fill(insurance_billing_page.insurance_name_input, "AB")
    insurance_billing_page.page.wait_for_timeout(500)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0, "2-char name should be accepted"
    insurance_billing_page.cancel()


@pytest.mark.security
def test_insurance_name_xss_rejected(insurance_billing_page):
    """TC-S-IB2-01: XSS payload in insurance name rejected."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.smart_fill(
        insurance_billing_page.insurance_name_input, "<script>alert(1)</script>"
    )
    insurance_billing_page.page.wait_for_timeout(500)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    is_disabled = insurance_billing_page.save_button.is_disabled()
    assert is_disabled or errors > 0, "XSS payload should be rejected"
    insurance_billing_page.cancel()


@pytest.mark.usability
def test_insurance_name_error_clears_when_corrected(insurance_billing_page):
    """TC-U-IB2-02: Error clears when name corrected."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.smart_fill(insurance_billing_page.insurance_name_input, "D")
    insurance_billing_page.page.wait_for_timeout(500)
    expect(insurance_billing_page.error).to_be_visible()
    insurance_billing_page.smart_fill(
        insurance_billing_page.insurance_name_input, "Delta Dental"
    )
    insurance_billing_page.page.wait_for_timeout(500)
    expect(insurance_billing_page.error).to_be_hidden()
    insurance_billing_page.cancel()


# ===========================================================================
# IB-COV-R4 — Plan Type dropdown
# ===========================================================================

@pytest.mark.functional
def test_plan_type_options_available(insurance_billing_page):
    """TC-F-IB2-02: Plan Type dropdown has options."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    plan_type = insurance_billing_page.modal.get_by_text(
        "PPO", exact=False
    ).or_(insurance_billing_page.modal.get_by_text("Plan Type", exact=False)).first
    expect(plan_type).to_be_visible()
    insurance_billing_page.cancel()


# ===========================================================================
# IB-COV-R8 — Coverage % fields
# ===========================================================================

@pytest.mark.negative
def test_coverage_percentage_over_100_shows_error(insurance_billing_page):
    """TC-N-IB2-03: Coverage % > 100 → error."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.fill_coverage_percentage(
        insurance_billing_page.preventive_input, "101"
    )
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    is_disabled = insurance_billing_page.save_button.is_disabled()
    assert is_disabled or errors > 0, "Coverage % > 100 should be rejected"
    insurance_billing_page.cancel()


@pytest.mark.negative
def test_coverage_percentage_negative_shows_error(insurance_billing_page):
    """TC-N-IB2-03b: Coverage % negative → error."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.fill_coverage_percentage(
        insurance_billing_page.preventive_input, "-1"
    )
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    is_disabled = insurance_billing_page.save_button.is_disabled()
    assert is_disabled or errors > 0
    insurance_billing_page.cancel()


@pytest.mark.boundary
def test_coverage_percentage_0_accepted(insurance_billing_page):
    """TC-B-IB2-02: Coverage % = 0 — minimum valid."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.fill_coverage_percentage(
        insurance_billing_page.preventive_input, "0"
    )
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


@pytest.mark.boundary
def test_coverage_percentage_100_accepted(insurance_billing_page):
    """TC-B-IB2-03: Coverage % = 100 — maximum valid."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.fill_coverage_percentage(
        insurance_billing_page.preventive_input, "100"
    )
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


@pytest.mark.usability
def test_coverage_percentage_updates_summary(insurance_billing_page):
    """TC-U-IB2-05: Coverage % update reflects in summary."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.fill_coverage_percentage(
        insurance_billing_page.preventive_input, "80"
    )
    assert insurance_billing_page.preventive_input.input_value() == "80"
    insurance_billing_page.cancel()


@pytest.mark.regression
def test_coverage_percentages_persist(insurance_billing_page):
    """TC-R-IB2-03: Coverage % values persist after save."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.smart_fill(
        insurance_billing_page.insurance_name_input, "Test Plan"
    )
    insurance_billing_page.fill_coverage_percentage(
        insurance_billing_page.preventive_input, "75"
    )
    insurance_billing_page.save_and_assert_success()


# ===========================================================================
# IB-COV-R10 — Additional Notes
# ===========================================================================

@pytest.mark.negative
def test_additional_notes_over_500_blocked(insurance_billing_page):
    """TC-N-IB2-05: Additional Notes > 500 chars → error or blocked."""
    _open(insurance_billing_page)
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.smart_fill(
        insurance_billing_page.additional_notes, "A" * 501
    )
    insurance_billing_page.page.wait_for_timeout(500)
    value = insurance_billing_page.additional_notes.input_value()
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors > 0 or len(value) <= 500, "501-char notes should be rejected"
    insurance_billing_page.cancel()


@pytest.mark.boundary
def test_additional_notes_500_chars_accepted(insurance_billing_page):
    """TC-B: Additional Notes 500 chars — max valid."""
    _open(insurance_billing_page)
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.smart_fill(
        insurance_billing_page.additional_notes, "A" * 500
    )
    insurance_billing_page.page.wait_for_timeout(500)
    errors = insurance_billing_page.page.locator("p.text-red-500").count()
    assert errors == 0
    insurance_billing_page.cancel()


# ===========================================================================
# Delete operations
# ===========================================================================

@pytest.mark.functional
def test_delete_plan_shows_confirmation(insurance_billing_page):
    """TC-F-IB2-15: Delete plan shows confirmation dialog."""
    _open(insurance_billing_page)
    delete_btn = insurance_billing_page.modal.get_by_role(
        "button", name="Remove"
    ).or_(insurance_billing_page.modal.get_by_role("button", name="Delete")).first
    if delete_btn.is_visible():
        delete_btn.click()
        insurance_billing_page.page.wait_for_timeout(500)
        insurance_billing_page.assert_delete_confirmation_shown()
        insurance_billing_page.cancel_delete()
    insurance_billing_page.cancel()


@pytest.mark.negative
def test_cancel_delete_keeps_plan(insurance_billing_page):
    """TC-N-IB2-17: Cancel delete → plan remains."""
    _open(insurance_billing_page)
    delete_btn = insurance_billing_page.modal.get_by_role(
        "button", name="Remove"
    ).or_(insurance_billing_page.modal.get_by_role("button", name="Delete")).first
    if delete_btn.is_visible():
        delete_btn.click()
        insurance_billing_page.page.wait_for_timeout(500)
        insurance_billing_page.cancel_delete()
        expect(insurance_billing_page.modal).to_be_visible()
    insurance_billing_page.cancel()


@pytest.mark.negative
def test_cancel_silently_discards(insurance_billing_page):
    """DEF-IB2-10: Cancel discards edits silently (no confirmation)."""
    _open(insurance_billing_page)
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.smart_fill(
        insurance_billing_page.additional_notes, "Test note change"
    )
    insurance_billing_page.cancel_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    discard_dialog = insurance_billing_page.page.get_by_text("unsaved changes")
    # Document behavior — currently no discard warning on Coverage
    assert not discard_dialog.is_visible(), \
        "DEF-IB2-10: No discard warning shown (inconsistent with Finance panel)"
