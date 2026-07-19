"""
tests/dentivoice/test_language_support.py — Phase 2
Language Support (DV·R3) — switches inside AI Identity panel

Confirmed: language options are button[role="switch"] + aria-checked
NOT input[type="checkbox"]
"""
import pytest
from playwright.sync_api import expect
from pages.dentivoice_page import DentiVoicePage


def _open(dv):
    dv.open_edit(DentiVoicePage.CARD["ai_identity"])


def _get_language_switches(dv):
    """Get all language switches inside the open modal."""
    modal = dv.page.locator('[role="dialog"]')
    return modal.locator('button[role="switch"]')


@pytest.mark.functional
def test_language_switches_visible(dentivoice_page):
    """TC-F-DV-04: Language switches are visible in AI Identity panel."""
    _open(dentivoice_page)
    switches = _get_language_switches(dentivoice_page)
    assert switches.count() >= 1, "Expected at least 1 language switch"
    dentivoice_page.cancel()


@pytest.mark.functional
def test_language_switch_toggleable(dentivoice_page):
    """TC-F-DV-05: Language switch can be toggled ON/OFF."""
    _open(dentivoice_page)
    switches = _get_language_switches(dentivoice_page)
    first = switches.first
    initial = first.get_attribute("aria-checked")
    first.click()
    dentivoice_page.page.wait_for_timeout(300)
    after = first.get_attribute("aria-checked")
    assert initial != after, "Language switch should toggle"
    dentivoice_page.cancel()


@pytest.mark.regression
def test_language_selection_persists(dentivoice_page):
    """TC-R-DV-01: Language selection persists after save + reload."""
    _open(dentivoice_page)
    switches = _get_language_switches(dentivoice_page)
    first = switches.first
    # Turn it ON
    if first.get_attribute("aria-checked") == "false":
        first.click()
        dentivoice_page.page.wait_for_timeout(300)
    dentivoice_page.fill_ai_name("Morgan" if dentivoice_page.ai_name_input.input_value() != "Morgan" else "Sofia")
    dentivoice_page.save_and_assert_success()

    dentivoice_page.navigate_to_dentivoice()
    _open(dentivoice_page)
    switches = _get_language_switches(dentivoice_page)
    assert switches.first.get_attribute("aria-checked") == "true"
    dentivoice_page.cancel()
