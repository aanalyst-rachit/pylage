
from nicegui import ui

state = {"status": "Ready", "rows": []}

@ui.page("/")
def main():
    ui.label("Complex Form")
    status = ui.label(state["status"])
    name = ui.input(label="Name")
    email = ui.input(label="Email")
    box = ui.column()

    def render():
        box.clear()
        with box:
            ui.label("Submitted:")
            for r in state["rows"]:
                ui.label(f'{r["name"]} | {r["email"]}')

    def submit():
        n = (name.value or "").strip()
        e = (email.value or "").strip()
        if not n or not e:
            state["status"] = "Please fill name and email"
            status.set_text(state["status"])
            return
        state["rows"] = [{"name": n, "email": e}] + state["rows"]
        name.value = ""
        email.value = ""
        state["status"] = "Saved"
        status.set_text(state["status"])
        render()

    ui.button("Submit", on_click=submit)
    render()

ui.run(host="127.0.0.1", port=3103, show=False, reload=False)
