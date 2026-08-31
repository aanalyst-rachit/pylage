from pylage import (
    run,
    Column,
    Row,
    Card,
    Divider,
    Badge,
    Avatar,
    Accordion,
    Carousel,
    Grid,
    Image,
    Video,
    Audio,
    Icon,
    Canvas,
    Heading,
    Text,
    Button,
    Input,
    Form,
    Table,
    Dialog,
    Navigation,
    Tabs,
    Checkbox,
    RadioGroup,
    Switch,
    Select,
    Slider,
    DatePicker,
    Alert,
    Toast,
    Spinner,
    ProgressBar,
    Skeleton,
    Breadcrumbs,
    Pagination,
    Menu,
    Drawer,
    Tooltip,
    Popover,
    Style,
)


# ============================================================
# GLOBAL STYLES
# ============================================================

page_style = Style(
    background_color="#f5f7fb",
    color="#172033",
    font_family="Arial, sans-serif",
    padding="32px",
)

section_style = Style(
    background_color="#ffffff",
    padding="24px",
    margin_bottom="24px",
    border_radius="14px",
    border="1px solid #e5e7eb",
    box_shadow="0 4px 16px rgba(0,0,0,0.05)",
)

hero_style = Style(
    background_color="#172033",
    color="#ffffff",
    padding="32px",
    border_radius="16px",
    margin_bottom="24px",
)

row_style = Style(
    display="flex",
    gap="16px",
    flex_wrap="wrap",
    margin_bottom="16px",
)

small_card_style = Style(
    background_color="#f8fafc",
    padding="18px",
    border_radius="10px",
    border="1px solid #e2e8f0",
)

button_style = Style(
    background_color="#2563eb",
    color="#ffffff",
    padding="10px 18px",
    border_radius="8px",
    cursor="pointer",
)

secondary_button_style = Style(
    background_color="#475569",
    color="#ffffff",
    padding="10px 18px",
    border_radius="8px",
    cursor="pointer",
)

badge_style = Style(
    background_color="#e8f7ee",
    color="#137333",
    padding="6px 10px",
    border_radius="999px",
)

avatar_style = Style(
    background_color="#2563eb",
    color="#ffffff",
    padding="14px",
    border_radius="50%",
)

input_style = Style(
    padding="10px",
    border="1px solid #cbd5e1",
    border_radius="8px",
    width="240px",
)

demo_image_style = Style(
    width="180px",
    height="100px",
    border_radius="10px",
)

progress_style = Style(
    width="100%",
)


# ============================================================
# APPLICATION
# ============================================================

