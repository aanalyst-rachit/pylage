# Benchmark

PyLage includes a reproducible browser-level benchmark comparing PyLage, NiceGUI, Streamlit, and Reflex across two small application scenarios.

The benchmark measures what a user can observe in the browser rather than internal framework implementation details.

## Scenarios

### Counter

The benchmark clicks an `Increment` button and waits until the displayed counter changes from `N` to `N + 1`.

### Form

The benchmark submits a unique name/email pair and waits until the corresponding new row appears.

The completion condition is the actual DOM-visible application state, not a fixed sleep or a persistent status message.

## Protocol

Each framework is measured independently:

1. Start a fresh server process.
2. Wait until the HTTP endpoint is ready.
3. Launch a fresh Playwright browser page.
4. Measure startup from page navigation until the benchmark UI is ready.
5. Run 20 warmup interactions.
6. Run 50 measured interactions.
7. Measure each interaction from the user action until the expected UI state is visible.
8. Save the raw samples plus startup, mean, P50, and P95.
9. Stop the complete server process group.

No artificial fixed sleep is used as the interaction completion condition.

## Final Results

### Counter

| Framework | Startup (ms) | P50 (ms) | P95 (ms) | Mean (ms) | N |
|---|---:|---:|---:|---:|---:|
| PyLage | 409.48 | 60.61 | 74.33 | 61.36 | 50 |
| NiceGUI | 1015.95 | 79.99 | 96.51 | 81.66 | 50 |
| Reflex | 709.79 | 61.18 | 68.06 | 61.28 | 50 |
| Streamlit | 3329.76 | 255.36 | 316.59 | 259.90 | 50 |

### Form

| Framework | Startup (ms) | P50 (ms) | P95 (ms) | Mean (ms) | N |
|---|---:|---:|---:|---:|---:|
| PyLage | 597.09 | 116.42 | 129.34 | 115.21 | 50 |
| NiceGUI | 1049.05 | 143.04 | 175.01 | 142.95 | 50 |
| Reflex | 722.71 | 85.41 | 108.14 | 87.48 | 50 |
| Streamlit | 3232.20 | 563.77 | 639.92 | 542.94 | 50 |

## Framework Run Modes

- **PyLage:** local Python application server.
- **NiceGUI:** local Python application server.
- **Streamlit:** `streamlit run` in headless mode.
- **Reflex:** `reflex run --env preview`.

The exact commands are defined in the benchmark runners.

## Reproduction

From the repository root:

```bash
python pylage-bench/measure/run_bench.py --framework all --samples 50 --warmup 20
python pylage-bench/measure/run_form_bench.py --framework all --samples 50 --warmup 20
python pylage-bench/measure/make_report.py
```

Raw result summaries are stored under `pylage-bench/results/`.

## Reports

- `pylage-bench/REPORT.md` — final counter benchmark report.
- `pylage-bench/REPORT_FORM.md` — final form benchmark report.
- `pylage-bench/results/*.json` — raw benchmark summaries and measured samples.
- `pylage-bench/logs/` — framework startup/runtime logs.

## Interpretation

These measurements represent the defined scenarios and protocol on the machine and software environment where they were run. They are not a universal performance ranking for every application or environment.

For the complete benchmark implementation, see the `pylage-bench/` directory.
