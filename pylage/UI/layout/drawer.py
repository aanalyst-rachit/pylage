from typing import Any

from pylage.ENGINE.components.basic import Drawer as PDrawer
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.state import State
from pylage.ENGINE.styling.responsive import ResponsiveStyle
from pylage.ENGINE.styling.style import Style
from pylage.UI.layout._drawer import normalize_responsive_mode


def Drawer(
    *children: Any,
    style: Style | ResponsiveStyle | None = None,
    responsive_mode: dict[str, Any] | None = None,
    **props: Any,
) -> Component:
    if responsive_mode is not None:
        responsive_mode = normalize_responsive_mode(responsive_mode)
    return PDrawer(
        *children,
        style=style,
        responsive_mode=responsive_mode,
        **props,
    )


def NavigationDrawer(
    *children: Any,
    style: Style | ResponsiveStyle | None = None,
    responsive_mode: dict[str, Any] | None = None,
    **props: Any,
) -> Component:
    if responsive_mode is not None:
        responsive_mode = normalize_responsive_mode(responsive_mode)
    props["_navigation_drawer"] = True
    open_state = props.get("open")
    drawer = PDrawer(
        *children,
        style=style,
        responsive_mode=responsive_mode,
        **props,
    )

    if isinstance(open_state, State):
        existing_dismiss = drawer.events.get("dismiss")

        def dismiss_navigation_drawer(*args: Any, **kwargs: Any) -> None:
            open_state.set(False)
            if existing_dismiss is not None:
                existing_dismiss(*args, **kwargs)

        drawer.events["dismiss"] = dismiss_navigation_drawer

    return drawer


def MobileSidebar(
    *children: Any,
    style: Style | ResponsiveStyle | None = None,
    responsive_mode: dict[str, Any] | None = None,
    **props: Any,
) -> Component:
    if responsive_mode is not None:
        responsive_mode = normalize_responsive_mode(responsive_mode)
    props["_mobile_sidebar"] = True
    open_state = props.get("open")
    drawer = PDrawer(
        *children,
        style=style,
        responsive_mode=responsive_mode,
        **props,
    )

    if isinstance(open_state, State):
        existing_dismiss = drawer.events.get("dismiss")

        def dismiss_mobile_sidebar(*args: Any, **kwargs: Any) -> None:
            open_state.set(False)
            if existing_dismiss is not None:
                existing_dismiss(*args, **kwargs)

        drawer.events["dismiss"] = dismiss_mobile_sidebar

    return drawer


__all__ = ["Drawer", "MobileSidebar", "NavigationDrawer"]
