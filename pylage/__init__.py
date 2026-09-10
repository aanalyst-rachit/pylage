"""PyLage public API facade."""

def run(*args, **kwargs):
    """Run a PyLage application using the server/browser runtime."""
    from pylage.ENGINE.app import run as _run
    return _run(*args, **kwargs)
from pylage.ENGINE.core.state import State as state
from pylage.ENGINE.components.basic import Accordion as accordion, Audio as audio, Canvas as canvas, Carousel as carousel, Grid as grid, Icon as icon, Image as image, Option as option, ProgressBar as progress_bar, Skeleton as skeleton, Spinner as spinner, Video as video
from pylage.UI.state import derived
from pylage.UI.colors import colors
from pylage.UI.style import style
from pylage.UI import themes as theme
from pylage.UI.themes import get_current_theme, set_theme
from pylage.UI.components import alert, avatar, badge, button, card, dashboard, dialog, dashboard_card, dashboard_grid, dashboard_header, dashboard_section, dataframe, data_list, divider, empty_state, error_state, heading, loading_state, loading_overlay, metric, metric_grid, stat_group, table, text, trend, toast, navigation_item, input, select, checkbox, radio_group, switch, slider, datepicker, form, form_field, textarea
from pylage.UI.layout.factories import AppShell as app_shell, Center as center, Container as container, Footer as footer, Header as header, Section as section, Split as split, Stack as stack, TwoColumn as two_column, ThreeColumn as three_column
from pylage.UI.layout.topbar import Topbar as topbar
from pylage.UI.layout import top_header, navbar, navigation, sidebar_layout, tabs, pagination, menu, navigation_controls, row, column
from pylage.UI.patterns.hero import Hero as hero
from pylage.UI.patterns.breadcrumbs import BreadcrumbTrail as breadcrumb_trail
from pylage.UI.patterns.contact import ContactSection as contact_section
from pylage.UI.patterns.content import ContentSection as content_section
from pylage.UI.patterns.cta import CTA as cta
from pylage.UI.patterns.faq import FAQ as faq
from pylage.UI.patterns.feature import FeatureSection as feature_section
from pylage.UI.patterns.list import List as list
from pylage.UI.patterns.newsletter import NewsletterSection as newsletter_section
from pylage.UI.patterns.pricing import PricingSection as pricing_section
from pylage.UI.patterns.search import SearchBar as search_bar
from pylage.UI.patterns.states import Loading as loading
from pylage.UI.patterns.stats import MetricCard as metric_card, StatsSection as stats_section
from pylage.UI.patterns.testimonial import Testimonial as testimonial
from pylage.UI.recipes.landing import LandingPage as landing_page
from pylage.UI.recipes.dashboard import Dashboard as dashboard_page
from pylage.UI.recipes.admin import AdminPanel as admin_panel
from pylage.UI.recipes.authentication import Authentication as authentication
from pylage.UI.recipes.profile import ProfilePage as profile_page
from pylage.UI.recipes.drawer import drawer, navigation_drawer, mobile_sidebar
from pylage.UI.recipes.tooltip import tooltip
from pylage.UI.recipes.popover import popover
from pylage.UI.recipes.confirmation_dialog import confirmation_dialog
from pylage.UI.recipes.modal import modal

__version__ = "1.0.2"

__all__ = [
    "run", "__version__", "colors", "style", "theme", "derived", "set_theme", "get_current_theme",
    "alert", "avatar", "badge", "button", "card", "dashboard", "dialog", "dashboard_card",
    "dashboard_grid", "dashboard_header", "dashboard_section", "dataframe", "data_list",
    "divider", "empty_state", "error_state", "heading", "loading_state", "loading_overlay",
    "metric", "metric_grid", "stat_group", "table", "text", "trend", "toast", "navigation_item",
    "input", "select", "checkbox", "radio_group", "switch", "slider", "datepicker", "form",
    "form_field", "textarea", "app_shell", "center", "container", "footer", "header", "section",
    "split", "stack", "two_column", "three_column", "row", "column", "topbar", "top_header",
    "navbar", "navigation", "sidebar_layout", "tabs", "pagination", "menu", "navigation_controls",
    "hero", "breadcrumb_trail", "contact_section", "content_section", "cta", "faq", "feature_section",
    "list", "newsletter_section", "pricing_section", "search_bar", "empty_state", "error_state",
    "loading", "metric", "metric_card", "stats_section", "testimonial", "landing_page", "dashboard_page",
    "admin_panel", "authentication", "profile_page", "drawer", "navigation_drawer", "mobile_sidebar",
    "tooltip", "popover", "confirmation_dialog", "modal", "accordion", "audio", "canvas", "carousel", "grid",
    "icon", "image", "option", "progress_bar", "skeleton", "spinner", "video", "state",
]

# Keep internal implementation packages out of the public root namespace.
del ENGINE, UI