app = Column(

    # ========================================================
    # HERO
    # ========================================================

    Column(
        Heading("PyLage Component Showcase"),

        Text(
            "A complete visual demonstration of the currently "
            "registered PyLage components and their supported props."
        ),

        Text(
            "Everything below is generated using Python-native "
            "PyLage components."
        ),

        Row(
            Button(
                "Primary Button",
                value="primary",
                title="Primary action",
                style=button_style,
            ),

            Button(
                "Disabled Button",
                value="disabled",
                disabled=True,
                title="Disabled action",
                style=secondary_button_style,
            ),
        ),

        style=hero_style,
    ),


    # ========================================================
    # BASIC CONTENT COMPONENTS
    # ========================================================

    Card(
        Heading("1. Basic Content Components"),

        Text(
            "Text component — demonstrates the text prop."
        ),

        Row(
            Badge(
                "Badge",
                title="Badge title",
                class_name="demo-badge",
                style=badge_style,
            ),

            Avatar(
                "RK",
                title="Avatar title",
                class_name="demo-avatar",
                style=avatar_style,
            ),

            Icon(
                name="★",
                title="Icon title",
                class_name="demo-icon",
                style=Style(
                    font_size="28px",
                    color="#f59e0b",
                ),
            ),
        ),

        Divider(),

        Text(
            "Heading uses the text prop and renders as an h1."
        ),

        style=section_style,
    ),


    # ========================================================
    # LAYOUT
    # ========================================================

    Card(
        Heading("2. Layout Components"),

        Text(
            "Column, Row and Grid are used to structure UI."
        ),

        Row(
            Card(
                Text("Row item 1"),
                title="First row item",
                class_name="row-card",
                style=small_card_style,
            ),

            Card(
                Text("Row item 2"),
                title="Second row item",
                class_name="row-card",
                style=small_card_style,
            ),

            style=row_style,
        ),

        Grid(
            Card(
                Text("Grid item A"),
                style=small_card_style,
            ),

            Card(
                Text("Grid item B"),
                style=small_card_style,
            ),

            Card(
                Text("Grid item C"),
                style=small_card_style,
            ),

            style=Style(
                display="grid",
                grid_template_columns="repeat(3, 1fr)",
                gap="16px",
            ),
        ),

        style=section_style,
    ),


    # ========================================================
    # CARD / ACCORDION / CAROUSEL
    # ========================================================

    Card(
        Heading("3. Containers & Interactive Structures"),

        Accordion(
            Heading("Accordion Example"),
            Text(
                "Accordion currently accepts class_name and title "
                "through the registry contract."
            ),
            class_name="demo-accordion",
            title="Accordion title",
            style=small_card_style,
        ),

        Divider(),

        Carousel(
            Card(
                Text("Carousel item 1"),
                style=small_card_style,
            ),
            Card(
                Text("Carousel item 2"),
                style=small_card_style,
            ),
            Card(
                Text("Carousel item 3"),
                style=small_card_style,
            ),
            class_name="demo-carousel",
            title="Carousel title",
            style=Style(
                display="flex",
                gap="12px",
                flex_wrap="wrap",
            ),
        ),

        style=section_style,
    ),


    # ========================================================
    # BUTTON
    # ========================================================

    Card(
        Heading("4. Button"),

        Text(
            "Button props: text, class_name, value, disabled and title."
        ),

        Row(
            Button(
                "Normal",
                class_name="normal-button",
                value="normal",
                disabled=False,
                title="Normal button",
                style=button_style,
            ),

            Button(
                "Disabled",
                class_name="disabled-button",
                value="disabled",
                disabled=True,
                title="Disabled button",
                style=secondary_button_style,
            ),
        ),

        style=section_style,
    ),


    # ========================================================
    # FORM
    # ========================================================

    Card(
        Heading("5. Form Components"),

        Form(
            Text("Form container"),

            Input(
                "Example value",
                title="Input title",
                disabled=False,
                style=input_style,
            ),

            Divider(),

            Checkbox(
                checked=True,
                title="Checkbox title",
            ),

            Text("Checkbox: checked=True"),

            Switch(
                checked=True,
                title="Switch title",
            ),

            Text("Switch: checked=True"),

            Select(
                Text("Option One"),
                Text("Option Two"),
                value="Option One",
                title="Select title",
                style=input_style,
            ),

            Text(
                "Select: value='Option One'"
            ),

            Slider(
                value=50,
                min=0,
                max=100,
                step=10,
                title="Slider title",
            ),

            Text(
                "Slider: value=50, min=0, max=100, step=10"
            ),

            DatePicker(
                value="2026-08-31",
                min="2026-01-01",
                max="2026-12-31",
                title="Date picker title",
                style=input_style,
            ),

            Text(
                "DatePicker: value, min and max"
            ),

            style=Style(
                display="flex",
                flex_direction="column",
                gap="12px",
            ),
        ),

        style=section_style,
    ),


    # ========================================================
    # RADIO GROUP
    # ========================================================

    Card(
        Heading("6. RadioGroup"),

        RadioGroup(
            Text("Option A"),
            Text("Option B"),
            Text("Option C"),
            class_name="demo-radio-group",
            title="Radio group title",
            style=Style(
                display="flex",
                flex_direction="column",
                gap="8px",
                padding="12px",
                background_color="#f8fafc",
                border_radius="8px",
            ),
        ),

        style=section_style,
    ),


    # ========================================================
    # FEEDBACK
    # ========================================================

    Card(
        Heading("7. Feedback Components"),

        Alert(
            Text("This is an Alert component."),
            title="Alert title",
            class_name="success-alert",
            style=Style(
                background_color="#ecfdf5",
                color="#065f46",
                padding="14px",
                border_radius="8px",
                margin_bottom="12px",
            ),
        ),

        Toast(
            Text("This is a Toast notification."),
            title="Toast title",
            class_name="demo-toast",
            style=Style(
                background_color="#eff6ff",
                color="#1e40af",
                padding="14px",
                border_radius="8px",
                margin_bottom="12px",
            ),
        ),

        Spinner(
            Text("Loading..."),
            title="Spinner title",
            class_name="demo-spinner",
            style=Style(
                padding="14px",
                color="#2563eb",
            ),
        ),

        ProgressBar(
            value=75,
            max=100,
            text="75% complete",
            title="Progress title",
            class_name="demo-progress",
            style=progress_style,
        ),

        Skeleton(
            Text("Loading placeholder"),
            title="Skeleton title",
            class_name="demo-skeleton",
            style=Style(
                background_color="#e2e8f0",
                padding="20px",
                border_radius="8px",
                margin_top="12px",
            ),
        ),

        style=section_style,
    ),


    # ========================================================
    # NAVIGATION
    # ========================================================

    Card(
        Heading("8. Navigation Components"),

        Navigation(
            Text("Home"),
            Text("Products"),
            Text("About"),
            class_name="main-navigation",
            title="Main navigation",
            style=Style(
                display="flex",
                gap="20px",
                padding="12px",
                background_color="#f8fafc",
                border_radius="8px",
            ),
        ),

        Divider(),

        Breadcrumbs(
            Text("Home"),
            Text("Components"),
            Text("Showcase"),
            class_name="breadcrumbs",
            title="Breadcrumb navigation",
            style=Style(
                display="flex",
                gap="10px",
            ),
        ),

        Divider(),

        Pagination(
            Text("1"),
            Text("2"),
            Text("3"),
            Text("Next"),
            class_name="pagination",
            title="Pagination navigation",
            style=Style(
                display="flex",
                gap="10px",
            ),
        ),

        Divider(),

        Menu(
            Text("Dashboard"),
            Text("Settings"),
            Text("Logout"),
            class_name="main-menu",
            title="Application menu",
            style=Style(
                display="flex",
                flex_direction="column",
                gap="8px",
                padding="12px",
                background_color="#f8fafc",
            ),
        ),

        style=section_style,
    ),


    # ========================================================
    # TABS
    # ========================================================

    Card(
        Heading("9. Tabs"),

        Tabs(
            Text("Overview"),
            Text("Details"),
            Text("Settings"),
            class_name="demo-tabs",
            title="Tabs container",
            style=Style(
                display="flex",
                gap="20px",
                padding="14px",
                background_color="#f1f5f9",
                border_radius="8px",
            ),
        ),

        style=section_style,
    ),


    # ========================================================
    # OVERLAYS
    # ========================================================

    Card(
        Heading("10. Overlay Components"),

        Dialog(
            Heading("Dialog Example"),
            Text(
                "This demonstrates the Dialog component and its "
                "class_name/title props."
            ),
            class_name="demo-dialog",
            title="Dialog title",
            style=Style(
                padding="20px",
                border="1px solid #cbd5e1",
                border_radius="10px",
            ),
        ),

        Divider(),

        Drawer(
            Heading("Drawer Example"),
            Text(
                "Drawer content is rendered inside an aside element."
            ),
            class_name="demo-drawer",
            title="Drawer title",
            style=Style(
                padding="20px",
                background_color="#f8fafc",
                border="1px solid #cbd5e1",
            ),
        ),

        Divider(),

        Tooltip(
            Text("Hover / tooltip content"),
            class_name="demo-tooltip",
            title="Tooltip title",
            style=Style(
                padding="12px",
                background_color="#172033",
                color="#ffffff",
                border_radius="8px",
            ),
        ),

        Divider(),

        Popover(
            Text("Popover content"),
            class_name="demo-popover",
            title="Popover title",
            style=Style(
                padding="16px",
                background_color="#ffffff",
                border="1px solid #cbd5e1",
                border_radius="8px",
                box_shadow="0 4px 12px rgba(0,0,0,0.1)",
            ),
        ),

        style=section_style,
    ),


    # ========================================================
    # MEDIA
    # ========================================================

    Card(
        Heading("11. Media Components"),

        Text(
            "Image — src, alt, class_name and title."
        ),

        Image(
            src="https://picsum.photos/400/200",
            alt="Demo image",
            class_name="demo-image",
            title="Image title",
            style=demo_image_style,
        ),

        Divider(),

        Text(
            "Video — src, controls, class_name and title."
        ),

        Video(
            src="https://www.w3schools.com/html/mov_bbb.mp4",
            controls=True,
            class_name="demo-video",
            title="Video title",
            style=Style(
                width="360px",
                border_radius="10px",
            ),
        ),

        Divider(),

        Text(
            "Audio — src, controls, class_name and title."
        ),

        Audio(
            src="https://www.w3schools.com/html/horse.mp3",
            controls=True,
            class_name="demo-audio",
            title="Audio title",
        ),

        style=section_style,
    ),


    # ========================================================
    # CANVAS / SVG
    # ========================================================

    Card(
        Heading("12. Canvas"),

        Text(
            "Canvas is currently represented by the SVG element "
            "and supports width, height, class_name and title."
        ),

        Canvas(
            Text("SVG / Canvas content"),
            width="320",
            height="120",
            class_name="demo-canvas",
            title="Canvas title",
            style=Style(
                background_color="#f8fafc",
                border="1px solid #cbd5e1",
                border_radius="8px",
            ),
        ),

        style=section_style,
    ),


    # ========================================================
    # TABLE
    # ========================================================

    Card(
        Heading("13. Table"),

        Table(
            Text("PyLage"),
            Text("Component"),
            Text("Props"),
            class_name="demo-table",
            title="Component table",
            style=Style(
                width="100%",
                border="1px solid #cbd5e1",
                padding="16px",
            ),
        ),

        Text(
            "Table currently exposes class_name and title through "
            "the registry contract."
        ),

        style=section_style,
    ),


    # ========================================================
    # FULL PROP SUMMARY
    # ========================================================

    Card(
        Heading("14. Current Registry Prop Reference"),

        Text("Text → text"),

        Text(
            "Card → class_name, title"
        ),

        Text(
            "Badge → class_name, title"
        ),

        Text(
            "Avatar → class_name, title"
        ),

        Text(
            "Accordion → class_name, title"
        ),

        Text(
            "Carousel → class_name, title"
        ),

        Text(
            "Image → src, alt, class_name, title"
        ),

        Text(
            "Video → src, controls, class_name, title"
        ),

        Text(
            "Audio → src, controls, class_name, title"
        ),

        Text(
            "Icon → name, class_name, title"
        ),

        Text(
            "Canvas → width, height, class_name, title"
        ),

        Text(
            "Heading → text"
        ),

        Text(
            "Button → text, class_name, value, disabled, title"
        ),

        Text(
            "Input → value, disabled, title"
        ),

        Text(
            "RadioGroup → class_name, title"
        ),

        Text(
            "Switch → class_name, title, checked"
        ),

        Text(
            "Select → class_name, title, value"
        ),

        Text(
            "Slider → class_name, title, value, min, max, step"
        ),

        Text(
            "DatePicker → class_name, title, value, min, max"
        ),

        Text(
            "Alert → class_name, title, text"
        ),

        Text(
            "Toast → class_name, title, text"
        ),

        Text(
            "Spinner → class_name, title, text"
        ),

        Text(
            "ProgressBar → class_name, title, value, max, text"
        ),

        Text(
            "Skeleton → class_name, title, text"
        ),

        Text(
            "Breadcrumbs → class_name, title"
        ),

        Text(
            "Pagination → class_name, title"
        ),

        Text(
            "Menu → class_name, title"
        ),

        Text(
            "Drawer → class_name, title"
        ),

        Text(
            "Tooltip → class_name, title"
        ),

        Text(
            "Popover → class_name, title"
        ),

        Text(
            "Form → no registered props"
        ),

        Text(
            "Table → class_name, title"
        ),

        Text(
            "Dialog → class_name, title"
        ),

        Text(
            "Navigation → class_name, title"
        ),

        Text(
            "Tabs → class_name, title"
        ),

        Text(
            "Checkbox → class_name, title, checked"
        ),

        Divider(),

        Text(
            "Styling is supplied independently through Style(...)."
        ),

        style=section_style,
    ),


    # ========================================================
    # FOOTER
    # ========================================================

    Card(
        Text(
            "PyLage — Python-native UI framework"
        ),

        Text(
            "Snapshot → IR → Analysis → Optimization → Runtime"
        ),

        style=Style(
            background_color="#172033",
            color="#ffffff",
            padding="24px",
            border_radius="14px",
            text_align="center",
        ),
    ),

    style=page_style,
)


if __name__ == "__main__":
    output = run(
        app,
        title="PyLage — Complete Component Showcase",
        output="sample.html",
        open_browser=False,
    )

    print(f"Generated: {output}")