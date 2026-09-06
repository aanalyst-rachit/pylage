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
from pylage.UI import *
from pylage.UI import __all__ as _ui_all
from pylage.UI import colors
from pylage.UI.style import style
from pylage.UI.recipes.modal import modal
from pylage.UI import themes as theme
from pylage.UI.themes import get_current_theme, set_theme
from pylage.ENGINE.components.basic import Accordion, Audio, Canvas, Carousel, Grid, Icon, Image, Option, ProgressBar, Skeleton, Spinner, Video
grid = Grid

# Root public package metadata.
# This is intentionally independent from the legacy pylage_ui facade.
IMPORT_NAME = "pylage"
PACKAGE_NAME = "pylage-ui-kit"

__all__ = list(dict.fromkeys([
    "run",
    *_ui_all,
    "style",
    "modal",
    "colors",
    "theme",
    "set_theme",
    "get_current_theme",
    "Accordion",
    "Audio",
    "Canvas",
    "Carousel",
    "Grid",
    "Icon",
    "Image",
    "Option",
    "ProgressBar",
    "Skeleton",
    "Spinner",
    "Video",
    "IMPORT_NAME",
    "PACKAGE_NAME",
])) # type: ignore
