import pylage as pl
# demo/demo_data_feedback.py

from pylage.ENGINE.core.component import Component, component


def get_app() -> Component:
    # pl.State management for interactive demos
    progress = pl.State(45)
    toast_visible = pl.State(True)
    accordion_open = pl.State("section1")
    carousel_index = pl.State(0)

    def increase_progress():
        val = progress.value + 15
        progress.set(100 if val > 100 else val)

    def reset_progress():
        progress.set(0)

    def toggle_toast():
        toast_visible.set(not toast_visible.value)

    return component(
        "div",
        pl.style(padding="20px", gap="20px", display="flex", flex_direction="column"),
        pl.heading("📊 Data & Feedback Components Live Demo", level=1),
        # 1. pl.badge & pl.alert
        pl.card(
            pl.heading("1. pl.badge & pl.alert", level=3),
            pl.row(
                pl.badge("Active Status", variant="success"),
                pl.badge("Warning", variant="warning"),
                pl.badge("Error", variant="danger"),
                pl.style(gap="10px", margin_bottom="15px"),
            ),
            pl.alert(
                "Info pl.alert: System maintenance scheduled for tonight.",
                type="info",
            ),
            pl.alert("Success pl.alert: Operation completed successfully!", type="success"),
        ),
        # 2. pl.table
        pl.card(
            pl.heading("2. pl.table Component", level=3),
            pl.table(
                headers=["ID", "Name", "Role", "Status"],
                data=[
                    ["1", "Rahul Sharma", "Developer", "Active"],
                    ["2", "Priya Singh", "Designer", "Pending"],
                    ["3", "Amit Kumar", "Manager", "Active"],
                ],
            ),
        ),
        # 3. pl.toast
        pl.card(
            pl.heading("3. pl.toast Component", level=3),
            pl.button(
                "Toggle pl.toast View",
                on_click=toggle_toast,
            ),
            pl.toast(
                "New Notification: You received a message!",
                visible=toast_visible,
            ),
        ),
        # 4. Spinner, ProgressBar & Skeleton
        pl.card(
            pl.heading("4. Loading States (Spinner, ProgressBar, Skeleton)", level=3),
            pl.row(
                pl.text("Spinner Loading: "),
                pl.Spinner(size="medium"),
                pl.style(align_items="center", gap="10px"),
            ),
            pl.row(
                pl.button("Increase Progress", on_click=increase_progress),
                pl.button("Reset", on_click=reset_progress),
                pl.style(gap="10px", margin_top="10px", margin_bottom="10px"),
            ),
            pl.ProgressBar(value=progress, max=100),
            pl.heading("Skeleton Placeholder Loading:", level=4),
            pl.Skeleton(width="100%", height="20px"),
            pl.Skeleton(width="60%", height="20px"),
        ),
        # 5. Accordion
        pl.card(
            pl.heading("5. Accordion Component", level=3),
            pl.Accordion(
                items=[
                    {
                        "id": "section1",
                        "title": "Section 1: Details",
                        "content": "Content for section 1 is loaded here.",
                    },
                    {
                        "id": "section2",
                        "title": "Section 2: Additional Info",
                        "content": "Additional information for section 2.",
                    },
                ],
                active_id=accordion_open,
            ),
        ),
        # 6. Carousel
        pl.card(
            pl.heading("6. Carousel Component", level=3),
            pl.Carousel(
                items=[
                    "Slide 1: Welcome to PyLage Showcase",
                    "Slide 2: High Performance Python UI Framework",
                    "Slide 3: Reactive pl.State and Modern Component System",
                ],
                current_index=carousel_index,
            ),
        ),
    )
