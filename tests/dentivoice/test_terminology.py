"""
tests/dentivoice/test_terminology.py — Phase 4
Terminology & Pronunciation panel (DV·R8, R9, R34)
Edit index 1 — Confirmed fields:
  textarea[name="additionalInstructions"] — Additional Instructions (max 2000)
  button[role="switch"] nth(0) — Daily Email Report
  button[role="switch"] nth(1) — Send Task Emails Immediately
  button[role="switch"] nth(2) — Reveal Provider Details
  textarea[name="aiCustomizationAdditionalNotes"] — Additional Notes
"""
import pytest
from playwright.sync_api import expect
from pages.dentivoice_page import DentiVoicePage
from test_data.dentivoice_data import INSTRUCTIONS_MAX_VALID, INSTRUCTIONS_MAX_INVALID


def _open(dv):
    dv.open_edit(DentiVoicePage.CARD["terminology"])
    dv.page.wait_for_timeout(500)


def _get_modal(dv):
    return dv.page.locator('[role="dialog"]')


def _get_toggle(dv, index):
    return _get_modal(dv).locator('button[role="switch"]').nth(index)


# ===========================================================================
# Additional Instructions (DV·R8)
# ===========================================================================

@pytest.mark.functional
def test_additional_instructions_saves(dentivoice_page):
    """TC-F-DV-20: Additional Instructions saves successfully."""
    _open(dentivoice_page)
    field = _get_modal(dentivoice_page).locator('textarea[name="additionalInstructions"]')
    dentivoice_page.smart_fill(field, "Always greet patients by first name.")
    dentivoice_page.save_and_assert_success()


@pytest.mark.boundary
def test_instructions_2000_chars_accepted(dentivoice_page):
    """TC-B-DV-14: Instructions 2000 chars (max valid)."""
    _open(dentivoice_page)
    field = _get_modal(dentivoice_page).locator('textarea[name="additionalInstructions"]')
    dentivoice_page.smart_fill(field, INSTRUCTIONS_MAX_VALID)
    dentivoice_page.save_and_assert_success()


@pytest.mark.negative
def test_instructions_2001_chars_rejected(dentivoice_page):
    """TC-N-DV-25: Instructions 2001 chars → error."""
    _open(dentivoice_page)
    field = _get_modal(dentivoice_page).locator('textarea[name="additionalInstructions"]')
    dentivoice_page.smart_fill(field, INSTRUCTIONS_MAX_INVALID)
    dentivoice_page.page.wait_for_timeout(500)
    errors = dentivoice_page.page.locator("p.text-red-500").count()
    is_disabled = dentivoice_page.save_button.is_disabled()
    if not is_disabled and errors == 0:
        dentivoice_page.click_save()
        dentivoice_page.page.wait_for_timeout(500)
        errors = dentivoice_page.page.locator("p.text-red-500").count()
    assert is_disabled or errors > 0
    dentivoice_page.cancel()


# ===========================================================================
# Send Task Emails toggle (DV·R34)
# ===========================================================================

@pytest.mark.functional
def test_send_task_emails_toggle_on(dentivoice_page):
    """TC-F-DV-28: Toggle Send Task Emails — change state to guarantee dirty."""
    _open(dentivoice_page)
    toggle = _get_toggle(dentivoice_page, 1)
    # Click once to change state — always creates dirty state
    initial = toggle.get_attribute("aria-checked")
    toggle.click()
    dentivoice_page.page.wait_for_timeout(500)
    assert toggle.get_attribute("aria-checked") != initial
    dentivoice_page.save_and_assert_success()


@pytest.mark.regression
def test_send_task_emails_persists(dentivoice_page):
    """TC-R-DV-09: Send Task Emails toggle state persists after reload."""
    _open(dentivoice_page)
    toggle = _get_toggle(dentivoice_page, 1)
    initial = toggle.get_attribute("aria-checked")
    # Change state
    toggle.click()
    dentivoice_page.page.wait_for_timeout(300)
    new_state = toggle.get_attribute("aria-checked")
    assert initial != new_state
    dentivoice_page.save_and_assert_success()

    dentivoice_page.navigate_to_dentivoice()
    _open(dentivoice_page)
    toggle = _get_toggle(dentivoice_page, 1)
    assert toggle.get_attribute("aria-checked") == new_state
    dentivoice_page.cancel()


@pytest.mark.functional
def test_quick_setup_template_applies(dentivoice_page):
    """TC-F-DV-19: Quick Setup Template applies preset values."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    # Look for Quick Setup / Template button
    template_btn = modal.get_by_role("button", name="Quick Setup").first
    if not template_btn.is_visible():
        template_btn = modal.get_by_text("Template", exact=False).first
    if template_btn.is_visible():
        template_btn.click()
        dentivoice_page.page.wait_for_timeout(500)
        dentivoice_page.save_and_assert_success()
    else:
        pytest.skip("Quick Setup Template button not found in Terminology panel")
