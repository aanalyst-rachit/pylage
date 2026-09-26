import pytest

from pylage.UI.layout._drawer import normalize_responsive_mode


def test_responsive_mode_normalizes_breakpoints():
    assert normalize_responsive_mode(
        {
            "base": "overlay",
            "md": "persistent",
            "lg": "persistent",
        }
    ) == {
        "base": "overlay",
        "md": "persistent",
        "lg": "persistent",
    }


def test_responsive_mode_defaults_base_to_overlay():
    assert normalize_responsive_mode(
        {"md": "persistent"}
    ) == {
        "base": "overlay",
        "md": "persistent",
    }


@pytest.mark.parametrize(
    "value",
    [
        {},
        None,
        [],
        "overlay",
    ],
)
def test_responsive_mode_requires_non_empty_mapping(value):
    with pytest.raises(ValueError, match="non-empty mapping"):
        normalize_responsive_mode(value)


def test_responsive_mode_rejects_unknown_breakpoint():
    with pytest.raises(ValueError, match="breakpoints"):
        normalize_responsive_mode({"tablet": "persistent"})


def test_responsive_mode_rejects_unknown_mode():
    with pytest.raises(ValueError, match="values"):
        normalize_responsive_mode({"base": "drawer"})


def test_drawer_accepts_responsive_mode():
    from pylage.UI.layout.drawer import Drawer

    component = Drawer(
        responsive_mode={
            "base": "overlay",
            "md": "persistent",
        }
    )

    assert component.props["responsive_mode"] == {
        "base": "overlay",
        "md": "persistent",
    }


def test_navigation_drawer_accepts_responsive_mode():
    from pylage.UI.layout.drawer import NavigationDrawer

    component = NavigationDrawer(
        responsive_mode={
            "base": "overlay",
            "md": "persistent",
        }
    )

    assert component.props["responsive_mode"]["md"] == "persistent"


def test_mobile_sidebar_accepts_responsive_mode():
    from pylage.UI.layout.drawer import MobileSidebar

    component = MobileSidebar(
        responsive_mode={
            "base": "overlay",
            "md": "persistent",
        }
    )

    assert component.props["responsive_mode"]["base"] == "overlay"


def test_drawer_renders_responsive_mode_configuration():
    from pylage.ENGINE.core.renderer import HTMLRenderer
    from pylage.UI.layout.drawer import Drawer

    html = HTMLRenderer().render(
        Drawer(
            responsive_mode={
                "base": "overlay",
                "md": "persistent",
            }
        )
    )

    assert (
        'data-pylage-responsive-mode="{&quot;base&quot;:&quot;overlay&quot;,&quot;md&quot;:&quot;persistent&quot;}"'
        in html
    )


def test_drawer_does_not_leak_responsive_mode_as_html_prop():
    from pylage.ENGINE.core.renderer import HTMLRenderer
    from pylage.UI.layout.drawer import Drawer

    html = HTMLRenderer().render(
        Drawer(responsive_mode={"base": "overlay"})
    )

    assert "responsive_mode=" not in html
    assert "data-pylage-responsive-mode=" in html


def test_drawer_without_responsive_mode_preserves_existing_markup():
    from pylage.ENGINE.core.renderer import HTMLRenderer
    from pylage.UI.layout.drawer import Drawer

    html = HTMLRenderer().render(Drawer(open=True))

    assert "data-pylage-responsive-mode=" not in html
    assert 'data-pylage-modal="true"' in html
    assert 'class="pylage-drawer-backdrop"' in html
