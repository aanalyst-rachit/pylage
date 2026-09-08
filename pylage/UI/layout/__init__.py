"""Canonical PyLage UI layout primitives and containers."""

from .row import row
from .column import column
from .factories import (
    AppShell,
    Center,
    Container,
    Footer,
    Header,
    Section,
    Split,
    Stack,
    TwoColumn,
    ThreeColumn,
)

from .navbar import navbar, Navbar
from .navigation import navigation, Navigation
from .sidebar import sidebar_layout, SidebarLayout
from .tabs import tabs, Tabs
from .pagination import pagination, Pagination
from .menu import menu, Menu
from .topbar import Topbar
from .navigation_controls import navigation_controls, NavigationControls

# Public semantic alias for the top navigation/header.
top_header = Topbar

# Lowercase names are the canonical public UI API.
__all__ = [
    "AppShell",
    "Center",
    "Container",
    "Footer",
    "Header",
    "Section",
    "Split",
    "Stack",
    "TwoColumn",
    "ThreeColumn",
    "row",
    "column",
    "Topbar",
    "top_header",
    "navbar",
    "navigation",
    "sidebar_layout",
    "tabs",
    "pagination",
    "menu",
    "navigation_controls",
]
