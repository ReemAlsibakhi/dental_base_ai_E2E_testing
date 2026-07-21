"""tests/dentivoice/conftest.py — DentiVoice module fixtures."""

import pytest
from playwright.sync_api import BrowserContext

from pages.dentivoice_page import DentiVoicePage


@pytest.fixture()
def dentivoice_page(admin_context: BrowserContext) -> DentiVoicePage:
    page = admin_context.new_page()
    dv = DentiVoicePage(page)
    dv.navigate_to_dentivoice()
    yield dv
    try:
        if not page.is_closed():
            dv.cancel()
    except Exception:
        pass
    if not page.is_closed():
        page.close()
