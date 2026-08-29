import pyskin as ps


app = ps.Column(
    ps.Heading("Hello PySkin"),
    ps.Button("Click me", variant="primary"),
)

output = ps.run(
    app,
    title="My PySkin App",
    output="test_output/index.html",
)

print("=== PYSKIN RUN TEST ===")
print("Output:", output)
print("Exists:", output.exists())
print("Size:", output.stat().st_size, "bytes")
