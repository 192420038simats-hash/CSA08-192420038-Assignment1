"""A4.1 - a scripted pdb session: break inside f_to_c, look at the variables, step, quit."""
import subprocess, sys
commands = "b buggy_cleaning.py:10\nc\np f\np c\np f - 32 * 5 / 9\np (f - 32) * 5 / 9\nn\nq\n"
r = subprocess.run([sys.executable, "-m", "pdb", "buggy_cleaning.py"], input=commands, capture_output=True, text=True)
print("commands typed into pdb:  b buggy_cleaning.py:10 | c | p f | p c | p f - 32 * 5 / 9 | p (f - 32) * 5 / 9 | n | q\n")
print("\n".join(l.replace(__import__("os").getcwd() + "/", "") for l in (r.stdout + r.stderr).splitlines() if l.strip()))
