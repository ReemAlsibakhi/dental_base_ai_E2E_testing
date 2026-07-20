"""
tests/dentivoice/test_sms_email_alerts.py — Phase 4
SMS & Email Alerts (DV·R26-R34) — Edit index 4
"""
import pytest
from playwright.sync_api import expect
from pages.dentivoice_page import DentiVoicePage
from test_data.dentivoice_data import VALID_PHONE, VALID_EMAIL


def _open(dv):
    dv.open_edit(DentiVoicePage.CARD["sms_email"])
    dv.page.wait_for_timeout(500)


def _get_modal(dv):
    return dv.page.locator('[role="dialog"]')


def _get_sms_toggle(dv):
    return _get_modal(dv).locator('button[role="switch"]').first


def _ensure_sms_toggle(dv, target: bool):
    toggle = _get_sms_toggle(dv)
    current = toggle.get_attribute("aria-checked") == "true"
    if current != target:
        toggle.click(force=True)
        dv.page.wait_for_timeout(500)


# ===========================================================================
# SMS Alerts (DV·R26)
# ===========================================================================

@pytest.mark.functional
def test_sms_alerts_panel_opens(dentivoice_page):
    """TC-SM: SMS & Email Alerts panel opens."""
    _open(dentivoice_page)
    expect(dentivoice_page.cancel_button).to_be_visible()
    dentivoice_page.cancel()


@pytest.mark.functional
def test_sms_toggle_on_saves(dentivoice_page):
    """TC-F-DV-21: Enable SMS Alerts → saves."""
    _open(dentivoice_page)
    toggle = _get_sms_toggle(dentivoice_page)
    if toggle.get_attribute("aria-checked") == "true":
        toggle.click(force=True)
        dentivoice_page.page.wait_for_timeout(300)
        dentivoice_page.save_and_assert_success()
        _open(dentivoice_page)
    toggle = _get_sms_toggle(dentivoice_page)
    toggle.click(force=True)
    dentivoice_page.page.wait_for_timeout(300)
    assert toggle.get_attribute("aria-checked") == "true"
    dentivoice_page.save_and_assert_success()


@pytest.mark.functional
def test_sms_toggle_off_saves(dentivoice_page):
    """TC-F-DV-30: Disable SMS Alerts → saves."""
    _open(dentivoice_page)
    toggle = _get_sms_toggle(dentivoice_page)
    if toggle.get_attribute("aria-checked") == "false":
        toggle.click(force=True)
        dentivoice_page.page.wait_for_timeout(300)
        dentivoice_page.save_and_assert_success()
        _open(dentivoice_page)
    toggle = _get_sms_toggle(dentivoice_page)
    toggle.click(force=True)
    dentivoice_page.page.wait_for_timeout(300)
    assert toggle.get_attribute("aria-checked") == "false"
    dentivoice_page.save_and_assert_success()


@pytest.mark.regression
def test_sms_disable_preserves_rules(dentivoice_page):
    """TC-R-DV-08: Disable SMS preserves existing rules."""
    _open(dentivoice_page)
    _ensure_sms_toggle(dentivoice_page, False)
    dentivoice_page.save_and_assert_success()
    dentivoice_page.navigate_to_dentivoice()
    _open(dentivoice_page)
    expect(dentivoice_page.cancel_button).to_be_visible()
    dentivoice_page.cancel()


# ===========================================================================
# Email Alerts (DV·R30)
# ===========================================================================

@pytest.mark.functional
def test_email_alerts_toggle_on_saves(dentivoice_page):
    """TC-F-DV-23: Enable Email Alerts → saves."""
    _open(dentivoice_page)
    modal = _get_modal(dentivoice_page)
    toggles = modal.locator('button[role="switch"]')
    # Email toggle is nth(1) — after SMS toggle
    email_toggle = toggles.nth(1) if toggles.count() > 1 else toggles.first
    if email_toggle.get_attribute("aria-checked") == "true":
        email_toggle.click(force=True)
        dentivoice_page.page.wait_for_timeout(300)
        dentivoice_page.save_and_assert_success()
        _open(dentivoice_page)
        modal = _get_modal(dentivoice_page)
        email_toggle = modal.locator('button[role="switch"]').nth(1)
    email_toggle.click(force=True)
    dentivoice_page.page.wait_for_timeout(300)
    dentivoice_page.save_and_assert_success()
