"""tests/practice_profile/conftest.py — Practice Profile module fixtures."""

import pytest
from playwright.sync_api import BrowserContext

from pages.practice_profile_page import PracticeProfilePage


@pytest.fixture()
def practice_profile_page(admin_context: BrowserContext) -> PracticeProfilePage:
    page = admin_context.new_page()
    pp = PracticeProfilePage(page)
    pp.navigate_to_practice_profile()
    pp.open_edit_form()
    yield pp
    try:
        if not page.is_closed():
            pp.cancel()
    except Exception:
        pass
    if not page.is_closed():
        page.close()


@pytest.fixture(scope="module")
def practice_profile_form_open(admin_context: BrowserContext) -> PracticeProfilePage:
    """Practice Profile edit form open for entire module."""
    page = admin_context.new_page()
    pp = PracticeProfilePage(page)
    pp.navigate_to_practice_profile()
    pp.open_edit_form()
    yield pp
    try:
        if not page.is_closed():
            pp.cancel()
    except Exception:
        pass
    if not page.is_closed():
        page.close()
