"""Task 4.3 - repaired library program: append mode, newline after every title, with statements, error log."""
import traceback
from datetime import datetime
from pathlib import Path

RETURNS_LOG = "returns.log"
ERROR_LOG = "errors.log"


def log_error(day_file, exc):
    """Append a time-stamped message AND the traceback to the error log (appended, never overwritten)."""
    with open(ERROR_LOG, "a", encoding="utf-8") as err:
        err.write(f"{datetime.now():%Y-%m-%d %H:%M:%S}  {day_file}: {type(exc).__name__}: {exc}\n")
        err.write("".join(traceback.format_exception(exc)))


def save_returns(day, books):
    """Append one line 'day,title' per book. The file is closed even if write() fails."""
    with open(RETURNS_LOG, "a", encoding="utf-8") as log:        # "a": earlier days are kept
        for b in books:
            log.write(f"{day},{b}\n")                            # newline after every title


def process(day_file):
    day = Path(day_file).stem
    try:
        with open(day_file, encoding="utf-8") as f:
            books = [line.strip() for line in f if line.strip()]  # no empty titles from the final newline
        save_returns(day, books)
    except FileNotFoundError as e:
        log_error(day_file, e)
        return False
    except (PermissionError, UnicodeDecodeError, TypeError) as e:
        log_error(day_file, e)
        return False
    except Exception as e:                                       # anything unexpected: record it, then do NOT hide it
        log_error(day_file, e)
        raise
    return True
