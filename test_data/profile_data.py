"""
test_data/profile_data.py

Centralised test data for the Profile module.
Keeping data here (not inline in tests) makes mass-updates trivial.
"""

# ---------------------------------------------------------------------------
# Shared error messages — single source of truth
# ---------------------------------------------------------------------------

ERR = {
    # First Name
    "fn_required": "First name is required",
    "fn_min": "First name must be at least 2 characters",
    "fn_max": "First name cannot exceed 50 characters",
    "fn_chars": "First name can only contain letters, spaces, hyphens, and apostrophes",
    "fn_consecutive": "First name cannot contain consecutive special characters",
    "fn_leading": "First name cannot start with a special character",
    "fn_trailing": "First name cannot end with a special character",
    # Last Name
    "ln_required": "Last name is required",
    "ln_min": "Last name must be at least 2 characters",
    "ln_max": "Last name cannot exceed 50 characters",
    "ln_chars": "Last name can only contain letters, spaces, hyphens, and apostrophes",
    "ln_consecutive": "Last name cannot contain consecutive special characters",
    "ln_leading": "Last name cannot start with a special character",
    "ln_trailing": "Last name cannot end with a special character",
    # Phone
    "ph_min_digits": "Phone number must be at least 10 digits",
    # Add User — Email
    "au_email_required": "Email is required",
    "au_email_format": "Please enter a valid email address",
    "au_email_duplicate": "This user is already a member",
}

# ---------------------------------------------------------------------------
# First Name
# ---------------------------------------------------------------------------

FIRST_NAME_VALID = [
    ("simple", "Reem"),
    ("hyphen_middle", "Mary-Jane"),
    ("apostrophe_middle", "O'Brien"),
    ("internal_space", "Anne Marie"),
    ("arabic_unicode", "رنا"),
    ("accented_latin", "José"),
    ("mixed_scripts", "Reemرنا"),
    ("exact_min_2", "Jo"),
    ("exact_max_50", "A" * 50),
]

FIRST_NAME_INVALID = [
    # (test_id, value, expected_error_key)
    ("empty", "", "fn_required"),
    ("whitespace_only", "     ", "fn_required"),
    ("one_char", "J", "fn_min"),
    ("over_max_51", "A" * 51, "fn_max"),
    ("digits", "Reem123", "fn_chars"),
    ("at_symbol", "John@Doe", "fn_chars"),
    ("underscore", "Test_Name", "fn_chars"),
    ("emoji", "Reem😊", "fn_chars"),
    ("script_tag", "<script>", "fn_chars"),
    ("consecutive_hyphens", "Mary--Jane", "fn_consecutive"),
    ("consecutive_apostrophes", "O''Brien", "fn_consecutive"),
    ("mixed_consecutive_hy_ap", "Mary-'Jane", "fn_consecutive"),
    ("mixed_consecutive_ap_hy", "Mary'-Jane", "fn_consecutive"),
    ("leading_hyphen", "-Reem", "fn_leading"),
    ("leading_apostrophe", "'Reem", "fn_leading"),
    ("trailing_hyphen", "Reem-", "fn_trailing"),
    ("trailing_apostrophe", "Reem'", "fn_trailing"),
]

# ---------------------------------------------------------------------------
# Last Name
# ---------------------------------------------------------------------------

LAST_NAME_VALID = [
    ("simple", "Sibakhi"),
    ("hyphen_middle", "Al-Hassan"),
    ("apostrophe_middle", "O'Neill"),
    ("internal_spaces", "Van Der Berg"),
    ("arabic_unicode", "سيباخي"),
    ("accented_latin", "Müller"),
    ("exact_min_2", "Li"),
    ("exact_max_50", "Abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwx"),
    ("single_hyphen_valid", "A-B"),
]

LAST_NAME_INVALID = [
    ("empty", "", "ln_required"),
    ("whitespace_only", "     ", "ln_required"),
    ("single_space", " ", "ln_required"),
    ("one_char", "L", "ln_min"),
    ("over_max_51", "Abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxy", "ln_max"),
    ("digits", "Smith99", "ln_chars"),
    ("at_symbol", "Hassan@1", "ln_chars"),
    ("underscore", "Test_Last", "ln_chars"),
    ("emoji", "Smith🎉", "ln_chars"),
    ("xss_img_tag", "<img onerror=1>", "ln_chars"),
    ("consecutive_hyphens", "Al--Hassan", "ln_consecutive"),
    ("consecutive_apostrophes", "O''Neill", "ln_consecutive"),
    ("mixed_consecutive_hy_ap", "Al-'Hassan", "ln_consecutive"),
    ("mixed_consecutive_ap_hy", "Al'-Hassan", "ln_consecutive"),
    ("leading_hyphen", "-Hassan", "ln_leading"),
    ("leading_apostrophe", "'Hassan", "ln_leading"),
    ("trailing_hyphen", "Hassan-", "ln_trailing"),
    ("trailing_apostrophe", "Hassan'", "ln_trailing"),
]

# ---------------------------------------------------------------------------
# Phone Number
# ---------------------------------------------------------------------------

PHONE_VALID = [
    ("formatted_us", "(603) 555-1234"),
    ("digits_10", "6035551234"),
    ("empty_optional", ""),
]

PHONE_INVALID = [
    ("five_digits", "12345", "ph_min_digits"),
    ("nine_digits", "603555123", "ph_min_digits"),
]

PHONE_ALPHA = "abcdefghij"  # Stripped silently per R-PH-3

# ---------------------------------------------------------------------------
# Add User — Email
# ---------------------------------------------------------------------------

ADD_USER_EMAIL_INVALID = [
    ("empty", "", "au_email_required"),
    ("no_domain", "notanemail", "au_email_format"),
    ("missing_domain", "user@", "au_email_format"),
    ("missing_local", "@dentivoice.com", "au_email_format"),
]

ADD_USER_EMAIL_VALID = "newuser+autotest@dentivoice.com"
ADD_USER_DUPLICATE_EMAIL = "osama+stg+opendental@dentalbase.ai"  # existing admin
