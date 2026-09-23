# PyLage Comparative Benchmarks

This directory contains the reproducible cross-framework benchmark suite for PyLage.

## Reference workload

The PyLage reference application contains one state-bound heading and one button.

Each measured interaction sends a real binary `EventMessage` through the WebSocket transport and waits for the corresponding differential `UpdateMessage`.

The benchmark therefore measures the application/runtime path rather than calling `State.set()` directly.

## Metrics

- Startup: benchmark process/server start until the server reports readiness.
- Initial render: HTTP GET `/` latency and response body size.
- State update latency: binary WebSocket event send until the corresponding update frame is received.
- Update payload: encoded WebSocket update frame size.
- Memory: resident set size (RSS) observed by the runner.

## Reproducibility

Record the following for every framework:

- operating system
- CPU and core count
- available memory
- Python version
- framework version
- application source
- exact command
- iteration count
- benchmark result file

Do not compare measurements collected under materially different system conditions.

## Cross-framework policy

Streamlit, Reflex, and NiceGUI must use equivalent user-visible workloads and separately documented adapters. They are not PyLage runtime dependencies.

Only measured values may appear in the final comparison table. Missing or incomparable metrics must be reported as N/A rather than estimated.
