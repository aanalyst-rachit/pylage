from typing import Any
from pylage.ENGINE.components.basic import Column, Row, Card, Navigation as PNavigation, Pagination as PPagination, Menu as PMenu, Tabs as PTabs, Drawer as PDrawer
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.styling.style import Style
from pylage.ENGINE.styling.responsive import ResponsiveStyle
from ._common import default_responsive_style, resolve_style


def Center(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    base_style = Style(display="flex", justify_content="center", align_items="center", width="100%")
    s = custom_style = style or base_style
    return Column(*children, style=s, **props)


def Container(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    return Column(*children, style=resolve_style(style), **props)


def Stack(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    return Column(*children, style=resolve_style(style), **props)


def Section(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    return Column(*children, style=resolve_style(style), **props)


def Split(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    resolved_style = base_style.merge(style) if isinstance(style, Style) else resolve_style(style)
    return Row(*children, style=resolved_style, **props)


def TwoColumn(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    return Row(*children, style=resolve_style(style), **props)


def ThreeColumn(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    return Row(*children, style=resolve_style(style), **props)


def SidebarLayout(sidebar: Any = None, content: Any = None, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    children = []
    if sidebar is not None:
        children.append(sidebar)
    if content is not None:
        children.append(content)
    return Row(*children, style=resolve_style(style), **props)


def Header(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    base_style = Style(width="100%", padding="1rem 1.5rem", display="flex", align_items="center", justify_content="space-between")
    resolved_style = base_style.merge(style) if isinstance(style, Style) else resolve_style(style)
    return Row(*children, style=resolved_style, **props)


def Footer(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    base_style = Style(width="100%", padding="2rem 1.5rem", display="flex", justify_content="center", align_items="center")
    resolved_style = base_style.merge(style) if isinstance(style, Style) else resolve_style(style)
    return Column(*children, style=resolved_style, **props)


def Navigation(*children: Any, **props: Any) -> Component:
    return PNavigation(*children, **props)


def Pagination(*children: Any, **props: Any) -> Component:
    return PPagination(*children, **props)


def Menu(*children: Any, **props: Any) -> Component:
    return PMenu(*children, **props)


def AppShell(
    header: Any = None,
    sidebar: Any = None,
    content: Any = None,
    footer: Any = None,
    style: Style | ResponsiveStyle | None = None,
    **props: Any,
) -> Component:
    body_children = []
    if sidebar is not None:
        body_children.append(sidebar)
    if content is not None:
        body_children.append(content)

    body = Row(*body_children, style=Style(display="flex", flex="1", width="100%"))

    shell_children = []
    if header is not None:
        shell_children.append(header)
    shell_children.append(body)
    if footer is not None:
        shell_children.append(footer)

    shell_style = style or Style(display="flex", flex_direction="column", min_height="100vh", width="100%")
    return Column(*shell_children, style=shell_style, **props)
