"""
tests/dentivoice/test_smoke_dentivoice.py — Phase 1
4 smoke tests — confirm tab loads and key panels open.
"""
import pytest
from playwright.sync_api import expect
from pages.dentivoice_page import DentiVoicePage


@pytest.mark.smoke
@pytest.mark.functional
def test_dentivoice_tab_loads(dentivoice_page):
    """TC-SM-DV-01: DentiVoice tab loads with Edit buttons visible."""
    edit_btns = dentivoice_page.page.get_by_role("button", name="Edit")
    assert edit_btns.count() >= 4


@pytest.mark.smoke
@pytest.mark.functional
def test_ai_identity_edit_opens(dentivoice_page):
    """TC-SM-DV-02: AI Identity panel opens with Assistant Name input."""
    dentivoice_page.open_edit(DentiVoicePage.CARD["ai_identity"])
    expect(dentivoice_page.ai_name_input).to_be_visible()
    dentivoice_page.cancel()


@pytest.mark.smoke
@pytest.mark.functional
def test_terminology_edit_opens(dentivoice_page):
    """TC-SM-DV-03: Terminology panel opens with Additional Instructions."""
    dentivoice_page.open_edit(DentiVoicePage.CARD["terminology"])
    expect(dentivoice_page.add_instructions).to_be_visible()
    dentivoice_page.cancel()


@pytest.mark.smoke
@pytest.mark.functional
def test_emergency_configure_opens(dentivoice_page):
    """TC-SM-DV-04: Emergency Handling Configure panel opens."""
    dentivoice_page.open_edit(DentiVoicePage.CARD["emergency"])
    dentivoice_page.page.wait_for_timeout(500)
    # Panel should be open — cancel button visible
    expect(dentivoice_page.cancel_button).to_be_visible()
    dentivoice_page.cancel()
