"""Re-creates an interactive session transcript with the >>> prompts and the commands echoed."""
import code, io, contextlib
cmds = [l.rstrip("\n") for l in open("session_commands.txt")]
con = code.InteractiveConsole()
out = []
for c in cmds:
    out.append(">>> " + c)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        con.push(c)
    if buf.getvalue(): out.append(buf.getvalue().rstrip("\n"))
text = "\n".join(o for o in out if o is not None)
open("interactive_session.txt", "w").write(text + "\n")
print(text)
