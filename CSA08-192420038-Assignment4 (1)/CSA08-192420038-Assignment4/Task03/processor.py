"""Task 3 - the attendance processor with the complete try statement and raise ... from ...

InvalidRecord       : one damaged LINE   - raised in parse_line(), handled in process_file() (processing continues)
AttendanceFileError : the whole FILE can't be processed - raised in process_file() from the original OSError /
                      UnicodeDecodeError (the cause is kept in __cause__), handled by the caller."""
from datetime import date


class InvalidRecord(Exception):
    """A line of an attendance file is damaged."""


class AttendanceFileError(Exception):
    """A whole attendance file cannot be read."""


def parse_line(line):
    parts = line.strip().split(",")
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    register, day, status = parts
    try:
        date.fromisoformat(day)
    except ValueError as e:
        raise InvalidRecord(f"invalid date '{day}'") from e          # keep the original ValueError as the cause
    if status not in ("P", "A"):
        raise InvalidRecord(f"invalid status '{status}'")
    return register, day, status


def process_file(path):
    """Return (present, absent, errors). Raises AttendanceFileError if the file as a whole cannot be read."""
    present = absent = 0
    errors = []
    f = None
    try:
        f = open(path, encoding="utf-8")
        for number, line in enumerate(f, start=1):
            try:
                _, _, status = parse_line(line)
            except InvalidRecord as e:                               # damaged line: log it and carry on
                errors.append((number, str(e)))
            else:                                                    # runs only when parse_line() succeeded
                if status == "P":
                    present += 1
                else:
                    absent += 1
    except FileNotFoundError as e:
        raise AttendanceFileError(f"file '{path}' does not exist") from e
    except PermissionError as e:
        raise AttendanceFileError(f"no permission to read '{path}'") from e
    except IsADirectoryError as e:
        raise AttendanceFileError(f"'{path}' is a folder, not a file") from e
    except UnicodeDecodeError as e:
        raise AttendanceFileError(f"'{path}' is not UTF-8 text (byte {e.start})") from e
    else:
        if present + absent + len(errors) == 0:
            errors.append((0, "file is empty"))                      # not an exception, but it must be reported
    finally:
        if f is not None:
            f.close()                                                # runs on success AND on every failure
    return present, absent, errors
