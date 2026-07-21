"""tests/profile/conftest.py — Profile module fixtures."""

import pytest
from playwright.sync_api import BrowserContext, Page

from pages.profile_page import ProfilePage


@pytest.fixture()
def profile_page(admin_page: Page) -> ProfilePage:
    pp = ProfilePage(admin_page)
    pp.navigate_to_profile()
    return pp


@pytest.fixture()
def profile_page_non_admin(non_admin_page: Page) -> ProfilePage:
    pp = ProfilePage(non_admin_page)
    pp.navigate_to_profile()
    return pp


@pytest.fixture(scope="module")
def profile_page_modal_open(admin_context: BrowserContext) -> ProfilePage:
    """Edit Profile modal open for entire module."""
    page = admin_context.new_page()
    pp = ProfilePage(page)
    pp.navigate_to_profile()
    pp.open_edit_modal()
    yield pp
    try:
        if pp.edit_modal.is_visible():
            pp.close_panel_button.click()
    except Exception:
        pass
    if not page.is_closed():
        page.close()


@pytest.fixture(scope="module")
def add_user_panel_open(admin_context: BrowserContext) -> ProfilePage:
    """Add User panel open for entire module."""
    page = admin_context.new_page()
    pp = ProfilePage(page)
    pp.navigate_to_profile()
    pp.open_add_user_form()
    yield pp
    try:
        if pp.add_user_modal.is_visible():
            pp.add_user_cancel_button.click()
    except Exception:
        pass
    if not page.is_closed():
        page.close()
