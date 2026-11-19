"""(c) reports."""


def write_percentage_report(pcts, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("register,present,total,percent\n")
        for r, (p, t, pc) in pcts.items():
            f.write(f"{r},{p},{t},{pc}\n")


def write_error_log(errors, path):
    with open(path, "w", encoding="utf-8") as f:
        for name, number, reason in errors:
            f.write(f"{name}:{number}: {reason}\n")
