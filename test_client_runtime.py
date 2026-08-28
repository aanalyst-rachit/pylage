from pyskin.runtime.client import get_client_runtime


print("=== PYSKIN CLIENT RUNTIME TEST ===")

runtime = get_client_runtime()

print("Runtime bytes:", len(runtime.encode("utf-8")))

assert isinstance(runtime, str)
assert len(runtime) > 0

assert "data-pyskin-id" in runtime
assert "data-pyskin-events" in runtime
assert "sendEvent" in runtime
assert "type: \"event\"" in runtime
assert "document.addEventListener" in runtime

print("Runtime present: PASS")
print("Event detection logic: PASS")
print("Event message generation: PASS")

print("=== CLIENT RUNTIME PASS ===")
