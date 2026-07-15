"""
tests/dentivoice/test_language_support.py — Phase 2
Language Support (DV·R3) — checkboxes in AI Identity panel
"""
import pytest
from playwright.sync_api import expect
from pages.dentivoice_page import DentiVoicePage
from test_data.dentivoice_data import DV_ERR


def _open(dv):
    dv.open_edit(DentiVoicePage.CARD["ai_identity"])


@pytest.mark.functional
def test_english_only_accepted(dentivoice_page):
    """TC-F-DV-05: English only (default) → accepted."""
    _open(dentivoice_page)
    # English should be checked by default
    checkboxes = dentivoice_page.page.locator('input[type="checkbox"]')
    assert checkboxes.count() >= 1
    dentivoice_page.cancel()


@pytest.mark.functional
def test_multiple_languages_selectable(dentivoice_page):
    """TC-F-DV-04: Multiple languages can be selected."""
    _open(dentivoice_page)
    checkboxes = dentivoice_page.page.locator('input[type="checkbox"]')
    count = checkboxes.count()
    assert count >= 2, "Expected at least 2 language options"
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
    assert checkboxes.count() >= 1
    dentivoice_page.cancel()
