"""Canonical reusable PyLage page recipes."""

from .admin import AdminPanel
from .authentication import Authentication
from .confirmation_dialog import confirmation_dialog
from .dashboard import Dashboard
from .documentation import Documentation
from .drawer import drawer, mobile_sidebar, navigation_drawer
from .landing import LandingPage
from .modal import modal
from .popover import popover
from .profile import ProfilePage
from .settings import Settings, SettingsPage
from .tooltip import tooltip

Admin = AdminPanel
Landing = LandingPage
Profile = ProfilePage

__all__ = [
    "AdminPanel",
    "Authentication",
    "Dashboard",
    "LandingPage",
    "ProfilePage",
    "confirmation_dialog",
    "drawer",
    "mobile_sidebar",
    "modal",
    "navigation_drawer",
    "popover",
    "tooltip",
]
