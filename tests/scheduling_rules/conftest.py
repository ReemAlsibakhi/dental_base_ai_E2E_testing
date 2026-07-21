"""tests/scheduling_rules/conftest.py — Scheduling Rules module fixtures."""

import pytest
from playwright.sync_api import BrowserContext

from pages.scheduling_rules_page import SchedulingRulesPage


@pytest.fixture()
def scheduling_rules_page(admin_context: BrowserContext) -> SchedulingRulesPage:
    page = admin_context.new_page()
    sr = SchedulingRulesPage(page)
    sr.navigate_to_scheduling_rules()
    yield sr
    try:
        if not page.is_closed():
            sr.cancel()
    except Exception:
        pass
    if not page.is_closed():
        page.close()
