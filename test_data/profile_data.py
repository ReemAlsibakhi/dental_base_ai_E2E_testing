"""
test_data/profile_data.py — Single source of truth for all Profile test data.

Error messages confirmed against live site (2026-06):
  fn_required   "First name is required"
  fn_min        "First name must be at least 2 characters"
  fn_chars      "First name can only contain letters, spaces, hyphens, and apostrophes"
  fn_consecutive"First name cannot contain consecutive special characters"
  fn_start_end  "First name must start and end with a letter"
  ln_required   "Last name is required"
  ln_min        "Last name must be at least 2 characters"
  ph_min_digits "Phone number must be at least 10 digits"

NOTE: fn_leading + fn_trailing share one message: "must start and end with a letter"
"""

# ---------------------------------------------------------------------------
# Error messages — single source of truth
# ---------------------------------------------------------------------------

ERR = {
    # First Name
    "fn_required":    "First name is required",
    "fn_min":         "First name must be at least 2 characters",
    "fn_max":         "First name must not exceed 50 characters",
    "fn_chars":       "First name can only contain letters, spaces, hyphens, and apostrophes",
    "fn_consecutive": "First name cannot contain consecutive special characters",
    "fn_start_end":   "First name must start and end with a letter",

    # Last Name
    "ln_required":    "Last name is required",
    "ln_min":         "Last name must be at least 2 characters",
    "ln_max":         "Last name must not exceed 50 characters",
    "ln_chars":       "Last name can only contain letters, spaces, hyphens, and apostrophes",
    "ln_consecutive": "Last name cannot contain consecutive special characters",
    "ln_start_end":   "Last name must start and end with a letter",

    # Phone
    "ph_min_digits":  "Phone number must be at least 10 digits",

    # Add User — Email (R-AU-EM-1/2/3)
    "au_email_required":  "Email is required",
    "au_email_format":    "Please enter a valid email address",
    "au_email_duplicate": "This user is already a member",

    # Add User — Username (R-UN-*)
    "un_required":    "Username is required",
    "un_min":         "Username must be at least 3 characters",
    "un_max":         "Username cannot exceed 30 characters",
    "un_chars":       "Username can only contain lowercase letters, numbers, hyphens, underscores, and dots",
    "un_consecutive": "Username cannot contain consecutive special characters",
    "un_start_end":   "Username must start and end with a letter or number",
    "un_duplicate":   "Username is already taken",
}

# ---------------------------------------------------------------------------
# First Name
# ---------------------------------------------------------------------------

FIRST_NAME_VALID = [
    ("simple",         "Reem"),
    ("hyphen_middle",  "Mary-Jane"),
    ("apostrophe_mid", "O'Brien"),
    ("internal_space", "Anne Marie"),
    ("arabic_unicode", "رنا"),
    ("accented_latin", "José"),
]

FIRST_NAME_INVALID = [
    ("empty",              "",           "fn_required"),
    ("whitespace_only",    "   ",        "fn_required"),
    ("one_char",           "J",          "fn_min"),
    ("digits",             "Reem123",    "fn_chars"),
    ("at_symbol",          "John@Doe",   "fn_chars"),
    ("underscore",         "Test_Name",  "fn_chars"),
    ("emoji",              "Reem😊",     "fn_chars"),
    ("script_tag",         "<script>",   "fn_chars"),
    ("consec_hyphens",     "Mary--Jane", "fn_consecutive"),
    ("consec_apostrophes", "O''Brien",   "fn_consecutive"),
    ("consec_hyphen_ap",   "Mary-'Jane", "fn_consecutive"),
    ("consec_ap_hyphen",   "Mary'-Jane", "fn_consecutive"),
    ("leading_hyphen",     "-Reem",      "fn_start_end"),
    ("leading_apostrophe", "'Reem",      "fn_start_end"),
    ("trailing_hyphen",    "Reem-",      "fn_start_end"),
    ("trailing_apostrophe","Reem'",      "fn_start_end"),
]

# ---------------------------------------------------------------------------
# Last Name
# ---------------------------------------------------------------------------

LAST_NAME_VALID = [
    ("simple",         "Sibakhi"),
    ("hyphen_middle",  "Al-Hassan"),
    ("apostrophe_mid", "O'Neill"),
    ("internal_spaces","Van Der Berg"),
    ("arabic_unicode", "سيباخي"),
    ("accented_latin", "Müller"),
]

