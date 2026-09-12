import pylage as pl
from pylage.ENGINE.runtime.asgi import ASGIApp

def create_test_app():
    root = pl.column(pl.heading("Factory Smoke"))
    document = "<html><body><h1>Granian Factory Smoke</h1></body></html>"
    return ASGIApp(root, document=document)
