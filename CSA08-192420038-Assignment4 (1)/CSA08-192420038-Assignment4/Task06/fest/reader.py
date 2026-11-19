"""Reading one department file."""


def read_lines(path):
    """Yield (line number, text) for every non-blank line, one line at a time (the file is never loaded whole).
    May raise FileNotFoundError, PermissionError, IsADirectoryError or UnicodeDecodeError - the caller decides."""
    with open(path, encoding="utf-8") as f:
        for number, line in enumerate(f, start=1):
            if line.strip():
                yield number, line.rstrip("\r\n")
