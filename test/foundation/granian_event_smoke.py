from pylage.ENGINE.core.component import Component
from pylage.ENGINE.runtime.asgi import ASGIApp
from pylage.ENGINE import Button, Column


calls = []


def create_test_app():
    def clicked():
        calls.append("clicked")


    button = Component(
        type="Button",
        props={"text": "Click me"},
        events={"click": clicked},
        id="granian-button",
    )
    root = Column(button)
    document = "<html><body><button id=\"granian-button\">Click me</button></body></html>"
    return ASGIApp(root, document=document)
