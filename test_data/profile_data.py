"""
test_data/profile_data.py — Single source of truth for all Profile test data.

Error messages confirmed against live site (2026-06):
  fn_required  : "First name is required"
  fn_min       : "First name must be at least 2 characters"
  fn_chars     : "First name can only contain letters, spaces, hyphens, and apostrophes"
  fn_consecutive: "First name cannot contain consecutive special characters"
  fn_start_end : "First name must start and end with a letter"   ← CONFIRMED
  ln_required  : "Last name is required"
  ln_min       : "Last name must be at least 2 characters"
  ph_min       : "Phone number must be at least 10 digits"

NOTE on fn_leading / fn_trailing:
  Live site shows ONE message for both: "First name must start and end with a letter"
  Both leading AND trailing specials map to the same error key: fn_start_end
"""

# ---------------------------------------------------------------------------
# Error message constants — confirmed from live site
# ---------------------------------------------------------------------------

ERR = {
    # First Name
    "fn_required":    "First name is required",
    "fn_min":         "First name must be at least 2 characters",
    "fn_max":         "First name cannot exceed 50 characters",
    "fn_chars":       "First name can only contain letters, spaces, hyphens, and apostrophes",
    "fn_consecutive": "First name cannot contain consecutive special characters",
    "fn_start_end":   "First name must start and end with a letter",

    # Last Name
    "ln_required":    "Last name is required",
    "ln_min":         "Last name must be at least 2 characters",
    "ln_max":         "Last name cannot exceed 50 characters",
    "ln_chars":       "Last name can only contain letters, spaces, hyphens, and apostrophes",
    "ln_consecutive": "Last name cannot contain consecutive special characters",
    "ln_start_end":   "Last name must start and end with a letter",

    # Phone
    "ph_min_digits":  "Phone number must be at least 10 digits",

    # Add User — Email
    "au_email_required":  "Email is required",
    "au_email_format":    "Please enter a valid email address",
    "au_email_duplicate": "This user is already a member",
}

# ---------------------------------------------------------------------------
# First Name — valid inputs (Phase 2 — medium priority)
# ---------------------------------------------------------------------------

FIRST_NAME_VALID = [
    ("simple",           "Reem"),
    ("hyphen_middle",    "Mary-Jane"),
    ("apostrophe_mid",   "O'Brien"),
    ("internal_space",   "Anne Marie"),
    ("arabic_unicode",   "رنا"),
    ("accented_latin",   "José"),
    ("exact_min_2",      "Jo"),
    ("exact_max_50",     "A" * 50),
]

# ---------------------------------------------------------------------------
# First Name — invalid inputs
# Format: (test_id, input_value, error_key)
# ---------------------------------------------------------------------------

FIRST_NAME_INVALID = [
    # Required
    ("empty",                 "",            "fn_required"),
    ("whitespace_only",       "   ",         "fn_required"),

    # Min length (R-FN-2)
    ("one_char",              "J",           "fn_min"),

    # Max length (R-FN-3)
    ("over_max_51",           "A" * 51,      "fn_max"),

    # Disallowed characters (R-FN-4)
    ("digits",                "Reem123",     "fn_chars"),
    ("at_symbol",             "John@Doe",    "fn_chars"),
    ("underscore",            "Test_Name",   "fn_chars"),
    ("emoji",                 "Reem😊",      "fn_chars"),
    ("script_tag",            "<script>",    "fn_chars"),

    # Consecutive specials (R-FN-5)
    ("consec_hyphens",        "Mary--Jane",  "fn_consecutive"),
    ("consec_apostrophes",    "O''Brien",    "fn_consecutive"),
    ("consec_hyphen_ap",      "Mary-'Jane",  "fn_consecutive"),
    ("consec_ap_hyphen",      "Mary'-Jane",  "fn_consecutive"),

    # Must start and end with letter (R-FN-6)
    ("leading_hyphen",        "-Reem",       "fn_start_end"),
    ("leading_apostrophe",    "'Reem",       "fn_start_end"),
    ("trailing_hyphen",       "Reem-",       "fn_start_end"),
    ("trailing_apostrophe",   "Reem'",       "fn_start_end"),
]

# ---------------------------------------------------------------------------
# Last Name — valid inputs
# ---------------------------------------------------------------------------

LAST_NAME_VALID = [
    ("simple",           "Sibakhi"),
    ("hyphen_middle",    "Al-Hassan"),
    ("apostrophe_mid",   "O'Neill"),
    ("internal_spaces",  "Van Der Berg"),
    ("arabic_unicode",   "سيباخي"),
    ("accented_latin",   "Müller"),
    ("exact_min_2",      "Li"),
    ("exact_max_50",     "B" * 50),
]

# ---------------------------------------------------------------------------
# Last Name — invalid inputs
# Format: (test_id, input_value, error_key)
# ---------------------------------------------------------------------------

LAST_NAME_INVALID = [
    # Required
    ("empty",                 "",             "ln_required"),
    ("whitespace_only",       "   ",          "ln_required"),

    # Min length (R-LN-2)
    ("one_char",              "L",            "ln_min"),

    # Max length (R-LN-3)
    ("over_max_51",           "B" * 51,       "ln_max"),

    # Disallowed characters (R-LN-4)
    ("digits",                "Smith99",      "ln_chars"),
    ("at_symbol",             "Hassan@1",     "ln_chars"),
    ("underscore",            "Test_Last",    "ln_chars"),
    ("emoji",                 "Smith🎉",      "ln_chars"),
    ("xss_img_tag",           "<img onerror=1>", "ln_chars"),

    # Consecutive specials (R-LN-5)
    ("consec_hyphens",        "Al--Hassan",   "ln_consecutive"),
    ("consec_apostrophes",    "O''Neill",     "ln_consecutive"),
    ("consec_hyphen_ap",      "Al-'Hassan",   "ln_consecutive"),
    ("consec_ap_hyphen",      "Al'-Hassan",   "ln_consecutive"),

    # Must start and end with letter (R-LN-6)
    ("leading_hyphen",        "-Hassan",      "ln_start_end"),
    ("leading_apostrophe",    "'Hassan",      "ln_start_end"),
    ("trailing_hyphen",       "Hassan-",      "ln_start_end"),
    ("trailing_apostrophe",   "Hassan'",      "ln_start_end"),
]

# ---------------------------------------------------------------------------
# Phone Number
# ---------------------------------------------------------------------------

PHONE_VALID = [
    ("digits_10",       "6035551234"),
    ("empty_optional",  ""),
]

PHONE_INVALID = [
    ("five_digits",   "12345",     "ph_min_digits"),
    ("nine_digits",   "603555123", "ph_min_digits"),
]

PHONE_ALPHA = "abcdefghij"   # alpha chars stripped silently (R-PH-3)

# ---------------------------------------------------------------------------
# Add User — Email
# ---------------------------------------------------------------------------

ADD_USER_EMAIL_INVALID = [
    ("empty",         "",               "au_email_required"),
    ("no_domain",     "notanemail",     "au_email_format"),
    ("missing_domain","user@",          "au_email_format"),
    ("missing_local", "@dentivoice.com","au_email_format"),
]

ADD_USER_EMAIL_VALID     = "newuser+autotest@dentivoice.com"
ADD_USER_DUPLICATE_EMAIL = "osama+stg+opendental@dentalbase.ai"
