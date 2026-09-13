"""Canonical PyLage UI layout primitives and containers."""

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
    ThreeColumn,
    TwoColumn,
)
from .menu import Menu, menu
from .navbar import Navbar, navbar
from .navigation import Navigation, navigation
from .navigation_controls import NavigationControls, navigation_controls
from .pagination import Pagination, pagination
from .row import row
from .sidebar import SidebarLayout, sidebar_layout
from .tabs import Tabs, tabs
from .topbar import Topbar

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
    "ThreeColumn",
    "Topbar",
    "TwoColumn",
    "column",
    "menu",
    "navbar",
    "navigation",
    "navigation_controls",
    "pagination",
    "row",
    "sidebar_layout",
    "tabs",
    "top_header",
]
