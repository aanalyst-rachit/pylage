from pylage.ENGINE.core.renderer import render
import pylage as pl


def test_form_control_visual_foundation_contract():
    components = {
        "input": pl.input(placeholder="Input"),
        "textarea": pl.textarea(placeholder="Textarea"),
        "select": pl.select(
            pl.Option("One", value="one"),
            pl.Option("Two", value="two"),
        ),
        "datepicker": pl.datepicker(),
        "checkbox": pl.checkbox(),
        "switch": pl.switch(),
        "slider": pl.slider(),
    }

    for name, component in components.items():
        html = render(component)
        assert f'data-pylage-id="{component.id}"' in html, name

        style = component.props.get("style")
        assert style is not None, name

    print("FORM CONTROL VISUAL FOUNDATION: PASS")
