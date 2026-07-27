"""
tests/insurance_billing/test_coverage.py
Coverage — Accepted Insurance Plans (IB-COV-R1 to R10)

Key patterns:
  - add_plan() helper handles full Add Custom flow with UUID names
  - Tab press after smart_fill to trigger validation
  - p[id$='-error'] for error detection (confirmed from live DOM)
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
    """TC-SM-IB-01: Coverage panel opens."""
    _open(insurance_billing_page)
    expect(insurance_billing_page.modal).to_be_visible()
    expect(insurance_billing_page.cancel_button).to_be_visible()
    insurance_billing_page.cancel()


@pytest.mark.smoke
@pytest.mark.functional
def test_add_custom_form_opens(insurance_billing_page):
    """TC-SM-IB-02: Add Custom reveals New Plan form."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    expect(insurance_billing_page.insurance_name_input).to_be_visible()
    expect(insurance_billing_page.payer_id_input).to_be_visible()
    insurance_billing_page.cancel()


# ===========================================================================
# Accept All Toggle (IB-COV-R1)
# ===========================================================================

@pytest.mark.functional
def test_accept_all_toggle_changes_state(insurance_billing_page):
    """TC-F-IB2-03: Accept All toggle changes state and saves."""
    _open(insurance_billing_page)
    toggle = insurance_billing_page.accept_all_toggle
    initial = toggle.get_attribute("aria-checked")
    toggle.click()
    insurance_billing_page.page.wait_for_timeout(800)
    assert toggle.get_attribute("aria-checked") != initial
    insurance_billing_page.save_and_assert_success()


# ===========================================================================
# Insurance Name (IB-COV-R2)
# ===========================================================================

@pytest.mark.functional
def test_insurance_name_valid_saves(insurance_billing_page):
    """TC-F-IB2-02: Valid plan saves via Add Custom flow."""
    _open(insurance_billing_page)
    insurance_billing_page.add_plan(
        name=InsuranceBillingPage.unique("Delta"),
        payer_id="99001"
    )


@pytest.mark.negative
def test_insurance_name_empty_blocked(insurance_billing_page):
    """TC-N-IB2-01: Empty name → Save Plan disabled."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.insurance_name_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    assert insurance_billing_page.save_plan_button.is_disabled() or \
           insurance_billing_page.error.is_visible()
    insurance_billing_page.cancel()


@pytest.mark.negative
def test_insurance_name_1_char_shows_error(insurance_billing_page):
    """TC-N-IB2-02: 1-char name → validation error."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.smart_fill(insurance_billing_page.insurance_name_input, "D")
    insurance_billing_page.insurance_name_input.press("Tab")
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
    insurance_billing_page.insurance_name_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    # No name error should appear
    name_error = insurance_billing_page.modal.locator("p[id$='-error']").filter(
        has_text="characters"
    )
    assert not name_error.is_visible()
    insurance_billing_page.cancel()


@pytest.mark.security
def test_insurance_name_xss_rejected(insurance_billing_page):
    """TC-S-IB2-01: XSS in name → blocked."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.smart_fill(
        insurance_billing_page.insurance_name_input, "<script>alert(1)</script>"
    )
    insurance_billing_page.insurance_name_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    assert insurance_billing_page.save_plan_button.is_disabled() or \
           insurance_billing_page.error.is_visible()
    insurance_billing_page.cancel()


@pytest.mark.usability
def test_insurance_name_error_clears_when_corrected(insurance_billing_page):
    """TC-U-IB2-02: Error clears when name corrected."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.smart_fill(insurance_billing_page.insurance_name_input, "D")
    insurance_billing_page.insurance_name_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    expect(insurance_billing_page.error).to_be_visible()
    insurance_billing_page.smart_fill(insurance_billing_page.insurance_name_input, "Delta Dental")
    insurance_billing_page.insurance_name_input.press("Tab")
    insurance_billing_page.page.wait_for_timeout(500)
    expect(insurance_billing_page.error).to_be_hidden()
    insurance_billing_page.cancel()


# ===========================================================================
# Coverage % (IB-COV-R8)
# ===========================================================================

