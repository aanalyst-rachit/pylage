
import pylage as pl

name = pl.state("")
email = pl.state("")
status = pl.state("Ready")
rows = pl.state([])

def submit():
    n = str(name.value).strip()
    e = str(email.value).strip()
    if not n or not e:
        status.set("Please fill name and email")
        return
    rows.set([{"name": n, "email": e}] + list(rows.value))
    name.set("")
    email.set("")
    status.set("Saved")

app = pl.column(
    pl.heading("Complex Form"),
    pl.text(status),
    pl.input(value=name, placeholder="Name"),
    pl.input(value=email, placeholder="Email"),
    pl.button("Submit", on_click=submit),
    pl.text("Submitted:"),
)

if __name__ == "__main__":
    pl.run(app, title="PyLage Form", host="127.0.0.1", port=3101, serve=True)
