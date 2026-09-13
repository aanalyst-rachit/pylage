"""Canonical reusable PyLage UI patterns."""

from .auth import LoginForm, SignupForm
from .breadcrumbs import BreadcrumbTrail
from .contact import ContactSection
from .content import ContentSection
from .cta import CTA
from .faq import FAQ
from .feature import FeatureSection
from .hero import Hero
from .list import List
from .newsletter import NewsletterSection
from .pricing import PricingSection
from .search import SearchBar
from .states import EmptyState, ErrorState, Loading
from .stats import Metric, MetricCard, StatsSection
from .testimonial import Testimonial

breadcrumb_trail = BreadcrumbTrail

__all__ = [
    "CTA",
    "FAQ",
    "BreadcrumbTrail",
    "ContactSection",
    "ContentSection",
    "EmptyState",
    "ErrorState",
    "FeatureSection",
    "Hero",
    "List",
    "Loading",
    "Metric",
    "MetricCard",
    "NewsletterSection",
    "PricingSection",
    "SearchBar",
    "StatsSection",
    "Testimonial",
    "breadcrumb_trail",
]
