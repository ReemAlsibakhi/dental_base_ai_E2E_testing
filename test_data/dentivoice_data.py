"""test_data/dentivoice_data.py — DentiVoice™ test data."""

DV_ERR = {
    "name_required":   "Assistant name is required",
    "name_min":        "Assistant name must be at least 2 characters",
    "name_max":        "Name must be 30 characters or less",
    "name_pronounce":  "Name is hard to pronounce",
    "name_chars":      "Name can only contain letters and spaces",
    "personality":     "Please select a personality type",
    "greeting_max":    "Greeting must be 500 characters or less",
    "after_hours_max": "After-hours greeting must be 500 characters or less",
    "lang_min":        "At least one language is required",
    "instructions_max":"Instructions must be 2000 characters or less",
    "first_aid_req":   "First-aid advice content is required when enabled",
    "first_aid_max":   "First-aid advice must be 3000 characters or less",
    "triage_max":      "Triage script must be 5000 characters or less",
    "oncall_req":      "On-call contact is required",
    "oncall_format":   "Please enter a valid phone number",
    "handling_min":    "Select at least one handling method",
    "transfer_name":   "Name is required",
    "transfer_phone":  "Phone number is required",
    "email_req":       "Email address is required when daily report is enabled",
    "email_format":    "Please enter a valid email address",
}

# Valid test data
VALID_AI_NAME     = "Sofia"
VALID_PHONE       = "555-123-4567"
VALID_EMAIL       = "test@clinic.com"

# Boundary values
AI_NAME_MIN_VALID  = "AI"           # 2 chars
AI_NAME_MIN_BELOW  = "X"            # 1 char — DEF-DV-03
AI_NAME_MAX_VALID  = "A" * 30       # 30 chars
AI_NAME_MAX_PLUS1  = "A" * 31       # 31 chars

GREETING_MAX_VALID   = "A" * 500
GREETING_MAX_INVALID = "A" * 501
INSTRUCTIONS_MAX_VALID   = "A" * 2000
INSTRUCTIONS_MAX_INVALID = "A" * 2001
FIRST_AID_MAX_VALID   = "A" * 3000
FIRST_AID_MAX_INVALID = "A" * 3001
TRIAGE_MAX_VALID   = "A" * 5000
TRIAGE_MAX_INVALID = "A" * 5001
