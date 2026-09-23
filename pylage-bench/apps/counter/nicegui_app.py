from nicegui import ui

state = {"count": 0}

@ui.page("/")
def main():
    ui.label("Counter")
    label = ui.label("0")
    def increment():
        state["count"] += 1
        label.set_text(str(state["count"]))
    ui.button("Increment", on_click=increment)

ui.run(host="127.0.0.1", port=3003, show=False, reload=False)
