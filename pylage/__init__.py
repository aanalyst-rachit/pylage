"""PyLage public API facade."""

def run(*args, **kwargs):
    """Run a PyLage application using the server/browser runtime."""
    from pylage.ENGINE.app import run as _run
    return _run(*args, **kwargs)
from pylage.ENGINE.components.basic import Accordion as accordion
from pylage.ENGINE.components.basic import Audio as audio
from pylage.ENGINE.components.basic import Canvas as canvas
from pylage.ENGINE.components.basic import Carousel as carousel
from pylage.ENGINE.components.basic import Grid as grid
from pylage.ENGINE.components.basic import Icon as icon
from pylage.ENGINE.components.basic import Image as image
from pylage.ENGINE.components.basic import Option as option
from pylage.ENGINE.components.basic import ProgressBar as progress_bar
from pylage.ENGINE.components.basic import Skeleton as skeleton
from pylage.ENGINE.components.basic import Spinner as spinner
from pylage.ENGINE.components.basic import Video as video
from pylage.ENGINE.core.reactive_list import ReactiveList as reactive_list
from pylage.ENGINE.core.state import State as state
from pylage.UI import themes as theme
from pylage.UI.colors import colors
from pylage.UI.components import (
    alert,
    avatar,
    badge,
    button,
    card,
    checkbox,
    cond,
    dashboard,
    dashboard_card,
    dashboard_grid,
    dashboard_header,
    dashboard_section,
    data_list,
    dataframe,
    datepicker,
    dialog,
    divider,
    empty_state,
    error_state,
    for_each,
    form,
    form_field,
    heading,
    input,
    loading_overlay,
    loading_state,
    metric,
    metric_grid,
    navigation_item,
    radio_group,
    select,
    slider,
    stat_group,
    switch,
    table,
    text,
    textarea,
    toast,
    trend,
)
from pylage.UI.layout import (
    column,
    menu,
    navbar,
    navigation,
    navigation_controls,
    pagination,
    row,
    sidebar_layout,
    tabs,
    top_header,
)
from pylage.UI.layout.factories import AppShell as app_shell
from pylage.UI.layout.factories import Center as center
from pylage.UI.layout.factories import Container as container
from pylage.UI.layout.factories import Footer as footer
from pylage.UI.layout.factories import Header as header
from pylage.UI.layout.factories import Section as section
from pylage.UI.layout.factories import Split as split
from pylage.UI.layout.factories import Stack as stack
from pylage.UI.layout.factories import ThreeColumn as three_column
from pylage.UI.layout.factories import TwoColumn as two_column
from pylage.UI.layout.topbar import Topbar as topbar
from pylage.UI.patterns.breadcrumbs import BreadcrumbTrail as breadcrumb_trail
from pylage.UI.patterns.contact import ContactSection as contact_section
from pylage.UI.patterns.content import ContentSection as content_section
from pylage.UI.patterns.cta import CTA as cta
from pylage.UI.patterns.faq import FAQ as faq
from pylage.UI.patterns.feature import FeatureSection as feature_section
from pylage.UI.patterns.hero import Hero as hero
from pylage.UI.patterns.list import List as list
from pylage.UI.patterns.newsletter import NewsletterSection as newsletter_section
from pylage.UI.patterns.pricing import PricingSection as pricing_section
from pylage.UI.patterns.search import SearchBar as search_bar
from pylage.UI.patterns.states import Loading as loading
from pylage.UI.patterns.stats import MetricCard as metric_card
from pylage.UI.patterns.stats import StatsSection as stats_section
from pylage.UI.patterns.testimonial import Testimonial as testimonial
from pylage.UI.recipes.admin import AdminPanel as admin_panel
from pylage.UI.recipes.authentication import Authentication as authentication
from pylage.UI.recipes.confirmation_dialog import confirmation_dialog
from pylage.UI.recipes.dashboard import Dashboard as dashboard_page
from pylage.UI.recipes.drawer import drawer, mobile_sidebar, navigation_drawer
from pylage.UI.recipes.landing import LandingPage as landing_page
from pylage.UI.recipes.modal import modal
from pylage.UI.recipes.popover import popover
from pylage.UI.recipes.profile import ProfilePage as profile_page
from pylage.UI.recipes.tooltip import tooltip
from pylage.UI.state import derived
from pylage.UI.style import style
from pylage.UI.themes import get_current_theme, set_theme

__version__ = "1.0.3"

__all__ = [
    "__version__",
    "accordion",
    "admin_panel",
    "alert",
    "app_shell",
    "audio",
    "authentication",
    "avatar",
    "badge",
    "breadcrumb_trail",
    "button",
    "canvas",
    "card",
    "carousel",
    "center",
    "checkbox",
    "colors",
    "column",
    "cond",
    "confirmation_dialog",
    "contact_section",
    "container",
    "content_section",
    "cta",
    "dashboard",
    "dashboard_card",
    "dashboard_grid",
    "dashboard_header",
    "dashboard_page",
    "dashboard_section",
    "data_list",
    "dataframe",
    "datepicker",
    "derived",
    "dialog",
    "divider",
    "drawer",
    "empty_state",
    "error_state",
    "faq",
    "feature_section",
    "footer",
    "for_each",
    "form",
    "form_field",
    "get_current_theme",
    "grid",
    "header",
    "heading",
    "hero",
    "icon",
    "image",
    "input",
    "landing_page",
    "list",
    "loading",
    "loading_overlay",
    "loading_state",
    "menu",
    "metric",
    "metric_card",
    "metric_grid",
    "mobile_sidebar",
    "modal",
    "navbar",
    "navigation",
    "navigation_controls",
    "navigation_drawer",
    "navigation_item",
    "newsletter_section",
    "option",
    "pagination",
    "popover",
    "pricing_section",
    "profile_page",
    "progress_bar",
    "radio_group",
    "reactive_list",
    "row",
    "run",
    "search_bar",
    "section",
    "select",
    "set_theme",
    "sidebar_layout",
    "skeleton",
    "slider",
    "spinner",
    "split",
    "stack",
    "stat_group",
    "state",
    "stats_section",
    "style",
    "switch",
    "table",
    "tabs",
    "testimonial",
    "text",
    "textarea",
    "theme",
    "three_column",
    "toast",
    "tooltip",
    "top_header",
    "topbar",
    "trend",
    "two_column",
    "video",
]

# Keep internal implementation packages out of the public root namespace.
globals().pop("ENGINE", None)
globals().pop("UI", None)
