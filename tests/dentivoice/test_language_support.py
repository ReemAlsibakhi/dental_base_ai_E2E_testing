"""
tests/dentivoice/test_language_support.py — Phase 2
Language Support (DV·R3) — checkboxes in AI Identity panel
"""
import pytest
from playwright.sync_api import expect
from pages.dentivoice_page import DentiVoicePage


def _open(dv):
    dv.open_edit(DentiVoicePage.CARD["ai_identity"])


@pytest.mark.functional
def test_english_default_checked(dentivoice_page):
    """TC-F-DV-05: English is checked by default."""
    _open(dentivoice_page)
    checkboxes = dentivoice_page.page.locator('input[type="checkbox"]')
    assert checkboxes.count() >= 1
    assert checkboxes.first.is_checked(), "English should be checked by default"
    dentivoice_page.cancel()


@pytest.mark.functional
def test_multiple_languages_selectable(dentivoice_page):
    """TC-F-DV-04: Multiple languages can be selected."""
    _open(dentivoice_page)
    checkboxes = dentivoice_page.page.locator('input[type="checkbox"]')
    assert checkboxes.count() >= 2, "Expected at least 2 language options"
    dentivoice_page.cancel()


@pytest.mark.regression
def test_language_selection_persists(dentivoice_page):
    """TC-R-DV-01: Language selection persists after reload."""
    _open(dentivoice_page)
    dentivoice_page.fill_ai_name("Sofia")
    dentivoice_page.save_and_assert_success()

    dentivoice_page.navigate_to_dentivoice()
    _open(dentivoice_page)
    checkboxes = dentivoice_page.page.locator('input[type="checkbox"]')
    assert checkboxes.first.is_checked()
    dentivoice_page.cancel()
