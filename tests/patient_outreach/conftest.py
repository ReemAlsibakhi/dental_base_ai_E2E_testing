"""tests/patient_outreach/conftest.py — Patient Outreach module fixtures."""

import pytest
from playwright.sync_api import BrowserContext

from pages.patient_outreach_page import PatientOutreachPage


@pytest.fixture()
def patient_outreach_page(admin_context: BrowserContext) -> PatientOutreachPage:
    page = admin_context.new_page()
    po = PatientOutreachPage(page)
    po.navigate_to_patient_outreach()
    yield po
    try:
        if not page.is_closed():
            po.cancel()
    except Exception:
        pass
    if not page.is_closed():
        page.close()
