# DentalBase Profile E2E — Playwright (Python)

## Stack
- Python 3.11+
- Playwright for Python
- pytest + pytest-playwright

## Quick Start

```bash
pip install playwright pytest pytest-playwright pytest-html python-dotenv
playwright install chromium
pytest --headed -v
```

## Required Environment Variables

Create a `.env` file from `.env.example`:

```env
BASE_URL=https://dentalbase-staging-v2.vercel.app
ADMIN_EMAIL=osama+stg+opendental@dentalbase.ai
ADMIN_PASSWORD=<your-password>
NON_ADMIN_EMAIL=<non-admin-user@domain.com>
NON_ADMIN_PASSWORD=<non-admin-password>
```

## Project Structure

```
profile_e2e/
├── conftest.py                   # Fixtures: browser, auth state, pages
├── pytest.ini                    # Pytest config
├── .env.example
├── pages/
│   ├── base_page.py              # BasePage with shared helpers
│   ├── login_page.py             # Login page POM
│   └── profile_page.py          # Profile/Settings POM (LOCATORS NEEDED)
├── fixtures/
│   └── auth_fixtures.py          # Auth state reuse
├── test_data/
│   └── profile_data.py           # All parametrised test data
├── utils/
│   └── helpers.py                # String generators, wait helpers
└── tests/profile/
    ├── test_edit_profile_first_name.py
    ├── test_edit_profile_last_name.py
    ├── test_edit_profile_phone.py
    ├── test_add_user.py
    ├── test_account_users_view_all.py
    └── test_profile_security.py
```

## ⚠️  LOCATORS REQUIRED FROM LIVE SITE

See `pages/profile_page.py` for all `TODO:` placeholders.
The following selectors must be confirmed from the live DOM before the
suite will run correctly:

### Login Page
| Placeholder | What to inspect |
|-------------|----------------|
| `LOGIN_EMAIL_INPUT` | Email/username input on /login |
| `LOGIN_PASSWORD_INPUT` | Password input on /login |
| `LOGIN_SUBMIT_BUTTON` | Sign-in button |

### Settings / Profile Page
| Placeholder | What to inspect |
|-------------|----------------|
| `SETTINGS_NAV_LINK` | Left-nav or top-nav link to /settings |
| `PROFILE_TAB` | "Profile" tab selector inside /settings |
| `EDIT_PROFILE_BUTTON` | "Edit" button on Profile Information card |
| **Edit Profile Modal** | |
| `EDIT_MODAL_CONTAINER` | Modal wrapper element |
| `FIRST_NAME_INPUT` | First Name field inside modal |
| `LAST_NAME_INPUT` | Last Name field inside modal |
| `PHONE_INPUT` | Phone Number field inside modal |
| `SAVE_BUTTON` | Save/Submit button inside modal |
| `CANCEL_BUTTON` | Cancel button inside modal |
| `FIRST_NAME_ERROR` | Inline error message under First Name |
| `LAST_NAME_ERROR` | Inline error message under Last Name |
| `PHONE_ERROR` | Inline error message under Phone |
| `SUCCESS_TOAST` | Success toast/notification |
| **Profile Card (read)** | |
| `FULL_NAME_DISPLAY` | Full name text on profile card |
| `PHONE_DISPLAY` | Phone text on profile card ("No phone" or number) |
| `EMAIL_DISPLAY` | Email display on profile card |
| **Account Users Card** | |
| `USER_COUNT_TEXT` | "N users with access" text |
| `ADD_USER_BUTTON` | "Add User" button |
| `VIEW_ALL_BUTTON` | "View All" button |
| **Add User Form/Modal** | |
| `ADD_USER_EMAIL_INPUT` | Email field in Add User form |
| `ADD_USER_FIRST_NAME_INPUT` | First Name in Add User (if separate) |
| `ADD_USER_LAST_NAME_INPUT` | Last Name in Add User (if separate) |
| `ADD_USER_SUBMIT_BUTTON` | Submit/Invite button |
| `ADD_USER_CANCEL_BUTTON` | Cancel button |
| `ADD_USER_EMAIL_ERROR` | Inline error on email field |
| **View All Modal** | |
| `VIEW_ALL_MODAL` | View All modal/panel container |
| `VIEW_ALL_USER_ROWS` | Each user row in the list |
