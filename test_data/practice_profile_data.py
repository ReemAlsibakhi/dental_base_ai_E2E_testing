"""
test_data/practice_profile_data.py
Single source of truth for Practice Profile & Hours test data.

Error messages based on requirements (PP·R1 to PP·R17).
Confirmed from live site where noted.
"""

# ===================================================================
# ERROR MESSAGES
# ===================================================================

PP_ERR = {
    # Legal Name (PP·R1)
    "ln_required":    "Legal name is required",
    "ln_min":         "Legal name must be at least 2 characters",
    "ln_max":         "Legal name must be under 150 characters",
    "ln_chars":       "Legal name may only contain letters, numbers, spaces, and",
    "ln_consecutive": "Legal name must not contain consecutive special characters",
    "ln_start_end":   "Legal name must start with a letter or number and",

    # DBA Name (PP·R2)
    "dba_required":    "DBA / Trade Name is required",
    "dba_min":         "DBA / Trade Name must be at least 2 characters",
    "dba_max":         "DBA / Trade Name must be under 150 characters",
    "dba_chars":       "DBA / Trade Name may only contain letters, numbers, spaces, and",
    "dba_consecutive": "DBA / Trade Name must not contain consecutive special characters",
    "dba_start_end":   "DBA / Trade Name must start with a letter or number and end with",

    # Phone (PP·R4/R5)
    "phone_required": "phone is required",
    "phone_min":      "Phone must be at least 10 digits",

    # Email (PP·R6)
    "email_format":   "Please enter a valid email address",

    # Website (PP·R7)
    "website_scheme": "Website must start with http:// or https://",
    "website_max":    "Website URL cannot exceed 2048 characters",

    # Street (PP·R8)
    "street_required": "Street address is required",
    "street_min":      "Street address must be at least 5 characters",
    "street_max":      "Street address cannot exceed 200 characters",

    # City (PP·R9)
    "city_required": "City is required",
    "city_min":      "City must be at least 2 characters",
    "city_max":      "City cannot exceed 100 characters",

    # State (PP·R10)
    "state_required": "State is required",

    # ZIP (PP·R11)
    "zip_required": "ZIP code is required",
    "zip_format":   "ZIP code must be in format 12345 or 12345-6789",

    # Timezone (PP·R12)
    "timezone_required": "Timezone is required",

    # Description (PP·R13)
    "desc_max": "Description cannot exceed 500 characters",
}

# ===================================================================
# LEGAL NAME — valid + invalid
# ===================================================================

LEGAL_NAME_VALID = [
    ("simple",          "DentiVoice Clinic LLC"),
    ("ampersand",       "Smith & Sons Dental"),
    ("period_apostrophe","Dr. Hassan's Clinic"),
    ("comma",           "ABC-Family Dental, Inc."),
    ("min_2",           "AB"),
    ("max_150",         "A" * 150),
]

LEGAL_NAME_INVALID = [
    # Required (R1a)
    ("empty",              "",            "ln_required"),
    ("whitespace",         "     ",       "ln_required"),
    # Min (R1b)
    ("one_char",           "A",           "ln_min"),
    # Max (R1c)
    ("over_max",           "A" * 151,     "ln_max"),
    # Chars (R1d)
    ("trademark",          "Clinic™",     "ln_chars"),
    ("emoji",              "Test😊Clinic", "ln_chars"),
    ("xss",                "<script>alert(1)</script>", "ln_chars"),
    # Consecutive (R1f)
    ("consec_hyphen",      "Clinic--Care",  "ln_consecutive"),
    ("consec_ampersand",   "Smith&&Jones",  "ln_consecutive"),
    ("consec_period_comma","Care.,Dental",  "ln_consecutive"),
    ("consec_period",      "Dr..Hassan",    "ln_consecutive"),
    ("consec_ap_hyphen",   "A'-B",          "ln_consecutive"),
    # Start/End (R1g)
    ("leading_hyphen",     "-Clinic Care",  "ln_start_end"),
    ("trailing_hyphen",    "Clinic Care-",  "ln_start_end"),
    ("leading_period",     ".DentiVoice",   "ln_start_end"),
    ("trailing_period",    "DentiVoice.",   "ln_start_end"),
    ("leading_apostrophe", "'Care Dental",  "ln_start_end"),
    ("trailing_comma",     "Smith Jones,",  "ln_start_end"),
]

