import pyskin as ps


app = ps.Column(
    ps.Heading("Hello PySkin"),
    ps.Button("Click me"),
)

ps.run(
    app,
    title="Hello PySkin",
    serve=True,
)
