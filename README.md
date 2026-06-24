# DentalBase Profile E2E — Playwright (Python)

## Stack
- Python 3.11+
- Playwright for Python
- pytest + pytest-playwright + pytest-html

## Quick Start

```bash
pip install playwright pytest pytest-playwright pytest-html python-dotenv
playwright install chromium
```

## Environment Setup

```bash
cp .env.example .env
# Edit .env and fill in your password
```

`.env` contents:
```env
BASE_URL=https://dentalbase-dev-v2.vercel.app
ADMIN_EMAIL=reem_user
ADMIN_PASSWORD=your_password
NON_ADMIN_EMAIL=
NON_ADMIN_PASSWORD=
HEADLESS=true
SLOW_MO=0
```

## Running Tests

```bash
# Phase 1 — Smoke only (4 tests, ~2 min)
pytest -m smoke --headed -v

# Smoke headless (CI mode)
pytest -m smoke -v

# Full suite
pytest -v

# With HTML report
pytest -m smoke -v --html=reports/report.html --self-contained-html

# Single test (debug)
pytest tests/profile/test_smoke.py::test_valid_first_name_saves_successfully --headed -v -s
```

## Auth Flow (Keycloak SSO)

Login happens **once per session** and is reused by all tests:

1. Navigate to `/login` → click **"Get started"**
2. Keycloak form → `#username` / `#password` → `#kc-login`
3. Redirected to `/overview`
4. Auth state saved to `.playwright_auth/admin.json`
5. Every test gets a fresh browser context pre-seeded with saved cookies

## Project Structure

```
├── conftest.py                    # Session fixtures + auth state reuse
├── pytest.ini                     # Markers + test paths
├── .env.example                   # Environment template
├── pages/
│   ├── base_page.py               # Shared helpers
│   ├── login_page.py              # Keycloak SSO POM
│   └── profile_page.py            # Settings → Profile POM
├── test_data/
│   └── profile_data.py            # All inputs + error strings
└── tests/profile/
    ├── test_smoke.py              # ← Phase 1: 4 smoke tests
    ├── test_edit_profile_first_name.py
    ├── test_edit_profile_last_name.py
    ├── test_edit_profile_phone.py
    ├── test_add_user.py
    ├── test_account_users_view_all.py
    └── test_profile_security.py
```

## Phase Execution Plan

| Phase | Scope | Tests | Status |
|-------|-------|-------|--------|
| **Phase 1** | Smoke — auth + 4 happy paths | 4 | 🔄 In Progress |
| Phase 2 | First Name + Last Name full validation | ~45 | ⏳ Pending |
| Phase 3 | Phone + Add User + Security/RBAC | ~70 | ⏳ Pending |
| Phase 4 | View All + Medium priority + CI pipeline | ~98 | ⏳ Pending |

## Confirmed Selectors (Live DOM)

| Element | Selector |
|---------|----------|
| Login — Username | `#username` |
| Login — Password | `#password` |
| Login — Submit | `#kc-login` |
| Edit modal | `[role="dialog"][aria-label="Edit Profile"]` |
| First Name input | `#first_name` |
| Last Name input | `#last_name` |
| Phone input | `#phone_number` |
| Save Changes | `button:has-text("Save Changes")` (scoped to modal) |
| Cancel | `button:has-text("Cancel")` (scoped to modal) |
| Close panel | `button[aria-label="Close panel"]` |
| Success toast | `p.text-sm.font-medium:has-text("Profile updated successfully")` |
| Add User modal | `[role="dialog"][aria-label="Add New User"]` |
| Add User email | `#email` |
| View All modal | `[role="dialog"][aria-label="All Users"]` |
