import pylage as ps
from pylage.ENGINE import Button, Column, Heading


app = Column(
    Heading("Hello PyLage"),
    Button("Click me", variant="primary"),
)

output = ps.run(
    app,
    title="My PyLage App",
    output="test_output/index.html",
)

print("=== PYLAGE RUN TEST ===")
print("Output:", output)
print("Exists:", output.exists())
print("Size:", output.stat().st_size, "bytes")
