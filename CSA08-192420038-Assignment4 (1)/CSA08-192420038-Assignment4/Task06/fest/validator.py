"""Validation of one registration line:  register,name,department,email,event1;event2;..."""


class InvalidRegistration(Exception):
    """A registration line breaks a rule; the message says which one."""


def valid_email(email):
    """E-mail check with string methods only (no regular expressions)."""
    if not email or " " in email or email.count("@") != 1:
        return False
    local, domain = email.split("@")
    if not local or not domain:
        return False
    if ".." in email or domain.startswith(".") or domain.endswith(".") or "." not in domain:
        return False
    tld = domain.rsplit(".", 1)[1]
    return len(tld) >= 2 and tld.isalpha()


def clean_events(text):
    """'Quiz;;drama ' -> ['Drama', 'Quiz'] : split on ';', trim, drop empty parts, Title Case, no repeats, sorted."""
    return sorted({e.strip().title() for e in text.split(";") if e.strip()})


def validate_line(line):
    """Return a dict for a valid line; raise InvalidRegistration(reason) otherwise."""
    parts = [p.strip() for p in line.strip().split(",")]
    if len(parts) != 5:
        raise InvalidRegistration(f"damaged line: expected 5 fields, found {len(parts)}")
    register, name, department, email, events_text = parts
    if not (register.isdigit() and len(register) == 9):
        raise InvalidRegistration(f"invalid register number '{register}'")
    if not name:
        raise InvalidRegistration("name is empty")
    if not department:
        raise InvalidRegistration("department is empty")
    if not valid_email(email):
        raise InvalidRegistration(f"invalid e-mail '{email}'")
    events = clean_events(events_text)
    if not events:
        raise InvalidRegistration("no event chosen")
    return {"register": register, "name": name, "department": department.upper(), "email": email.lower(), "events": events}
