"""PyLage public API.

Users interact with PyLage through this module.

Public surface:
    pl.*       -> UI components, layouts, patterns, recipes
    style.*    -> individual style presets
    theme.*    -> complete themes

ENGINE is an internal implementation detail and is intentionally
not exported from the root public API.
"""

from pylage.ENGINE.app import run
from pylage.ENGINE.core.state import State
from pylage.UI.state import derived
from pylage.UI import (
    IMPORT_NAME, PACKAGE_NAME, __version__, colors, alert, avatar, badge, button, card,
    dashboard, dialog, dashboard_card, dashboard_grid, dashboard_header, dashboard_section,
    dataframe, data_list, divider, empty_state, error_state, heading, loading_state,
    loading_overlay, metric, metric_grid, stat_group, table, text, trend, toast,
    navigation_item, input, select, checkbox, radio_group, switch, slider, datepicker,
    form, form_field, textarea, AppShell, Center, Container, Footer, Header, Section, Split,
    Stack, TwoColumn, ThreeColumn, row, column, Topbar, topheader, navbar, navigation,
    sidebar_layout, tabs, pagination, menu, navigation_controls, Hero, BreadcrumbTrail,
    ContactSection, ContentSection, CTA, FAQ, FeatureSection, List, NewsletterSection,
    PricingSection, SearchBar, EmptyState, ErrorState, Loading, Metric, MetricCard,
    StatsSection, Testimonial, breadcrumb_trail, LandingPage, Dashboard, AdminPanel,
    Authentication, ProfilePage, drawer, navigation_drawer, mobile_sidebar, tooltip, popover,
    confirmation_dialog,
)
from pylage.UI.style import style
from pylage.UI.recipes.modal import modal
from pylage.UI import themes as theme
from pylage.UI.themes import get_current_theme, set_theme
from pylage.ENGINE.components.basic import Accordion, Audio, Canvas, Carousel, Grid, Icon, Image, Option, ProgressBar, Skeleton, Spinner, Video

grid = Grid

__all__ = [
    "run", "IMPORT_NAME", "PACKAGE_NAME", "__version__", "colors",
    "alert", "avatar", "badge", "button", "card", "dashboard", "dialog",
    "dashboard_card", "dashboard_grid", "dashboard_header", "dashboard_section",
    "dataframe", "data_list", "divider", "empty_state", "error_state", "heading",
    "loading_state", "loading_overlay", "metric", "metric_grid", "stat_group",
    "table", "text", "trend", "toast", "navigation_item", "input", "select",
    "checkbox", "radio_group", "switch", "slider", "datepicker", "form", "form_field",
    "textarea", "AppShell", "Center", "Container", "Footer", "Header", "Section",
    "Split", "Stack", "TwoColumn", "ThreeColumn", "row", "column", "Topbar",
    "topheader", "navbar", "navigation", "sidebar_layout", "tabs", "pagination",
    "menu", "navigation_controls", "Hero", "BreadcrumbTrail", "ContactSection",
    "ContentSection", "CTA", "FAQ", "FeatureSection", "List", "NewsletterSection",
    "PricingSection", "SearchBar", "EmptyState", "ErrorState", "Loading", "Metric",
    "MetricCard", "StatsSection", "Testimonial", "breadcrumb_trail", "LandingPage",
    "Dashboard", "AdminPanel", "Authentication", "ProfilePage", "drawer",
    "navigation_drawer", "mobile_sidebar", "tooltip", "popover", "confirmation_dialog",
    "style", "modal", "theme", "derived", "set_theme", "get_current_theme", "Accordion", "Audio",
    "Canvas", "Carousel", "Grid", "Icon", "Image", "Option", "ProgressBar", "Skeleton",
    "Spinner", "Video",
]
