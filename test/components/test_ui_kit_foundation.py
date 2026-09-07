import pylage as ps


def test_ui_kit_import():
    assert ps.IMPORT_NAME == "pylage"


def test_ui_kit_package_name():
    assert ps.PACKAGE_NAME == "pylage-ui-kit"


def test_ui_kit_version():
    assert ps.__version__ == "0.1.0"


def test_ui_kit_public_api():
    # Root pylage is the public facade. It exposes the complete
    # UI surface plus the public run/style/theme namespaces.
    assert hasattr(ps, "run")
    assert hasattr(ps, "style")
    assert hasattr(ps, "theme")

    required_public_ui = [
        "avatar",
        "badge",
        "button",
        "card",
        "dashboard",
        "dashboard_card",
        "dashboard_grid",
        "dashboard_header",
        "dashboard_section",
        "dataframe",
        "data_list",
        "divider",
        "empty_state",
        "error_state",
        "heading",
        "loading_state",
        "metric",
        "metric_grid",
        "stat_group",
        "table",
        "text",
        "trend",
    ]

    for name in required_public_ui:
        assert hasattr(ps, name), f"pylage missing public UI export: {name}"

    # Public facade must not expose ENGINE as part of __all__.
    forbidden_internal = {
        "ENGINE",
        "State",
        "Style",
        "Theme",
        "ResponsiveStyle",
        "Component",
        "Runtime",
        "Renderer",
    }

    assert forbidden_internal.isdisjoint(set(ps.__all__))

