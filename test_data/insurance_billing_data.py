"""
test_data/insurance_billing_data.py
Test data for Insurance & Billing module.
"""

# Coverage
INSURANCE_NAME_VALID   = "Delta Dental PPO"
INSURANCE_NAME_MIN     = "AB"       # 2 chars — minimum
INSURANCE_NAME_INVALID = "D"        # 1 char — below minimum

COVERAGE_PCT_MIN       = "0"
COVERAGE_PCT_MAX       = "100"
COVERAGE_PCT_INVALID   = "101"

NOTES_MAX_VALID        = "A" * 500
NOTES_MAX_INVALID      = "A" * 501

# Membership Plans
PLAN_NAME_VALID        = "Individual Adult Plan"
DISCOUNT_PCT_MIN       = "0"
DISCOUNT_PCT_MAX       = "100"
DISCOUNT_PCT_INVALID   = "101"
ANNUAL_FEE_VALID       = "299"
ANNUAL_FEE_INVALID     = "-1"

# Finance
PROVIDER_NAME_VALID    = "CareCredit"
APR_VALID              = "26.99"
APR_MIN                = "0"
APR_INVALID            = "-1"

# Service Pricing
SERVICE_NAME_VALID     = "Teeth Cleaning"
SERVICE_NAME_MAX       = "A" * 100
CDT_CODE_VALID         = "D0120"
PRICE_VALID            = "150"
PRICE_MIN              = "0"
PRICE_INVALID          = "-1"

# Active Offers
OFFER_NAME_VALID       = "Summer Special"
PROMO_PRICE_VALID      = "50"
ORIGINAL_PRICE_VALID   = "100"
EXPIRY_DAYS_VALID      = "30"
EXPIRY_DAYS_INVALID    = "0"

# Pricing Policy
PRICING_OPTIONS = [
    "Always Provide Exact Pricing",
    "Require Exam First",
    "Provide Range Only",
    "Do Not Discuss Pricing",
]

AI_SCRIPT_MAX_VALID    = "A" * 2000
AI_SCRIPT_MAX_INVALID  = "A" * 2001