# ===================================================================
# DBA NAME — identical rules to Legal Name
# ===================================================================

DBA_NAME_VALID = [
    ("simple",     "Smile Dental Center"),
    ("ampersand",  "Smile & Care Dental"),
    ("comma",      "Care Dental, LLC"),
    ("min_2",      "AB"),
    ("max_150",    "B" * 150),
]

DBA_NAME_INVALID = [
    ("empty",              "",             "dba_required"),
    ("whitespace",         "     ",        "dba_required"),
    ("one_char",           "A",            "dba_min"),
    ("over_max",           "B" * 151,      "dba_max"),
    ("emoji",              "Clinic🦷",     "dba_chars"),
    ("xss",                "<img onerror=1>", "dba_chars"),
    ("consec_hyphen",      "Smile--Care",  "dba_consecutive"),
    ("consec_ampersand",   "Smith&&Jones", "dba_consecutive"),
    ("consec_period_comma","Care.,Dental", "dba_consecutive"),
    ("leading_hyphen",     "-Smile Dental","dba_start_end"),
    ("trailing_comma",     "Smile Dental,","dba_start_end"),
]

# ===================================================================
# PHONE
# ===================================================================

PHONE_VALID = [
    ("ten_digits", "6035551234"),
]

PHONE_INVALID = [
    ("nine_digits", "603555123", "phone_min"),
    ("empty",       "",          "phone_required"),
]

# ===================================================================
# EMAIL
# ===================================================================

EMAIL_VALID   = "admin@clinic.com"
EMAIL_INVALID = [
    ("no_domain",   "notanemail",    "email_format"),
    ("missing_at",  "userdomain.com","email_format"),
    ("missing_domain", "user@",      "email_format"),
]
EMAIL_MAX_VALID   = "a" * 64 + "@" + "b" * 185 + ".com"  # 254 chars
EMAIL_MAX_INVALID = "a" * 64 + "@" + "b" * 186 + ".com"  # 255 chars

# ===================================================================
# WEBSITE
# ===================================================================

WEBSITE_VALID   = "https://clinic.com"
WEBSITE_INVALID = [
    ("no_scheme",     "clinic.com",           "website_scheme"),
    ("ftp_scheme",    "ftp://clinic.com",      "website_scheme"),
    ("javascript",    "javascript:alert(1)",   "website_scheme"),
]
WEBSITE_MAX_VALID   = "https://" + "a" * 2039 + ".com"  # 2048 chars
WEBSITE_MAX_INVALID = "https://" + "a" * 2040 + ".com"  # 2049 chars

# ===================================================================
# ADDRESS
# ===================================================================

STREET_VALID        = "123 Main Street"
STREET_MIN_VALID    = "123 A"       # 5 chars
STREET_MIN_INVALID  = "123 "        # 4 chars
STREET_MAX_VALID    = "A" * 200
STREET_MAX_INVALID  = "A" * 201

CITY_VALID          = "Winston-Salem"
CITY_MIN_VALID      = "AB"          # 2 chars
CITY_MIN_INVALID    = "A"           # 1 char
CITY_MAX_VALID      = "A" * 100
CITY_MAX_INVALID    = "A" * 101

ZIP_VALID_5         = "12345"
ZIP_VALID_PLUS4     = "12345-6789"
ZIP_INVALID_4       = "1234"
ZIP_INVALID_PLUS4   = "12345-678"   # ZIP+4 incomplete
ZIP_INVALID_ALPHA   = "ABCDE"

# ===================================================================
# DESCRIPTION (PP·R13) — max 500
# ===================================================================

DESC_MAX_VALID   = "A" * 500
DESC_MAX_INVALID = "A" * 501
