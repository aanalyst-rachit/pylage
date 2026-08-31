import pylage as ps


app = ps.Column(
    ps.Heading("Hello PyLage"),
    ps.Button("Click me"),
)

ps.run(
    app,
    title="Hello PyLage",
    serve=True,
)
