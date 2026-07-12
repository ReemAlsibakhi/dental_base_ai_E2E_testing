"""test_data/patient_outreach_data.py"""

PO_ERR = {
    "end_before_start": "End time must be after start time",
    "timing_zero":      "Timing must be at least 1",
    "min_days_zero":    "Must be at least 1",
    "msg_max":          "Message cannot exceed 500 characters",
}

# Card indices — Global tab
GLOBAL_CARD = {
    "master_switch":   0,
    "preferred_hours": 1,
}

# Card indices — Flows tab
FLOW_CARD = {
    "reminders":    0,
    "confirmation": 1,
}

# Toggle indices inside Master Switch panel
MASTER_TOGGLE       = 0  # "Enable all outreach"
REMINDERS_TOGGLE    = 1  # "Enable Appointment Reminders"
CONFIRMATION_TOGGLE = 2  # "Enable Appointment Confirmation"

# Message limits
MSG_MAX_VALID   = "A" * 500
MSG_MAX_INVALID = "A" * 501
