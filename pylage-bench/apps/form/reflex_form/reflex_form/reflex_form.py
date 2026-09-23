import reflex as rx


class State(rx.State):
    name: str = ""
    email: str = ""
    status: str = "Ready"
    rows: list[str] = []

    def set_name(self, value: str):
        self.name = value

    def set_email(self, value: str):
        self.email = value

    def submit(self):
        n = self.name.strip()
        e = self.email.strip()
        if not n or not e:
            self.status = "Please fill name and email"
            return
        self.rows = [f"{n} | {e}"] + self.rows
        self.name = ""
        self.email = ""
        self.status = "Saved"


def index() -> rx.Component:
    return rx.vstack(
        rx.heading("Complex Form"),
        rx.text(State.status),
        rx.input(placeholder="Name", value=State.name, on_change=State.set_name),
        rx.input(placeholder="Email", value=State.email, on_change=State.set_email),
        rx.button("Submit", on_click=State.submit),
        rx.text("Submitted:"),
        rx.foreach(State.rows, lambda r: rx.text(r)),
    )


app = rx.App()
app.add_page(index)
