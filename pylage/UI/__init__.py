"""PyLage public UI API.

The UI package contains the public component, layout, pattern,
recipe, theme, and token surface of PyLage.
"""

from ._meta import IMPORT_NAME, PACKAGE_NAME
from .components import *
from .components import __all__ as _component_all
from .components.navigation_item import navigation_item

from .layout import *
from .layout import __all__ as _layout_all

from .patterns import *
from .patterns import __all__ as _pattern_all

from .recipes import *
from .recipes import __all__ as _recipe_all

from . import themes
from . import tokens
from .colors import colors

__version__ = "0.1.0"

# Public semantic alias.
# The implementation already exists as Topbar.
from .layout.topbar import Topbar
topheader = Topbar

__all__ = [
    "IMPORT_NAME",
    "PACKAGE_NAME",
    "__version__",
    "colors",
    *_component_all,
    *_layout_all,
    *_pattern_all,
    *_recipe_all,
]
