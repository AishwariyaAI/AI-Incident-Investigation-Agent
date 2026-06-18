VALID_TRANSITIONS = {
    "OPEN": ["ACK", "RESOLVED"],
    "ACK": ["RESOLVED"],
    "RESOLVED": ["CLOSED"],
    "CLOSED": []
}


def can_transition(current, new):
    return new in VALID_TRANSITIONS.get(current, [])