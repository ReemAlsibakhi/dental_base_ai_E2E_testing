"""
tests/scheduling_rules/test_override_pms.py — Phase 3
Override PMS (SR·R8) — card index 4
Toggle only — no number input
"""
import pytest
from playwright.sync_api import expect
from pages.scheduling_rules_page import SchedulingRulesPage
from test_data.scheduling_rules_data import CARD


@pytest.mark.functional
@pytest.mark.smoke
def test_override_pms_enable(scheduling_rules_page):
    """TC-F-SR-26: Enable Override PMS toggle."""
    scheduling_rules_page.open_edit(CARD["override_pms"])
    scheduling_rules_page.turn_toggle_on()
    assert scheduling_rules_page.is_toggle_on()
    scheduling_rules_page.save_and_assert_success()


@pytest.mark.functional
def test_override_pms_disable(scheduling_rules_page):
    """TC-F-SR-27: Disable Override PMS toggle."""
    scheduling_rules_page.open_edit(CARD["override_pms"])
    scheduling_rules_page.turn_toggle_off()
    assert not scheduling_rules_page.is_toggle_on()
    scheduling_rules_page.save_and_assert_success()
