"""
test_data/scheduling_rules_data.py
Single source of truth for Scheduling Rules test data.

Error messages based on live DOM (confirmed from test cases file).
"""

SR_ERR = {
    # Lead Time (SR·R1)
    "lt_min":    "Minimum lead time must be at least 1",

    # Advance Booking (SR·R2)
    "ab_min":    "Advance booking must be at least 1",

    # Cancellation Policy (SR·R5)
    "cp_min":    "Cancellation notice must be at least 1",

    # No-Show Policy (SR·R6)
    "ns_min":    "No-show window must be at least 1",
}

# Card indices (confirmed from live DOM)
CARD = {
    "lead_time":          0,
    "advance_booking":    1,
    "cancellation":       2,
    "no_show":            3,
    "override_pms":       4,
    "business_hours":     5,   # Manual only
    "holiday":            6,   # Manual only
    "additional_notes":   7,
}

# Valid values
LEAD_TIME_VALID    = "60"
ADVANCE_BOOKING_VALID = "90"
CANCELLATION_VALID = "24"
NO_SHOW_VALID      = "30"

# Boundary values
LEAD_TIME_MIN_VALID    = "1"
CANCELLATION_MAX_VALID = "720"
CANCELLATION_MAX_PLUS1 = "721"   # DEF-SR-03: saves without error
NO_SHOW_MAX_VALID      = "720"
NO_SHOW_MAX_PLUS1      = "721"   # DEF-SR-04: saves without error

# Additional Notes
NOTES_MAX_VALID   = "A" * 1000
NOTES_MAX_INVALID = "A" * 1001
