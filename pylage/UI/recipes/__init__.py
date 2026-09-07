"""Canonical reusable PyLage page recipes."""

from .landing import LandingPage
from .dashboard import Dashboard
from .admin import AdminPanel
from .authentication import Authentication
from .profile import ProfilePage
from .settings import Settings, SettingsPage
from .documentation import Documentation
from .modal import modal
from .drawer import drawer, navigation_drawer, mobile_sidebar
from .tooltip import tooltip
from .popover import popover
from .confirmation_dialog import confirmation_dialog

Admin = AdminPanel
Landing = LandingPage
Profile = ProfilePage

__all__ = [
    "LandingPage", "Dashboard", "AdminPanel", "Authentication", "ProfilePage",
    "drawer", "navigation_drawer", "mobile_sidebar", "tooltip", "popover",
    "confirmation_dialog",
]
