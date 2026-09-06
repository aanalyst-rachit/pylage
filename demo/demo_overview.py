import pylage as pl
"""Master Component & Pattern Manual Aggregator for PyLage and PyLage Layout."""


from demo import (
    demo_button,
    demo_card,
    demo_form,
    demo_grid,
    demo_input,
    demo_heading,
    demo_text,
    demo_row,
    demo_column,
    demo_media,
    demo_switch,
    demo_select,
    demo_modern_button,
    demo_nav_interaction,
    demo_data_feedback,
    demo_table,
    demo_accordion,
    demo_carousel,
    demo_dialog,
    demo_drawer,
    demo_tabs,
    demo_datepicker,
    demo_popover_tooltip,
    demo_pagination,
    demo_avatar_badge_divider,
    demo_audio_video_canvas,
    demo_slider_radio_checkbox,
    demo_menu_breadcrumbs_pagination,
    demo_patterns,
    demo_templates,
    demo_layout_primitives,
    demo_themes_tokens,
)


MANUAL_REGISTRY = {
    "Overview": None,
    "Buttons & Modern Actions": demo_modern_button.get_app,
    "Inputs & Form Fields": demo_input.get_app,
    "Sliders, Radios & Checkboxes": demo_slider_radio_checkbox.get_app,
    "Headings & Typography": demo_heading.get_app,
    "Cards & Surfaces": demo_card.get_app,
    "Layout Columns & Rows": demo_column.get_app,
    "CSS Grid Layouts": demo_grid.get_app,
    "Layout Primitives & AppShell": demo_layout_primitives.get_app,
    "Interactive Forms & Validation": demo_form.get_app,
    "Switches & Toggles": demo_switch.get_app,
    "Select Dropdowns": demo_select.get_app,
    "DatePickers": demo_datepicker.get_app,
    "Tables & Data Grids": demo_table.get_app,
    "Tabs & Segmented Controls": demo_tabs.get_app,
    "Accordions & Collapsibles": demo_accordion.get_app,
    "Carousels & Sliders": demo_carousel.get_app,
    "Dialogs & Modals": demo_dialog.get_app,
    "Drawers & Sidepanels": demo_drawer.get_app,
    "Popovers & Tooltips": demo_popover_tooltip.get_app,
    "Navigation & Menus": demo_menu_breadcrumbs_pagination.get_app,
    "Media, Canvas & Graphics": demo_audio_video_canvas.get_app,
    "Badges, Avatars & Dividers": demo_avatar_badge_divider.get_app,
    "Feedback, Progress & Toast": demo_data_feedback.get_app,
    "Layout Patterns (Hero, FAQ, Stats)": demo_patterns.get_app,
    "Application Templates": demo_templates.get_app,
    "Design Tokens & Themes": demo_themes_tokens.get_app,
}


def get_app() -> pl.column:
    active_section = pl.State("Overview")

    header = pl.row(
        pl.heading("⚡ PyLage UI Engine — Interactive Component Manual", level=2, style=pl.style(margin=0)),
        pl.badge("v1.0.0 Stable", variant="success"),
        style=pl.style(display="flex", justify_content="space-between", align_items="center", margin_bottom="1.5rem"),
    )

    overview_summary = pl.card(
        pl.heading("Welcome to the PyLage & PyLage Layout Manual", level=3),
        pl.text(
            "PyLage is a Python-first reactive UI framework (similar to Streamlit & Reflex) providing full "
            "declarative tree composition, two-way pl.State bindings, WebSocket delta patching, and enterprise design tokens."
        ),
        pl.row(
            pl.badge("38 UI Components", variant="primary"),
            pl.badge("15 Layout Patterns", variant="secondary"),
            pl.badge("7 Application Templates", variant="info"),
            pl.badge("100% Test Suite Pass", variant="success"),
            style=pl.style(gap="0.5rem", margin_top="1rem"),
        ),
        style=pl.style(padding="1.5rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem", margin_bottom="1.5rem"),
    )

    # -----------------------------------------------------------------
    # Content area — this is the piece that was missing.
    # It's the actual consumer of `active_section` pl.State: whenever the
    # pl.State changes, we swap its children to the selected manual's app.
    # -----------------------------------------------------------------
    content_area = pl.column(
        pl.card(
            pl.heading("👋 Pick a section above", level=4),
            pl.text("Click any button in the catalog below to preview that component or pattern live."),
            style=pl.style(padding="1.5rem", background="#ffffff", border="1px dashed #cbd5e1", border_radius="0.75rem"),
        ),
        style=pl.style(margin_top="1.5rem"),
    )

    def switch_section(name: str):
        def handler(e=None):
            active_section.set(name)

            factory = MANUAL_REGISTRY.get(name)

            if factory is None:
                # "Overview" selected — reset to the placeholder card.
                content_area.set_children(
                    pl.card(
                        pl.heading("👋 Pick a section above", level=4),
                        pl.text("Click any button in the catalog below to preview that component or pattern live."),
                        style=pl.style(padding="1.5rem", background="#ffffff", border="1px dashed #cbd5e1", border_radius="0.75rem"),
                    )
                )
                return

            # Build the selected manual's app fresh and mount it.
            content_area.set_children(factory())

        return handler

    # Component Catalog Grid
    catalog_items = []
    for section_name in MANUAL_REGISTRY.keys():
        if section_name == "Overview":
            continue
        catalog_items.append(
            pl.button(
                section_name,
                on_click=switch_section(section_name),
                style=pl.style(
                    padding="0.625rem 1rem",
                    text_align="left",
                    background="#f8fafc",
                    border="1px solid #e2e8f0",
                    border_radius="0.5rem",
                    cursor="pointer",
                    font_size="0.875rem",
                ),
            )
        )

    nav_grid = pl.card(
        pl.heading("📚 Component & Module Manual Catalog", level=4),
        pl.row(*catalog_items, style=pl.style(display="grid", grid_template_columns="repeat(auto-fill, minmax(240px, 1fr))", gap="0.75rem", margin_top="1rem")),
        style=pl.style(padding="1.5rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem"),
    )

    return pl.column(
        header,
        overview_summary,
        nav_grid,
        content_area,
        style=pl.style(padding="2rem", max_width="1100px", margin="0 auto"),
    )