LAST_NAME_INVALID = [
    ("empty",              "",               "ln_required"),
    ("whitespace_only",    "   ",            "ln_required"),
    ("one_char",           "L",              "ln_min"),
    ("digits",             "Smith99",        "ln_chars"),
    ("at_symbol",          "Hassan@1",       "ln_chars"),
    ("underscore",         "Test_Last",      "ln_chars"),
    ("emoji",              "Smith🎉",        "ln_chars"),
    ("xss_img_tag",        "<img onerror=1>","ln_chars"),
    ("consec_hyphens",     "Al--Hassan",     "ln_consecutive"),
    ("consec_apostrophes", "O''Neill",       "ln_consecutive"),
    ("consec_hyphen_ap",   "Al-'Hassan",     "ln_consecutive"),
    ("consec_ap_hyphen",   "Al'-Hassan",     "ln_consecutive"),
    ("leading_hyphen",     "-Hassan",        "ln_start_end"),
    ("leading_apostrophe", "'Hassan",        "ln_start_end"),
    ("trailing_hyphen",    "Hassan-",        "ln_start_end"),
    ("trailing_apostrophe","Hassan'",        "ln_start_end"),
]

# ---------------------------------------------------------------------------
# Phone Number
# ---------------------------------------------------------------------------

PHONE_VALID = [
    ("digits_10",      "6035551234"),
    ("empty_optional", ""),
]

PHONE_INVALID = [
    ("five_digits",  "12345",     "ph_min_digits"),
    ("nine_digits",  "603555123", "ph_min_digits"),
]

PHONE_ALPHA = "abcdefghij"

# ---------------------------------------------------------------------------
# Add User — Email (R-AU-EM-1 to R-AU-EM-4)
# ---------------------------------------------------------------------------

ADD_USER_EMAIL_INVALID = [
    ("empty",          "",                "au_email_required"),
    ("no_domain",      "notanemail",      "au_email_format"),
    ("missing_domain", "user@",           "au_email_format"),
    ("missing_local",  "@dentivoice.com", "au_email_format"),
]

# RFC 5321 boundary: 254 chars total (64 local + @ + 189 domain)
ADD_USER_EMAIL_MAX_VALID   = "a" * 64 + "@" + "b" * 185 + ".com"  # 254 chars
ADD_USER_EMAIL_MAX_INVALID = "a" * 64 + "@" + "b" * 186 + ".com"  # 255 chars

ADD_USER_EMAIL_VALID     = "newuser+autotest@dentivoice.com"
ADD_USER_DUPLICATE_EMAIL = "osama+stg+opendental@dentalbase.ai"

# ---------------------------------------------------------------------------
# Add User — Username (R-UN-1 to R-UN-6)
# ---------------------------------------------------------------------------

USERNAME_VALID = [
    ("simple_lower",     "reemtest"),
    ("with_numbers",     "reem123"),
    ("with_hyphen",      "reem-test"),
    ("with_underscore",  "reem_test"),
    ("with_dot",         "reem.test"),
    ("exact_min_3",      "abc"),
    ("exact_max_30",     "a" * 30),
]

USERNAME_INVALID = [
    # Required (R-UN-1)
    ("empty",              "",           "un_required"),

    # Min length (R-UN-2)
    ("one_char",           "a",          "un_min"),
    ("two_chars",          "ab",         "un_min"),

    # Max length (R-UN-2)
    ("over_max_31",        "a" * 31,     "un_max"),

    # Disallowed chars (R-UN-3)
    ("uppercase",          "Reem",       "un_chars"),
    ("space",              "reem test",  "un_chars"),
    ("at_symbol",          "reem@test",  "un_chars"),
    ("exclamation",        "reem!",      "un_chars"),

    # Consecutive specials (R-UN-4)
    ("consec_dots",        "reem..test", "un_consecutive"),
    ("consec_hyphens",     "reem--test", "un_consecutive"),
    ("consec_underscores", "reem__test", "un_consecutive"),
    ("consec_dot_hyphen",  "reem.-test", "un_consecutive"),

    # Must start/end with letter or number (R-UN-5)
    ("leading_underscore", "_reem",      "un_start_end"),
    ("leading_hyphen",     "-reem",      "un_start_end"),
    ("leading_dot",        ".reem",      "un_start_end"),
    ("trailing_underscore","reem_",      "un_start_end"),
    ("trailing_hyphen",    "reem-",      "un_start_end"),
    ("trailing_dot",       "reem.",      "un_start_end"),
]