@pytest.mark.negative
def test_coverage_percentage_over_100_blocked(insurance_billing_page):
    """TC-N-IB2-03: Coverage % > 100 → blocked."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.fill_coverage_percentage(
        insurance_billing_page.preventive_input, "101"
    )
    assert insurance_billing_page.save_plan_button.is_disabled() or \
           insurance_billing_page.modal.locator("p[id$='-error']").count() > 0
    insurance_billing_page.cancel()


@pytest.mark.negative
def test_coverage_percentage_negative_blocked(insurance_billing_page):
    """TC-N-IB2-03b: Coverage % negative → blocked."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.fill_coverage_percentage(
        insurance_billing_page.preventive_input, "-1"
    )
    assert insurance_billing_page.save_plan_button.is_disabled() or \
           insurance_billing_page.modal.locator("p[id$='-error']").count() > 0
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
    pct_error = insurance_billing_page.modal.locator("p[id$='-error']").filter(
        has_text="Preventive"
    )
    assert not pct_error.is_visible()
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
    pct_error = insurance_billing_page.modal.locator("p[id$='-error']").filter(
        has_text="Preventive"
    )
    assert not pct_error.is_visible()
    insurance_billing_page.cancel()


@pytest.mark.regression
def test_coverage_percentages_persist(insurance_billing_page):
    """TC-R-IB2-03: Plan with coverage % saves and persists."""
    _open(insurance_billing_page)
    insurance_billing_page.add_custom_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    name = InsuranceBillingPage.unique("Coverage")
    insurance_billing_page.smart_fill(insurance_billing_page.insurance_name_input, name)
    insurance_billing_page.insurance_name_input.press("Tab")
    insurance_billing_page.smart_fill(insurance_billing_page.payer_id_input, "55555")
    insurance_billing_page.fill_coverage_percentage(insurance_billing_page.preventive_input, "75")
    insurance_billing_page.save_plan_and_assert_success()


# ===========================================================================
# Additional Notes (IB-COV-R10)
# ===========================================================================

@pytest.mark.negative
def test_additional_notes_over_500_blocked(insurance_billing_page):
    """TC-N-IB2-05: Notes > 500 chars → error or capped."""
    _open(insurance_billing_page)
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.smart_fill(
        insurance_billing_page.additional_notes, "A" * 501
    )
    insurance_billing_page.page.wait_for_timeout(500)
    value = insurance_billing_page.additional_notes.input_value()
    errors = insurance_billing_page.modal.locator("p[id$='-error']").count()
    assert errors > 0 or len(value) <= 500
    insurance_billing_page.cancel()


@pytest.mark.boundary
def test_additional_notes_500_chars_accepted(insurance_billing_page):
    """TC-B-IB2: Notes 500 chars — max valid."""
    _open(insurance_billing_page)
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.smart_fill(
        insurance_billing_page.additional_notes, "A" * 500
    )
    insurance_billing_page.page.wait_for_timeout(500)
    errors = insurance_billing_page.modal.locator("p[id$='-error']").count()
    assert errors == 0
    insurance_billing_page.cancel()


# ===========================================================================
# Delete
# ===========================================================================

@pytest.mark.functional
def test_delete_plan_shows_confirmation(insurance_billing_page):
    """TC-F-IB2-15: Delete plan shows confirmation."""
    _open(insurance_billing_page)
    delete_btn = insurance_billing_page.modal.get_by_role(
        "button", name="Remove"
    ).or_(insurance_billing_page.modal.get_by_role("button", name="Delete")).first
    if delete_btn.is_visible():
        delete_btn.click()
        insurance_billing_page.page.wait_for_timeout(500)
        insurance_billing_page.assert_delete_confirmation_shown()
        insurance_billing_page.cancel()
    else:
        pytest.skip("No plan to delete")


@pytest.mark.functional
def test_cancel_with_changes(insurance_billing_page):
    """TC-F-IB2: Cancel with unsaved changes."""
    _open(insurance_billing_page)
    insurance_billing_page.page.wait_for_timeout(500)
    insurance_billing_page.smart_fill(
        insurance_billing_page.additional_notes, "Unsaved change"
    )
    insurance_billing_page.cancel_button.click()
    insurance_billing_page.page.wait_for_timeout(500)
    discard = insurance_billing_page.page.get_by_role("button", name="Discard")
    if discard.is_visible():
        discard.click()
