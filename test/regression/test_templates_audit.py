"""
RULE 6 — Page Recipes Audit

Historical "templates" are now canonical UI recipes.

Canonical package:
    pylage.UI.recipes
"""

import importlib

import pytest


RECIPE_MODULES = [
    "landing",
    "dashboard",
    "admin",
    "admin_panel",
    "authentication",
    "profile",
    "settings",
    "documentation",
    "drawer",
]

PUBLIC_RECIPES = [
    "LandingPage",
    "Dashboard",
    "AdminPanel",
    "Authentication",
    "ProfilePage",
    "drawer",
    "navigation_drawer",
    "mobile_sidebar",
    "tooltip",
    "popover",
    "confirmation_dialog",
]


def test_recipes_package_imports():
    recipes = importlib.import_module("pylage.UI.recipes")
    assert recipes is not None


@pytest.mark.parametrize("module_name", RECIPE_MODULES)
def test_recipe_module_imports(module_name):
    module = importlib.import_module(
        f"pylage.UI.recipes.{module_name}"
    )
    assert module is not None


def test_recipes_public_exports_exist():
    recipes = importlib.import_module("pylage.UI.recipes")

    for name in PUBLIC_RECIPES:
        assert hasattr(
            recipes,
            name,
        ), f"recipes missing public export: {name}"


def test_recipes_all_matches_public_api():
    recipes = importlib.import_module("pylage.UI.recipes")

    assert set(recipes.__all__) == set(PUBLIC_RECIPES)


def test_recipes_are_callable():
    recipes = importlib.import_module("pylage.UI.recipes")

    for name in PUBLIC_RECIPES:
        recipe = getattr(recipes, name)

        assert callable(recipe), (
            f"recipes.{name} must be callable"
        )


def test_recipes_return_pylage_components():
    recipes = importlib.import_module("pylage.UI.recipes")

    for name in PUBLIC_RECIPES:
        recipe = getattr(recipes, name)
        if name == "confirmation_dialog":
            component = recipe("Confirm action")
        else:
            component = recipe()

        assert component is not None, (
            f"{name} returned None"
        )

        assert hasattr(component, "type"), (
            f"{name} must return a PyLage component"
        )
