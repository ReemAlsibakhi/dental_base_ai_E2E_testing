# DentalBase Profile E2E — Playwright (Python)

## Stack
- Python 3.11+
- Playwright for Python
- pytest + pytest-playwright + pytest-html

## Quick Start

```bash
pip install playwright pytest pytest-playwright pytest-html python-dotenv
playwright install chromium
pytest --headed -v
```

## Environment Variables

Create a `.env` file:

```env
BASE_URL=https://dentalbase-dev-v2.vercel.app
ADMIN_EMAIL=reem_user
ADMIN_PASSWORD=your_password
NON_ADMIN_EMAIL=non_admin_user
NON_ADMIN_PASSWORD=non_admin_password
HEADLESS=true
SLOW_MO=0
```

## Auth Flow (Keycloak SSO)

The app uses Keycloak SSO. The login sequence is:
1. Navigate to `/login` on the main app
2. Click **"Get started"** → redirected to `keycloak-dev.dentalbase.ai`
3. Fill `#username` + `#password` → click `#kc-login`
4. Redirected back to `/overview`

`conftest.py` handles this once per session and reuses the auth state for all tests.

## Project Structure

```
├── conftest.py                   # Fixtures + auth state reuse
├── pytest.ini                    # Markers + test paths
├── .env.example                  # Environment template
├── pages/
│   ├── base_page.py              # Shared helpers
│   ├── login_page.py             # Keycloak SSO login POM
│   └── profile_page.py          # Settings → Profile POM (real selectors)
├── test_data/
│   └── profile_data.py           # All test inputs + error strings
└── tests/profile/
    ├── test_edit_profile_first_name.py
    ├── test_edit_profile_last_name.py
    ├── test_edit_profile_phone.py
    ├── test_add_user.py
    ├── test_account_users_view_all.py
    └── test_profile_security.py
```

## Run Subsets

```bash
pytest -m smoke          # Quick sanity check (CI per-PR)
pytest -m regression     # Full suite (nightly)
pytest -m negative       # Validation / error paths only
pytest -m security       # RBAC tests only
```

## Real Selectors (extracted from live DOM)

| Element | Selector |
|---------|----------|
| Login — Username | `#username` |
| Login — Password | `#password` |
| Login — Submit | `#kc-login` |
| Settings nav link | `a[href="/settings"]` |
| Profile tab | `button:has-text("Profile")` |
| Edit button | `button[type="button"]:has-text("Edit")` |
| Edit modal | `[role="dialog"][aria-label="Edit Profile"]` |
| First Name input | `#first_name` |
| Last Name input | `#last_name` |
| Phone input | `#phone_number` |
| Save Changes | `button:has-text("Save Changes")` (inside modal) |
| Cancel | `button:has-text("Cancel")` (inside modal) |
| Close panel | `button[aria-label="Close panel"]` |
| Success toast | `p.text-sm.font-medium:has-text("Profile updated successfully")` |
| User count | `p.text-sm.text-gray-500:has-text("users with access")` |
| Add User button | `button:has-text("Add User")` |
| View all button | `button:has-text("View all")` |
| Add User modal | `[role="dialog"][aria-label="Add New User"]` |
| Add User — Email | `#email` |
| Add User — First Name | `#first_name` (inside Add User modal) |
| Add User — Last Name | `#last_name` (inside Add User modal) |
| Add User — Username | `#username` (inside Add User modal) |
| View All modal | `[role="dialog"][aria-label="All Users"]` |
| View All — user rows | `.space-y-1 > div.flex.items-center` (inside modal) |
