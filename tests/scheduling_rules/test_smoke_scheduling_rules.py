"""
tests/scheduling_rules/test_smoke_scheduling_rules.py — Phase 1

4 smoke tests — confirm page loads and key panels open.
All use function-scoped scheduling_rules_page fixture.
"""

import pytest
from playwright.sync_api import expect

from pages.scheduling_rules_page import SchedulingRulesPage
from test_data.scheduling_rules_data import CARD


@pytest.mark.smoke
@pytest.mark.functional
def test_scheduling_rules_tab_loads(
    scheduling_rules_page: SchedulingRulesPage,
) -> None:
    """TC-SM-SR-01: Scheduling Rules tab loads with all Edit buttons visible."""
    edit_btns = scheduling_rules_page.page.get_by_role("button", name="Edit")
    assert edit_btns.count() >= 8, "Expected at least 8 Edit buttons"


@pytest.mark.smoke
@pytest.mark.functional
def test_lead_time_edit_opens(
    scheduling_rules_page: SchedulingRulesPage,
) -> None:
    """TC-SM-SR-02: Lead Time Edit panel opens with toggle and number input."""
    scheduling_rules_page.open_edit(CARD["lead_time"])
    expect(scheduling_rules_page.toggle).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.smoke
@pytest.mark.functional
def test_cancellation_policy_edit_opens(
    scheduling_rules_page: SchedulingRulesPage,
) -> None:
    """TC-SM-SR-03: Cancellation Policy Edit panel opens."""
    scheduling_rules_page.open_edit(CARD["cancellation"])
    expect(scheduling_rules_page.toggle).to_be_visible()
    scheduling_rules_page.cancel()


@pytest.mark.smoke
@pytest.mark.functional
def test_additional_notes_edit_opens(
    scheduling_rules_page: SchedulingRulesPage,
) -> None:
    """TC-SM-SR-04: Additional Notes Edit panel opens with textarea."""
    scheduling_rules_page.open_edit(CARD["additional_notes"])
    expect(scheduling_rules_page.notes_textarea).to_be_visible()
    scheduling_rules_page.cancel()
