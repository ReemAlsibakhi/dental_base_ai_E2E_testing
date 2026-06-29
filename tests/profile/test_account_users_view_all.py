"""
tests/profile/test_account_users_view_all.py — Phase 4

View All panel opens ONCE via view_all_panel_open fixture.

Covers:
  TC-F-P-VA-01  View All panel opens with user rows visible
  TC-F-P-VA-02  Row count matches Account Users card count
  TC-S-P-VA-01  Non-admin cannot see View All button (RBAC)
  TC-R-P-VA-01  Name change reflected in View All immediately
"""

import pytest
from playwright.sync_api import expect, BrowserContext

from pages.profile_page import ProfilePage


# ===========================================================================
# TC-F — Functional (panel stays open)
# ===========================================================================

@pytest.mark.functional
def test_view_all_opens_with_user_rows(profile_page: ProfilePage) -> None:
    """TC-F-P-VA-01: View All panel opens and shows at least one user row."""
    profile_page.open_view_all()
    expect(profile_page.view_all_modal).to_be_visible()
    expect(profile_page.view_all_user_rows.first).to_be_visible()
    profile_page.view_all_modal.locator('button[aria-label="Close panel"]').click()


@pytest.mark.functional
def test_view_all_count_matches_card(profile_page: ProfilePage) -> None:
    """TC-F-P-VA-02: Row count in View All equals 'N users with access' on card."""
    card_count = profile_page.get_user_count_number()
    profile_page.open_view_all()
    row_count = profile_page.get_view_all_row_count()
    profile_page.view_all_modal.locator('button[aria-label="Close panel"]').click()
    assert row_count == card_count, (
        f"View All shows {row_count} rows but card says {card_count} users"
    )


# ===========================================================================
# TC-S — Security (RBAC)
# ===========================================================================

@pytest.mark.security
def test_non_admin_cannot_see_view_all(
    profile_page_non_admin: ProfilePage,
) -> None:
    """TC-S-P-VA-01: Non-admin cannot see View All button."""
    expect(profile_page_non_admin.view_all_button).to_be_hidden()


# ===========================================================================
# TC-R — Regression
# ===========================================================================

@pytest.mark.regression
def test_name_updates_in_view_all_after_edit(profile_page: ProfilePage) -> None:
    """TC-R-P-VA-01: Name change in Edit Profile reflected in View All immediately."""
    profile_page.open_edit_modal()
    current = profile_page.last_name_input.input_value().strip()
    new_name = "Hassan" if current != "Hassan" else "Sibakhi"

    profile_page.last_name_input.click(click_count=3)
    profile_page.last_name_input.fill(new_name)
    expect(profile_page.modal_save_button).to_be_enabled(timeout=5_000)
    profile_page.save_and_assert_success()

    profile_page.open_view_all()
    expect(profile_page.page.get_by_text(new_name).first).to_be_visible()
    profile_page.view_all_modal.locator('button[aria-label="Close panel"]').click()
